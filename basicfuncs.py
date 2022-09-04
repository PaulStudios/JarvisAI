import sys
import webbrowser
import logging
import ChatbotAPI
import speech_recognition as sr
import ecapture as ec
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
logger = logging
user = ""
logname = ""
dev = 0


def error(code, severity=0, type=""):
    if severity > 0:
        logger.warning("Error has been detected. Investigating...")
        if type == "auth":
            logger.error("Authentication error has been detected. Error code : " + code)
            raise AuthError(code)
        if type == "args":
            logger.error("Argument error has been detected. Error code : " + code)
            raise ArgumentError(code)
        else:
            logger.error("Program error has been detected. Error code : " + code)
            raise BaseError(code)
        exit(1)
    else:
        logger.error(f"Error has been detected. Investigating... Error Code : {code}")
        logger.error("Severity is low. Continuing...")
        print("Something went wrong. Error Code :- " + code + ".")
        print("Please seek support from developer with the error code.")


def init():
    global engine, voices, apiurl, mainapi, authdata, logname, chatbot, logger
    logger = logging.getLogger("JarvisAI.processor")
    logger.info("Loading environment variables")
    load_dotenv()
    logger.info("Setting up voice")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[1].id')
    logger.info("Setting up API")
    mainapi = os.getenv("MAINAPI")
    apiurl = os.getenv("TESTAPI")
    logger.info("Setting up Chatbot")
    chatbot = ChatbotAPI.ChatBot(os.getenv("BRAINID"), os.getenv("BRAINKEY"), history=True, debug=True)
    #chatbot.spellcheck(True)
    webbrowser.get('windows-default')
    logger.info("Setting up development/production module")
    if len(sys.argv) > 1 and sys.argv[1] == "development":
        print("Development mode enabled")
        mainapi = apiurl
        pass
    else:
        print("Production mode enabled")
        apiurl = mainapi
    apiurl = apiurl + "/jarvis"
    logger.info("Checking connection to server")
    checkconnect()
    logger.info("JarvisAI has been initialized successfully. All systems online")


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
        logger.info("Submitted email is valid")
    else:
        logger.warning("Submitted email is invalid")
        error("Email has been detected as Invalid", 1, "auth")


def checkconnect():
    global apiurl, connection
    print("Connecting to server...")
    time.sleep(2)
    try:
        checkapi = requests.get(mainapi)
        if checkapi.status_code == 200:
            print("Successfully connected to PaulStudios server")
        else:
            error(f"ER11 - [Cannot connect to {mainapi}, " + str(checkapi.status_code) + "]", 1)
    except requests.exceptions.ConnectionError:
        error(f"ER11 - [Cannot connect to {mainapi}, " + str(checkapi.status_code) + "]", 1)
    try:
        checkapi = requests.get(apiurl)
        if checkapi.status_code == 200:
            print("Paulstudios : JarvisAPI is online")
            connection = 1
            return "success"
        else:
            error(f"ER11 - [Cannot connect to {apiurl}, " + str(checkapi.status_code) + "]", 1)
    except requests.exceptions.ConnectionError:
        error(f"ER11 - [Cannot connect to {apiurl}, " + str(checkapi.status_code) + "]", 1)


def login_back(username, password):
    global user
    print("Trying to log in...")
    logger.info("Trying to login...")
    item = {
        'name': username,
        'pass': password
    }
    logger.info("Sending login request to server")
    response = requests.get(apiurl + "/login", item).text
    if response == "OK":
        print("Logged in successfully")
        chatbot.changename(username)
        user = username
        logger.info("Logged in successfully")
        return "success"
    else:
        logger.info("Login failed")
        error(response, 1, "auth")
        exit(0)


def register_back(rname, rpass, rmail):
    global user
    print("Trying to register...")
    logger.info("Trying to register...")
    item = {
        'email': rmail,
        'name': rname,
        'pass': rpass
    }
    logger.info("Sending register request to server")
    response = requests.get(apiurl + "/register", item).text
    if response == "OK":
        print("Registered successfully")
        # chatbot.changename(rname)
        # user = rname
        logger.info("Registered successfully")
        return "success"
    else:
        logger.info("Registration failed")
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
        resp = f"The current time is {strTime}"

    elif "open stackoverflow" in msg:
        webbrowser.open_new_tab("https://stackoverflow.com/login")
        resp = "Here is stackoverflow"

    elif "camera" in msg or "take a photo" in msg:
        resp = "Feature is in production"
        #takepic()

    elif 'search' in msg:
        msg = msg.replace("search", "")
        webbrowser.open_new_tab(msg)
        resp = "Browser opened"
        time.sleep(5)
    else:
        resp = chatbot.sendmsg(msg)
    logging.info("Bot response module process completed")
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
    logger.info("Initiating registration module")
    username = input("Pls enter your new username: ")
    password = input("Pls enter your new password: ")
    emailofuser = input("Pls enter your new email: ")
    logger.info("Registering user")
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
    logger.info("Initiating login module")
    username = input("Pls enter your username: ")
    password = input("Pls enter your password: ")
    logger.info("Logging in user")
    check = login_back(username, password)


def start():
    global mode
    speak("Loading Jarvis 2 point 0")
    logger.info("Starting Jarvis 2.0")
    time.sleep(0.5)
    print("Please choose command module:")
    print("    1. Microphone (You will have to say the words) [Feature coming soon]")
    print("    2. Keyboard (You will have to type the words)")
    mode = input("Please input your choice (1/2): ")
    if mode.isdecimal():
        rchoice = choiceselector(int(mode))
        if rchoice == "one":
            logger.warning("Feature is in production. Coming Soon")
            logger.warning("Defaulting to keyboard mode")
            mode = 2
        elif rchoice == "two":
            mode = 2
        else:
            error("ER12 - [Invalid Choice]")
            logger.warning("Defaulting to keyboard mode")
            time.sleep(0.5)
            print("Invalid choice. Defaulting to keyboard mode")
            mode = 2
    else:
        error("ER12 - [Invalid Choice]")
        logger.warning("Defaulting to keyboard mode")
        time.sleep(0.5)
        print("Invalid choice. Defaulting to keyboard mode")
        mode = 2
    logger.info("Command module selected as " + str(mode))
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
            error("ER12 - [Invalid Choice]", 1, "args")
    else:
        error("ER12 - [Invalid Choice]", 1, "args")
    logger.info("User has been logged in to JarvisAI")


# To DO: Add devmode.
# How to comment code-blocks:- Alt+3 & Alt+4
##def devcheck():
##    global dev
##    if len(sys.argv) == 4:
##        if sys.argv[1] == "devmode":
##            print("Initializing Developer Mode")
##            argcode = [sys.argv[1], sys.argv[3], sys.argv[2]]


def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source=source)
        audio=r.listen(source, timeout=5)

        try:
            statement=r.recognize_google(audio)
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


init()
