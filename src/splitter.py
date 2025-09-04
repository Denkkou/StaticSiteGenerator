from textnode import TextNode, TextType

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
                    if part[1] != "": # skip empty
                        if part[0] % 2 == 0: # evens are plain
                            new_nodes.append(TextNode(part[1], TextType.TEXT))
                        else: # odds are special
                            new_nodes.append(TextNode(part[1], text_type))
            else:
                raise Exception("Invalid markdown syntax: Unpaired delimiter")
    return new_nodes
                
