""" The database handler for the the db manager """
import csv

from common import dblink


class ManagerDBHandler():
    """
    This class reads the following files and builds a datbase from them:
    
    - cfg/events.csv: A list of events with their limits, filter times
        and descriptions.
    - cfg/fields.csv: A list of fields in all tabls in the database. This
        includes ip addresses and all I/O points in the system.
    - cfg/tables.csv: A list of all tables in the database and the definition
        of their fields.
        
    PostgreSQL must be installed with a database named 'jasco' before launching.
    """
    def __init__(self, db_params):
        """ 
        Class constructor
        
        db_params: The database login parameters.
        """
        self.db_link = dblink.DBLink(db_params)
        
    def close(self):
        """ Close the database connection """
        if self.db_link.is_connected():
            self.db_link.close()
    
    def drop_all_connections(self):
        """ Drop all connections from the database """
        self.db_link.drop_all_connections()                       
    
    
    def rebuild(self):
        """ 
        Rebuild all tables
        
        delete_events: If True, will delete the event history along 
            with everything else.
        """
        # Build a new set of tables as defined in tables.csv
        with open('dbmanagement/cfg/tables.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row_num, row in enumerate(csv_reader):
                if row_num > 0:
                    schema = row[0]
                    table = row[1]
                    field_info = row[2]
                    # Drop existing table
                    self.db_link.drop_table(args={
                                'schema':schema, 
                                'tbl':table})
                    # Create an empty table based with config in cfg/tables.csv
                    self.db_link.create_table(args={
                                'schema':schema, 
                                'tbl':table},
                            field_info=field_info)
                    self._set_table_access(schema=schema,
                                           table=table) 
                    
        name_val_tables = ['decks.csv',
                           'locations.csv',
                           'variables.csv']  
        
        for nv in name_val_tables:
            file_name = ''.join(['dbmanagement/cfg/', nv])                                                    
            # Populate the I/O data in the database                    
            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row_num, row in enumerate(csv_reader):
                    if row_num > 0:
                        if len(row) >= 3:
                            schema = row[0]
                            table = row[1]
                            name = row[2]
                            self.db_link.insert_row(args={
                                'schema':schema,
                                'table':table,
                                'f1':'name',
                                'l_f1':name}, 
                                num_fields=1) 
                            
        with open('dbmanagement/cfg/cards.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row_num, row in enumerate(csv_reader):
                    if row_num > 0:
                        if len(row) >= 5:
                            schema = row[0]
                            table = row[1]
                            deck = row[2]
                            card = row[3]
                            location = row[4]
                            self.db_link.insert_row(args={
                                'schema':schema,
                                'table':table,
                                'f1':'deck',                                
                                'f2':'card',                                
                                'f3':'location',
                                'l_f1':deck,
                                'l_f2':card,
                                'l_f3':location}, 
                                num_fields=3) 
                        
    def _set_table_access(self, schema, table):
        """ Runs a series of GRANT queries to set desired access rights """
        commands = [
            'GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {0}.{1} TO red;'
                .format(schema, table),
            'GRANT INSERT, SELECT, UPDATE ON TABLE {0}.{1} TO blue;'
                .format(schema, table)]      
        
        self._execute_commands(commands)
            
            
    def _create_roles(self):
        """ Create the Postgres roles used by the server, client and manager and give them rights """
        commands = [          
            """CREATE ROLE blue WITH
              LOGIN
              NOSUPERUSER
              INHERIT
              NOCREATEDB
              NOCREATEROLE
              NOREPLICATION
              ENCRYPTED PASSWORD 'md51315eacc05eed91b0776f60ec5ec8bdb';""",          
            """CREATE ROLE red WITH
              LOGIN
              NOSUPERUSER
              INHERIT
              NOCREATEDB
              NOCREATEROLE
              NOREPLICATION
              ENCRYPTED PASSWORD 'md5c9be7a6439f2e4458f8d3fb25f7106d9';""",
          """CREATE SCHEMA quatan
                AUTHORIZATION postgres;""",   
            """GRANT ALL ON SCHEMA quatan TO postgres;""",        
            """GRANT ALL ON SCHEMA quatan TO red;""",        
            """GRANT USAGE ON SCHEMA quatan TO blue;"""                   
        ]        
        self._execute_commands(commands)
            
    def create_database(self):
        """ 
        This function steps through the sequence of 
        building new tables and granting rights
        """    
        self._create_roles()     
        self.rebuild()
        
    def _execute_commands(self,commands):
        """ Helper function to execute SQL queries """
        for c in commands:
            self.db_link._run_update_query(c)
        
                            