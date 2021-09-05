import json
from ecapture import ecapture as ec
from ChatbotAPI.chatbasics import sendmsg
from ChatbotAPI.chatbasics import chatbotsetup
import pyttsx3
import os
import time
import datetime
import requests
import re
from dotenv import load_dotenv

engine = 0
voices = 0
apiurl = 0
testapi = 0
useruid = 0
logging = 0
logname = ""
dev = 0
authdata = {}
logfile = ""


def init():
    global  useruid, engine, voices, apiurl, testapi, authdata, logname
    load_dotenv()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[1].id')
    testapi = os.getenv("TESTAPI")
    apiurl = os.getenv("MAINAPI")
    useruid = ""
    logname = "logs/ChatLogs-" + datetime.datetime.now().strftime("%f") + ".txt"
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    open(logname,'x')
    authdata = {
        "test": {
            "name": "testing",
            "email": "testing"
        },
        "owner": {
            "name": "pass132",
            "email": "owner@ps.com"
        },
        "hilfing": {
            "name": "indra",
            "email": "indradip.paul@outlook.com"
        }
    }

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


def talk(msg1):
    if useruid == "" or useruid == 0:
        print("Pls Login!")
        return "not logged in"
    chatbotsetup("156099", "4TG9iu82pFOu9XjD", useruid)
    chat = sendmsg(msg1)
    print(chat)
    speak(chat)
    return chat

def talk2(msg1):
    if useruid == "" or useruid == 0:
        print("Pls Login!")
        return "not logged in"
    chatbotsetup("156099", "4TG9iu82pFOu9XjD", useruid)
    chat = sendmsg(msg1)
    return chat

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
    global apiurl
    print("Connecting to PaulStudiosAPI...")
    time.sleep(2)
    try:
        checkapi = requests.get(apiurl)
        if checkapi.status_code == 200:
            print("Successfully connected to server")
            return "success"
        else:
            print("Cannot connect to server")
            return "failed"
    except requests.exceptions.ConnectionError:
        print("Cannot connect to server")
        return "failed"


def login(username, password):
    global useruid
    users = json.loads(requests.get(apiurl + "/customers").text)
    print("Trying to log in through PaulStudiosAPI")
    time.sleep(1)
    usersdata = [i['name'] for i in users]
    if username in usersdata:
        for name in usersdata:
            if name == username:
                nameofuser = name
    else:
        print("Username not found")
        return "not found user"

    print("Found username. Fetching User data")
    time.sleep(1)
    userindex = usersdata.index(nameofuser) + 1
    userdata = json.loads(requests.get(apiurl + "/customers/" + str(userindex)).text)
    userpass = userdata['pass']
    if userpass == password:
        print("Password Matched. Logging in")
        time.sleep(1)
        print("Successfully logged in")
        useruid = username
        return username
    else:
        print("Wrong password")
        return "wrong pass"


def register(rname, rpass, rmail):
    users = json.loads(requests.get(apiurl + "/customers").text)
    print("Trying to register through PaulStudiosAPI")
    time.sleep(2)
    usernames = [i['name'] for i in users]
    useremails = [i['email'] for i in users]
    if rname in usernames:
        print("Username already exists.")
        return "same name"
    if rmail in useremails:
        print("Email already exists.")
        return "same mail"
    rdata = {
        'email': rmail,
        'name': rname,
        'pass': rpass,
        'active': 1
    }
    response = requests.post(apiurl + "/customers", data=rdata)
    return json.loads(response.text)


def getownerkey(mode, user, key):
    print("Connecting to PaulStudiosAPI Developer Database.")
    spcauth = {
        "key" : key,
        "mode" : mode,
        "user" : user
    }
    r = requests.get(testapi + "/keys", spcauth).text
    return r


def devmode(mode, user):
    global dev
    print("Authenticating " + mode + " from user " + user)
    time.sleep(1)
    r = addlogs(mode, user)
    print(r)
    dev = 1
    login(user, authdata[user]["name"])
    return r


def checklogs():
    if dev >= 1:
        r = "Here are the Logs  :\n" + requests.get(testapi + "/log").text
        return r
    else:
        return "Devmode is not enabled!"

def addlogs(mode, user):
    auth = {
        "mode": mode,
        "user": user
    }
    r = requests.post(testapi + "/log", data=auth).text
    print("System Access has been logged")
    return r

def deletelogs():
    if dev == 2:
        r = requests.delete(testapi + "/log").text
        return r
    else:
        return "Adminmode is not enabled!"

def adminmode(mode, user):
    global dev
    print("Authenticating " + mode + " from user " + user)
    time.sleep(1)
    r = addlogs(mode, user)
    print(r)
    dev = 2
    login(user, authdata[user]["name"])
    return r

def startlogs():
    global logging
    if dev >= 1:
        logging = 1
        r = "Logger Started in " + logname 
        return r
    else:
        "Devmode is not enabled!"

def dologs(m1, m2):
    if logging == 1:
        logfile = open(logname, "a+")
        logfile.writelines(m1)
        logfile.writelines(m2)
        logfile.close()

def stoplogs():
    global logging
    if logging >= 1:
        logging = 0
        r = "Logger Stopped"
        return r
    else:
        "Logging is not enabled!"

