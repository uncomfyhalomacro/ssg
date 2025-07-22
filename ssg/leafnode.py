from ssg.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Error: value cannot be None.")
        super().__init__(tag, value, [], props)

    def to_html(self):
        html_attr = self.props_to_html()
        if self.tag is None:
            return f"{self.value}"
        inline_html = (
            f"<{self.tag} {html_attr}>{self.value}</{self.tag}>"
            if html_attr != ""
            else f"<{self.tag}>{self.value}</{self.tag}>"
        )
        return inline_html
