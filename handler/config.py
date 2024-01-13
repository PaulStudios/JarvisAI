# pylint: disable=W0719

"""
Config Parser for database info
"""

from configparser import ConfigParser


def db_config(filename='config.ini', section='db_info'):
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
