""" This file contains a variety of constants used throughout the UI """
import wx


# This has to be here to access wx objects in the script
a = wx.App()

# Image Paths
image_path = 'client/view/image/'

# Blank Slots
img_blank_settlement = wx.Bitmap(''.join([image_path,'blank/settlement.JPG']))
img_blank_road = wx.Bitmap(''.join([image_path,'blank/road.JPG']))
img_blank_build = wx.Bitmap(''.join([image_path,'blank/build.JPG']))
img_blank_region = wx.Bitmap(''.join([image_path,'blank/region.JPG']))
img_blank_token = wx.Bitmap(''.join([image_path,'blank/token.JPG']))

# Widget Symbols
img_frame_launch_button = wx.Bitmap(''.join([image_path,'icons/button-triangle.png']))

# Colours
col_bg = wx.Colour(184,184,184)
col_heading = wx.Colour(184,184,184)
col_label = wx.Colour(184,184,184)
col_mux = wx.Colour(184,184,184)
col_storinator = wx.Colour(184,184,184)
col_pow_control_panel = wx.Colour(184,184,184)
col_pow_button = wx.Colour(184,184,184)
col_dynamic_field = wx.Colour(255,255,255)
col_static_field = wx.Colour(184,184,184)
col_alm_panel = wx.Colour(184,184,184)
col_evt_field = wx.Colour(255,255,255)

# Fonts
font_heading = wx.Font(pointSize=13, 
                       family=wx.FONTFAMILY_DEFAULT, 
                       style=wx.FONTSTYLE_NORMAL, 
                       weight=wx.FONTWEIGHT_BOLD)
font_label = wx.Font(pointSize=13, 
                     family=wx.FONTFAMILY_DEFAULT, 
                     style=wx.FONTSTYLE_NORMAL, 
                     weight=wx.FONTWEIGHT_NORMAL)
font_dynamic_field = wx.Font(pointSize=10, 
                     family=wx.FONTFAMILY_DEFAULT, 
                     style=wx.FONTSTYLE_NORMAL, 
                     weight=wx.FONTWEIGHT_NORMAL)
font_alarm_field = wx.Font(pointSize=12, 
                     family=wx.FONTFAMILY_DEFAULT, 
                     style=wx.FONTSTYLE_NORMAL, 
                     weight=wx.FONTWEIGHT_NORMAL)
font_static_field = wx.Font(pointSize=10, 
                     family=wx.FONTFAMILY_DEFAULT, 
                     style=wx.FONTSTYLE_NORMAL, 
                     weight=wx.FONTWEIGHT_NORMAL)
font_evt_field = wx.Font(pointSize=10, 
                     family=wx.FONTFAMILY_DEFAULT, 
                     style=wx.FONTSTYLE_NORMAL, 
                     weight=wx.FONTWEIGHT_NORMAL)

# Dimensions
dim_main = wx.Size(1400,1200)
dim_slot = 75
dim_dice = 30
dim_token = 50
dim_con_frame = wx.Size(350,450)
dim_event_frame = wx.Size(500,500)
dim_pow_button = wx.Size(20,20)
dim_static_panel = wx.Size(80,40)
dim_alm_panel = wx.Size(1036,37)
dim_alm_time = wx.Size(200,22)
dim_alm_desc = wx.Size(900,22)
dim_analog_field = wx.Size(80,20)
dim_textentry_field = wx.Size(150,25)
dim_evt_desc = wx.Size(350,20)
dim_evt_time = wx.Size(180,20)
dim_leg_width = 50






