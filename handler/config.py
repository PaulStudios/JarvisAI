# pylint: disable=W0719

"""
Config Parser for database info
"""

from configparser import ConfigParser


def db_config(filename='config.ini', section='database'):
    """Parsing the database info from config file"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db


def chat_config(filename='config.ini', section='chatbot'):
    """Parsing Chatbot credentials from config file"""
    parser = ConfigParser()
    parser.read(filename)
    creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            creds[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return creds


def sec_config(filename='config.ini', section='security'):
    parser = ConfigParser()
    parser.read(filename)
    creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            creds[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return creds