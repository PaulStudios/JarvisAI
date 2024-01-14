"""
Main file
"""
import datetime
import logging
import os
import sys
from os import system

import basicfuncs
from user import User
from chatbot import Bot

LOGGER: logging.Logger = logging.getLogger("JarvisAI")
LOGNAME: str = ""
user: User = User()
chatbot: Bot = Bot()

def initlogs():
    """Initialize logging module"""
    global LOGNAME, LOGGER
    LOGNAME = "logs/JarvisAI_Logs-" + datetime.datetime.now().strftime("%f") + ".log"
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    with open(LOGNAME, 'w', encoding='utf8') as file_test:
        file_test.write(" ")
    LOGGER.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(LOGNAME)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s : %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s : %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logging
    LOGGER.addHandler(c_handler)
    LOGGER.addHandler(f_handler)
    # logging.basicConfig(
    # filename=LOGNAME, level=logging.DEBUG, format='%(asctime)s :
    # %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def init():
    global user, chatbot
    print('Loading your AI personal assistant - Jarvis...')
    initlogs()
    LOGGER.info("Loading logging module.")
    print(f"Logger module has been initiated in {LOGNAME}\n")
    LOGGER.info("Starting JarvisAI")
    basicfuncs.init()
    user: User = User()
    chatbot: Bot = Bot()


def display_menu(menu):
    """
    Display a menu where the key identifies the name of a function.
    :param menu: dictionary, key identifies a value which is a function name
    :return:
    """
    for k, function in menu.items():
        print(str(k)+".", function.__name__)


def Login():
    user.login()
    Bot.userset(user.username)
    system('cls')  # clears stdout


def Register():
    user.register()
    Bot.userset(user.username)
    system('cls')  # clears stdout


def done():
    system('cls')  # clears stdout
    print("Goodbye")
    sys.exit()


def start():
    # Create a menu dictionary where the key is an integer number and the
    # value is a function name.
    functions_names = [Login, Register, done]
    menu_items = dict(enumerate(functions_names, start=1))
    display_menu(menu_items)
    selection = int(input("Please enter your selection number: "))  # Get function key
    selected_value = menu_items[selection]  # Gets the function name
    selected_value()  # add parentheses to call the function


if __name__ == "__main__":
    init()
    start()
