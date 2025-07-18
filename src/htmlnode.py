
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        html_attr = self.props_to_html()
        if self.tag is None:
            return f"{self.value}"
        inline_html = f"<{self.tag} {html_attr}>{self.value}</{self.tag}>" if html_attr != "" else f"<{self.tag}>{self.value}</{self.tag}>"
        return inline_html

    def props_to_html(self):
        html_attr = []
        if self.props is None or self.props == {}:
            return ""
        for (attribute, value) in self.props.items():
            html_attr.append(f"{attribute}=\"{value}\"")
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


