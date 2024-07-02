""" This file contains classes used for Graphical representation of the storinator """
import wx

from client.view import constants
from client.view.deck import Deck


class DeckPanel(wx.Panel):
    """ Panel containing the storinator indications """  
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(DeckPanel, self).__init__(*args,**kw,style=wx.BORDER_SIMPLE)      
        self.SetBackgroundColour(constants.col_mux) 
        # Build the lists of widgets to be displayed inside the panel       
        self.decks=[Deck(parent=self, deck_name='regions'),
                    Deck(parent=self, deck_name='roads'),
                    Deck(parent=self, deck_name='settlements'),
                    Deck(parent=self, deck_name='cities'),
                    Deck(parent=self, deck_name='events'),
                    Deck(parent=self, deck_name='events_discard'),
                    Deck(parent=self, deck_name='basic_1'),
                    Deck(parent=self, deck_name='basic_2'),
                    Deck(parent=self, deck_name='basic_3')]
            
        self._init_ui()   

    def _init_ui(self):
        """ Layout the widgets """
        sizer = wx.GridBagSizer(5,5)                
        border=5
        
        # Row
        row = 0             
        for col,d in enumerate(self.decks):
            sizer.Add(d,
                      pos=(row,col),
                      span=(1,1),
                      flag=wx.ALIGN_CENTER,
                      border=border)
        
        sizer.Layout() 
        self.SetSizerAndFit(sizer)           
        
    def update(self):
        """ Refresh the lamps and space indication """
        for d in self.decks:
            d.update()

