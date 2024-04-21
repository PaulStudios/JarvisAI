"""
Logging Module
"""

import os

import cfg
from handler.utilities import printn

class Logger:
    """Logging Class"""
    def __init__(self, name: str = "JarvisAI"):
        self.name = name
        self.filename = cfg.log_name

    def setup(self):
        """Sets up file"""
        if os.path.exists('logs'):
            pass
        else:
            os.mkdir('logs')
        with open(self.filename, 'w', encoding='utf8') as file_test:
            file_test.write("JarvisAI v3.0\n")
