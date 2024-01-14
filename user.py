# pylint: disable=W0718
# pylint: disable=R1710

"""
Login and Register handling
"""

import re
import logging

import handler
from errors import error
from handler import database


LOGGER = logging
user = ()


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
    login(username, password)


def login(username="", password=""):
    """Logs in user"""
    global user
    if username == "" or password == "":
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
    data = [["username", username], ["password", password]]
    i = ()
    try:
        i = database.get_user(table="users", data=data, columns=2)
    except Exception as e:
        error("ER10 - Database fetch failed, " + str(e), 1)
    if i is None:
        print("Incorrect data entered. Please re-enter your credentials.")
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        data = [["username", username], ["password", password]]
        try:
            i = database.get_user(table="users", data=data, columns=2)
        except Exception as e:
            error("ER10 - Database fetch failed, " + str(e), 1)
        if i is None:
            error("ER2 - Incorrect username/password", 1, "auth")
    user = i
    return user
