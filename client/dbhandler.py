""" Database handler for the Jasco Supervisor Client """

from common import dblink
from client.card import Card
import csv


class ClientDBHandler():    
    """
    Higher Level class between the client and the database
    """
    db_link = None
    
    parameters = {
        'numeric_dice'      : 1,
        'event_dice'        : 1,
        'last_event'        : 'Welcome to Rivals for Quatan!'
    }
    
    cards = {
        'principality_red'  : dict([]),
        'principality_blue' : dict([]),
        'player_red'        : dict([]),
        'player_blue'       : dict([]),
        'basic_1'           : dict([]),
        'basic_2'           : dict([]),
        'basic_3'           : dict([]),
        'cities'            : dict([]),
        'roads'             : dict([]),
        'regions'           : dict([]),
        'settlements'       : dict([]),
        'cities'            : dict([]),
        'events'            : dict([]),
        'events_discard'    : dict([]),
        'tokens'            : dict([])
    }
    
    @staticmethod
    def connect(params):
        """ Connect to the database using supplied params """
        try:
            ClientDBHandler.db_link = dblink.DBLink(params)
        except (Exception) as error:
            raise Exception(error) 
    
    @staticmethod
    def disconnect():
        """ Close the handlers database connection """
        ClientDBHandler.db_link.close()
    
    @staticmethod 
    def is_connected():
        """ Check if the handler has an open database connection """
        if ClientDBHandler.db_link is not None:
            return ClientDBHandler.db_link.is_connected()
        else:
            return False
            
    @staticmethod
    def set_outputs():  
        pass

    @staticmethod        
    def init_game():
        """ Load data required to initialize and build the UI """
        ClientDBHandler.db_link.clear_table(args={
                                        'schema'    : 'quatan',
                                        'tbl'       : 'cards'})
        
        with open('dbmanagement/cfg/cards.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row_num, row in enumerate(csv_reader):
                    if row_num > 0:
                        if len(row) >= 6:
                            schema = row[0]
                            table = row[1]
                            deck = row[2]
                            card = row[3]                            
                            location = row[4]
                            position = row[5]
                            ClientDBHandler.db_link.insert_row(args={
                                'schema':schema,
                                'table':table,
                                'f1':'deck',                                
                                'f2':'card',                                
                                'f3':'location',
                                'f4':'position',
                                'l_f1':deck,
                                'l_f2':card,
                                'l_f3':location,
                                'l_f4':position}, 
                                num_fields=4) 
            
    @staticmethod 
    def _change_position(location, card, new_position):
        ClientDBHandler.db_link.update_where(args={
                                    'schema':'quatan', 
                                    'tbl':'cards',                                        
                                    'upd_f1':'position',
                                    'l_upd_f1_val':new_position,                                   
                                    'cmp_f1':'location', 
                                    'l_cmp_f1_val':location, 
                                    'cmp_f2':'card', 
                                    'l_cmp_f2_val':card},
                                    num_to_update=1)
        
    @staticmethod 
    def _change_location(location, card, new_location, new_position):
        ClientDBHandler.db_link.update_where(args={
                                    'schema':'quatan', 
                                    'tbl':'cards',                                        
                                    'upd_f1':'location',
                                    'l_upd_f1_val':new_location,
                                    'upd_f2':'position',
                                    'l_upd_f2_val':new_position,                                   
                                    'cmp_f1':'location', 
                                    'l_cmp_f1_val':location, 
                                    'cmp_f2':'card', 
                                    'l_cmp_f2_val':card},
                                    num_to_update=2)
        
    @staticmethod 
    def _set_dice_val(dice_type, value):
        ClientDBHandler.db_link.update_where(args={
                                    'schema':'quatan', 
                                    'tbl':'variables',                                        
                                    'upd_f1':'value',
                                    'l_upd_f1_val':str(value),                                   
                                    'cmp_f1':'name', 
                                    'l_cmp_f1_val':dice_type, 
                                    'cmp_f2':'name', 
                                    'l_cmp_f2_val':dice_type},
                                    num_to_update=1)
    
    @staticmethod
    def read_inputs():
        """ Read the inputs from the database: connections, di, ai, events """
        for location in ClientDBHandler.cards:
            card_list = ClientDBHandler.db_link.select_where(args={
                                    'c1':'deck',
                                    'c2':'card',
                                    'c3':'position',
                                    'c4':'rotation',
                                    'schema':'quatan',
                                    'table':'cards',                                    
                                    'comp_f1':'location',
                                    'l_comp_f1':location,
                                    'order':'position'},
                                    num_cols=4)
            
            if card_list is not None:
                temp = dict([])
                for card in card_list:
                    deck = card[0]
                    card_name = card[1]
                    position = card[2]
                    rotation = card[3]
                    temp[position] = Card(
                        deck=deck,
                        location=location,                    
                        card=card_name,
                        position=position,
                        rotation=rotation)
                
                ClientDBHandler.cards[location] = temp
                
            else:
                ClientDBHandler.cards[location] = None
        
        for p in ClientDBHandler.parameters:
            value = ClientDBHandler.db_link.select_where(args={
                                        'c1':'value',
                                        'schema':'quatan',
                                        'table':'variables',                                    
                                        'comp_f1':'name',
                                        'l_comp_f1':p,
                                        'order':'name'},
                                        num_cols=1)[0]
            ClientDBHandler.parameters[p] = str(value)    
