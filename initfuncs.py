import time
print('Loading your AI personal assistant - Jarvis')
import sys
from errors import ArgumentError
from basicfuncs import speak, error
import basicfuncs
dev = 0


def register():
    username = input("Pls enter your new username: ")
    password = input("Pls enter your new password: ")
    emailofuser = input("Pls enter your new email: ")
    mailcheck = basicfuncs.checkmail(emailofuser)
    if mailcheck == "valid":
        do = basicfuncs.register(username, password, emailofuser)
        if do == "same name":
            print("Shutting down...")
            time.sleep(1)
            exit(0)
        elif do == "same mail":
            print("Shutting down...")
            time.sleep(1)
            exit(0)
        elif do['name'] == username:
            print("You have been successfully registered. Logging you in")
            time.sleep(1.5)
            basicfuncs.login(username, password)

    elif mailcheck == "invalid":
        print("Shutting down...")
        time.sleep(1)
        exit(0)


def login():
    username = input("Pls enter your username: ")
    password = input("Pls enter your password: ")
    check = basicfuncs.login(username, password)

def devcheck():
    global dev
    if len(sys.argv) == 4:
        if sys.argv[1] == "devmode":
            print("Initializing Developer Mode")
            argcode = [sys.argv[1], sys.argv[3], sys.argv[2]]


def start():
    basicfuncs.init()
    speak("Loading Jarvis 2 point 0")
    print("You must login to use JarvisAI")
    print("    1. Register")
    print("    2. Login")
    registered = input("Please input your choice (1/2): ")
    if registered.isdecimal():
        rchoice = basicfuncs.choiceselector(int(registered))
        if rchoice == "one":
            register()
            return
        elif rchoice == "two":
            login()
            return
    else:
        raise(ArgumentError("Invalid Choice"))



def start2():
    print("Jarvis can run in 2 modes :")
    print("   1. Typing mode(Commands have to typed in keyboard)")
    print("   2. Microphone mode(Commands need to said to microphone)")
    inputofuser = input("Enter your choice (1/2): ")
    check = inputofuser.isdecimal()
    if check:
        choice = basicfuncs.choiceselector(int(inputofuser))
        if choice == "one":
            exec(open("TypeAI.py").read())
        elif choice == "two":
            exec(open("MicAI.py").read())
    else:
        print("Invalid Choice. Shutting Down")
        exit(0)
