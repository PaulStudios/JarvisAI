"""
Error handling for the program.
"""

import logging
import sys
from time import sleep

from rich.console import Console
from rich.traceback import install
from rich.progress import track

LOGGER = logging.getLogger("JarvisAI.ErrorHandler")
install(extra_lines=0, show_locals=False)
console = Console()
m_name = "JarvisAI.ErrorHandler: "


class ArgumentError(Exception):
    """Exception raised for errors in the input."""


class AuthError(Exception):
    """Authentication Error"""


class ConnectError(Exception):
    """Server Connection error"""


class BaseError(Exception):
    """Base error class"""


class FileAlreadyExistsError(Exception):
    """File already exists error"""


def error(code, severity=0, errortype=""):
    """Error function to better handle and log errors"""
    LOGGER.warning("Error has been detected. Investigating...")
    console.log(m_name + "Error has been detected. Investigating...", style="bright_red")
    for i in track(range(30), description="[bright_red]Checking Background Processes for error..."):
        sleep(0.1)
    if severity > 0:
        if errortype == "auth":
            LOGGER.critical("Authentication error detected. Error code : %s", code)
            console.log(m_name + "Authentication error detected. Error code : ", code, style="bright_red")
        elif errortype == "args":
            LOGGER.critical("Argument error detected. Error code : %s", code)
            console.log(m_name + "Argument error detected. Error code : ", code, style="bright_red")
        elif errortype == "conn":
            LOGGER.critical("Connection error detected. Error code : %s", code)
            console.log(m_name + "Connection error detected. Error code : ", code, style="bright_red")
        else:
            LOGGER.critical("Program error detected. Error code : %s", code)
            console.log(m_name + "Program error detected. Error code : ", code, style="bright_red")
        sys.exit(0)
    LOGGER.error("Error Code %s", code)
    LOGGER.error("Severity is low. Continuing...")
    console.log(m_name + "Error Code : " + code + " \n" + m_name + "Severity is low. Continuing...", style="bright_red")
