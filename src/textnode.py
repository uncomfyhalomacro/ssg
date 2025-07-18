from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode

class TextType(Enum):
    PLAIN=0
    BOLD=1
    ITALIC=2
    INLINE_CODE=3
    LINK=4
    IMAGE=5

class TextNode:
    def __init__(self, text, text_type=TextType.PLAIN, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self):
        url = { "href": f"{self.url}" } if (self.url is not None) else None
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


    def __eq__(self, other):
        if isinstance(self, TextNode) and isinstance(other, TextNode):
            return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
        raise TypeError("Error: one or two passed parameters are not of type `TextNode`.")

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
