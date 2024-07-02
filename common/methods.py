""" This file contains a collection of methods used by client, server, and dbmanager """
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import time

import wx

def scale_bitmap(bitmap, dim):
    """ """
    image = wx.Bitmap.ConvertToImage(bitmap)
    image = image.Scale(dim, dim, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result

def rotate_bitmap(bitmap, clockwise=True):
    """ """
    image = wx.Bitmap.ConvertToImage(bitmap)
    image = image.Rotate90(clockwise=clockwise)
    result = wx.Bitmap(image)
    return result

def get_time_in_utc(fmt='%Y-%m-%d %H:%M:%S.%f'):
    """
    Return the computer UTC time
    
    fmt: A string representing the format for the returned time
    
    Returns:
        str: Computer time in a human readable format
    """
    current_time = datetime.utcnow().strftime(fmt)
    if '%f' in fmt:
        current_time = current_time[:-3]
    return current_time

def get_local_time(fmt='%Y-%m-%d %H:%M:%S.%f'):
    """
    Return the computer local time
    
    fmt: A string representing the format for the returned time
    
    Returns:
        str: Computer time in a human readable format
    """
    current_time = datetime.now().strftime(fmt)
    if '%f' in fmt:
        current_time = current_time[:-3]
    return current_time

def get_dt(t1, t2, 
           tformat1='%Y-%m-%d %H:%M:%S.%f', 
           tformat2='%Y-%m-%d %H:%M:%S.%f'):
    """ 
    Get the difference between two times in seconds
    
    t1: Time 1
    t2: Time 2
    tformat1: The string format of t1
    tformat2: The string format of t2
    
    returns: t1 - t2 (seconds)
    """
    dt = (datetime.strptime(t1,tformat1) \
        - datetime.strptime(t2,tformat2)).total_seconds()        
    return dt    

def build_dict(src_list, def_val=None, vals=False):
    """
    Build a two-level dictionary, assigning values to each entry
    
    src_list: The list to build a dictionary from
    def_value: Default value to assign to each dictionary item
    vals: True if the values for each entry are included in the list
    
    returns: A dictionary built from src_list
    """
    new_dict = dict([])
    if src_list is not None:
        for item in src_list:
            device = item[0]
            signal = item[1]
            if device not in new_dict:
                new_dict[device] = dict([])
                if vals == True:
                    if len(item) == 3:
                        new_dict[device][signal] = item[2]
                    if len(item) == 4:
                        new_dict[device][signal] = [item[2],item[3]]                        
                else:
                    new_dict[device][signal] = def_val
    return new_dict

def check_bit(num, bit):
    """
    Check a bit in an int.
    
    num: The int
    bit: The bit number to check
    
    returns: True if the bit is on
    """
    if num & (1 << bit):
        return True
    else:
        return False

def configure_logging(app_name, log_path='applogs/'):
    """
    Configure logging for the application
    
    app_name: The name to give the log
    log_path: The path to give the log relative to working dir
    """
    # Set up the logger and rotating file handler for the
    # application logs.  
    make_dir(log_path)
    log_file = ''.join([log_path, app_name, '.log'])
    logging.Formatter.converter = time.gmtime
    log_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S')        
    log_handler = RotatingFileHandler(
        log_file, mode='a+', maxBytes=2*1024*1024, 
        backupCount=2, encoding=None, delay=0)        
    log_handler.setFormatter(log_formatter)      
    app_log = logging.getLogger()
    app_log.setLevel(print)
    app_log.addHandler(log_handler)
    
def make_dir(path):
    """
    This function will create a directory
    
    The built-in mkdir function will only create one level of
    directory so this function runs it as many times as 
    required to create a full path. If any part of the path
    cannot be created an exception will be logged.
    
    Parameters:
        path (str): The path to be created
    """
    path = path.replace('\\','/')
    folders = path.split('/')
    new_dir = ''
    for f in folders:
        new_dir = new_dir + f + '/'
        if not os.path.exists(new_dir):
            try:
                os.mkdir(new_dir)
            except:
                print('Failed to create ' + new_dir)
                print('Exception occurred', exc_info=True)
                
def get_bin_dict_entry(dictionary, key):
    """
    Get a binary value from a dictionary.
    
    dictionary: The dictionary to search.
    key: The key to look for.
    
    returns: True if the key is in the dictionary and the entry is true. 
    """
    val = False
    if key in dictionary.keys():
        val = dictionary[key]
    
    # If val is a signal, extract its value
    if hasattr(val, 'value'):
        val = val.value
        
    return val

def error_with_ui(parent, msg):
    """
    Log an error and display a modal error message to the user.
    
    parent: Widget that will own the message window.
    msg: The message to display to the user.
    """
    print(msg)
    message_window = wx.MessageDialog(parent=parent,
                                       message=msg,
                                       caption='Error')
    message_window.ShowModal()
    
def log_and_print(msg, error=True):
    """
    Log an error and print it to the output stream, for
    command line tools.
    
    msg: The message to display to the user.
    error: A boolean, if true the message will be logged as 
        an error. If false, it will be logged as info.
    """
    if error == True:
        print(msg)
    else:
        print(msg)
    print(msg)
    
def set_working_dir():
    """
    Sets the working directory to the directory one level above this
    file's location. This allows the script to be called from any
    directory.
    """
    # Get the full file path of this file
    file_path = os.path.realpath(__file__)
    # Strip the file name 
    file_dir = os.path.dirname(file_path)
    # Go up one level
    working_dir = os.path.realpath(''.join([file_dir,'\..']))
    # Change the working directory
    os.chdir(working_dir)
