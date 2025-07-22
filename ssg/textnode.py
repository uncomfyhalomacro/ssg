import re
from enum import Enum

from ssg.leafnode import LeafNode
from ssg.htmlnode import VoidNode


class TextType(Enum):
    PLAIN = None
    BOLD = "**"  # r"\*\*(.+?)\*\*"
    ITALIC = "_"  # r"_(.+?)_"
    INLINE_CODE = "`"  # r"`(.+?)`"
    IMAGE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    LINK = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def get_regex_for_pairs(text_type):
    if text_type not in [TextType.BOLD, TextType.ITALIC, TextType.INLINE_CODE]:
        raise ValueError(
            f"Error: passing a value not part of the pairs. Value: `text_type`"
        )
    if text_type == TextType.BOLD:
        return r"\*\*(.+?)\*\*"
    if text_type == TextType.ITALIC:
        return r"_(.+?)_"
    if text_type == TextType.INLINE_CODE:
        return r"`(.+?)`"
    raise Exception("Error: Something went wrong in here.")


ALL_TEXTYPES_LIST = [
    TextType.BOLD,
    TextType.ITALIC,
    TextType.INLINE_CODE,
    TextType.LINK,
    TextType.IMAGE,
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
            return VoidNode("img", props)

    def extract_markdown_links(self):
        return re.findall(TextType.LINK.value, self.text)

    def extract_markdown_images(self):
        return re.findall(TextType.IMAGE.value, self.text)

    def md_to_nodes(
        self, delimiter=None
    ):  # TODO: Create util functions to process self.extract_markdown_images and self.extract_markdown_links.
        if isinstance(delimiter, str):
            find = list(filter(lambda x: x.value == delimiter, ALL_TEXTYPES_LIST))
            if len(find) == 1:
                delimiter = find[0]
            else:
                raise ValueError("Error: not a valid delimiter")

        new_nodes = []
        current = self.text
        if delimiter in [TextType.LINK, TextType.IMAGE]:
            # Links and images share similar logic anyway.
            all_link_tuples = (
                self.extract_markdown_images()
                if delimiter == TextType.IMAGE
                else self.extract_markdown_links()
            )
            if all_link_tuples == []:  # Just return self inside a list
                new_nodes.append(self)
                return new_nodes
            rejoined_link_as_strings = [
                f"[{x}]({y})" if delimiter == TextType.LINK else f"![{x}]({y})"
                for (x, y) in all_link_tuples
            ]
            initial = 0
            for idx in range(0, len(rejoined_link_as_strings)):
                found_index = current.index(rejoined_link_as_strings[idx])
                plain_text = current[initial:found_index]
                plain_new_node = TextNode(plain_text)
                linked_new_node = TextNode(
                    all_link_tuples[idx][0], delimiter, all_link_tuples[idx][1]
                )
                new_nodes.append(plain_new_node)
                new_nodes.append(linked_new_node)
                initial = found_index + len(rejoined_link_as_strings[idx])

            last_text = current[initial:]
            if last_text != "":
                plain_new_node = TextNode(last_text)
                new_nodes.append(plain_new_node)
        elif delimiter in [TextType.BOLD, TextType.ITALIC, TextType.INLINE_CODE]:
            regex = get_regex_for_pairs(delimiter)
            rejoined_paired_strings = [
                f"{delimiter.value}{f}{delimiter.value}"
                for f in re.findall(regex, current)
            ]
            initial = 0
            for idx in range(0, len(rejoined_paired_strings)):
                found_index = current.index(rejoined_paired_strings[idx])
                plain_text = current[initial:found_index]
                plain_new_node = TextNode(plain_text)
                special_paired_node = TextNode(
                    rejoined_paired_strings[idx].strip(delimiter.value), delimiter, None
                )
                new_nodes.append(plain_new_node)
                new_nodes.append(special_paired_node)
                initial = found_index + len(rejoined_paired_strings[idx])

            last_text = current[initial:]
            if last_text != "":
                plain_new_node = TextNode(last_text)
                new_nodes.append(plain_new_node)
        if delimiter is None:
            raise Exception(
                "Error: no delimiter passed. You can pass the following: **, `, _."
            )

        return new_nodes

    def text_to_textnodes(self):
        new_nodes = []
        all_indices_tuple = []
        for delimiter in ALL_TEXTYPES_LIST[:3]:
            if delimiter.value in self.text:
                all_indices_tuple.append((self.text.index(delimiter.value), delimiter))
        for delimiter in ALL_TEXTYPES_LIST[3:]:
            for a_match in re.finditer(delimiter.value, self.text):
                all_indices_tuple.append((a_match.start(), delimiter))
        all_indices_tuple = sorted(all_indices_tuple, key=lambda item: item[0])
        for idx, text_type in all_indices_tuple:
            nodes = self.md_to_nodes(text_type)
            while nodes:
                node = nodes.pop(0)
                if any(
                    [node.text.count(d.value) > 1 for d in ALL_TEXTYPES_LIST[:3]]
                ) or any(
                    [
                        len(re.findall(d.value, node.text)) > 0
                        for d in ALL_TEXTYPES_LIST[3:]
                    ]
                ):
                    temp_nodes = node.text_to_textnodes()
                    for tnode in temp_nodes:
                        if tnode not in new_nodes:
                            new_nodes.append(tnode)
                elif all(
                    [node.text.count(d.value) <= 1 for d in ALL_TEXTYPES_LIST[:3]]
                ) and all(
                    [
                        len(re.findall(d.value, node.text)) == 0
                        for d in ALL_TEXTYPES_LIST[3:]
                    ]
                ):
                    if node not in new_nodes:
                        new_nodes.append(node)
        if new_nodes == []:
            return [self]
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
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'
