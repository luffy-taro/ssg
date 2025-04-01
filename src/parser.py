import re
from typing import List
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    output = []
    for node in old_nodes:
        # iterate over node text
        found_opening = False
        prev = None
        for i, c in enumerate(node.text):
            if c == delimiter:
                if not found_opening:
                    found_opening = True
                    n = TextNode(text=node.text[:i], text_type=TextType.TEXT)
                    output.append(n)
                    prev = i
                else:
                    found_opening = False
                    n = TextNode(text=node.text[prev + 1 : i], text_type=text_type)
                    output.append(n)
                    prev = i

        # append remaining string
        n = TextNode(text=node.text[prev + 1 :], text_type=TextType.TEXT)
        output.append(n)

    return output


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
