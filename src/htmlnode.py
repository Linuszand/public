

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        arr = []
        if self.props == None:
            return ""
        else:
           for key, value in self.props.items():
               pair = f' {key}="{value}"'
               arr.append(pair)
        return " ".join(arr)

    def __repr__(self):
        node = f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
        return node

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid: Value needed.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
        
    def to_html(self):
        content = ''
        if self.tag == None:
            raise ValueError("Invalid: Object has no tag")
        if self.children == None:
            raise ValueError("Invalid: No children in the house")
        for child in self.children:
            content += child.to_html()
        
        return f'<{self.tag}{self.props_to_html()}>{content}</{self.tag}>'
