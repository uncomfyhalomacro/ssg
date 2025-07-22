import unittest
from ssg.utils import extract_title


class UtilsTest(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is a title

WOAH
"""
        self.assertEqual("This is a title", extract_title(md))

    def test_fail_no_title(self):
        md = """
## This is a title but not a title
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_fail_no_content(self):
        md = """




"""
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
