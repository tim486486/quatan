'''
Created on Mar 28, 2020

@author: timti
'''
from client.view import constants

from client.view import slot

class SettlementSlot(slot.Slot):
    """ Button used to manipulate a digital field in the database """
    
    STATE_SETTLEMENT = 1
    STATE_CITY = 2
    
    def __init__(self,
                 *args, **kw):
        self.blank_bitmap = constants.img_blank_settlement
        self.width = constants.dim_slot
        super(SettlementSlot, self).__init__(size=(self.width,self.width),
                                             *args,**kw)

        

    def _on_left_click(self,event):
        """ Button press action """
        
        # Disable the button on press
        self.Hide()
        
        if self.state == SettlementSlot.STATE_BLANK:
            next_state = SettlementSlot.STATE_SETTLEMENT          
        elif self.state == SettlementSlot.STATE_SETTLEMENT:
            next_state = SettlementSlot.STATE_CITY       
        else: 
            self._start_unlock_timer()
            return 
        
        # Perform button action
        if next_state == SettlementSlot.STATE_SETTLEMENT:
            self.state = next_state
#             self.SetBitmap(constants.img_settlement)
        elif next_state == SettlementSlot.STATE_CITY:
            self.state = next_state
#             self.SetBitmap(constants.img_city)
            
        self._start_unlock_timer()
        
    def _on_right_click(self,event):
        """ Button press action """
        # Disable the button on press
        self.Hide()            
        
        if self.state == SettlementSlot.STATE_SETTLEMENT \
            or self.state == SettlementSlot.STATE_CITY:
            next_state = SettlementSlot.STATE_BLANK          
        else: 
            self._start_unlock_timer()
            return 
        
        if next_state == SettlementSlot.STATE_BLANK:
            self.state = next_state
            self.SetBitmap(constants.img_blank_settlement)
                
        self._start_unlock_timer()
            