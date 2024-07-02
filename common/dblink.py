""" This file contains low level calls to the Postgres database """

from psycopg2 import sql
import psycopg2


class DBLink():
    """ Low Level Class for handling SQL queries """    
    def __init__(self, params):
        """ 
        Class constructor
        
        params: A dictionary containing the login parameters for Postgres
        """
        self.connection = None
        self.connected = False
        try:
            self.connection = psycopg2.connect(**params)
            self.connected = True
        # If the connection fails, raise an error
        except (psycopg2.DatabaseError) as error:
            print(''.join([' Database Connection Error: ', 
                                   str(error)]))
            raise Exception(error) 

    def is_connected(self):
        """ returns: True if database connection open """
        return self.connected
    
    def close(self):
        """ Close the database connection """
        try:
            self.connection.close()
        except (psycopg2.DatabaseError) as error:
            print(''.join([' Database Close Error: ', 
                                   str(error)])) 
        
    def select_cols(self, args, num_cols, num_rows=None):
        """
        Runs a SELECT query on the specified table
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        num_cols: The number of columns to select.
        num_rows: The maximum number of rows to return.
        
        returns: A lists containing all requested fields.
        """
        arg_labels = self._format_args(args=args)
        
        # build the SELECT section
        select_fields = 'SELECT {0}'
        var_index = 1
        while var_index < num_cols:
            new_field = ',{0}'.format(''.join(['{',str(var_index),'}']))
            select_fields = ''.join([select_fields,new_field])
            var_index = var_index + 1
            
        # set the variable numbers for the next part of the query
        arg_nums=[]
        while var_index < len(args):
            arg_nums.append(''.join(['{',str(var_index),'}']))
            var_index = var_index + 1
        
        # build the FROM and ORDER section
        from_fields = """ FROM {0}.{1}
                          ORDER BY {2} DESC;""".format(*arg_nums)
        
        # finally join it all together and insert the field names  
        sql_command = ''.join([select_fields, from_fields])
        sql_command = sql_command.format(*arg_labels)
                
        query = sql.SQL(sql_command).format(**args)
        data = self._run_select_query(query, num_cols, num_rows)
        return data
    
    def select_where(self, args, num_cols, num_rows=None):
        """
        Runs a SELECT WHERE query on the specified Table
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        num_cols: The number of columns to select.
        num_rows: The maximum number of rows to return.
        
        returns: A lists containing all requested fields.
        """
        arg_labels = self._format_args(args=args)
        
        # build the SELECT section
        select_fields = 'SELECT {0}'
        var_index = 1
        while var_index < num_cols:
            new_field = ',{0}'.format(''.join(['{',str(var_index),'}']))
            select_fields = ''.join([select_fields,new_field])
            var_index = var_index + 1
            
        # set the variable numbers for the next part of the query
        arg_nums=[]
        while var_index < len(args):
            arg_nums.append(''.join(['{',str(var_index),'}']))
            var_index = var_index + 1
                    
        # build the FROM, WHERE and ORDER section
        from_fields = """ FROM {0}.{1}
                          WHERE {2} = {3}
                          ORDER BY {4};""".format(*arg_nums)
        
        # finally join it all together and insert the field names  
        sql_command = ''.join([select_fields, from_fields])
        sql_command = sql_command.format(*arg_labels)
                              
        query = sql.SQL(sql_command).format(**args)
        data = self._run_select_query(query, num_cols, num_rows)
        return data
        
    def update_where(self, num_to_update, args):
        """
        Runs an UPDATE WHERE query on the specified Table
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        num_to_update: The number of columns to update, must be [1,2]
        
        returns: Number of rows updated.
        """
        arg_labels = self._format_args(args=args)               
        # define the command format
        if num_to_update == 1:
            sql_command = """ UPDATE {0}.{1}
                              SET {2} = {3}
                              WHERE {4} = {5}
                                AND {6} = {7};""".format(*arg_labels)
        if num_to_update == 2:
            sql_command = """ UPDATE {0}.{1}
                              SET {2} = {3}, 
                                  {4} = {5}
                              WHERE {6} = {7}
                                AND {8} = {9};""".format(*arg_labels)
                                
        query = sql.SQL(sql_command).format(**args)
        data = self._run_update_query(query)
        return data
                                             
    def insert_event(self, args):        
        """ 
        Runs an INSERT query on the specified Table
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        
        returns: The value of the column supplied last in args.
        """
        arg_labels = self._format_args(args=args)                 
        # define the command format 
        sql_command = """ INSERT INTO {0}.{1} ({2},{3},{4})
                          VALUES({5},{6},{7})
                          RETURNING {8};""".format(*arg_labels)                  
        query = sql.SQL(sql_command).format(**args)
        data = self._run_update_query(query, data_back=True)
        return data
    
    def _run_select_query(self, query, num_cols, num_rows):
        """ 
        Execute any SELECT query on the datase 
        
        query: A fully formed SQL query
        num_cols: The number of columns to select
        num_rows: The maximum number of rows to return
        
        returns: A list containg the data requested, None if empty.
        """
        data = []
        try:   
            with self.connection as conn, conn.cursor() as cur:        
                # create the sql query and execute                 
                cur.execute(query)
                # fetch the data
                if num_rows is not None:
                    fetched = cur.fetchmany(size=num_rows)          
                else: 
                    fetched = cur.fetchall()                    
                # convert to a Python friendly data format                    
                for f in fetched:
                    if num_cols==1:
                        data.append(f[0])
                    else:
                        data.append(list(f))                               
        except (psycopg2.DatabaseError, 
                psycopg2.OperationalError, 
                psycopg2.InterfaceError) as error:
            print(''.join(['Database Select Query Error: ', 
                                   str(error)]))
            self.connected = False 
            return None
            
        if len(data) == 0:
            return None
        else:                
            return data
    
    def _run_update_query(self, query, data_back=False):
        """ 
        Execute any UPDATE query on the datase 
        
        query: A fully formed SQL query
        data_back: True if requesting data back from the query
        
        returns: A list containing the data requested, None if empty.
        """
        data = None
        try:                                     
            with self.connection as conn, conn.cursor() as cur:            
                # create the sql query and execute                
                cur.execute(query)
                if data_back:
                    data = cur.fetchone()
                conn.commit()   
        except (psycopg2.DatabaseError, 
                psycopg2.OperationalError, 
                psycopg2.InterfaceError) as error:
            print(''.join(['Database Update Query Error: ', 
                                   str(error)]))
            self.connected = False
            return None 
        return data
    
    def _format_args(self, args):
        """ Helper function to format the arguments for a query """
        arg_labels = []
        for k in args:
            arg_labels.append(''.join(['{',k,'}']))
            # SQL Literal (e.g. a field value)
            if k.startswith('l_'):
                args[k] = sql.Literal(args[k])
            # SQL Identifier (e.g. a field name)
            else:
                args[k] = sql.Identifier(args[k])
        return arg_labels
    
    def drop_table(self, args):
        """ 
        Execute a DROP TABLE query on the datase 
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        """
        arg_labels = self._format_args(args=args)                 
        # define the command format
        sql_command = """ DROP TABLE 
                          IF EXISTS {0}.{1} CASCADE;""".format(*arg_labels)
                                
        query = sql.SQL(sql_command).format(**args)
        data = self._run_update_query(query)
        return data
    
    def create_table(self, args, field_info):
        """ 
        Execute a CREATE TABLE query on the datase 
        
        args: An ordered dictionary containing the schema and table name.
        field_info: A list of all fields to be included in the table and their properties.
        """        
        arg_labels = self._format_args(args=args)
        # define the command format
        sql_command = ''.join(['CREATE TABLE {0}.{1}(',
                               field_info,
                               ');']).format(*arg_labels)
        query = sql.SQL(sql_command).format(**args)
        self._run_update_query(query)
                               
    def insert_row(self, args, num_fields):        
        """ 
        Execute an INSERT INTO query on the datase 
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        num_fields: The number of columns in the row.
        """
        arg_labels = self._format_args(args=args)
                       
        # define the command format        
        insert_line = 'INSERT INTO {0}.{1} ('
        values_line = 'VALUES('
        
        for i in range(num_fields):
            new_insert_field = ''.join(['{',str(i+2),'},'])
            new_values_field = ''.join(['{',str(i+2+num_fields),'},'])
            insert_line = ''.join([insert_line, new_insert_field])
            values_line = ''.join([values_line, new_values_field])
            
        insert_line = insert_line[:-1]
        values_line = values_line[:-1]
        
        insert_line = ''.join([insert_line, ') '])
        values_line = ''.join([values_line, ');'])
        
        full_command = ''.join([insert_line, values_line])       
        sql_command = full_command.format(*arg_labels)
               
        query = sql.SQL(sql_command).format(**args)        
        self._run_update_query(query)
        
    def clear_table(self, args):        
        """ 
        Runs an INSERT query on the specified Table
        
        args: An ordered dictionary containing parameters needed for the query.
                Literals MUST start with l_.
        
        returns: The value of the column supplied last in args.
        """
        arg_labels = self._format_args(args=args)                 
        # define the command format 
        sql_command = """ DELETE FROM {0}.{1};""".format(*arg_labels)                  
        query = sql.SQL(sql_command).format(**args)
        data = self._run_update_query(query, data_back=False)
        return data
        
    def drop_all_connections(self):
        """ Drop all connections from the database """        
        query = """SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = 'quatan'
                    AND pid <> pg_backend_pid();"""         
        self._run_update_query(query)
        
    def change_owner(self, args):
        """ Change the owner of a table """
        arg_labels = self._format_args(args=args)
        sql_command = """ALTER TABLE {0}.{1}
                         OWNER TO {2};""".format(*arg_labels)
        query = sql.SQL(sql_command).format(**args)
        self._run_update_query(query)
         
        
