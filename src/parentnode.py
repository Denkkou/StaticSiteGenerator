from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("Children are not an optional property of ParentNode")
        
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return f"<{self.tag}>{children_string}</{self.tag}>"
    