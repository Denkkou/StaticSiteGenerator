import unittest
from splitters import split_nodes_delimiter, split_nodes_image, split_nodes_link
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
    
    # Splitter functions for images and links
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This text starts with an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This text starts with an image.", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_images_end(self):
        node = TextNode(
            "This text ends with an image. ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text ends with an image. ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode(
            "There is no image in this text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There is no image in this text.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),               
            ],
            new_nodes,
        )

    def test_split_links_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) This text starts with a link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" This text starts with a link.", TextType.TEXT),            
            ],
            new_nodes,
        )

    def test_split_links_end(self):
        node = TextNode(
            "This text ends with a link. [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text ends with a link. ", TextType.TEXT),    
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),        
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),        
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode(
            "This text has no links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has no links.", TextType.TEXT),        
            ],
            new_nodes,
        )