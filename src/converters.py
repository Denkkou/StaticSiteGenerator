from textnode import TextNode, TextType
from leafnode import LeafNode
from splitters import *
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode text_type unhandled")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Code > Images > Links > Bold > Italics
    splitters = [
        lambda ns: split_nodes_delimiter(ns, "`", TextType.CODE),
        lambda ns: split_nodes_image(ns),
        lambda ns: split_nodes_link(ns),
        lambda ns: split_nodes_delimiter(ns, "**", TextType.BOLD),
        lambda ns: split_nodes_delimiter(ns, "_", TextType.ITALIC),
    ]
    return apply_splitters(nodes, splitters)
    
def apply_splitters(nodes, splitter_list):
    current = nodes
    for splitter in splitter_list:
        current = splitter(current)
    return current

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    stripped_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            stripped_blocks.append(stripped)
    return stripped_blocks