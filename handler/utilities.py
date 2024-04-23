# pylint: disable=E0401

# skipcq
"""
Various small commands
"""
import os
import re
import sys

from rich import pretty
from rich.console import Console
from textblob import TextBlob

from cfg import countries

pretty.install()
console = Console()


def print_custom(text: str, st: str = None):
    """Wrapper"""
    console.print(text, end='', style=st)


def choice_selector(argument):
    """Replacement for switch-case function"""
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
    }
    return switcher.get(argument, "Invalid Choice")


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # skipcq: PYL-W0212
    except Exception:  # skipcq: PYL-W0703
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def correction(data):
    """Spellcheck"""
    text = TextBlob(data)
    text = text.correct()
    return str(text)


def get_field_index(field: str) -> int:
    """Returns index for a field name"""
    f = field
    switcher = {
        "Name": 0,
        "Username": 1,
        "Country": 2,
        "Email": 3,
        "Password": 4
    }
    i = switcher.get(f, 10)
    return i


def checkmail(email: str) -> bool:
    """Checks Syntax for emails"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return True
    return False


def countries_exist(val: str):
    """Checks if country exists"""
    c = val.lower()
    if c in countries:
        return True
    return False


def hide_info(value: str, itype: int = 0) -> str:
    """Replaces sensitive info with '*'"""
    field_data = ""
    if itype == 1:
        full = value.split("@")
        f = full[0]
        field_data = ""
        for unused_i in f:
            field_data = field_data + "*"
        field_data = field_data + "@" + full[1]
    elif itype == 0:
        f = value
        field_data = ""
        for unused_i in f:
            field_data = field_data + "*"
    return field_data


def createlist(r) -> list:
    """Creates list from a number"""
    return list(range(0, r))
