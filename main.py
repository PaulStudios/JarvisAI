import time

print('Loading your AI personal assistant - Jarvis')

from basicfuncs import speak
import basicfuncs

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
    uid = basicfuncs.login(username, password)
    if uid == "wrong pass":
        print("Shutting down...")
        time.sleep(1)
        exit(0)
    elif uid == "not found user":
        print("Shutting down...")
        time.sleep(1)
        exit(0)
    else:
        print("You are now logged in as " + uid + ".")


def start():
    speak("Loading Jarvis one point O")
    basicfuncs.init()
    connection = basicfuncs.checkconnect()
    time.sleep(1)
    if connection == "failed":
        exit(0)

    print("You must login to use JarvisAI")
    print("    1. Register")
    print("    2. Login")
    registered = input("Pls enter your answer (1/2): ")
    if registered.isdecimal():
        rchoice = basicfuncs.choiceselector(int(registered))
        if rchoice == "one":
            register()
        elif rchoice == "two":
            login()
    else:
        print("Invalid Choice")
        exit(0)



def start2():
    speak("Loading Jarvis one point O")
    basicfuncs.init()
    connection = basicfuncs.checkconnect()
    time.sleep(1)
    if connection == "failed":
        exit(0)

    print("You must login to use JarvisAI")
    print("    1. Register")
    print("    2. Login")
    registered = input("Pls enter your answer (1/2): ")
    if registered.isdecimal():
        rchoice = basicfuncs.choiceselector(int(registered))
        if rchoice == "one":
            register()
        elif rchoice == "two":
            login()


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
