from leafnode import LeafNode

class ParentNode:
    def __init__(self, tag=None, children=None, props=None):
        self.tag = tag
        if self.tag is None:
            raise ValueError("Error: `tag` value cannot be None.")
        self.children = children
        if self.children is None:
            raise ValueError("Error: parent node has no children. Infertility moment.")
        self.props = props

    def to_html(self):
        html_attr = self.props_to_html()
        rendered_children = ""
        for child in self.children:
            if isinstance(child, LeafNode) or isinstance(child, ParentNode):
                rendered_children += child.to_html()
            else:
                raise TypeError("Error: a child in children is not type `LeafNode`.")
        inline_html = f"<{self.tag} {html_attr}>{rendered_children}</{self.tag}>" if html_attr != "" else f"<{self.tag}>{rendered_children}</{self.tag}>"
        return inline_html

    def props_to_html(self):
        html_attr = []
        if self.props is None or self.props == {}:
            return ""
        for (attribute, value) in self.props.items():
            html_attr.append(f"{attribute}=\"{value}\"")
        return " ".join(html_attr)


