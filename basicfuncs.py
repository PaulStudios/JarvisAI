# pylint: disable=W0603
# pylint: disable=W0702
# pylint: disable=E0401

"""
All the function of JarvisAI
"""

import datetime
import logging
import os
import sys
import time
import webbrowser
import ChatbotAPI
import ecapture as ec
import pyttsx3
import requests
from dotenv import load_dotenv

from handler import config
import user
from errors import error

ENGINE = ""
VOICES = 0
MODE = 0
TESTAPI = ""
CONNECTION = 0
MAINAPI = ""
CHATBOT = ChatbotAPI.ChatBot()
LOGGER = logging
USER = ""
LOGNAME = ""
DEV = 0


def init():
    """Initialising function for all variables and basic checks before starting program"""
    global ENGINE, VOICES, TESTAPI, MAINAPI, CHATBOT, LOGGER
    LOGGER = logging.getLogger("JarvisAI.processor")
    LOGGER.info("Loading environment variables")
    load_dotenv()
    LOGGER.info("Setting up voice")
    ENGINE = pyttsx3.init('sapi5')
    VOICES = ENGINE.getProperty('voices')
    ENGINE.setProperty('voice', 'voices[1].id')
    LOGGER.info("Setting up API")
    MAINAPI = str(os.environ["MAINAPI"])
    TESTAPI = str(os.environ["TESTAPI"])
    LOGGER.info("Setting up Chatbot")
    cred = config.chat_config()
    CHATBOT = ChatbotAPI.ChatBot(cred['brainid'], cred['brainkey'], history=True, debug=True)
    # chatbot.spellcheck(True)
    webbrowser.get('windows-default')
    LOGGER.info("Setting up development/production module")
    if len(sys.argv) > 1 and sys.argv[1] == "development":
        print("Development mode enabled")
        MAINAPI = TESTAPI
    else:
        print("Production mode enabled")
        TESTAPI = MAINAPI
    TESTAPI = TESTAPI + "/jarvis"
    LOGGER.info("Checking connection to server")
    checkconnect()
    user.checkdb()
    LOGGER.info("JarvisAI has been initialized successfully. All systems online")


def speak(text):
    """Text-to-Speech function"""
    ENGINE.say(text)
    ENGINE.runAndWait()


def wish_me():
    """Wish the user"""
    hour = datetime.datetime.now().hour
    if 12 > hour >= 0:
        return "Hello,Good Morning"
    if 18 > hour >= 12:
        return "Hello,Good Afternoon"
    return "Hello,Good Evening"


def choice_selector(argument):
    """Replacement for switch-case function"""
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
    }
    return switcher.get(argument, "Invalid Choice")


def take_picture(delay=0):
    """Take a photo"""
    current_date_and_time = datetime.datetime.now()
    filename = "img-" + current_date_and_time.strftime("%f") + ".jpg"
    if delay == 0:
        ec.capture(0, False, filename)
    if delay >= 0:
        ec.delay_imcapture(0, False, filename, delay)
    return filename


def checkconnect():
    """Check server connection"""
    global CONNECTION
    print("Authenticating with JarvisAPI...")
    try:
        checkapi = requests.get(TESTAPI, timeout=10)
        if checkapi.status_code == 200:
            print("Paulstudios : JarvisAPI is online")
            CONNECTION = 1
            return "success"
        error(
            f"ER11A - [Cannot connect to {TESTAPI}, " + str(checkapi.status_code) + "]", 1)
    except requests.exceptions.ConnectionError:
        error(
            f"ER11A - [Cannot connect to {TESTAPI}, " + str(checkapi.status_code) + "]", 1)
    return "failure"


def login_back(username, password):
    """Login server processor"""
    global USER
    print("Trying to log in...")
    LOGGER.info("Trying to login...")
    item = {
        'name': username,
        'pass': password
    }
    LOGGER.info("Sending login request to server")
    response = requests.get(TESTAPI + "/login", item, timeout=10).text
    if response == "OK":
        print("Logged in successfully")
        CHATBOT.changename(username)
        USER = username
        LOGGER.info("Logged in successfully")
        return "success"
    LOGGER.info("Login failed")
    error(response, 1, "auth")
    sys.exit(0)


def register_back(rname, rpass, rmail):
    """Register server processor"""
    print("Trying to register...")
    LOGGER.info("Trying to register...")
    item = {
        'email': rmail,
        'name': rname,
        'pass': rpass
    }
    LOGGER.info("Sending register request to server")
    response = requests.get(TESTAPI + "/register", item, timeout=10).text
    if response == "OK":
        print("Registered successfully")
        # chatbot.changename(rname)
        # user = rname
        LOGGER.info("Registered successfully")
        return "success"
    LOGGER.info("Registration failed")
    error(response, 1, "auth")
    sys.exit(0)


