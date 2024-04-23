# skipcq
"""
Error handling for the program.
"""

import sys
import time
from time import sleep
from rich.console import Console
from rich.traceback import install
from rich.progress import track

from handler.logger import Logger
from handler.utilities import print_custom

LOGGER: Logger = Logger("JarvisAI.ErrorHandler")
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
    if severity > 0:
        if errortype == "auth":
            LOGGER.critical("Authentication error detected. Error code : " +
                            code)
        elif errortype == "args":
            LOGGER.critical("Argument error detected. Error code : " + code)
        elif errortype == "conn":
            LOGGER.critical("Connection error detected. Error code : " + code)
        else:
            LOGGER.critical("Program error detected. Error code : " + code)
        Exit()
    LOGGER.error("Error Code " + code)
    LOGGER.error("Severity is low. Continuing...")


def Exit():
    """Exit"""
    print("\n")
    print_custom("Goodbye", "bright_red")
    time.sleep(6)
    sys.exit()
