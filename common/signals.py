""" This file contains the class for representing signals """
class Signal():
    """ A single class type for di, do, ai, and ao signals """
    def __init__(self, 
                    device_label, 
                    value=None, 
                    label=None, 
                    update_time=None, 
                    units='', 
                    description=None):
        """
        Class constructor.
        
        device_label: The device associated with the signal. Must align
                    with a row in the connections database.
        value: The value of the signal.
        label: The id associated with the signal in the database. Must align
                with an entry in the di, do, ai, or ao tables.
        update_time: The last time the signal was updated.
        units: The signal units (applies to analog signals only)
        """
        self.device_label = device_label
        self.value = value
        self.label = label      
        self.update_time = update_time
        self.units = units