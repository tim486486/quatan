""" Program Control Flags for Signalling between threads """

class ProgramControl():
    """ Static class for storing control bits """
    
    test_mode = False
    window_closed = False
    last_update_complete = False
    control_mode = False
    user = None
    button_lockout_time = 0.1
