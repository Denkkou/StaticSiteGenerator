import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    # Extract header tests
    def test_extract_header(self):
        md = """
# Hello this is a h1 heading

This is not a heading

# This is an erroneous extra h1
"""

        heading = extract_title(md)
        self.assertEqual(
            heading,
            "Hello this is a h1 heading"
        )

    def test_extract_header_multiple(self):
        md = """
## This is not the heading we want

# This is the heading we want

This is not a heading

# This is an erroneous extra h1
"""
        heading = extract_title(md)
        self.assertEqual(
            heading,
            "This is the heading we want"
        )

    def test_extract_header_none(self):
        md = """
This markdown text contains no headers

Maybe a cheeky hidden # one that shouldn't be found
"""
        with self.assertRaises(Exception):
            heading = extract_title(md)