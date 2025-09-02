class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props.items()})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attributes_string = ""
        if self.props is not None and self.props != {}:
            for key, value in self.props.items():
                attributes_string += f' {key}="{value}"'
        return attributes_string
            
