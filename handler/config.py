# pylint: disable=W0719
# skipcq
"""
Config Parser for database info
"""

from configparser import ConfigParser

from handler.utilities import resource_path


def db_config(filename='config.ini', section='database'):
    """Parsing the database info from config file"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(resource_path(filename))

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


def sec_config(filename='config.ini', section='security'):
    """Parsing Encryption credentials from config file"""
    parser = ConfigParser()
    parser.read(resource_path(filename))
    creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            creds[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return creds


def program_config(filename='config.ini', section='Jarvis'):
    """Parsing program details from config file"""
    parser = ConfigParser()
    parser.read(resource_path(filename))
    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return data
