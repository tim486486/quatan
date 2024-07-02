#!/usr/bin/env python
""" File containing the class for launching the main dashboard frame """
import wx
import os
from copy import copy
from client.view import constants
from client.dbhandler import ClientDBHandler
from itertools import cycle

class DeckFrame(wx.Frame):
    """ Main Dashboard Frame """    
          
    def __init__(self, deck_name, *args, **kw):
        """ Class constructor """
        self.deck_name = deck_name
        super(DeckFrame, self).__init__(*args, **kw,
                                        title=self.deck_name,
                                        style=(wx.DEFAULT_FRAME_STYLE
                                           | wx.FRAME_FLOAT_ON_PARENT
                                           | wx.FULL_REPAINT_ON_RESIZE)
                                           & ~(wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER))
        
        
        self.Bind(wx.EVT_SHOW, self.on_show)
        
        self.blank_bitmap = wx.Bitmap(''.join([constants.image_path,
                                               'blank/deck.JPG']))   
        self.current_bitmap = None
        self.Bind(wx.EVT_CLOSE, self._on_close)         
        self.image_box = wx.StaticBitmap(parent=self,
                                         size=(300,300))
        self._init_ui()               
        self.SetBackgroundColour(constants.col_bg)
        self.Fit()
        self.Hide()

    def _init_ui(self):
        panel = wx.Panel(parent=self)
        panel.SetBackgroundColour(constants.col_bg)
        
        b_size = wx.Size(150,30)
        
        # Create and bind the buttons on the window
        buttons = [wx.Button(parent=panel, label='Next', size=b_size)]        
        for b in buttons:
            if b.GetLabel() == 'Next':
                b.Bind(wx.EVT_BUTTON, self._b_next)
        
        sizer = wx.GridBagSizer(2,2)
        border = 5        
        
        # Row        
        row = 0
        sizer.Add(self.image_box,
                  pos=(row,0),
                  span=(1,2),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        
        # Row
        row = 1
        for col,b in enumerate(buttons):
            sizer.Add(b,
                  pos=(row,col),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)       
        sizer.Layout()         
        panel.SetSizerAndFit(sizer)
    
    def _b_next(self, event):
        """ """
        new_bitmap = None
        if self.card_it is not None:
            db_key = next(self.card_it)            
            if db_key in self.cards.keys() \
                and self.cards[db_key] is not None:
            
                card = self.cards[db_key]
                image_path = ''.join([constants.image_path,
                                      card.deck,
                                      '/',
                                      card.card,
                                      '.JPG'])
                new_bitmap = wx.Bitmap(image_path)
        
        self.current_bitmap = new_bitmap       
        self._set_picture()
        
    def _set_picture(self):
        """ """
        if self.current_bitmap is not None:                                 
            self.image_box.SetBitmap(self.current_bitmap)
        else:
            self.image_box.SetBitmap(self.blank_bitmap)
                
    def update(self): 
        """ Post a refresh trigger, called from another thread """
        pass
        
    def _on_close(self, event):
        """Close the frame, terminating the application."""
        # Grey out the window for quick user feedback
        f = event.GetEventObject()
        f.Hide()
        
    def on_show(self, event):
        """ """
        self.cards = copy(ClientDBHandler.cards[self.deck_name])
        if self.cards is not None:
            self.card_it = cycle(sorted(self.cards.keys()))
        else:
            self.card_it = None
        self._b_next(None)
        



            


