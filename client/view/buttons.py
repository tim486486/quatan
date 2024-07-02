""" This class contains a number of wx.Button extensions """
import wx

from client.view import constants

class FrameShowButton(wx.BitmapButton):
    """ Button used to display a wx.Frame object """
    def __init__(self, frame, 
                 bitmap=constants.img_frame_launch_button, 
                 *args, **kw):
        """
        Class constructor
        
        frame: The wx.Frame object to show on press
        bitmap: The image to show inside the button
        """
        super(FrameShowButton, self).__init__(*args,**kw,
                                               bitmap=bitmap,
                                               id=wx.ID_ANY)
        self.frame = frame
        self.Bind(wx.EVT_BUTTON, self._on_button)
       
    
    def _on_button(self, event):
        """ Button press action """
        if not self.frame.IsShown():
            self.frame.Center()
            self.frame.Show(show=True)
        self.frame.Maximize(maximize=False)
        self.frame.SetFocus()
        

        

        
            