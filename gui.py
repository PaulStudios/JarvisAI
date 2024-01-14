# pylint: disable=W0603
# pylint: disable=W0702
# pylint: disable=C0413
# pylint: disable=W0613
# pylint: disable=R0903
# pylint: disable=maybe-no-member

"""
Main file containing graphics ui and LOGGER module
"""

import datetime
import time
import os
from tkinter import DISABLED, END, NORMAL, Button, Entry, Label, Scrollbar, Text, Tk
import logging
import basicfuncs


LOGGER = logging
LOGNAME = ""


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
    LOGGER = logging.getLogger("JarvisAI")
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


print('Loading your AI personal assistant - Jarvis...')
initlogs()
LOGGER.info("Starting JarvisAI")
time.sleep(1)
LOGGER.info("Loading logging module.")
print(f"Logger module has been initiated in {LOGNAME}\n")
basicfuncs.init()


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BOT_NAME = "JarvisAI"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:
    """Graphics UI class for Chatbot"""

    def __init__(self):
        LOGGER.info("JarvisAI Graphical Interface starting...")
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        """Run the chatbot"""
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("JarvisAI")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=1080, height=720, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome to JarvisAI", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.987)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        initmsg = basicfuncs.wish_me()
        initmsg = f"{BOT_NAME}: {initmsg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, initmsg)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        LOGGER.info("JarvisAI Graphical Interface started")

    def _on_enter_pressed(self, event):
        LOGGER.info("Initiating bot response module")
        if basicfuncs.MODE == 2:
            msg: str = self.msg_entry.get()
        elif basicfuncs.MODE == 1:
            basicfuncs.error("ER14 - [Feature Coming Soon]", 1)
        else:
            basicfuncs.error("ER16 - [Invalide mode option set]", 1)
        self._insert_message(msg, basicfuncs.USER.capitalize())

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        bot_response_msg = get_response(msg)
        msg2 = f"{BOT_NAME}: {bot_response_msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        # basicfuncs.dologs(msg1, msg2)
        self.text_widget.see(END)

        # if basicfuncs.dev >= 1:
        # print(f"{sender}: {msg}")
        # print(f"{BOT_NAME}: {bot_response_msg}")
        LOGGER.info("%s : %s", sender, msg)
        LOGGER.info("%s : %s", BOT_NAME, bot_response_msg)
        # LOGGER.info(f"{sender}: {msg}")
        # LOGGER.info(f"{BOT_NAME}: {bot_response_msg}")
        LOGGER.info("User Input & Bot reply successfully processed")


def get_response(msg1):
    """Get response from chatbot module"""
    chat = basicfuncs.talk(msg1)
    return chat


if __name__ == "__main__":
    basicfuncs.start()
    app = ChatApplication()
    app.run()
