import re

import handler
from errors import error
from handler import database
import logging


"""
Login and Register handling
"""

LOGGER = logging


def checkdb():
    """Check connection"""
    print("Connecting to User Database...")
    try:
        database.connect()
        database.check()
        print("Using Database : JarvisAI.")
    except (Exception, handler.database.DataBaseError):
        error("ER11B - Failed to connect to Database", 1, "conn")
    return


def checkmail(email):
    """Validate mail"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return email
    else:
        email2 = input("Your email is invalid. Please re-enter your email: ")
        if re.match(regex, email2):
            return email2
        else:
            error("ER5 - Invalid email entered during registration.", 1, "auth")


def register():
    """Registers new user"""
    LOGGER.info("Initiating registration module")
    LOGGER.info("Registering new user")
    # Taking inputs
    name_in = input("Please enter your full name (Only First name and Last name): ")
    name = name_in.split()
    country = input("In which country do you live? ")
    mail = input("Please enter your email address: ")
    mail = checkmail(mail)
    username = input("Please enter a username: ")
    password = input("Please enter a strong password for your account: ")
    p = input("Please confirm your password: ")
    if p == password:
        print("Processing inputs...")
    else:
        print("Your passwords do not match.")
        p = input("Please re-confirm your password: ")
        if p == password:
            print("Processing inputs...")
        else:
            error("ER5 - Incorrect Password during registration.", 1, "auth")
    userdata = [name[0], name[1], mail, username, password, country]
    fields = ["first_name", "last_name", "email", "username", "password", "country"]
    try:
        database.insert(table="users", rows=6, fields=fields, data=userdata)
    except Exception as e:
        error("ER9 - Database insertion failed, " + str(e), 1)
    print("You have been successfully registered. Logging you in")

