import datetime
import time
import os
from tkinter import *
import logging
import errors

logger = logging
logname = ""

def initlogs():
    global logname, logger
    logname = "logs/JarvisAI_Logs-" + datetime.datetime.now().strftime("%f") + ".log"
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    try:
        open(logname, 'x')
    except FileExistsError:
        raise errors.FileExistsError("Log File already exists. Fix : Delete logs folder.", 1)
    logger = logging.getLogger("JarvisAI")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(logname)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s : %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    f_format = logging.Formatter('%(asctime)s - %(name)s : %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logging
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    #logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

print('Loading your AI personal assistant - Jarvis...')
initlogs()
logger.info("Starting JarvisAI")
time.sleep(1)
logger.info("Loading logging module.")
print(f"Logger module has been initiated in {logname}\n")
import basicfuncs

shutdown = 0

def get_response(msg1):
    chat = basicfuncs.talk(msg1)
    return chat

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
bot_name = "JarvisAI"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        logger.info("JarvisAI Graphical Interface starting...")
        self.window = Tk()
        self._setup_main_window()

    def run(self):
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
        initmsg = basicfuncs.wishMe()
        initmsg = f"{bot_name}: {initmsg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, initmsg)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        logger.info("JarvisAI Graphical Interface started")



    def _on_enter_pressed(self, event):
        logger.info("Initiating bot response module")
        if basicfuncs.mode == 2:
            msg = self.msg_entry.get()
        elif basicfuncs.mode == 1:
            raise basicfuncs.error("ER14 - [Feature Coming Soon]", 1)
        else:
            raise basicfuncs.error("ER16 - [Invalide mode option set]", 1)
        self._insert_message(msg, basicfuncs.user.capitalize())

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        m = get_response(msg)
        msg2 = f"{bot_name}: {m}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        #basicfuncs.dologs(msg1, msg2)
        self.text_widget.see(END)

        #if basicfuncs.dev >= 1:
        print(f"{sender}: {msg}")
        print(f"{bot_name}: {m}")
        logger.info(f"{sender}: {msg}")
        logger.info(f"{bot_name}: {m}")
        logger.info("User Input & Bot reply successfully processed")


if __name__ == "__main__":

    basicfuncs.start()
    app = ChatApplication()
    app.run()
