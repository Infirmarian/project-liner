# © Robert Geil 2018
import unittest
import comutils
import localprog
import os


class TestCommutils(unittest.TestCase):
    def test_language_id(self):
        self.assertEqual("C#", comutils.get_language("some random file.cs"))
        self.assertEqual("Java", comutils.get_language("java.java"))
        self.assertEqual("C++", comutils.get_language("this.has/other.periods/proj.cpp"))
        self.assertEqual("HTML", comutils.get_language("sometimesTheseAreCapitalized.HTML"))
        self.assertEqual(None, comutils.get_language("unknownextension.ttyla"))
        self.assertEqual(None, comutils.get_language("noextension"))

class TestLocalprog(unittest.TestCase):
    def test_hidden_directories(self):
        self.assertTrue(localprog.is_hidden(".git"))
        self.assertTrue(localprog.is_hidden(".someotherfile"))
        self.assertTrue(localprog.is_hidden("/.someotherfile"))
        self.assertTrue(localprog.is_hidden("/Users/absoute/path/.someotherfile"))

        self.assertFalse(localprog.is_hidden("Not a hidden file"))
        self.assertFalse(localprog.is_hidden("/Users/file.cpp"))

    def test_file_length(self):
        self.assertEqual(0, localprog.get_lines_from_file("/Users/this/is/definitely/not/a/file"))
        self.assertEqual(0, localprog.get_lines_from_file(""))
        self.assertEqual(0, localprog.get_lines_from_file(os.path.dirname(os.path.realpath(__file__))))
        self.assertEqual(0, localprog.get_lines_from_file("test_data"))
        self.assertEqual(0, localprog.get_lines_from_file("test_data/empty.txt"))

        self.assertEqual(5, localprog.get_lines_from_file("test_data/5lines.txt"))
    

if __name__ == '__main__':
    unittest.main()