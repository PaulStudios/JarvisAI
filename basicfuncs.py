import json
from ecapture import ecapture as ec
from BrainshopChatbotAPI.chatbasics import sendmsg
from BrainshopChatbotAPI.chatbasics import chatbotsetup
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


def init():
    global  useruid, engine, voices, apiurl, testapi
    load_dotenv()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[1].id')
    testapi = os.getenv("TESTAPI")
    apiurl = os.getenv("MAINAPI")
    useruid = ""

def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")


def choiceselector(argument):
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
    }
    return switcher.get(argument, "Invalid Choice")


def talk(msg1):
    if useruid == "":
        print("Pls Login!")
        return "not logged in"
    chatbotsetup("156099", "4TG9iu82pFOu9XjD", useruid)
    chat = sendmsg(msg1)
    print(chat)
    speak(chat)
    return chat

def talk2(msg1):
    if useruid == "":
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
    elif delay >= 0:
        ec.delay_imcapture(0, False, y, delay)


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
    print("Connecting to PaulStudiosAPI Key Database.")
    time.sleep(2)
    spcauth = {
        "key" : key,
        "mode" : mode,
        "user" : user
    }
    r = requests.get(testapi + "/keys", spcauth).text
    return r


def devmode(mode, user):
    print("Authenticating " + mode + " from user " + user)
    time.sleep(1)
    auth = {
        "mode": mode,
        "user": user
    }
    r = requests.post(testapi + "/log", data=auth).text
    print(r)
    if user == "test":
        login("test", "testing")
    return r