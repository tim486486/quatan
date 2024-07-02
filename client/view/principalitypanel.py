""" This file contains classes used for Graphical representation of the storinator """
import wx

from client.view import constants
from client.view.settlementslot import SettlementSlot
from client.view.roadslot import RoadSlot
from client.view.buildslot import BuildSlot
from client.view.regionslot import RegionSlot
from client.view.cardframe import CardFrame

class TownShipPanel(wx.Panel):
    """ Panel containing the storinator indications """  
    def __init__(self, player, *args, **kw):
        """ Class constructor """
        super(TownShipPanel, self).__init__(*args,**kw,style=wx.BORDER_SIMPLE)      
        self.SetBackgroundColour(constants.col_mux) 
        self.player = player
        # Build the lists of widgets to be displayed inside the panel       
        self.settlement_slots = []
        self.road_slots = []
        self.build_slots = []
        self.region_slots = []
        self.max_settlements = 6        
        self.card_frame = CardFrame(parent=self)
        
        col = 1
        for i in range(self.max_settlements):
            self.settlement_slots.append(SettlementSlot(parent=self,
                                                        player=player,
                                                        row=2,
                                                        col=col))
            col += 2
        
        col = 0   
        for i in range(self.max_settlements + 1):
            self.road_slots.append(RoadSlot(parent=self,
                                            player=player,
                                            row=2,
                                            col=col))
            col += 2
        
        
        col = 1    
        for i in range(self.max_settlements):
            row = 0
            for j in range(4):                
                self.build_slots.append(BuildSlot(parent=self,
                                                  player=player,
                                                  row=row,
                                                  col=col))
                row = row + 1
                if row == 2:
                    row = row + 1                
            col = col + 2
                
        
        col = 0   
        for i in range (self.max_settlements+1):
            row = 1
            for j in range(2):
                self.region_slots.append(RegionSlot(parent=self,
                                                    player=player,
                                                    row=row,
                                                    col=col))
                row = row + 2
            col = col + 2
            
        self._init_ui()   

    def _init_ui(self):
        """ Layout the widgets """
        self.sizer = wx.GridBagSizer(5,5)                
        border=5
           
        for s in self.settlement_slots:
            self.sizer.Add(s,
                      pos=(s.row,s.col),
                      span=(1,1),
                      flag=wx.ALIGN_CENTER,
                      border=border)
        for r in self.road_slots:
            self.sizer.Add(r,
                      pos=(r.row,r.col),
                      span=(1,1),
                      flag=wx.ALIGN_CENTER,
                      border=border)
        for b in self.build_slots:
            self.sizer.Add(b,
                      pos=(b.row,b.col),
                      span=(1,1),
                      flag=wx.ALIGN_CENTER,
                      border=border)
        for r in self.region_slots:
            self.sizer.Add(r,
                      pos=(r.row,r.col),
                      span=(1,1),
                      flag=wx.ALIGN_CENTER,
                      border=border)    

        self.sizer.Layout() 
        self.SetSizerAndFit(self.sizer)
        
    def show_card_frame(self, picture):
        self.card_frame.set_picture(picture=picture)
        if not self.card_frame.IsShown():
            self.card_frame.Center()
            self.card_frame.Show(show=True)
        self.card_frame.Maximize(maximize=False)
        self.card_frame.SetFocus()         
        
    def update(self):
        """ Refresh the lamps and space indication """
        for s in self.settlement_slots:
            s.update()
        for r in self.road_slots:
            r.update()
        for b in self.build_slots:
            b.update()
        for r in self.region_slots:
            r.update()
