""" The UI Frame for the Database Manager """
import wx


class DBManagerFrame(wx.Frame):
    """ This class creates the frame for the DB Manager """  
    def __init__(self, db_handler, *args, **kw):
        """ Class constructor """
        super(DBManagerFrame, self).__init__(*args, **kw,
                                             style=(wx.DEFAULT_FRAME_STYLE
                                                | wx.STAY_ON_TOP
                                                | wx.FULL_REPAINT_ON_RESIZE)
                                                & ~(wx.MINIMIZE_BOX 
                                                    | wx.MAXIMIZE_BOX 
                                                    | wx.RESIZE_BORDER))
        self.db_handler = db_handler        
        self._init_ui()        
        self.Fit()
        
    def _init_ui(self):
        """ Create and position the widgets """
        panel = wx.Panel(parent=self)
        panel.SetBackgroundColour(wx.Colour(184,184,184))
        sizer = wx.GridBagSizer(10,10)
        b_size = wx.Size(150,30)
        
        # Create and bind the buttons on the window
        b_build = wx.Button(parent=panel,
                       label='Build Database',
                       size=b_size)
        b_build.Bind(wx.EVT_BUTTON, self._b_build_press)
        
        b_rebuild = wx.Button(parent=panel,
                       label='Rebuild Tables',
                       size=b_size)
        b_rebuild.Bind(wx.EVT_BUTTON, self._b_rebuild_press)
        
        b_drop_connections = wx.Button(parent=panel,
                       label='Drop All Connections',
                       size=b_size)
        b_drop_connections.Bind(wx.EVT_BUTTON, self._b_drop_connections_press)
        
        # Place the buttons in a single column
        buttons = [b_build,
                   b_rebuild,
                   b_drop_connections]        
        border = 20
        for i,b in enumerate(buttons):
            flag = wx.ALIGN_CENTER_HORIZONTAL \
                    | wx.ALIGN_CENTER \
                    | wx.TOP \
                    | wx.RIGHT \
                    | wx.LEFT
            if i == len(buttons)-1:
                flag = flag | wx.BOTTOM
            sizer.Add(b,
                      pos=(i,0),
                      flag=flag,
                      border=border)            
                    
        sizer.Layout()
        panel.SetSizerAndFit(sizer, deleteOld=True)
        
    def _b_build_press(self, event):
        """ Build Database Button Press """
        event.GetEventObject().Disable()
        self.db_handler.create_database()
        event.GetEventObject().Enable()
        
    def _b_rebuild_press(self, event):
        """ Rebuild Tables Button Press """
        event.GetEventObject().Disable()
        self.db_handler.rebuild()
        event.GetEventObject().Enable() 
        
    def _b_drop_connections_press(self, event):
        """ Drop All Connections Button Press """
        event.GetEventObject().Disable()
        self.db_handler.drop_all_connections()
        event.GetEventObject().Enable()           
        

