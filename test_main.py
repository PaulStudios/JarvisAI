# pylint: disable=R0903

"""
Pytest test file for main.py
"""

import basicfuncs

class TestClass:
    """Test class for main.py"""
    import basicfuncs
    def test_server_connection(self):
        assert basicfuncs.CONNECTION == 1

    def test_login(self):
        assert basicfuncs.login_back("test", "tester") == "success"
        assert "test" == basicfuncs.USER

    def test_bot(self):
        assert basicfuncs.CHATBOT.authorname == "HilFing"
        assert basicfuncs.talk("Hi") == "Hi there!"
