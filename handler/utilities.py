# pylint: disable=E0401

# skipcq
"""
Various small commands
"""
import os
import sys

from rich import pretty
from rich.console import Console

pretty.install()
console = Console()


def printn(text: str, st: str = None):
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
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
