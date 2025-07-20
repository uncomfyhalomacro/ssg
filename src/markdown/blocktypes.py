from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH=0
    HEADING1=1
    HEADING2=2
    HEADING3=3
    HEADING4=4
    HEADING5=5
    HEADING6=6
    QUOTE=7
    UNORDERED_LIST=8
    ORDERED_LIST=9
    CODE_BLOCK=10

def block_to_block_type(block):
    if block.startswith("#" * 1 + " "):
        return BlockType.HEADING1
    if block.startswith("#" * 2 + " "):
        return BlockType.HEADING2
    if block.startswith("#" * 3 + " "):
        return BlockType.HEADING3
    if block.startswith("#" * 4 + " "):
        return BlockType.HEADING4
    if block.startswith("#" * 5 + " "):
        return BlockType.HEADING5
    if block.startswith("#" * 6 + " "):
        return BlockType.HEADING6
    if block.startswith("> "):
        return BlockType.QUOTE
    if block.startswith("- "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE_BLOCK
    return BlockType.PARAGRAPH
