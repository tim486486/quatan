""" The user login frame shown on client startup """
import sys

import wx

from client.dbhandler import ClientDBHandler
from client.programcontrol import ProgramControl
from client.view import labels
from common import cfg
from common import methods


class LoginFrame(wx.Frame):
    """ This class contains the login frame and handles database login """     
    def __init__(self, cfg_file, *args, **kw):
        """
        Class constructor
        
        cfg_file: Path to the config file containing default database info.
        """
        super(LoginFrame, self).__init__(*args, **kw,
                                             style=(wx.DEFAULT_FRAME_STYLE
                                                | wx.STAY_ON_TOP
                                                | wx.FULL_REPAINT_ON_RESIZE)
                                                & ~(wx.MINIMIZE_BOX 
                                                    | wx.MAXIMIZE_BOX 
                                                    | wx.RESIZE_BORDER
                                                    | wx.CLOSE_BOX))
        # Bind an event so the user can login by pressing enter in the 
        # password entry field
        self.Bind(event=wx.EVT_TEXT_ENTER, 
                  handler=self._login_press)
        # Read the postgresql section of the ini file, if this throws
        # an error exit immediately.
        self.cfg_file = cfg_file
        try:
            self.params = cfg.read(filename=self.cfg_file,
                                     section='postgresql')                  
        except (AttributeError) as error:
            methods.error_with_ui(parent=self, 
                                  msg=''.join(['Config Error: ', 
                                               str(error)]))
            sys.exit(1)
        # Labels from the config file and for the text entry fields           
        self.labels = ['host', 'port', 'database', 'user', 'password']
        self.text_entry = dict([])    
        self._init_ui()        
        self.Fit()
        self.Center()  
        # Skip the login screen in test mode, make sure the
        # password is added to the ini file
        if ProgramControl.test_mode == True:
            self._login_press(event=None)      
        
    def _init_ui(self):
        """ Layout the widgets """
        panel = wx.Panel(parent=self)
        panel.SetBackgroundColour(wx.Colour(184,184,184))
        sizer = wx.GridBagSizer(10,10)
        # Button Size
        b_size = wx.Size(80,30)
        # Create the login and cancel buttons
        login = wx.Button(parent=panel,
                       label='Login',
                       size=b_size)
        login.Bind(wx.EVT_BUTTON, self._login_press)
        
        cancel = wx.Button(parent=panel,
                       label='Cancel',
                       size=b_size)
        cancel.Bind(wx.EVT_BUTTON, self._cancel_press)        
        
        border = 2
        row = 0
        for l in self.labels:
            label = labels.Label(parent=panel,
                                 label=''.join([l.capitalize(),':']))
            if l == 'password':
                te = labels.PasswordEntryField(parent=panel)
            else:
                te = labels.TextEntryField(parent=panel)
                
            self.text_entry[l] = te
            
            if l in self.params.keys():
                self.text_entry[l].SetValue(self.params[l])
            
            sizer.Add(label, 
                      pos=(row,0), 
                      span=(1,1), 
                      flag=wx.ALIGN_LEFT
                        | wx.ALIGN_CENTER_VERTICAL
                        | wx.LEFT
                        | wx.TOP
                        | wx.BOTTOM, 
                      border=border)
            sizer.Add(te, 
                      pos=(row,1), 
                      span=(1,2), 
                      flag=wx.ALIGN_LEFT
                        | wx.ALL
                        | wx.EXPAND, 
                      border=border)
            row = row + 1
            
        sizer.Add(cancel, 
                  pos=(row,1), 
                  span=(1,1), 
                  flag=wx.ALIGN_LEFT
                    | wx.LEFT
                    | wx.TOP
                    | wx.BOTTOM, 
                  border=border)
        sizer.Add(login, 
                  pos=(row,2), 
                  span=(1,1), 
                  flag=wx.ALIGN_CENTRE_HORIZONTAL
                    | wx.ALL, 
                  border=border)            
       
        sizer.Layout()
        panel.SetSizerAndFit(sizer, deleteOld=True)
        
    def _login_press(self, event):
        """ Login button press action """
        # Put all of the user entries into a dictionary
        params = dict([])
        for key in self.text_entry:
            params[key] = self.text_entry[key].GetValue()            
        try:
            # Try to connect to the database
            ClientDBHandler.connect(params)
            # If you make it this far the login was successful so
            # write the parameters to the cfg file for next time.
            # We do not store the password.
            ProgramControl.user = params['user']
            params.pop('password')
            cfg.write(filename=self.cfg_file,
                      section='postgresql',
                      fields=params)
            # Close the login frame, this will also stop the
            # blocking call in main and advance the software to
            # show the main dashboard.
            self.Close()            
        except (Exception) as error:
            # If the login failed, show the error from
            # postgres
            methods.error_with_ui(parent=self,
                                  msg=str(error))
        
    def _cancel_press(self, event):
        """ Cancel button press action """
        self.Close()
        sys.exit(0)
        
    def _on_close(self, event):
        """ Action on close of the login frame """
        sys.exit(0)
        

