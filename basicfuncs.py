import json

import ChatbotAPI
from ecapture import ecapture as ec
import pyttsx3
import os
import time
import datetime
import requests
import re
from dotenv import load_dotenv
from errors import AuthError, BaseError, ArgumentError


engine = 0
voices = 0
apiurl = 0
connection = 0
mainapi = 0
chatbot = ""
logging = 0
user = ""
logname = ""
dev = 0
logfile = ""

def error(code, severity = 0, type = ""):
    if severity > 0:
        if type == "auth":
            raise(AuthError(code))
        if type == "args":
            raise(ArgumentError(code))
        else:
            raise(BaseError(code))
    else:
        print("Something went wrong. Error Code :- " + code + ".")
        print("Please seek support from developer with the error code.")


def init():
    global  engine, voices, apiurl, mainapi, authdata, logname, chatbot
    load_dotenv()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[1].id')
    mainapi = os.getenv("MAINAPI")
    apiurl = os.getenv("JARVISAPI")
    chatbot = ChatbotAPI.ChatBot(os.getenv("BRAINID"), os.getenv("BRAINKEY"), "", True, True)
    chatbot.spellcheck(True)
    #initlogs()
    checkconnect()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<12:
        return "Hello,Good Morning"
    elif hour>=12 and hour<18:
        return "Hello,Good Afternoon"
    else:
        return "Hello,Good Evening"


def choiceselector(argument):
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
    }
    return switcher.get(argument, "Invalid Choice")

def initlogs():
    global logname
    logname = "logs/ChatLogs-" + datetime.datetime.now().strftime("%f") + ".txt"
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    try:
        open(logname, 'x')
    except FileExistsError:
        raise (BaseError("Log File already exists. Fix : Delete logs folder."))
def takepic(delay = 0):
    x = datetime.datetime.now()
    y = "img-" + x.strftime("%f") + ".jpg"
    if delay == 0:
        ec.capture(0, False, y)
        return y
    elif delay >= 0:
        ec.delay_imcapture(0, False, y, delay)
        return y


def checkmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.match(regex, email)):
        print("Email has been detected as Valid")
        return "valid"
 
    else:
        print("Email has been detected as Invalid")
        return "invalid"


def checkconnect():
    global apiurl, connection
    print("Connecting to server...")
    time.sleep(2)
    try:
        checkapi = requests.get(mainapi)
        if checkapi.status_code == 200:
            print("Successfully connected to PaulStudios server")
        else:
            error("ER11 - [Cannot connect to server]", 1)
    except requests.exceptions.ConnectionError:
        error("ER11 - [Cannot connect to server]", 1)
    try:
        checkapi = requests.get(apiurl)
        if checkapi.status_code == 200:
            print("Paulstudios : JarvisAPI is online")
            connection = 1
            return "success"
        else:
            error("ER11 - [Cannot connect to server]", 1)
    except requests.exceptions.ConnectionError:
        error("ER11 - [Cannot connect to server]", 1)


def login(username, password):
    global user
    print("Trying to log in...")
    item = {
        'name': username,
        'pass': password
    }
    response = requests.get(apiurl + "/login", item).text
    if response == "OK":
        print("Logged in successfully")
        chatbot.changename(username)
        user = username
        return "success"
    else:
        error(response, 1, "auth")
        exit(0)


def register(rname, rpass, rmail):
    global user
    print("Trying to register...")
    item = {
        'email': rmail,
        'name': rname,
        'pass': rpass
    }
    response = requests.get(apiurl + "/register", item).text
    if response == "OK":
        print("Registered successfully")
        chatbot.changename(rname)
        user = rname
        return "success"
    else:
        error(response, 1, "auth")
        exit(0)

def talk(msg):
    resp = chatbot.sendmsg(msg)
    return resp
