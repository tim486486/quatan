#!/usr/bin/env python
""" File containing the class for launching the main dashboard frame """

import wx.lib.newevent

from client.programcontrol import ProgramControl
from client.view import constants
from client.view import mainpanel


class MainFrame(wx.Frame):
    """ Main Dashboard Frame """    
    frames = dict([])    
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(MainFrame, self).__init__(*args, **kw,
                                        style=wx.DEFAULT_FRAME_STYLE
                                        | wx.FULL_REPAINT_ON_RESIZE)        
               
        # The ui is refreshed whenever the database is updated but 
        # it is handled in a separate thread. This event is triggered
        # by the database handler thread.      
        self.db_updated, EVT_DB_UPDATED = wx.lib.newevent.NewEvent()                
        self.Bind(EVT_DB_UPDATED, self._on_db_update)
        
        # Defines action on Window Close
        self.code_close, EVT_CLOSE_CODE =wx.lib.newevent.NewEvent()     
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(EVT_CLOSE_CODE, self._on_close)
        
        # Set up the scroll bars, for using on smaller monitors and laptops
        self.scroll = wx.ScrolledWindow(parent=self)        
        self.main_panel = mainpanel.MainPanel(parent=self.scroll)
        self.scroll.SetBackgroundColour(constants.col_bg)
        
        self.scroll.SetScrollbars(pixelsPerUnitX=20, 
                                  pixelsPerUnitY=20, 
                                  noUnitsX=constants.dim_main.width/20, 
                                  noUnitsY=constants.dim_main.height/20, 
                                  xPos=0, 
                                  yPos=0, 
                                  noRefresh=False)
        self.statusbar = self.CreateStatusBar(1)   

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.main_panel)
        self.scroll.SetSizerAndFit(sizer, deleteOld=True)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.scroll)
        self.SetSizerAndFit(sizer, deleteOld=True)
        
        self.SetMaxSize(self.GetSize())
        self.Maximize(maximize=True)
                
    def update(self): 
        """ Post a refresh trigger, called from another thread """
        wx.PostEvent(self, self.db_updated())
        
    def close_from_code(self):
        """ Closed by an exception in code """
        wx.PostEvent(self, self.code_close())
        
    def _on_db_update(self, event): 
        """ Pick-up point of the update event """ 
        self.statusbar.SetStatusText('Waiting for players to connect')       
        self.main_panel.update()  
           
        
    def _on_close(self, event):
        """Close the frame, terminating the application."""
        # Grey out the window for quick user feedback
        self.scroll.Hide()         
        # Set the window closed flag which will trigger a graceful
        # database disconnect in the db update thread
        ProgramControl.window_closed = True
        # Then wait for the database disconnect
        while not ProgramControl.last_update_complete:
            pass
        # Close any open windowsand then self
        for f in self.frames:
            self.frames[f].Destroy()
        self.Destroy()
        



            


