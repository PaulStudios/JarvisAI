# pylint: disable=E0401
# pylint: disable=W0602
# pylint: disable=C0103
# pylint: disable=W0622

"""
Main file
"""
import datetime
from time import sleep
import logging
import os
import sys
from os import system
from rich import pretty, print
from rich.console import Console
from rich.traceback import install

import gui
import user
import chatbot
from handler.utilities import printn
from handler.errors import error


def initlogs():
    """Initialize logging module"""
    global LOGNAME, LOGGER
    LOGNAME = "logs/JarvisAI_Logs-" + datetime.datetime.now().strftime("%f") + ".log"
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    with open(LOGNAME, 'w', encoding='utf8') as file_test:
        file_test.write("JarvisAI v3.0\n")
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
    #LOGGER.addHandler(c_handler)
    LOGGER.addHandler(f_handler)
    # logging.basicConfig(
    # filename=LOGNAME, level=logging.DEBUG, format='%(asctime)s :
    # %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


system('cls')
LOGGER: logging.Logger = logging.getLogger("JarvisAI")
LOGNAME: str = ""
pretty.install()
install(extra_lines=0, show_locals=False)
console = Console()
console.print('Loading your AI personal assistant - Jarvis...', style="bright_yellow")
with console.status("[bold green]Setting up JarvisAI...") as status:
    console.log("Starting core systems...")
    initlogs()
    LOGGER.info("Loading logging module...")
    sleep(1)
    LOGGER.info("Setting up JarvisAI...")
    console.log("Connecting to PaulStudios Database")
    user_class: user.User = user.User()
    console.log("Connected")
    sleep(0.9)
    console.log("Initiated User Module")
    bot: chatbot.Bot = chatbot.Bot()
    sleep(1.5)
    console.log("Initiated Chatbot Module")
    sleep(2)
    ui = gui.JarvisGui()
    console.log("User Interface prepared.")
    sleep(1)
    console.log("Setup Complete")
console.print(f"Logger module has been initiated in {LOGNAME}\n", style="bright_yellow")


def display_menu(menu):
    """
    Display a menu where the key identifies the name of a function.
    :param menu: dictionary, key identifies a value which is a function name
    :return:
    """
    for k, function in menu.items():
        console.print(str(k)+".", function.__name__, style="dark_orange3")


def Login():
    """Login Function"""
    user_class.login()
    bot.userset(user_class.name)


def Register():
    """Register Function"""
    user_class.register()
    bot.userset(user_class.name)


def Exit():
    """Exit"""
    print("Goodbye")
    sys.exit()


def start():
    """Start"""
    console.print("Loading Jarvis 3.0", style="chartreuse3")
    LOGGER.info("Starting Jarvis 3.0")
    functions_names = [Login, Register, Exit]
    menu_items = dict(enumerate(functions_names, start=1))
    display_menu(menu_items)
    printn("Please enter your selection number: ", 'slate_blue1')
    try:
        selection = int(input())
        selected_value = menu_items[selection]
        selected_value()
    except (TypeError, KeyError, ValueError):
        error("ER1 - Incorrect input", 1, "args")


if __name__ == "__main__":
    start()
    ui.sub_title = ui.sub_title + "  { User : " + user_class.name + "}"
    ui.USER = user_class.userdata
    ui.run()
