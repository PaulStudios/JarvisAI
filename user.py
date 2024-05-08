# pylint: disable=W0718
# pylint: disable=R1710
# pylint: disable=W0603
# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=W1201
# pylint: disable=W0622

# skipcq
"""
Login and Register handling
"""

from rich import pretty
from rich.console import Console

import handler
from handler import database, config
from handler import encrypt, decrypt
from handler.errors import error
from handler.logger import Logger
from handler.utilities import print_custom, checkmail, createlist, get_field_index, countries_exist

ser = ()
table_name = config.program_config()['table']
pretty.install()
console = Console()
LOGGER: Logger = Logger("JarvisAI.user")


def checkdb():
    """Check connection"""
    try:
        database.connect()
        database.check()
    except (Exception, handler.database.DataBaseError):  # skipcq: PYL-W0714
        error("ER11B - Failed to connect to Database", 1, "conn")


class User:
    """User Class"""

    def __init__(self):
        LOGGER.info("Connecting to database...")
        checkdb()
        self.userdata: tuple = ()
        self.username: str = ""
        self.name: str = ""
        self._mail: str = ""
        self.country: str = ""
        self.auth: bool = False
        LOGGER.info(
            "Successfully connected to database: JarvisAI - User_Profiles")

    def register(self) -> None:
        """Registers new user"""
        LOGGER.info("Initiating registration module")

        # Taking inputs
        name_check = False
        country_check = False
        email_check = False
        user_check = False
        name = country = email = username = ""

        while not name_check:
            print_custom(
                "Please enter your full name (Only First name and Last name): ",
                "sky_blue1")
            name_in = input()
            if " " not in name_in:
                print_custom("Invalid Name Entered.","bright_red")
                print("\n")
                continue
            name = name_in.split()
            if len(name[0]) < 3 or len(name[1]) < 2:
                print_custom("Invalid Name Entered.", "bright_red")
                print("\n")
                continue
            name_check = True

        while not country_check:
            print_custom("In which country do you live? ", "sky_blue1")
            country = input()
            if not countries_exist(country):
                print_custom(
                    "Invalid Country Entered. Please check the spelling.",
                    "bright_red")
                print("\n")
                continue
            country_check = True

        while not email_check:
            print_custom("Please enter your email address: ", "sky_blue1")
            email = input()
            if not checkmail(email):
                print_custom("Invalid Email Entered.","bright_red")
                print("\n")
                continue
            email_check = True

        while not user_check:
            print_custom("Please enter a username: ", "sky_blue1")
            username = input()
            if len(username) < 5:
                print_custom("Username is too short.", "bright_red")
                print("\n")
                continue
            user_check = True

        print_custom("Please enter a strong password for your account: ",
                     "sky_blue1")
        password = input()
        print_custom("Please confirm your password: ", "sky_blue1")
        pwd = input()
        if pwd == password:
            console.print("Processing inputs...", style="bright_magenta")
        else:
            print_custom("Your passwords do not match.", "bright_red")
            print_custom("Please re-confirm your password: ", "sky_blue1")
            pwd = input()
            if pwd == password:
                console.print("Processing inputs...", style="bright_magenta")
            else:
                error("ER5 - Incorrect Password during registration.", 1,
                      "auth")
        mail = encrypt(email, password)
        pwd = encrypt(password)
        userdata = [name[0], name[1], mail, username, pwd, country]
        fields = [
            "first_name", "last_name", "email", "username", "password",
            "country"
        ]
        LOGGER.info("Registering new user")
        try:
            database.insert(table=table_name, fields=fields, data=userdata)
        except Exception as e:  # skipcq: PYL-W0703
            error("ER9 - Database insertion failed, " + str(e), 1)
        LOGGER.info("Registered new user: " + username)
        console.print("You have been successfully registered. Logging you in",
                      style="bright_green")
        self.login(username, password)

    def login(self, username: str = None, password: str = None) -> None:
        """Logs in user"""
        LOGGER.info("Initiating login module")
        check = 0
        if username is None or password is None:
            check = 1
        if check == 1:
            print_custom("Please enter your username: ", "sky_blue1")
            username = input()
            print_custom("Please enter your password: ", "sky_blue1")
            password = input()
        data = ["username", username]
        i = ()
        LOGGER.info("Logging in user")
        console.print("Processing inputs...", style="bright_magenta")
        try:
            i = database.get_user(table=table_name, data=data)
        except Exception as e:  # skipcq: PYL-W0703
            error("ER10 - Database fetch failed, " + str(e), 1)
        if i is None:
            error("ER2 - Incorrect username", 1, "auth")
        if password == decrypt(i[5].tobytes()):
            self.userdata = i
            self.__putdata(self.userdata)
            self.auth = True
            LOGGER.info("Successfully logged in '" + self.username + "'")
            console.print("\nYou have been successfully logged in!",
                          style="bright_green")
        else:
            error("ER2 - Incorrect password", 1, "auth")

    def __putdata(self, data: tuple):
        """Setup profile"""
        LOGGER.info("Setting up user profile...")
        self.username = data[4]
        self.name = data[1] + " " + data[2]
        self._mail = decrypt(data[3].tobytes(), decrypt(data[5].tobytes()))
        self.country = data[6]


def process_edits(edits: dict, username: str, password: str) -> bool:
    """Processes all edits to DB and encrypts sensitive info"""
    LOGGER.info("Attempting Edits to user profile")
    namedata = ["username", username]
    i = []
    fields = []
    data = []
    new = {}
    fields_full = [
        "first_name", "last_name", "username", "country", "email", "password"
    ]
    try:
        i = database.get_user(table=table_name, data=namedata)
    except Exception as e:  # skipcq: PYL-W0703
        error("ER10 - Database fetch failed, " + str(e), 1)
    if i is None:
        error("ER2 - Incorrect username", 1, "auth")
    if password == decrypt(i[5].tobytes()):
        LOGGER.info("Starting Profile Edits")
        if 0 in edits:
            new.update({0: edits[0].split(" ")[0]})
            new.update({1: edits[0].split(" ")[1]})
            edits.pop(0)
        for key, value in edits.items():
            new.update({key + 1: value})

        for n in createlist(len(fields_full)):
            if n in new:
                fields.append(fields_full[n])
                data.append(new[n])
        database.edit_user(table_name, fields, data, username)
        LOGGER.info("Data update has been processed.")
        pass_i = get_field_index("Password") + 1
        mail_i = get_field_index("Email") + 1
        enc = {}
        if pass_i in new:
            passwrd = new[pass_i]
            enc_pass = encrypt(passwrd)
            enc.update({pass_i: enc_pass})
        else:
            passwrd = password
        if mail_i in new:
            mail = new[mail_i]
            enc_mail = encrypt(mail, passwrd)
            enc.update({mail_i: enc_mail})
        if pass_i in enc or mail_i in enc:
            fields2, data2 = [], []
            for n in createlist(len(fields_full)):
                if n in enc:
                    fields2.append(fields_full[n])
                    data2.append(enc[n])
            database.edit_user(table_name, fields2, data2, username)
            LOGGER.info("Sensitive data has been encrypted")
        return True
    error("ER11 - Profile update failed due to incorrect password", 0, "auth")
    return False
