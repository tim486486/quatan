""" This class contains a number of wx.Text extensions """
import logging

import wx

from client.dbhandler import ClientDBHandler
from client.programcontrol import ProgramControl
from client.view import constants


class Label(wx.StaticText):
    """ A simple static label for indicators """
    def __init__(self,*args,**kw):
        """ Class constructor """
        super(Label,self).__init__(*args,**kw)
        self.SetBackgroundColour(constants.col_label)
        self.SetFont(constants.font_label)
        
class Heading(wx.StaticText):
    """ A heading label for frames and panels """
    def __init__(self,*args,**kw):
        """ Class constructor """
        super(Heading,self).__init__(*args,**kw)
        self.SetBackgroundColour(constants.col_heading)
        self.SetFont(constants.font_heading)
        
class StaticField(wx.StaticText):
    """ A static text box """
    def __init__(self,*args,**kw):
        """ Class constructor """
        super(StaticField,self).__init__(*args,**kw,
                                         style=wx.BORDER_NONE
                                         | wx.ALIGN_BOTTOM
                                         | wx.ALIGN_CENTER)
        self.SetBackgroundColour(constants.col_static_field)
        self.SetFont(constants.font_static_field)
        
class DynamicField(wx.TextCtrl):
    """ A dynamic text field """
    def __init__(self,
                 device_label='',
                 ai_label='',
                 fail_label='***',
                 *args,
                 **kw):
        """
        Class constructor.
        
        device_label: The device that the analog indicator is associated with, must align
                        with a device in the connections database.
        ai_label: The analog field to show on the panel. Must
                    align with an ai_label in the ai database.
        fail_label: What to show in the field when the ai has failed.            
        """
        super(DynamicField,self).__init__(*args,**kw,
                                          value=fail_label,
                                          style=wx.SIMPLE_BORDER 
                                                | wx.TE_CENTRE
                                                | wx.TE_READONLY
                                                | wx.ST_NO_AUTORESIZE)        
        self.SetBackgroundColour(constants.col_dynamic_field)
        self.SetFont(constants.font_dynamic_field)
        self.SetMinSize(constants.dim_analog_field)
        self.device_label = device_label
        # Associated dictionary key in db handler
        self.key = ''.join([device_label, '_', ai_label])
        self.fail_label = fail_label
        if ProgramControl.test_mode == True:
            self.SetToolTip(self.key)
    
    def update(self):
        """ Refresh the field """
        units = ''
        try:
            # First check if the device is connected
            if ClientDBHandler.connections[self.device_label] == False:
                val = self.fail_label
            # If connected, get the ai value and units from the database              
            else:
                sig = ClientDBHandler.ai[self.key]
                val = "{0:.2f}".format(float(sig.value))
                # If 'deg' is in the units, replace with the symbol
                units = sig.units.replace('deg',u'\N{DEGREE SIGN}')
        # If the key can't be found in the dictionary, raise an error
        except (KeyError) as error:
            val = self.fail_label
            logging.error(''.join(['Dynamic Text ', self.device_label, ' Key Error: ', str(error)]))            
        # Only write a new label to the screen if something has changed
        old_label = self.GetValue()  
        new_label = ''.join([str(val), units])        
        if not old_label == new_label:
            self.SetValue(new_label)                   
        
class EventBannerField(wx.TextCtrl):
    """ Static field for the event banner """
    def __init__(self,*args,**kw):
        """ Class constructor """
        super(EventBannerField,self).__init__(*args,**kw,
                                        value='***',
                                        style=wx.SIMPLE_BORDER 
                                                | wx.TE_CENTRE
                                                | wx.TE_READONLY
                                                | wx.ST_NO_AUTORESIZE)
        self.SetBackgroundColour(constants.col_dynamic_field)
        self.SetFont(constants.font_alarm_field)      

class EventFrameField(wx.TextCtrl):
    """ Static field for the event frame """
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(EventFrameField,self).__init__(*args,**kw,
                                         style=wx.SIMPLE_BORDER 
                                                | wx.TE_CENTRE
                                                | wx.TE_READONLY
                                                | wx.ST_NO_AUTORESIZE)
        self.SetBackgroundColour(constants.col_evt_field)
        self.SetFont(constants.font_evt_field)
        
class TextEntryField(wx.TextCtrl):
    """ Text Entry field, to collect user input """
    def __init__(self, *args, **kw):
        """ Class constructor """
        super(TextEntryField,self).__init__(*args,**kw,
                                         style=wx.SIMPLE_BORDER 
                                                | wx.TE_CENTRE
                                                | wx.ST_NO_AUTORESIZE)
        self.SetBackgroundColour(constants.col_dynamic_field)
        self.SetFont(constants.font_dynamic_field)
        self.SetMinSize(constants.dim_textentry_field)
        self.SetMaxLength(20)
        
class PasswordEntryField(wx.TextCtrl):
    """ Text Entry field, to collect a password from the user """
    def __init__(self, *args, **kw):
        super(PasswordEntryField,self).__init__(*args,**kw,
                                         style=wx.SIMPLE_BORDER 
                                                | wx.TE_CENTRE
                                                | wx.TE_PASSWORD
                                                | wx.ST_NO_AUTORESIZE
                                                | wx.TE_PROCESS_ENTER)
        self.SetBackgroundColour(constants.col_dynamic_field)
        self.SetFont(constants.font_dynamic_field)
        self.SetMinSize(constants.dim_textentry_field)
        self.SetMaxLength(20)
        
        
        