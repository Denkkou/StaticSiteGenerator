from textnode import TextNode, TextType
from regex_helpers import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
             new_nodes.append(node)
        else:
            delim_count = node.text.count(delimiter)
            if delim_count > 0 and delim_count % 2 == 0:
                parts = node.text.split(delimiter)
                enum_parts = enumerate(parts)

                for part in enum_parts:
                    if part[1] != "":
                        if part[0] % 2 == 0:
                            new_nodes.append(TextNode(part[1], TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(part[1], text_type))
            elif delim_count == 0:
                new_nodes.append(node)
            else:
                raise Exception("Invalid markdown syntax: Unpaired delimiter")
    return new_nodes
                
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_images = extract_markdown_images(original_text)

        if len(extracted_images) <= 0:
            new_nodes.append(node)
        else:
            remaining_text = original_text
            for image in extracted_images:
                sections = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) > 1:
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))

                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        extracted_links = extract_markdown_links(original_text)
        if len(extracted_links) <= 0:
            new_nodes.append(node)
        else:
            remaining_text = original_text
            for link in extracted_links:
                sections = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(sections) > 1:
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes