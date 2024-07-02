'''
Created on Mar 28, 2020

@author: timti
'''
import threading
import wx
from client.view import constants
from common import methods
from client.programcontrol import ProgramControl
from client.dbhandler import ClientDBHandler

class Slot(wx.BitmapButton):
    
    STATE_BLANK = 0
    
    def __init__(self,
                 player,
                 row,
                 col,
                 token=False,
                 *args, **kw):

        super(Slot, self).__init__(*args,**kw,id=wx.ID_ANY)        
        self.player = player
        self.row = row 
        self.col = col
        if token == False:
            self.db = ''.join(['principality_', player])
            self.db_key = '{0},{1}'.format(row, col)
        else:
            if player is not None:
                self.db = ''.join(['player_', player])
                self.db_key = '{0},{1}'.format(row, col)
            else:
                self.db = 'tokens'
                self.db_key = '{0},{1}'.format(row, col)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_click)  
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)
        self.state = Slot.STATE_BLANK
        self.card = 0
        self.SetToolTip(self.db_key)
        
    def SetBitmap(self, bitmap, dim=constants.dim_slot, *args, **kwargs):
        bitmap = methods.scale_bitmap(bitmap=bitmap, dim=dim)
        return wx.BitmapButton.SetBitmap(self, bitmap, *args, **kwargs)  
        
    def _on_button(self):
        pass
    
    def _on_left_click(self, event):
        pass
    
    def _on_right_click(self, event):
        pass
    
    def _start_unlock_timer(self):
        # Reenable the button after a timeout period
        t = threading.Timer(ProgramControl.button_lockout_time, self._unlock)
        t.start()

    def _unlock(self):
        """ Unlock the button, allowing it to be enabled again """
        self.Show()
        
    def update(self):
        """ """
        card = self.card
        
        if ClientDBHandler.cards[self.db] is not None \
            and self.db_key in ClientDBHandler.cards[self.db]:
                card = ClientDBHandler.cards[self.db][self.db_key]
        else:
            card = None
        
        if card != self.card:
            self.card = card
            if card is not None:
                new_bitmap = wx.Bitmap(''.join([constants.image_path,
                                            card.deck,
                                            '/',
                                            card.card,
                                            '.JPG']))
                self.SetBitmap(new_bitmap, self.width)
            else:
                self.SetBitmap(self.blank_bitmap, self.width)
                
        
            
