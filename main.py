# pylint: disable=E0401
# pylint: disable=W0602
# pylint: disable=C0103
# pylint: disable=W0622

# skipcq
"""
Main file
"""
import sys
from os import system
from time import sleep

from rich.console import Console
from rich.progress import track
from rich.traceback import install

import cfg
import chatbot
import gui
import user
from handler.errors import error
from handler.utilities import print_custom
from handler.logger import Logger

LOGGER: Logger = Logger("JarvisAI.core")

system('cls')  # skipcq: BAN-B607
install(extra_lines=0, show_locals=False)
console = Console()
console.print('Loading your AI personal assistant - Jarvis...',
              style="bright_yellow")
with console.status("[bold green]Setting up JarvisAI...") as status:
    console.log("Starting core systems...")
    sleep(1)
    LOGGER.info("Setting up JarvisAI...")
    console.log("Connecting to PaulStudios Database")
    user_class: user.User = user.User()
    LOGGER.info("Connected to PaulStudios Database")
    console.log("Connected")
    sleep(0.9)
    console.log("Initiated User Module")
    LOGGER.info("Initiated User Module")
    bot: chatbot.Bot = chatbot.Bot()
    if not bot.process("Hi") == "Hi there!":
        error(
            "ER1 - Cannot connect to ChatbotAPI. Please contact developer with corresponding logfile.",
            severity=1)
    sleep(0.5)
    console.log("Initiated Chatbot Module")
    LOGGER.info("Initiated Chatbot Module")
    sleep(2)
    ui = gui.JarvisGui()
    console.log("User Interface prepared.")
    sleep(1)
    console.log("Setup Complete")
    LOGGER.info("Initial setup complete")
    LOGNAME = cfg.log_name
console.print(f"Logger module has been initiated in {LOGNAME}\n",
              style="bright_yellow")


def display_menu(menu):
    # skipcq
    """
    Display a menu where the key identifies the name of a function.
    """
    for k, function in menu.items():
        console.print(str(k) + ".", function.__name__, style="dark_orange3")


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
    print("\n")
    print_custom("Goodbye", "bright_red")
    sys.exit()


def start():
    """Start"""
    console.print("Loading Jarvis 3.0", style="chartreuse3")
    LOGGER.info("Starting Jarvis 3.0")
    functions_names = [Login, Register, Exit]
    menu_items = dict(enumerate(functions_names, start=1))
    display_menu(menu_items)
    print_custom("Please enter your choice: ", 'slate_blue1')
    try:
        selection = int(input())
        selected_value = menu_items[selection]
        selected_value()
    except (TypeError, KeyError, ValueError):
        error("ER1 - Incorrect input", 1, "args")


if __name__ == "__main__":
    start()
    ui.sub_title = ui.sub_title + "  { User : " + user_class.name + "}"
    gui.USER = user_class.userdata
    gui.bot.userset(user_class.username)
    print_custom("Press [cyan]ENTER[/cyan] to open Chat Interface.")
    input()
    # skipcq: PYL-W0612
    for i in track(range(15), description="[bright_cyan]Loading GUI..."):
        sleep(0.1)
    LOGGER.info("Transitioning to GUI")
    ui.run()
