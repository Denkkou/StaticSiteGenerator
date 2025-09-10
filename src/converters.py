from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode
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

def markdown_to_html_node(markdown):
    parent_htmlnode = HTMLNode("div", None, [], None)
    blocknodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        blocknode = None        
        match block_type:
            case BlockType.HEADING: 
                blocknode = heading_block_to_html(block)
            case BlockType.CODE:
                blocknode = code_block_to_html(block)
            case BlockType.QUOTE:
                blocknode = quote_block_to_html(block)
            case BlockType.UNORDERED_LIST:
                blocknode = unordered_list_block_to_html(block)
            case BlockType.ORDERED_LIST:
                blocknode = ordered_list_block_to_html(block)
            case BlockType.PARAGRAPH:
                blocknode = paragraph_block_to_html(block)
            case _:
                raise Exception("Unhandled error")      
        blocknodes.append(blocknode)    
    parent_htmlnode.children = blocknodes
    return parent_htmlnode

def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def heading_block_to_html(block):
    number_of_hashes = 0
    while number_of_hashes < min(6, len(block)) and block[number_of_hashes] == "#":
        number_of_hashes += 1
    
    text = block[number_of_hashes+1:].strip()    
    children = text_to_children(text)
    return HTMLNode(f"h{number_of_hashes}", None, children, None)

def code_block_to_html(block):
    code_lines = block.splitlines()
    code_text = "\n".join(code_lines[1:-1]) + "\n"
    code_html = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return HTMLNode("pre", None, [code_html], None)

def quote_block_to_html(block):
    quote_lines = block.splitlines()
    tidied_lines = []
    for line in quote_lines:
        if line.startswith(">"):
            line = line[1:].strip()
        elif line.startswith("> "):
            line = line[2:].strip()
        tidied_lines.append(line)     
    text = "\n".join(tidied_lines)
    children = text_to_children(text)
    return HTMLNode("blockquote", None, children, None)

def unordered_list_block_to_html(block):
    list_lines = block.splitlines()
    li_children = []
    for line in list_lines:
        line = line[2:].strip()
        li_children.append(HTMLNode("li", None, text_to_children(line), None)) 
    return HTMLNode("ul", None, li_children, None)
    

def ordered_list_block_to_html(block):
    list_lines = block.splitlines()
    li_children = []
    for line in list_lines:
        dot_space = line.find(". ")
        line = line[dot_space + 2:].strip()
        li_children.append(HTMLNode("li", None, text_to_children(line), None)) 
    return HTMLNode("ol", None, li_children, None)

def paragraph_block_to_html(block):
    text = " ".join(block.splitlines()).strip()
    children = text_to_children(text)
    return HTMLNode("p", None, children, None)