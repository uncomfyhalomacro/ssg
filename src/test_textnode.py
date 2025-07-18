import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_boldtext_node_to_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_boldtext_node_to_html_with_rendered_inline_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italictext_node_to_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italictext_node_to_html_with_rendered_inline_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_inlinecode_node_to_html(self):
        node = TextNode("This is a text node", TextType.INLINE_CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_inlinecode_node_to_html_with_rendered_inline_html(self):
        node = TextNode("This is a text node", TextType.INLINE_CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link_node_to_html(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_node_to_html_with_rendered_inline_html(self):
        node = TextNode("This is a text node", TextType.LINK)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<a>This is a text node</a>")

    def test_link_node_to_html_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_link_node_to_html_with_rendered_inline_html_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(
            html_node.to_html(), '<a href="https://example.com">This is a text node</a>'
        )

    def test_img_node_to_html_without_anything(self):
        node = TextNode("", TextType.IMAGE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {})

    def test_img_node_to_html_with_alt_text_and_src(self):
        node = TextNode(
            "Beautiful image", TextType.IMAGE, "https://example.com/beautiful.png"
        )
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/beautiful.png", "alt": "Beautiful image"},
        )

    def test_img_node_to_html_with_alt_text_and_src_with_rendered_inline_html(self):
        node = TextNode(
            "Beautiful image", TextType.IMAGE, "https://example.com/beautiful.png"
        )
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        # NOTE: Order affects the order of the attributes. Remember LIFO I guess.
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/beautiful.png", "alt": "Beautiful image"},
        )
        self.assertEqual(
            html_node.to_html(),
            """<img alt="Beautiful image" src="https://example.com/beautiful.png"></img>""",
        )

    def test_plaintext_node_to_html(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_plaintext_node_to_html_with_rendered_inline_html(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_md_to_new_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = node.md_to_nodes(TextType.INLINE_CODE)
        cmp_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.INLINE_CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(cmp_nodes, new_nodes)

    def test_md_to_new_nodes_italic_text(self):
        node = TextNode("This is text with a _italic text_ word", TextType.PLAIN)
        new_nodes = node.md_to_nodes("_")
        cmp_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(cmp_nodes, new_nodes)

    def test_md_to_new_nodes_italic_bold_code(self):
        node = TextNode(
            "This is `code` and this is an _italic_. This is very **bold** as well."
        )
        new_nodes = node.md_to_nodes("**")
        cmp_nodes = [
            TextNode(
                "This is `code` and this is an _italic_. This is very ",
                TextType.PLAIN,
                None,
            ),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" as well.", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, cmp_nodes)

    def test_md_to_new_nodes_uneven(self):
        node = TextNode("This is **text with a `code block` word", TextType.PLAIN)
        with self.assertRaises(Exception):
            node.md_to_nodes("**")

    def test_md_to_nodes_plain_no_value_passed(self):
        node = TextNode("Hello, World!")
        with self.assertRaises(Exception) as err:
            new_nodes = node.md_to_nodes()
        self.assertEqual(
            str(err.exception),
            "Error: no delimiter passed. You can pass the following: **, `, _.",
        )

    def test_md_to_new_nodes_nested(self):  # TODO: NOT IMPLEMENTED YET
        node = TextNode("This is **_text_** with a `code block` word", TextType.PLAIN)
        with self.assertRaises(Exception):
            new_nodes = node.md_to_nodes()


if __name__ == "__main__":
    unittest.main()
