from tkinter import *

import basicfuncs
from basicfuncs import speak, talk2
import main
import time
import wikipedia
shutdown = 0
def get_response(msg1):
    msg = msg1.lower()
    global shutdown
    if "good bye" in msg or "goodbye" in msg or "ok bye" in msg:
        chat = talk2(msg)
        shutdown = 1
        return chat
    elif "take my photo" in msg or "take my pic" in msg or "take my picture" in msg or "say cheese" in msg:
        pic = basicfuncs.takepic()
        chat = "Taking your photo... Pic saved as " + pic 
        print("Pls ignore the warn. It is harmless")
        return chat
    if 'wikipedia' in msg:
        try:
            statement = msg.replace("wikipedia", "")
            r = wikipedia.search(statement)
            results = "According to Wikipedia :\n" + wikipedia.summary(r[0], sentences=3)
            return results
        except IndexError:
            return "No results found."
    elif 'check access logs' in msg:
        r = basicfuncs.checklogs()
        return r
    elif 'delete logs' in msg:
        r = basicfuncs.deletelogs()
        return r
    elif 'start logging' in msg:
        res = basicfuncs.startlogs()
        return res
    elif 'stop logging' in msg:
        res = basicfuncs.stoplogs()
        return res

    chat = talk2(msg)
    return chat

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
bot_name = "JarvisAI"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
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



    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if shutdown == 1:
            self._insert_message(msg, "You")
            print('your personal assistant Jarvis is shutting down,Good bye')
            time.sleep(2)
            print("Successfully Logged out and shut down")
            self.window.destroy()
            exit(0)
        self._insert_message(msg, basicfuncs.useruid.capitalize())

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
        basicfuncs.dologs(msg1, msg2)
        self.text_widget.see(END)

        if basicfuncs.dev >= 1:
            print(msg1)
            print("Bot: " + m)


if __name__ == "__main__":
    r = main.devcheck()
    if r == 0:
        r = main.start()
    if r == "choice":
        exit(0)
    app = ChatApplication()
    app.run()
