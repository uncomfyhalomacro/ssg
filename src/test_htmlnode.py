import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_hello_world_with_example_dot_org(self):
        node1 = LeafNode("a", "Hello, World!", {"href": "https://example.com"})
        string_repr = """<a href="https://example.com">Hello, World!</a>"""
        self.assertEqual(node1.to_html(), string_repr)

    def test_hello_world_without_attr(self):
        node1 = LeafNode("p", "Hello, World!")
        string_repr = "<p>Hello, World!</p>"
        self.assertEqual(node1.to_html(), string_repr)

    def test_leaf_hello_world_with_example_dot_org_with_link_tag(self):
        leafnode1 = LeafNode("a", "Hello, World!", {"href": "https://example.com"})
        string_repr = """<a href="https://example.com">Hello, World!</a>"""
        self.assertEqual(leafnode1.to_html(), string_repr)

    def test_leaf_hello_world_with_example_dot_org_without_a_tag_is_raw_text(self):
        leafnode1 = LeafNode(None, "Hello, World!", {"href": "https://example.com"})
        self.assertEqual(leafnode1.to_html(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
