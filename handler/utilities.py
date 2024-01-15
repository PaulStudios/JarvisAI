"""
Various small commands
"""

from rich import pretty, print
from rich.console import Console

pretty.install()
console = Console()


def printn(text: str, st:str = None):
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
