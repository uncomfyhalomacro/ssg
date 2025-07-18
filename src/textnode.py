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

    def __eq__(self, t1, t2):
        if isinstance(t1, TextNode) and isinstance(t2, TextNode):
            return (t1.text == t2.text) and (t1.text_type == t2.text_type) and (t1.url == t2.url)
        raise TypeError("Error: one or two passed parameters are not of type `TextNode`.")

