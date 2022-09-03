import unittest
import basicfuncs

class MyTestCase(unittest.TestCase):
    def test_server_connection(self):
        self.assertEqual(basicfuncs.connection, 1)

    def test_login(self):
        self.assertEqual(basicfuncs.login_back("test", "tester"), "success")
        self.assertEqual("test", basicfuncs.user)

    def test_bot(self):
        self.assertEqual(basicfuncs.chatbot.authorname, "HilFing")
        print(basicfuncs.chatbot.getcreds())
        self.assertEqual(basicfuncs.talk("Hi"), "Hi there!")


if __name__ == '__main__':
    unittest.main()
