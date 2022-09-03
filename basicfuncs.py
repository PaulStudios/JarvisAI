import json
import subprocess
import sys
import webbrowser
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
mode = 0
apiurl = 0
connection = 0
mainapi = 0
chatbot = ChatbotAPI.ChatBot()
logging = 0
user = ""
logname = ""
dev = 0
logfile = ""


def error(code, severity=0, type=""):
    if severity > 0:
        if type == "auth":
            raise AuthError(code)
        if type == "args":
            raise ArgumentError(code)
        else:
            raise BaseError(code)
        exit(1)
    else:
        print("Something went wrong. Error Code :- " + code + ".")
        print("Please seek support from developer with the error code.")


def init():
    global engine, voices, apiurl, mainapi, authdata, logname, chatbot
    load_dotenv()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[1].id')
    mainapi = os.getenv("MAINAPI")
    apiurl = os.getenv("JARVISAPI")
    chatbot = ChatbotAPI.ChatBot(os.getenv("BRAINID"), os.getenv("BRAINKEY"), history=True, debug=True)
    chatbot.spellcheck(True)
    webbrowser.get('windows-default')
    # initlogs()
    checkconnect()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        return "Hello,Good Morning"
    elif hour >= 12 and hour < 18:
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


def takepic(delay=0):
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
    if (re.match(regex, email)):
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
            error("ER11 - [Cannot connect to server, " + str(checkapi.status_code) + "]", 1)
    except requests.exceptions.ConnectionError:
        error("ER11 - [Cannot connect to server, " + str(checkapi.status_code) + "]", 1)
    try:
        checkapi = requests.get(apiurl)
        if checkapi.status_code == 200:
            print("Paulstudios : JarvisAPI is online")
            connection = 1
            return "success"
        else:
            error("ER11 - [Cannot connect to server, " + str(checkapi.status_code) + "]", 1)
    except requests.exceptions.ConnectionError:
        error("ER11 - [Cannot connect to server, " + str(checkapi.status_code) + "]", 1)


def login_back(username, password):
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


def register_back(rname, rpass, rmail):
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
        # chatbot.changename(rname)
        # user = rname
        return "success"
    else:
        error(response, 1, "auth")
        exit(0)


def talk(msg):
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

    elif "weather" in msg:
        get_weather(msg)

    elif 'time' in msg:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        resp = f"the time is {strTime}"

    elif "open stackoverflow" in msg:
        webbrowser.open_new_tab("https://stackoverflow.com/login")
        resp = "Here is stackoverflow"

    elif "camera" in msg or "take a photo" in msg:
        resp = "Feature is in production"
        takepic()

    elif 'search' in msg:
        msg = msg.replace("search", "")
        webbrowser.open_new_tab(msg)
        resp = "Browser opened"
        time.sleep(5)
    else:
        resp = chatbot.sendmsg(msg)
    return resp

def get_weather(city):
    raise error("ER14 - [Feature Coming Soon]", 1)
    api_key = "8ef61edcf1c576d65d836254e11ea420"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    speak("whats the city name")
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        resp = " Temperature in kelvin unit is " + str(current_temperature) + "\n humidity in percentage is " + str(current_humidiy) + "\n description  " + str(weather_description)
    else:
        resp = " City Not Found "


def register_front():
    username = input("Pls enter your new username: ")
    password = input("Pls enter your new password: ")
    emailofuser = input("Pls enter your new email: ")
    mailcheck = checkmail(emailofuser)
    if mailcheck == "valid":
        do = register_back(username, password, emailofuser)
        print("You have been successfully registered. Logging you in")
        time.sleep(1.5)
        login_back(username, password)


    elif mailcheck == "invalid":
        print("Shutting down...")
        time.sleep(1)
        exit(0)


def login_front():
    username = input("Pls enter your username: ")
    password = input("Pls enter your password: ")
    check = login_back(username, password)


def start():
    global mode
    speak("Loading Jarvis 2 point 0")
    print("Please choose command module:")
    print("    1. Microphone (You will have to say the words) [Feature coming soon]")
    print("    2. Keyboard (You will have to type the words)")
    mode = input("Please input your choice (1/2): ")
    if mode.isdecimal():
        rchoice = choiceselector(int(mode))
        if rchoice == "one":
            print("Feature is in production. Coming Soon")
            print("Defaulting to keyboard mode")
            mode = 2
        elif rchoice == "two":
            mode = 2
    else:
        raise ArgumentError("Invalid Choice")

    print("\nYou must login to use JarvisAI")
    print("    1. Register")
    print("    2. Login")
    registered = input("Please input your choice (1/2): ")
    if registered.isdecimal():
        rchoice2 = choiceselector(int(registered))
        if rchoice2 == "one":
            register_front()
            return
        elif rchoice2 == "two":
            login_front()
            return
    else:
        raise ArgumentError("Invalid Choice")


# To DO: Add devmode and integrate legacy options.
# How to comment code-blocks:- Alt+3 & Alt+4
##def devcheck():
##    global dev
##    if len(sys.argv) == 4:
##        if sys.argv[1] == "devmode":
##            print("Initializing Developer Mode")
##            argcode = [sys.argv[1], sys.argv[3], sys.argv[2]]
##

print('Loading your AI personal assistant - Jarvis...')
time.sleep(1)
init()
