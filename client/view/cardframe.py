#!/usr/bin/env python
""" File containing the class for launching the main dashboard frame """
import wx
from client.view import constants

class CardFrame(wx.Frame):
    """ Main Dashboard Frame """    
      
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(CardFrame, self).__init__(*args, **kw,
                                        title='Card View',
                                        style=(wx.DEFAULT_FRAME_STYLE
                                           | wx.FRAME_FLOAT_ON_PARENT
                                           | wx.FULL_REPAINT_ON_RESIZE)
                                           & ~(wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER))       
        self.Bind(wx.EVT_CLOSE, self._on_close)                     
        
        self.image_box = wx.StaticBitmap(parent=self,
                                         size=(300,300))
        self._init_ui()               
        self.SetBackgroundColour(constants.col_bg)
        self.Fit()
        
    def _init_ui(self):
        panel = wx.Panel(parent=self)
        panel.SetBackgroundColour(constants.col_bg)
        
        sizer = wx.GridBagSizer(2,2)
        border = 5        
        
        # Row        
        row = 0
        sizer.Add(self.image_box,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)

        sizer.Layout()         
        panel.SetSizerAndFit(sizer)        
        
    def set_picture(self, picture):
        """ """       
        self.image_box.SetBitmap(label=picture) 
        
    def _on_close(self, event):
        """Close the frame, terminating the application."""
        # Grey out the window for quick user feedback
        f = event.GetEventObject()
        f.Hide()
        



            