def talk(msg):
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

    elif "weather" in msg:
        get_weather(msg)

    elif 'time' in msg:
        date_and_time_now = datetime.datetime.now().strftime("%H:%M:%S")
        resp = f"The current time is {date_and_time_now}"

    elif "open stackoverflow" in msg:
        webbrowser.open_new_tab("https://stackoverflow.com/login")
        resp = "Here is stackoverflow"

    elif "camera" in msg or "take a photo" in msg:
        resp = "Feature is in production"
        # takepic()

    elif 'search' in msg:
        msg = msg.replace("search", "")
        webbrowser.open_new_tab(msg)
        resp = "Browser opened"
        time.sleep(5)
    else:
        resp = CHATBOT.sendmsg(msg)
    logging.info("Bot response module process completed")
    return resp


def get_weather(city):
    """Get weather of a city"""
    error("ER14 - [Feature Coming Soon]", 1)
    api_key = os.environ['WEATHER_API']
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    print("whats the city name")
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url, timeout=10)
    server_response = response.json()
    if server_response["cod"] != "404":
        internal_server_response = server_response["main"]
        current_temperature = internal_server_response["temp"]
        current_humidiy = internal_server_response["humidity"]
        weather = server_response["weather"]
        weather_description = weather[0]["description"]
        resp = " Temperature in kelvin unit is " + str(
            current_temperature) + "\n humidity in percentage is " + str(
            current_humidiy) + "\n description  " + str(weather_description)
    else:
        resp = " City Not Found "
    return resp


def login_front():
    """Login user"""
    LOGGER.info("Initiating login module")
    username = input("Pls enter your username: ")
    password = input("Pls enter your password: ")
    LOGGER.info("Logging in user")
    login_back(username, password)


def start():
    """Start the program"""
    global MODE
    print("Loading Jarvis 2.0")
    LOGGER.info("Starting Jarvis 2.0")
    time.sleep(0.5)
    print("Please choose command module:")
    print(
        "    1. Microphone (You will have to say the words) [Feature coming soon]")
    print("    2. Keyboard (You will have to type the words)")
    MODE = input("Please input your choice (1/2): ")
    if MODE.isdecimal():
        rchoice = choice_selector(int(MODE))
        if rchoice == "one":
            LOGGER.warning("Feature is in production. Coming Soon")
            LOGGER.warning("Defaulting to keyboard mode")
            MODE = 2
        elif rchoice == "two":
            MODE = 2
        else:
            error("ER12 - [Invalid Choice]")
            LOGGER.warning("Defaulting to keyboard mode")
            time.sleep(0.5)
            print("Invalid choice. Defaulting to keyboard mode")
            MODE = 2
    else:
        error("ER12 - [Invalid Choice]")
        LOGGER.warning("Defaulting to keyboard mode")
        time.sleep(0.5)
        print("Invalid choice. Defaulting to keyboard mode")
        MODE = 2
    LOGGER.info("Command module selected as %s", str(MODE))
    print("\nYou must login to use JarvisAI")
    print("    1. Register")
    print("    2. Login")
    registered = input("Please input your choice (1/2): ")
    if registered.isdecimal():
        rchoice2 = choice_selector(int(registered))
        if rchoice2 == "one":
            user.register()
            return
        if rchoice2 == "two":
            login_front()
            return
        error("ER12 - [Invalid Choice]", 1, "args")
    else:
        error("ER12 - [Invalid Choice]", 1, "args")
    LOGGER.info("User has been logged in to JarvisAI")


# To DO: Add devmode.
# How to comment code-blocks:- Alt+3 & Alt+4
# def devcheck():
#    global dev
# if len(sys.argv) == 4:
# if sys.argv[1] == "devmode":
#            print("Initializing Developer Mode")
#            argcode = [sys.argv[1], sys.argv[3], sys.argv[2]]

#def mic_input():
#    """Speech-to-Text function"""
#    input_from_mic = sr.Recognizer()
#    with sr.Microphone() as source:
#        print("Listening...")
#        input_from_mic.adjust_for_ambient_noise(source=source)
#        audio = input_from_mic.listen(source, timeout=5)
#
#        try:
#            statement = input_from_mic.recognize_google(audio)
#            print(f"user said:{statement}\n")
#
#        except:
#            speak("Pardon me, please say that again")
#            return "None"
#        return statement
