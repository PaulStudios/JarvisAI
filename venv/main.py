import pyttsx3
import os
import time
import subprocess
from dotenv import load_dotenv

print('Loading your AI personal assistant - Jarvis')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[1].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def choiceselector(argument):
    switcher = {
        1: "type",
        2: "mic",
    }
    return switcher.get(argument, "Invalid Choice")

speak("Loading Jarvis one point O")
print("Jarvis can run in 2 modes :")
print("   1. Typing mode(Commands have to typed in keyboard)")
print("   2. Microphone mode(Commands need to said to microphone)")
input = input("Enter your choice (1/2): ")
check = input.isdecimal()
if check :
    choice = choiceselector(int(input))
    if choice == "type":
        exec(open("TypeAI.py").read())
    elif choice == "mic":
        exec(open("MicAI.py").read())
else:
    print("Invalid Choice. Shutting Down")
    exit(0)


