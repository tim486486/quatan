'''
Created on Mar 25, 2020

@author: timti
'''
import wx
import time
import threading

from client.view import mainframe
from client.view import loginframe
from client.dbhandler import ClientDBHandler
from client.programcontrol import ProgramControl
from common import methods

class Main():
    
    def __init__(self):
        
        # Frame setup
        app = wx.App() 
        
        login_frame = loginframe.LoginFrame(cfg_file='client/ini/client.ini',
                                            parent=None,
                                            title='Rivals for Quatan Login')
        login_frame.Show()
        
        # This call is blocking and will hold until the login frame is closed
        app.MainLoop() 
               
        self.frame = mainframe.MainFrame(parent=None, 
                                         title='Rivals for Quatan')
        self.frame.Show()
        
        if ProgramControl.user == 'red':
            ClientDBHandler.init_game()
        
        # A separate thread is launched to periodically query the database
        self.running = True
        loop_thread = threading.Thread(target=self.loop) 
        loop_thread.start()
        
        app.MainLoop()
        
    def loop(self):
        """ Database Query thread main loop """
        
        while True:
            # If the connection is open, query the data
            if ClientDBHandler.is_connected():
                ClientDBHandler.read_inputs()
                # Trigger a UI Refresh event, to be picked up by Main thread                         
                self.frame.update()
                # Set the outputs, if any buttons were pressed
                ClientDBHandler.set_outputs()                
            # If not connected, display an error and close the client
            else:
                methods.error_with_ui(parent=self.dashboard,
                                      msg='Lost connection to the database')
                # Setting this flag triggers a graceful disconnect/close sequence
                ProgramControl.last_update_complete = True
                self.dashboard.close_from_code()
                break
            # Close action
            if ProgramControl.window_closed:
                ProgramControl.last_update_complete = True
                break   
            # Program scan period
            time.sleep(1)        
        # Close the database connection
        if ClientDBHandler.is_connected():
            ClientDBHandler.disconnect() 
            