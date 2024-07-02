'''
Created on Mar 28, 2020

@author: timti
'''
import wx
from client.view import constants
from client.view import slot

class BuildSlot(slot.Slot):
    """ Button used to manipulate a digital field in the database """
    
    STATE_BUILDING = 1
    
    def __init__(self,
                 *args, **kw):
        self.blank_bitmap = constants.img_blank_build
        self.width = constants.dim_slot
        super(BuildSlot, self).__init__(size=(self.width,self.width),
                                        *args,**kw)
        

    def _on_left_click(self,event):
        """ Button press action """
        # Disable the button on press
        self.Hide()            
        
        if self.state == BuildSlot.STATE_BLANK:
            next_state = BuildSlot.STATE_BUILDING           
        else:
#             self.GetParent().show_card_frame(picture=constants.img_bs_buildings[0]) 
            self._start_unlock_timer()
            return 
        
        if next_state == BuildSlot.STATE_BUILDING:
            self.state = next_state
#             self.SetBitmap(constants.img_bs_buildings[0])
                
        self._start_unlock_timer()
        
    def _on_right_click(self,event):
        """ Button press action """
        # Disable the button on press
        self.Hide()            
        
        if self.state == BuildSlot.STATE_BUILDING:
            next_state = BuildSlot.STATE_BLANK          
        else: 
            self._start_unlock_timer()
            return 
        
        confirmation = wx.MessageDialog(parent=self.GetParent(), 
                                        message='Are you sure you want to remove this?', 
                                        caption='Confirmation Dialog',
                                        style=wx.YES_NO 
                                            | wx.NO_DEFAULT 
                                            | wx.ICON_QUESTION)
        answer = confirmation.ShowModal()

        if answer == wx.ID_YES and next_state == BuildSlot.STATE_BLANK:
            self.state = next_state
            self.SetBitmap(constants.img_blank_build)
                
        self._start_unlock_timer()
            
            

    
    