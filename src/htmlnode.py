class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    
    def to_html(self):
        raise NotImplementedError('to_html method not implemented')
    
    def props_to_html(self):
        if not self.props:
            return ''
        formatted_props = ''
        for prop in self.props:
            formatted_props += f' {prop}="{self.props[prop]}"'
        return formatted_props
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.props})'
    
    def to_html(self):
        if self.value is None:
            raise ValueError(f"invalid HTML: no value in LeafNode with tag={self.tag}, props={self.props}")
        if not self.tag:
            return self.value
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f'ParentNode({self.tag}, children: {self.children}, {self.props})'

    def to_html(self):
        if not self.tag:
            raise ValueError('invalid HTML: no tag')
        if not self.children:
            raise ValueError('Children required in ParentNode')
        children_html = ''
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
    
