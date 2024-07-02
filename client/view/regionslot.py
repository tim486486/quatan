'''
Created on Mar 28, 2020

@author: timti
'''

from client.view import constants
from client.view import slot
from common import methods

class RegionSlot(slot.Slot):
    """ Button used to manipulate a digital field in the database """
    
    STATE_REGION_ASSIGNED = 1
    
    def __init__(self,
                 *args, **kw):
        self.blank_bitmap = constants.img_blank_region
        self.width = constants.dim_slot
        super(RegionSlot, self).__init__(size=(self.width,self.width),
                                         *args,**kw)
        

    def _on_left_click(self,event):
        """ Button press action """
        # Disable the button on press
        self.Hide()
        
        rotate = False
        if self.state == RegionSlot.STATE_BLANK:
            next_state = RegionSlot.STATE_REGION_ASSIGNED
        else:
            next_state = RegionSlot.STATE_REGION_ASSIGNED
            rotate = True

        if next_state == RegionSlot.STATE_REGION_ASSIGNED:
            self.state = next_state
            if rotate == False:
#                 self.SetBitmap(constants.img_red_regions[0])
                pass
            else:
                rotated_bitmap = methods.rotate_bitmap(self.GetBitmap(), 
                                                       clockwise=False)
                self.SetBitmap(rotated_bitmap)
            
        self._start_unlock_timer()
            
    def _on_right_click(self,event):
        """ Button press action """
        
        # Disable the button on press
        self.Hide()
        
        if self.state == RegionSlot.STATE_REGION_ASSIGNED:
            rotated_bitmap = methods.rotate_bitmap(self.GetBitmap(), clockwise=True)
            self.SetBitmap(rotated_bitmap)
        
        # Reenable the button after a timeout period
        self._start_unlock_timer()
    