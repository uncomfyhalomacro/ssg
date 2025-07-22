import unittest

from textnode import TextNode, TextType
from textnode import ALL_TEXTYPES_LIST


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
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {})

    def test_img_node_to_html_with_alt_text_and_src(self):
        node = TextNode(
            "Beautiful image", TextType.IMAGE, "https://example.com/beautiful.png"
        )
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
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
        self.assertEqual(html_node.value, None)
        # NOTE: Order affects the order of the attributes. Remember LIFO I guess.
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/beautiful.png", "alt": "Beautiful image"},
        )
        self.assertEqual(
            html_node.to_html(),
            '<img alt="Beautiful image" src="https://example.com/beautiful.png">',
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

    def test_md_to_nodes_plain_no_value_passed(self):
        node = TextNode("Hello, World!")
        with self.assertRaises(Exception) as err:
            new_nodes = node.md_to_nodes()
            self.assertEqual(
                str(err.exception),
                "Error: no delimiter passed. You can pass the following: **, `, _.",
            )

    def test_md_to_nodes_with_every_text_type_but_every_return_is_one_plain_node(self):
        node = TextNode("Hello, World!")
        for delimiter in ALL_TEXTYPES_LIST:
            self.assertEqual([node], node.md_to_nodes(delimiter))

    def test_md_to_new_nodes_nested(self):  # TODO: NOT IMPLEMENTED YET
        node = TextNode("This is **_text_** with a `code block` word", TextType.PLAIN)
        with self.assertRaises(Exception):
            new_nodes = node.md_to_nodes()

    def test_extracted_markdown_links(self):
        node = TextNode(
            "This is a [Google Form](https://forms.google.com). This is a [Google Sheet](https://sheets.google.com)"
        )
        matches = node.extract_markdown_links()
        assert_matches = [
            ("Google Form", "https://forms.google.com"),
            ("Google Sheet", "https://sheets.google.com"),
        ]
        self.assertEqual(matches, assert_matches)

    def test_extracted_markdown_links_but_not_image(self):
        node = TextNode(
            "This is an [image](https://example.com/image.svg) and [another image](https://image.com/image.svg)."
        )
        matches = node.extract_markdown_links()
        assert_matches = [
            ("image", "https://example.com/image.svg"),
            ("another image", "https://image.com/image.svg"),
        ]
        self.assertEqual(matches, assert_matches)
        matches = node.extract_markdown_images()
        self.assertNotEqual(assert_matches, matches)
        self.assertEqual([], matches)

    def test_extracted_markdown_images(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.svg) and ![another image](https://image.com/image.svg)."
        )
        matches = node.extract_markdown_links()
        assert_matches = [
            ("image", "https://example.com/image.svg"),
            ("another image", "https://image.com/image.svg"),
        ]
        self.assertNotEqual(matches, assert_matches)
        self.assertEqual([], matches)
        matches = node.extract_markdown_images()
        self.assertEqual(assert_matches, matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = node.md_to_nodes(TextType.IMAGE)
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_but_no_image_to_capture(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = node.md_to_nodes(TextType.IMAGE)
        self.assertNotEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        self.assertEqual([node], new_nodes)

    def test_get_all_nodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        test_node = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.INLINE_CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(node.text_to_textnodes(), test_node)

    def test_get_all_nodes_v2(self):
        node = TextNode(
            "This is _italic text_ with an **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        test_node = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.INLINE_CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(node.text_to_textnodes(), test_node)


if __name__ == "__main__":
    unittest.main()
