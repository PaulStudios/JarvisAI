"""
Error handling for the program.
"""

import logging

LOGGER = logging.getLogger("JarvisAI.ErrorHandler")


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
            LOGGER.critical("Authentication error detected. Error code : %s", code)
            raise AuthError(code)
        if errortype == "args":
            LOGGER.critical("Argument error detected. Error code : %s", code)
        if errortype == "conn":
            LOGGER.critical("Connection error detected. Error code : %s", code)
        else:
            LOGGER.critical("Program error detected. Error code : %s", code)
        exit(1)
    LOGGER.error("Error Code %s", code)
    LOGGER.error("Severity is low. Continuing...")
