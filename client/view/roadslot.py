'''
Created on Mar 28, 2020

@author: timti
'''
from client.view import constants
from client.view import slot

class RoadSlot(slot.Slot):
    """ Button used to manipulate a digital field in the database """

    STATE_ROAD = 1
    
    def __init__(self,
                 *args, **kw):
        self.blank_bitmap = constants.img_blank_road
        self.width = constants.dim_slot
        super(RoadSlot, self).__init__(size=(self.width,self.width),
                                       *args,**kw)
        

    def _on_left_click(self,event):
        """ Button press action """
        
        # Disable the button on press
        self.Hide()
        
        if self.state == RoadSlot.STATE_BLANK:
            next_state = RoadSlot.STATE_ROAD          
        else: 
            self._start_unlock_timer()
            return 
        
        if next_state == RoadSlot.STATE_ROAD:
            self.state = next_state
#             self.SetBitmap(constants.img_road)
            
        # Reenable the button after a timeout period
        self._start_unlock_timer()
        
    def _on_right_click(self,event):
        """ Button press action """
        # Disable the button on press
        self.Hide()            
        
        if self.state == RoadSlot.STATE_ROAD:
            next_state = RoadSlot.STATE_BLANK          
        else: 
            self._start_unlock_timer()
            return 
        
        if next_state == RoadSlot.STATE_BLANK:
            self.state = next_state
            self.SetBitmap(constants.img_blank_road)
                
        self._start_unlock_timer()
