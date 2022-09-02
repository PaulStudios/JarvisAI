import unittest
import basicfuncs

basicfuncs.init()

class MyTestCase(unittest.TestCase):
    def test_server_connection(self):
        self.assertEqual(basicfuncs.connection, 1)

    def test_bot(self):
        self.assertEqual(basicfuncs.login("test", "tester"), "success")
        self.assertEqual("test", basicfuncs.user)
        self.assertEqual(basicfuncs.talk("Hi"), "Hi there!")


if __name__ == '__main__':
    unittest.main()
