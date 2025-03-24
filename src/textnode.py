from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    LINK = "url"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node)

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node, {"href": text_node.url})
    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    
    
