import unittest
import choboutil


class TestStringMethods(unittest.TestCase):
    def test_basic(self):
        preData = "abcde\nefg\nhi"
        postData = ("<br>").join(preData.split("\n"))
        print (postData)

    def test_checkFilename(self):
        file = "test.cm"
        self.assertTrue((file[-3:]) == ".cm")
        exportFilePath = "apple.htm"
        self.assertTrue(exportFilePath[-4:].lower() == ".htm")
        exportFilePath = "apple.txt"
        self.assertTrue(exportFilePath[-4:].lower() == ".txt")

    def test_hash(self):
        print (choboutil.hash("hello"))
        self.assertTrue(choboutil.hash("0") == 48)

if __name__ == '__main__':
    unittest.main()