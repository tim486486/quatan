""" Files parsing the .ini files for client, server, and dbmanager """
import configparser


def read(filename, section):
    """
    Read a single section of the config file.
    
    filename: The full path and filename to the config file
    section: The section of the config file to read
    
    returns: A dictionary containing config parameters 
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    
    # Read the section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            db[p[0]] = p[1]
    else:
        # If the section doesn't exist raise an error
        raise AttributeError('Section {0} not found in '\
                             'the {1} file'.format(section, filename))
    
    return db

def write(filename, section, fields):
    """ 
    Writes a series of lines to a config file.
    
    filename: The full path and filename to the config file
    section: The section of the config file to read
    fields: A dictionary containg name, value pairs to write    
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    
    for key in fields:
        parser.set(section=section,
                   option=key,
                   value=fields[key])
 
    with open(filename,'w') as f:
        parser.write(f, space_around_delimiters=False)

def get_sections(filename):
    """
    Look for all section names in a config file
    
    filename: The full path and filename to the config file
    
    returns: A list of all sections in the config file 
    """
    parser = configparser.ConfigParser()
    parser.read(filename)
    return parser.sections()