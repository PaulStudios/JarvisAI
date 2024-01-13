# pylint: disable=R0903
# pylint: disable=W0104

"""
Pytest test file for main.py
"""

#import basicfuncs

class TestClass:
    """Test class for main.py"""

    def test_temp(self):
        """Temporary"""
        assert 1+1 == 2


#    def test_server_connection(self):
#        """Testing if API server is online"""
#        assert basicfuncs.CONNECTION == 1

#    def test_login(self):
#        """Testing login module"""
#        assert basicfuncs.login_back("test", "tester") == "success"
#        assert "test" == basicfuncs.USER

#    def test_bot(self):
#        """testing bot response module"""
#        assert basicfuncs.CHATBOT.authorname == "HilFing"
#        assert basicfuncs.talk("Hi") == "Hi there!"
