import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_full(self):
        node = HTMLNode("p", "text inside paragraph", [1, 2, 3], {"href": "www.google.com", "target": "_blank"})
        self.assertIsNotNone(node.props_to_html())

    def test_props_empty(self):
        node = HTMLNode("p", "text inside paragraph", [1, 2, 3], {})
        self.assertEqual("", node.props_to_html())
    
    def test_props_none(self):
        node = HTMLNode("p", "text inside paragraph", [1, 2, 3], None)
        self.assertEqual("", node.props_to_html())
    
    def test_repr(self):
        node = HTMLNode("p", "text inside paragraph", [1, 2, 3], {"href": "www.google.com", "target": "_blank"})
        self.assertIn("HTMLNode(", node.__repr__())

    def test_tohtml(self):
        node = HTMLNode("p", "text inside paragraph", [1, 2, 3], {"href": "www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()