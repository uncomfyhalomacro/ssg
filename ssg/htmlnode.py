from enum import Enum


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "Error: function is not implemented for this type. Are you using its child classes `LeafNode` and `ParentNode`?"
        )

    def props_to_html(self):
        html_attr = []
        if self.props is None or self.props == {}:
            return ""
        for attribute, value in self.props.items():
            html_attr.append(f'{attribute}="{value}"')
        return " ".join(html_attr).strip()

    def __repr__(self):
        return f"""
HTMLNode(
    tag: {self.tag}
    value: {self.value}
    children: {self.children}
    props: {self.props}
)
"""


class VoidTag(Enum):
    BREAKLINE = "br"
    HORIZONTAL_LINE = "hr"
    IMAGE = "img"
    # TODO: Add more if necessary. For now, these two seems "important". Open a PR if you are interested to add more.
    # NOTE: See also <https://developer.mozilla.org/en-US/docs/Glossary/Void_element>.


class VoidNode(HTMLNode):
    def __init__(self, tag=None, props=None):
        if tag is None:
            raise ValueError(
                "Error: Please provide a void element such as 'br' or 'hr'."
            )

        if isinstance(tag, VoidTag):
            tag = tag.value
        elif isinstance(tag, str):
            if tag not in [vtag.value for vtag in VoidTag]:
                raise NotImplementedError(
                    f"Error: tag `{tag}` is not yet implemented as a void tag."
                )

        super().__init__(tag=tag, props=props)

    def to_html(self):
        html_attr = self.props_to_html()
        inline_html = (
            f"<{self.tag} {html_attr}>" if html_attr != "" else f"<{self.tag}>"
        )
        return inline_html
