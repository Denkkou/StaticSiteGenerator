import unittest
from regex_helpers import extract_markdown_images, extract_markdown_links

class TestRegexHelpers(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://img/image.png)"
        )
        self.assertListEqual([("image", "https://img/image.png")], matches)

    def test_extract_markdown_images_mult(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://img/image1.png) and ![image2](https://img/image2.png)"
        )
        self.assertListEqual([("image1", "https://img/image1.png"),("image2", "https://img/image2.png")], matches)
    
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images")
        self.assertEqual([], matches)
    
    def test_extract_markdown_links_mult(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_mult(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links")
        self.assertEqual([], matches)