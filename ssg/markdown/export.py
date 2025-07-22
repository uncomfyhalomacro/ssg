from ssg.markdown.blocks import markdown_to_blocks
from ssg.markdown.blocktypes import BlockType, block_to_block_type
from ssg.textnode import TextNode, TextType
from ssg.parentnode import ParentNode
from ssg.htmlnode import VoidNode
import re

ALL_HEADING_TYPES = [
    BlockType.HEADING1,
    BlockType.HEADING2,
    BlockType.HEADING3,
    BlockType.HEADING4,
    BlockType.HEADING5,
    BlockType.HEADING6,
]


def markdown_to_html_node(markdown):
    parent_tag = "div"
    blocks_and_block_types = markdown_to_block_and_block_types(markdown)
    nodes = []
    for block, block_type in blocks_and_block_types:
        if block_type in ALL_HEADING_TYPES:
            grandchild_node = block_heading_to_html_node(block, block_type)
            nodes.append(grandchild_node)
        elif block_type == BlockType.PARAGRAPH:
            grandchild_node = block_paragraph_to_html_node(block)
            nodes.append(grandchild_node)
        elif block_type == BlockType.QUOTE:
            grandchild_node = block_quote_to_html_node(block)
            nodes.append(grandchild_node)
        elif block_type == BlockType.UNORDERED_LIST:
            grandchild_node = block_unordered_list_to_html_node(block)
            nodes.append(grandchild_node)
        elif block_type == BlockType.ORDERED_LIST:
            grandchild_node = block_ordered_list_to_html_node(block)
            nodes.append(grandchild_node)
        elif block_type == BlockType.CODE_BLOCK:
            grandchild_node = block_codeblock_to_html_node(block)
            nodes.append(grandchild_node)
    return ParentNode(parent_tag, nodes, None)


def markdown_to_block_and_block_types(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_and_block_types = [(block, block_to_block_type(block)) for block in blocks]
    return blocks_and_block_types


def block_paragraph_to_html_node(block):
    parent_tag = "p"
    block = block.replace("\n", " ")
    tn = TextNode(block)
    tn_nodes = tn.text_to_textnodes()
    children = [tn_node.to_html_node() for tn_node in tn_nodes]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def block_heading_to_html_node(block, heading_type):
    parent_tag = ""
    if heading_type == BlockType.HEADING1:
        parent_tag = "h1"
        block = block.removeprefix("# ")
    elif heading_type == BlockType.HEADING2:
        parent_tag = "h2"
        block = block.removeprefix("## ")
    elif heading_type == BlockType.HEADING3:
        parent_tag = "h3"
        block = block.removeprefix("### ")
    elif heading_type == BlockType.HEADING4:
        parent_tag = "h4"
        block = block.removeprefix("#### ")
    elif heading_type == BlockType.HEADING5:
        parent_tag = "h5"
        block = block.removeprefix("##### ")
    elif heading_type == BlockType.HEADING6:
        parent_tag = "h6"
        block = block.removeprefix("###### ")
    else:
        raise TypeError(
            f"Error: passing a block with a type not in one of the heading types. Passed type is `{heading_type}`"
        )
    tn = TextNode(block)
    tn_nodes = tn.text_to_textnodes()
    children = [tn_node.to_html_node() for tn_node in tn_nodes]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def block_quote_to_html_node(block):
    parent_tag = "blockquote"
    children = []
    splits = block.split("\n")
    removed_prefixes = [sp.removeprefix(">").lstrip() for sp in splits]
    for line in removed_prefixes:
        if line.strip() == "":
            children.append(VoidNode("br"))
        else:
            tn = TextNode(line)
            tn_nodes = tn.text_to_textnodes()
            children += [tn_node.to_html_node() for tn_node in tn_nodes]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def block_unordered_list_to_html_node(block):
    parent_tag = "ul"
    normalise_block = normalise_ul_list(block)
    splits = normalise_block.split("\n")
    children = [inline_item_to_html_nodes(split) for split in splits]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def block_ordered_list_to_html_node(block):
    parent_tag = "ol"
    normalise_block = normalise_ol_list(block)
    splits = normalise_block.split("\n")
    children = [inline_item_to_html_nodes(split) for split in splits]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def inline_item_to_html_nodes(item):
    parent_tag = "li"
    tn = TextNode(item)
    tn_nodes = tn.text_to_textnodes()
    children = [tn_node.to_html_node() for tn_node in tn_nodes]
    parent_node = ParentNode(parent_tag, children, None)
    return parent_node


def normalise_ul_list(ul_list_block):
    splits = ul_list_block.split("\n")
    block = ""
    for sp in splits:
        if sp.startswith("- "):
            block += sp.removeprefix("- ")
            block += "\n"
        else:
            if block.endswith("\n"):
                block = block.rstrip("\n")
                block += " " + sp
                block += "\n"

    return block.strip()


def normalise_ol_list(ol_list_block):
    splits = ol_list_block.split("\n")
    block = ""
    for sp in splits:
        if re.match(r"\d+\. ", sp):
            block += sp.removeprefix(re.match(r"\d+\. ", sp)[0])
            block += "\n"
        else:
            if block.endswith("\n"):
                block = block.rstrip("\n")
                block += " " + sp
                block += "\n"

    return block.strip()


def block_codeblock_to_html_node(block):
    parent_tag = "pre"
    subparent_tag = "code"
    get_lang = get_code_block_lang(block)
    class_attr = ("language-" + get_lang) if get_lang.strip() != "" else ""
    splits = block.split("\n")
    if len(splits) == 1:
        block = block.strip("```")
        # NOTE: This will be just a single code block without <pre>
        node = TextNode(block, TextType.INLINE_CODE)
        html_node = node.to_html_node()
        if class_attr.strip != "":
            html_node.props = {"class": class_attr}
        return html_node
    else:
        rejoins = "\n".join(splits[1:]).rstrip("```")
        node = TextNode(rejoins, TextType.PLAIN)
        subparent_node = ParentNode(
            subparent_tag,
            [node.to_html_node()],
            {"class": class_attr} if class_attr.strip() != "" else None,
        )
        parent_node = ParentNode(parent_tag, [subparent_node], None)
        return parent_node


def get_code_block_lang(block):
    splits = block.split("\n")
    first_line = splits[0]
    first_line = first_line.strip("```")
    first_line = first_line.strip()
    return first_line
