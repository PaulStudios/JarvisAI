import json

from BrainshopChatbotAPI.chatbasics import sendmsg
from BrainshopChatbotAPI.chatbasics import chatbotsetup
import pyttsx3
import os
import time
import datetime
import requests
import re
from dotenv import load_dotenv

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[1].id')
load_dotenv()
apiurl = os.getenv("URL")
useruid = 0


def init():
    global  useruid
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
    pass


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
    checkapi = requests.get(apiurl)
    if checkapi.status_code == 200:
        print("Successfully connected to server")
        return "success"
    else:
        print("Cannot connect to server")
        return "failed"


def login(username, password):
    global useruid
    users = requests.get(apiurl + "/users").json()
    print("Trying to log in through PaulStudiosAPI")
    time.sleep(1)
    usersdata = [i['name'] for i in users.values()]
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
    userdata = requests.get(apiurl + "/users/" + str(userindex)).json()
    userpass = userdata['password']
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
    users = requests.get(apiurl + "/users").json()
    print("Trying to register through PaulStudiosAPI")
    time.sleep(2)
    usernames = [i['name'] for i in users.values()]
    useremails = [i['email'] for i in users.values()]
    if rname in usernames:
        print("Username already exists.")
        return "same name"
    if rmail in useremails:
        print("Email already exists.")
        return "same mail"
    rdata = {
        'name': rname,
        'password': rpass,
        'rank': "user",
        'email': rmail
    }
    response = requests.post(apiurl + "/users", data=rdata)
    return response.text
