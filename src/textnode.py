from enum import Enum

class TextType(Enum):
    PLAIN="plain text"
    BOLD="bold text"
    ITALIC="italicised text"
    INLINE_CODE="inline code"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(self, TextNode) and isinstance(other, TextNode):
            return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
        raise TypeError("Error: one or two passed parameters are not of type `TextNode`.")

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
