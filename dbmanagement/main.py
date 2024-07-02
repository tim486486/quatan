""" Launch Point of the Database Management Tool """
import wx

from common import cfg
from dbmanagement import dbhandler
from dbmanagement import view


class Main():
    """ Launch Class of the Database Management Tool """
    
    def __init__(self):
        """ Class constructor """        
        # Read connection parameters
        try:
            db_params = cfg.read(filename='dbmanagement/ini/dbmanager.ini',
                                        section='postgresql')                       
        except (AttributeError) as error:
            print(''.join(['Config Error: ', 
                                   str(error)]))
        
        # Create the database handler that will handle calls to the database
        db_handler = dbhandler.ManagerDBHandler(db_params=db_params)
        
        # Launch the UI Window           
        app = wx.App()     
        viewport = view.DBManagerFrame(db_handler=db_handler,
                                       parent=None,
                                       title='Quatan DB Manager')
        viewport.Show(show=True)
        
        # This call will block until the UI is closed
        app.MainLoop()
        
        # Close the database connection
        db_handler.close()


