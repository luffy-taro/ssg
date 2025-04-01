import re
from typing import List
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    output = []
    for node in old_nodes:
        if node.text.find(delimiter) == -1:
            output.append(node)
            continue

        # iterate over node text
        node_text = node.text

        while node_text.find(delimiter) > -1:
            opening = node_text.find(delimiter)
            closing = node_text.find(delimiter, opening + len(delimiter))

            if closing == -1:
                if node_text:
                    output.append(TextNode(text=node_text, text_type=TextType.TEXT))
                break

            before_text = node_text[:opening]
            if before_text:
                output.append(TextNode(text=before_text, text_type=TextType.TEXT))

            inner_text = node_text[opening + len(delimiter) : closing]
            
            if inner_text:
                output.append(TextNode(text=inner_text, text_type=text_type))
            
            node_text = node_text[closing + len(delimiter):]
            
        if node_text:
            output.append(TextNode(text=node_text, text_type=TextType.TEXT))

    return output


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    output = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if matches:
            node_text = node.text
            for match in matches:
                image_text = f"![{match[0]}]({match[1]})"
                before_text = node_text.split(image_text, 1)
                if before_text and before_text[0]:
                    output.append(
                        TextNode(text=before_text[0], text_type=TextType.TEXT)
                    )
                    node_text = node_text[
                        node_text.find(image_text) + len(image_text) :
                    ]

                output.append(
                    TextNode(match[0], text_type=TextType.IMAGE, url=match[1])
                )
            if node_text:
                output.append(
                    TextNode(text=node_text, text_type=node.text_type)
                )
        else:
            output.append(node)
    return output


def split_nodes_link(old_nodes: List[TextNode]):
    output = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if matches:
            node_text = node.text
            for match in matches:
                image_text = f"[{match[0]}]({match[1]})"
                before_text = node_text.split(image_text, 1)
                if before_text and before_text[0]:
                    output.append(
                        TextNode(text=before_text[0], text_type=node.text_type)
                    )

                output.append(
                    TextNode(match[0], text_type=TextType.LINK, url=match[1])
                )
                node_text = node_text[
                    node_text.find(image_text) + len(image_text) :
                ]
            
            if node_text:
                output.append(
                    TextNode(text=node_text, text_type=node.text_type)
                )

        else:
            output.append(node)
    return output


def text_to_textnodes(text):
    types = (
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    )
    initial_node = TextNode(text=text, text_type=TextType.TEXT)
    output = [initial_node]

    for t in types:
        output = split_nodes_delimiter(output, delimiter=t[0], text_type=t[1])

    output = split_nodes_image(output)
    output = split_nodes_link(output)
    return output