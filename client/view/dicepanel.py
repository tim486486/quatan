""" This file contains classes used for Graphical representation of the storinator """
import wx
import os

from client.view import constants
from common import methods
from client.view.tokenslot import TokenSlot
from client.dbhandler import ClientDBHandler
import random

class DicePanel(wx.Panel):
    """ Panel containing the storinator indications """  
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(DicePanel, self).__init__(*args,**kw,style=wx.BORDER_NONE)      
        self.SetBackgroundColour(constants.col_mux) 
        # Build the lists of widgets to be displayed inside the panel       
        self.numeric_dice = wx.StaticBitmap(parent=self, 
                                            size=(constants.dim_dice,constants.dim_dice), 
                                            style=wx.BORDER_SIMPLE)
        self.event_dice = wx.StaticBitmap(parent=self, 
                                          size=(constants.dim_dice,constants.dim_dice), 
                                          style=wx.BORDER_SIMPLE)
                    
        self.tokens = [TokenSlot(parent=self,
                                 player=None,
                                 row=0,
                                 col=0,
                                 token=True),
                       TokenSlot(parent=self,
                                 player=None,
                                 row=0,
                                 col=1,
                                 token=True)]
        
        self.brigitta = wx.CheckBox(parent=self)
                         
        self._init_ui()   

    def _init_ui(self):
        """ Layout the widgets """
        sizer = wx.GridBagSizer(5,5)                
        border=5
        
        b_roll = wx.Button(parent=self, label='Roll')
        b_roll.Bind(wx.EVT_BUTTON, self._b_roll)
        
        # Row
        row = 0  
        sizer.Add(b_roll,
                  pos=(row,0),
                  span=(1,2),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        sizer.Add(self.numeric_dice,
                  pos=(row,2),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        sizer.Add(self.event_dice,
                  pos=(row,3),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        sizer.Add(self.tokens[0],
                  pos=(row,4),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border) 
        sizer.Add(self.tokens[1],
                  pos=(row,5),
                  span=(1,1),
                  flag=wx.ALIGN_CENTER,
                  border=border)
        
        # Row
        row = row + 1
        sizer.Add(wx.StaticText(parent=self, 
                                label='Brigitta: ', 
                                style=wx.ALIGN_RIGHT),
                  pos=(row,0),
                  span=(1,1),
                  flag=wx.ALIGN_RIGHT,
                  border=border)
        sizer.Add(self.brigitta,
                  pos=(row,1),
                  span=(1,1),
                  flag=wx.ALIGN_LEFT,
                  border=border)  
        
        sizer.Layout() 
        self.SetSizerAndFit(sizer)
        
    def _b_roll(self, event):
        numeric_dice_val = str(random.randint(1,6))
        event_dice_val = str(random.randint(1,6))
        if self.brigitta.GetValue() == True:
            dice_entry = wx.TextEntryDialog(parent=self, message='Brigitta says...')
            dice_entry.SetMaxLength(1)
            if dice_entry.ShowModal() == wx.ID_OK:
                if dice_entry.GetValue() in ['1','2','3','4','5','6']:
                    numeric_dice_val = str(dice_entry.GetValue())
        ClientDBHandler._set_dice_val('numeric_dice', numeric_dice_val)
        ClientDBHandler._set_dice_val('event_dice', event_dice_val)
        
    def update(self):
        """ Refresh the lamps and space indication """
        for t in self.tokens:
            t.update()
        numeric_dice_val = ClientDBHandler.parameters['numeric_dice']
        event_dice_val = ClientDBHandler.parameters['event_dice']
        
        numeric_image = methods.scale_bitmap(wx.Bitmap(''.join([constants.image_path,
                                 'dice/numeric/',
                                 str(numeric_dice_val),
                                 '.JPG'])), constants.dim_dice)
        event_image = methods.scale_bitmap(wx.Bitmap(''.join([constants.image_path,
                                 'dice/event/',
                                 str(event_dice_val),
                                 '.JPG'])), constants.dim_dice)
        if numeric_image != self.numeric_dice.GetBitmap():
            self.numeric_dice.SetBitmap(numeric_image)
        if event_image != self.event_dice.GetBitmap():
            self.event_dice.SetBitmap(event_image)
        


