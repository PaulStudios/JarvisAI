# pylint: disable=E0401
# pylint: disable=C0103

# skipcq
"""
Chatbot functions
"""
import datetime
import time
import webbrowser
from rich import pretty
from rich.console import Console

import ChatbotAPI
import ecapture as ec

from handler import config
from handler.logger import Logger

pretty.install()
console = Console()


def wish_me():
    """Wish the user"""
    hour = datetime.datetime.now().hour
    if 12 > hour >= 0:
        return "Hello, Good Morning"
    if 18 > hour >= 12:
        return "Hello, Good Afternoon"
    return "Hello,Good Evening"


def take_picture():
    """Take a photo"""
    current_date_and_time = datetime.datetime.now()
    filename = "img-" + current_date_and_time.strftime("%f") + ".jpg"
    ec.capture(0, False, filename)
    return filename


class Bot:
    """ChatBot"""

    def __init__(self):
        self.reply: str = "No response has been generated yet..."
        self.creds: dict = config.chat_config()
        self.LOGGER: Logger = Logger("JarvisAI.chatbot")
        self.LOGGER.info("Authenticating with ChatBotAPI")
        self.Chatbot: ChatbotAPI.ChatBot = ChatbotAPI.ChatBot(
            self.creds['brainid'],
            self.creds['brainkey'],
            history=True,
            debug=True)
        webbrowser.get('windows-default')

    def userset(self, name: str):
        """Set username"""
        self.Chatbot.changename(name=name)

    def process(self, msg):
        """Get response from bot"""
        if 'open youtube' in msg:
            webbrowser.open_new_tab("https://www.youtube.com")
            resp = "Youtube is open now"
            time.sleep(5)

        elif 'open google' in msg:
            webbrowser.open_new_tab("https://www.google.com")
            resp = "Google chrome is open now"
            time.sleep(5)

        elif 'open gmail' in msg:
            webbrowser.open_new_tab("gmail.com")
            resp = "Google Mail is open now"
            time.sleep(5)

        elif 'time' in msg:
            date_and_time_now = datetime.datetime.now().strftime("%H:%M:%S")
            resp = f"The current time is {date_and_time_now}"

        elif "open stackoverflow" in msg:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            resp = "Here is stackoverflow"

        elif "camera" in msg or "take a photo" in msg:
            f = take_picture()
            resp = "Image has been stored as " + f

        elif 'search' in msg:
            msg = msg.replace("search", "")
            webbrowser.open_new_tab(msg)
            resp = "Browser opened"
            time.sleep(5)
        else:
            resp = self.Chatbot.sendmsg(msg)
        self.reply = resp
        self.LOGGER.info("Bot response module process completed")
        return resp
