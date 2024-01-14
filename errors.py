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
    if severity > 0:
        LOGGER.warning("Error has been detected. Investigating...")
        if errortype == "auth":
            LOGGER.error("Authentication error has been detected. Error code : %s", code)
            raise AuthError(code)
        if errortype == "args":
            LOGGER.error("Argument error has been detected. Error code : %s", code)
            raise ArgumentError(code)
        if errortype == "conn":
            LOGGER.error("Connection error has been detected. Error code : %s", code)
            raise ConnectError(code)
        LOGGER.error("Program error has been detected. Error code : %s", code)
        raise BaseError(code)
    LOGGER.error("Error has been detected. Investigating... Error Code %s", code)
    LOGGER.error("Severity is low. Continuing...")
    print("Something went wrong. Error Code :- " + code + ".")
    print("Please seek support from developer with the error code.")
