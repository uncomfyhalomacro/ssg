from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode


class TextType(Enum):
    PLAIN = None
    BOLD = "**"
    ITALIC = "_"
    INLINE_CODE = "`"
    LINK = 4  # TODO: We will turn this into a regex
    IMAGE = 5  # TODO: Same as this one


ALL_TEXTYPES_LIST = [
    TextType.BOLD,
    TextType.ITALIC,
    TextType.INLINE_CODE,
]  # NOTE: For now only these three


class TextNode:
    def __init__(self, text, text_type=TextType.PLAIN, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self):
        url = {"href": f"{self.url}"} if (self.url is not None) else None
        if self.text_type == TextType.PLAIN:
            return LeafNode(None, self.text, None)
        if self.text_type == TextType.BOLD:
            return LeafNode("b", self.text, None)
        if self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text, None)
        if self.text_type == TextType.INLINE_CODE:
            return LeafNode("code", self.text, None)
        if self.text_type == TextType.LINK:
            return LeafNode("a", self.text, url)
        if self.text_type == TextType.IMAGE:
            props = dict()
            if self.text.strip() != "":
                props["alt"] = self.text
            if self.url is not None:
                props["src"] = self.url
            return LeafNode("img", "", props)

    def md_to_nodes(self, delimiter=TextType.PLAIN):
        if self.text_type != TextType.PLAIN:
            return [self]
        if isinstance(delimiter, str):
            find = list(filter(lambda x: x.value == delimiter, ALL_TEXTYPES_LIST))
            if len(find) == 1:
                delimiter = find[0]
            else:
                raise ValueError("Error: not a valid delimiter")

        if delimiter == TextType.PLAIN:
            raise Exception(
                "Error: no delimiter passed. You can pass the following: **, `, _."
            )

        new_nodes = []
        current = self.text
        if not any([d.value in self.text for d in ALL_TEXTYPES_LIST]):
            new_node = TextNode(self.text)
            new_nodes.append(new_node)
            return new_nodes
        split_list = current.split(delimiter.value)
        if len(split_list) > 1 and len(split_list) % 2 == 1:
            median = len(split_list) // 2
            for i in range(0, len(split_list)):
                if i == median:
                    new_node = TextNode(split_list[i], delimiter)
                    if new_node not in new_nodes:
                        new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_list[i])
                    if new_node not in new_nodes:
                        new_nodes.append(new_node)
        else:  # This means, the split did not find any pair.
            raise Exception(
                f"Error: not valid markdown. There should be another pair of `{delimiter}`"
            )
        return new_nodes

    def __eq__(self, other):
        if isinstance(self, TextNode) and isinstance(other, TextNode):
            return (
                (self.text == other.text)
                and (self.text_type == other.text_type)
                and (self.url == other.url)
            )
        raise TypeError(
            "Error: one or two passed parameters are not of type `TextNode`."
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
