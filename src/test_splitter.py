import unittest
from splitter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_code_text(self):
        node = TextNode("This block contains `code text` within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This block contains ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" within it", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_text(self):
        node = TextNode("This block contains **bold text** within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This block contains ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" within it", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_text(self):
        node = TextNode("This block contains _italic text_ within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This block contains ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" within it", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unpaired_delimiter(self):
        node = TextNode("This block contains an _unpaired delimiter within it", TextType.TEXT)
        with self.assertRaises(Exception):
                new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    
    def test_multiple_delimiter_pairs(self):
        node = TextNode("This block contains **bold text 1** and **bold text 2** within it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This block contains ", TextType.TEXT),
            TextNode("bold text 1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold text 2", TextType.BOLD),
            TextNode(" within it", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)