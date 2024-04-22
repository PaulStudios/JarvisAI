# skipcq

"""
Logging Module
"""

import os
from datetime import datetime
from rich.console import Console

import cfg

console = Console()

f_level = 0
c_level = 0


class Logger:
    """Logging Class"""

    def __init__(self, name: str = "JarvisAI"):
        self.name = name
        self.filename = cfg.log_name

    def update_path(self):
        self.filename = cfg.log_name

    def info(self, msg: str = ""):
        """Error :- INFO"""
        self.update_path()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        er_format = "[" + dt_string + "]" + " - " + self.name + " : " + "INFO" + " - " + msg
        if f_level <= 2:
            with open(self.filename, 'a', encoding='utf8') as file:
                file.write(er_format)
                file.write("\n")
        if c_level <= 2:
            console.log(er_format)

    def warning(self, msg: str = ""):
        """Error :- WARNING"""
        self.update_path()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        c_format = self.name + " : " + "ERROR" + " - " + msg
        er_format = "[" + dt_string + "]" + " - " + self.name + " : " + "WARNING" + " - " + msg
        if f_level <= 3:
            with open(self.filename, 'a', encoding='utf8') as file:
                file.write(er_format)
                file.write("\n")
        if c_level <= 3:
            console.log(c_format, style="bright_yellow")

    def error(self, msg: str = ""):
        """Error :- ERROR"""
        self.update_path()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        c_format = self.name + " : " + "ERROR" + " - " + msg
        er_format = "[" + dt_string + "]" + " - " + self.name + " : " + "ERROR" + " - " + msg
        if f_level <= 4:
            with open(self.filename, 'a', encoding='utf8') as file:
                file.write(er_format)
                file.write("\n")
        if c_level <= 4:
            console.log(c_format, style="bright_red")

    def critical(self, msg: str = ""):
        """Error :- CRITICAL"""
        self.update_path()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        c_format = self.name + " : " + "ERROR" + " - " + msg
        er_format = "[" + dt_string + "]" + " - " + self.name + " : " + "CRITICAL" + " - " + msg
        if f_level <= 5:
            with open(self.filename, 'a', encoding='utf8') as file:
                file.write(er_format)
                file.write("\n")
        if c_level <= 5:
            console.log(c_format, style="bright_red")


def setup_logger(f_lvl: int = 0, c_lvl: int = 0):
    global f_level, c_level
    """Sets up file"""
    if os.path.exists('logs'):
        pass
    else:
        os.mkdir('logs')
    filename = cfg.log_name
    with open(filename, 'w', encoding='utf8') as file_test:
        file_test.write("JarvisAI v3.0\n")
    f_level = f_lvl
    c_level = c_lvl

def initlogs():
    """Initialize logging module"""
    logname = "logs/JarvisAI_Logs-" + datetime.now().strftime(
        "%f") + ".log"
    cfg.log_name = logname
    setup_logger(2, 10)
