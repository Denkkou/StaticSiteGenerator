from textnode import TextNode, TextType
from leafnode import LeafNode
from splitters import *
from enum import Enum
import re
    
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

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_blocktype(md_block):
    # Code > Headings > UList > OList > Quote > Paragraph
    md_block = md_block.strip()
    lines = md_block.split("\n")

    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} [^\s].*", md_block):
        return BlockType.HEADING
    
    if all(re.match(r"^- [^\s].*$", line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(re.match(r"^\d. .*$", line) for line in lines):
        current_number = 1
        for line in lines:
            if re.match(f"^{current_number}. ", line):
                current_number += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    if all(re.match(r"^>.*$", line) for line in lines):
        return BlockType.QUOTE
    
    return BlockType.PARAGRAPH