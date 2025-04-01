import re
from typing import List
from BlockNode import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    output = []
    for node in old_nodes:
        if node.text.find(delimiter) == -1 or node.text_type != TextType.TEXT:
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

                output.append(
                    TextNode(match[0], text_type=TextType.IMAGE, url=match[1])
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


def split_nodes_link(old_nodes: List[TextNode]):
    output = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if matches:
            node_text = node.text
            for match in matches:
                link_text = f"[{match[0]}]({match[1]})"
                before_text = node_text.split(link_text, 1)
                if before_text and before_text[0]:
                    output.append(
                        TextNode(text=before_text[0], text_type=node.text_type)
                    )

                output.append(
                    TextNode(match[0], text_type=TextType.LINK, url=match[1])
                )
                node_text = node_text[
                    node_text.find(link_text) + len(link_text) :
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
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
    )
    initial_node = TextNode(text=text, text_type=TextType.TEXT)
    output = [initial_node]

    output = split_nodes_image(output)
    output = split_nodes_link(output)

    for t in types:
        output = split_nodes_delimiter(output, delimiter=t[0], text_type=t[1])

    return output



def markdown_to_blocks(md):
    out = []
    for line in md.split("\n\n"):
        line = line.strip()
        out.append(line)

    return out


def list_block_to_list_html_items(block):
    list_items = []
    for list_item in block.split("\n"):
        list_item = list_item.split(" ", 1)[1]
        nodes = text_to_textnodes(list_item)
        leaf_nodes = []
        for node in nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        list_items.append(ParentNode("li", children=leaf_nodes))
    return list_items


def block_children_to_html(block):
    leaf_nodes = []
    nodes = text_to_textnodes(block)
    for node in nodes:
        leaf_nodes.append(text_node_to_html_node(node))

    return leaf_nodes


def strip_header_hashes(block):
    no_of_hashes = block[:6].count("#")
    block = block[no_of_hashes:]
    block = block.lstrip()
    return no_of_hashes, block


def block_to_html(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        tag = "p"
        block = " ".join(block.splitlines())
        leaf_nodes = block_children_to_html(block)
    
    if block_type == BlockType.HEADING:
        no_of_hashes, block = strip_header_hashes(block)
        tag = f"h{no_of_hashes}"
        leaf_nodes = block_children_to_html(block)
    
    if block_type == BlockType.QUOTE:
        tag = "blockquote"
        leaf_nodes = []
        lines = block.splitlines()
        for line in lines:
            line = line.lstrip(">").strip()
            if not line:
                continue
            leaf_nodes = leaf_nodes + block_children_to_html(line)

    if block_type == BlockType.CODE:
        tag = "pre"
        code_content = block.strip("```")
        code_content = code_content.lstrip()
        leaf_nodes = [LeafNode("code", value=code_content)]
    
    if block_type == BlockType.UNORDERED_LIST:
        tag = "ul"
        leaf_nodes = list_block_to_list_html_items(block)

    if block_type == BlockType.ORDERED_LIST:
        tag = "ol"
        leaf_nodes = list_block_to_list_html_items(block)

    if not leaf_nodes:
        return None

    return ParentNode(tag, children=leaf_nodes)


def extract_title(markdown):
    block = markdown_to_blocks(markdown)[0]
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING and not block.startswith("# "):
        raise Exception("Markdown file needs to have a header")
    _, block = strip_header_hashes(block)
    return block

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    tags = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block = block.strip()
        if not block:
            continue

        html_node = block_to_html(block, block_type)
        if not html_node:
            continue
        tags.append(html_node)

    return ParentNode("div", children=tags)
