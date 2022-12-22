# pylint: disable=R0903
# pylint: disable=W0104

"""
Pytest test file for main.py
"""

import basicfuncs

class TestClass:
    """Test class for main.py"""
    def test_server_connection(self):
        """Testing if API if server is online"""
        basicfuncs.MAINAPI == "https://PaulStudiosAPI.hilfing.repl.co"
        assert basicfuncs.CONNECTION == 1

    def test_login(self):
        """Testing login module"""
        assert basicfuncs.login_back("test", "tester") == "success"
        basicfuncs.EXECMODE = "test"
        assert "test" == basicfuncs.USER

    def test_bot(self):
        """testing bot response module"""
        assert basicfuncs.CHATBOT.authorname == "HilFing"
        assert basicfuncs.talk("Hi") == "Hi there!"
