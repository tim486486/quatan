'''
Created on Mar 28, 2020

@author: timti
'''
import wx
from client.view import constants
from client.view import slot

class TokenSlot(slot.Slot):
    """ Button used to manipulate a digital field in the database """

    STATE_STRENGTH = 1
    STATE_TRADE = 2
    
    def __init__(self,
                 *args, **kw):
        self.width = constants.dim_token
        self.blank_bitmap = wx.Bitmap(constants.img_blank_token)
        super(TokenSlot, self).__init__(size=(self.width,self.width),
                                        *args,
                                        **kw)
        
 
    def _on_left_click(self,event):
        """ Button press action """
        
        # Disable the button on press
        self.Hide()
        
        if self.state == TokenSlot.STATE_BLANK:
            next_state = TokenSlot.STATE_STRENGTH          
        elif self.state == TokenSlot.STATE_STRENGTH:
            next_state = TokenSlot.STATE_TRADE
        else:
            self._start_unlock_timer()
            return
        
        # Perform button action
        if next_state == TokenSlot.STATE_STRENGTH:
            self.state = next_state
        elif next_state == TokenSlot.STATE_TRADE:
            self.state = next_state            
            
        # Reenable the button after a timeout period
        self._start_unlock_timer()
        
    def _on_right_click(self,event):
        """ Button press action """
        
        # Disable the button on press
        self.Hide()
        
        if self.state == TokenSlot.STATE_STRENGTH \
            or self.state == TokenSlot.STATE_TRADE :
            next_state = TokenSlot.STATE_BLANK
        else:
            self._start_unlock_timer()
            return
        
        # Perform button action
        if next_state == TokenSlot.STATE_BLANK:
            self.state = next_state
            self.SetBitmap(wx.Bitmap(constants.img_blank_token), 
                           constants.dim_token)
                        
        # Reenable the button after a timeout period
        self._start_unlock_timer()

    
