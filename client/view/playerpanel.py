""" This file contains classes used for Graphical representation of the storinator """
import wx

from client.view import constants
from client.view.deck import Deck
from client.view.tokenslot import TokenSlot


class PlayerPanel(wx.Panel):
    """ Panel containing the storinator indications """  
    def __init__(self, player, *args, **kw):
        """ Class constructor """
        super(PlayerPanel, self).__init__(*args,**kw,style=wx.BORDER_SIMPLE)      
        self.SetBackgroundColour(constants.col_mux) 
        
        # Build the lists of widgets to be displayed inside the panel     
        self.deck = Deck(parent=self, 
                         deck_name=''.join(['player_',
                                            player]))
            
        self.tokens = [TokenSlot(parent=self,
                                 player=player,
                                 row=0,
                                 col=0,
                                 token=True),
                       TokenSlot(parent=self,
                                 player=player,
                                 row=0,
                                 col=1,
                                 token=True)]   
           
        self._init_ui()   

    def _init_ui(self):
        """ Layout the widgets """
        sizer = wx.GridBagSizer(5,5)                
        border=5
        
        # Row
        row = 0             
        sizer.Add(self.deck,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        sizer.Add(self.tokens[0],
                  pos=(row,1),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        sizer.Add(self.tokens[1],
                  pos=(row,2),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        
        sizer.Layout() 
        self.SetSizerAndFit(sizer)           
        
    def update(self):
        """ Refresh the lamps and space indication """
        for t in self.tokens:
            t.update()
        self.deck.update()

