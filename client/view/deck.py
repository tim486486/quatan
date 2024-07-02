'''
Created on Mar 28, 2020

@author: timti
'''
import threading
import wx
from client.view import constants
from common import methods
from client.programcontrol import ProgramControl
from client.view import deckframe

class Deck(wx.BitmapButton):
    
    def __init__(self,
                 deck_name,
                 *args, **kw):
        super(Deck, self).__init__(*args,**kw,id=wx.ID_ANY)        
        self.Bind(wx.EVT_LEFT_UP, self._on_left_click)  
        self.Bind(wx.EVT_RIGHT_UP, self._on_right_click)
        self.frame = deckframe.DeckFrame(parent=self, 
                                         deck_name=deck_name)
        if 'hand' in  deck_name:
            deck_name = 'basic_1'
        icon = wx.Bitmap(''.join([constants.image_path,
                             'backs/',
                             deck_name,
                             '.JPG']))
        self.SetBitmap(bitmap=icon)
        self.Enable()
        
    def SetBitmap(self, bitmap, *args, **kwargs):
        bitmap = methods.scale_bitmap(bitmap=bitmap, dim=constants.dim_slot)
        return wx.BitmapButton.SetBitmap(self, bitmap, *args, **kwargs)  
    
    def _on_left_click(self, event):
        if not self.frame.IsShown():
            self.frame.Center()
            self.frame.Show(show=True)
        self.frame.Maximize(maximize=False)
        self.frame.SetFocus()
    
    def _on_right_click(self, event):
        pass
    
    def _start_unlock_timer(self):
        # Reenable the button after a timeout period
        t = threading.Timer(ProgramControl.button_lockout_time, self._unlock)
        t.start()

    def _unlock(self):
        """ Unlock the button, allowing it to be enabled again """
        self.Enable()
        
    def update(self):
        self.frame.update()