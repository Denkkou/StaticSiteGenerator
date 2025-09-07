import unittest
from converters import text_node_to_html_node, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType
from htmlnode import HTMLNode

class TestConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">This is a link text node</a>')

    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="www.google.com" alt="This is an image text node"></img>')
    
    def test_unhandled(self):
        with self.assertRaises(Exception):
            node = TextNode("This is an unhandled node type", 10)
            html_node = text_node_to_html_node(node)
    
    # Text to TextNode
    def test_comprehensive_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            textnodes
        )

    def test_comprehensive_split_text(self):
        text = "There is nothing to split in this text."
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("There is nothing to split in this text.", TextType.TEXT),
            ],
            textnodes
        )
    
    def test_comprehensive_split_nested(self):
        text = "There are delimiters within the image ![image_with_underscores](https://image.img)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("There are delimiters within the image ", TextType.TEXT),
                TextNode("image_with_underscores", TextType.IMAGE, "https://image.img")
            ],
            textnodes
        )
    
    # Markdown to Blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_gappy(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here


This is the same paragraph on a new line


- This is a list


- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "- This is a list",
                "- with items",
            ],
        )