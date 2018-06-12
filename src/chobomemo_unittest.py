import unittest
import os


class TestStringMethods(unittest.TestCase):
    def test_basic(self):
        preData = "abcde\nefg\nhi"
        postData = ("<br>").join(preData.split("\n"))
        print (postData)

if __name__ == '__main__':
    unittest.main()