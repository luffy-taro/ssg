
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplemented()
    
    def props_to_html(self) -> str:
        if self.props:
            attrs = []
            for k, v in self.props.items():
                attrs.append(f'{k}="{v}"')
            
            return " ".join(attrs)
        return ""
        
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __eq__(self, value: 'HTMLNode') -> bool:
        return all([self.tag == value.tag, self.value == value.value, self.children == value.children, self.props == value.props])
    
    def get_opening_tag(self) -> str:
        attrs = self.props_to_html()
        return f"<{self.tag}{' ' + attrs if attrs else ''}>"
    
    def get_closing_tag(self) -> str:
        return f"</{self.tag}>"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value="", props=None):
      if not value:
          raise ValueError("value is required")
      
      super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        return f"{self.get_opening_tag()}{self.value}{self.get_closing_tag()}"
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        return f"{self.get_opening_tag()}{''.join([child.to_html() for child in self.children])}{self.get_closing_tag()}"
