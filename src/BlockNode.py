

from enum import Enum

from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith("#"):
        no_of_hashes = block[:6].count("#")
        if block.startswith("#" * no_of_hashes + " "):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all([l.startswith(">") for l in block.split("\n")]):
        return BlockType.QUOTE

    if all([l.startswith("- ") for l in block.split("\n")]):
        return BlockType.UNORDERED_LIST
    
    if all([l.startswith(f"{i+1}. ") for i, l in enumerate(block.split("\n"))]):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


