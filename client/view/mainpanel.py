'''
Created on Mar 25, 2020

@author: timti
'''

import wx

from client.view.principalitypanel import TownShipPanel
from client.view.deckpanel import DeckPanel
from client.view.dicepanel import DicePanel
from client.view.playerpanel import PlayerPanel

class MainPanel(wx.Panel):
    
    def __init__(self, *args, **kw):
        """ Class Constructor """
        super(MainPanel, self).__init__(style=wx.BORDER_SIMPLE, *args, **kw)             
        self.player_panel = PlayerPanel(parent=self, player='red')
        self.player_township = TownShipPanel(parent=self, player='red')
        self.decks = DeckPanel(parent=self)
        self.dice = DicePanel(parent=self)
        self.opp_township = TownShipPanel(parent=self, player='blue')
        self.opp_panel = PlayerPanel(parent=self, player='blue')
        self._init_ui()
        
    def _init_ui(self):
        """ Position the Widgets """
        self.sizer = wx.GridBagSizer(5,5)                
        border=5
        
        # Row
        row = 0
        self.sizer.Add(self.player_panel,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border)
        
        # Row
        row = row + 1
        self.sizer.Add(self.player_township,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border)
        # Row
        row = row + 1
        self.sizer.Add(self.decks,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border) 
        
        # Row
        row = row + 1 
        self.sizer.Add(self.dice,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border)        
        # Row
        row = row + 1
        self.sizer.Add(self.opp_township,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border)
        
        # Row
        row = row + 1
        self.sizer.Add(self.opp_panel,
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER | wx.ALL,
                  border=border)
        
        self.sizer.Layout() 
        self.SetSizerAndFit(self.sizer) 
        
    def update(self):
        self.player_panel.update()
        self.player_township.update()
        self.decks.update()
        self.dice.update()
        self.opp_township.update()
        self.opp_panel.update()
