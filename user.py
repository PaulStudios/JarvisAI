# pylint: disable=W0718
# pylint: disable=R1710
# pylint: disable=W0603
"""
Login and Register handling
"""

import re
import logging

import handler
from errors import error
from handler import database, config
from handler import encrypt, decrypt

LOGGER = logging
user = ()
table_name = config.program_config()['table']


def checkdb():
    """Check connection"""
    print("Connecting to User Database...")
    try:
        database.connect()
        database.check()
        print("Using Database : JarvisAI.")
    except (Exception, handler.database.DataBaseError):
        error("ER11B - Failed to connect to Database", 1, "conn")


def checkmail(email1=""):
    """Validate mail"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email1):
        return email1
    email2 = input("Your email is invalid. Please re-enter your email: ")
    if re.match(regex, email2):
        return email2
    error("ER5 - Invalid email entered during registration.", 1, "auth")


def register():
    """Registers new user"""
    LOGGER.info("Initiating registration module")
    LOGGER.info("Registering new user")
    # Taking inputs
    name_in = input(
        "Please enter your full name (Only First name and Last name): ")
    name = name_in.split()
    country = input("In which country do you live? ")
    email = input("Please enter your email address: ")
    email = checkmail(email)
    username = input("Please enter a username: ")
    password = input("Please enter a strong password for your account: ")
    pwd = input("Please confirm your password: ")
    if pwd == password:
        print("Processing inputs...")
    else:
        print("Your passwords do not match.")
        pwd = input("Please re-confirm your password: ")
        if pwd == password:
            print("Processing inputs...")
        else:
            error("ER5 - Incorrect Password during registration.", 1, "auth")
    mail = encrypt(email, password)
    pwd = encrypt(password)
    userdata = [name[0], name[1], mail, username, pwd, country]
    fields = [
        "first_name", "last_name", "email", "username", "password", "country"
    ]
    try:
        database.insert(table=table_name, fields=fields, data=userdata)
    except Exception as e:
        error("ER9 - Database insertion failed, " + str(e), 1)
    print("You have been successfully registered. Logging you in")
    u = login(username, password)
    return u


def login(username: str = None, password: str = None) -> tuple:
    """Logs in user"""
    global user
    check = 0
    if username is None or password is None:
        check = 1
    if check == 1:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
    data = ["username", username]
    i = ()
    try:
        i = database.get_user(table=table_name, data=data)
    except Exception as e:
        error("ER10 - Database fetch failed, " + str(e), 1)
    if password == decrypt(i[5].tobytes()):
        user = i
        return user
    error("ER2 - Incorrect username/password", 1, "auth")
