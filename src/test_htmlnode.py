import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_hello_world_with_example_dot_org(self):
        node1 = HTMLNode("a", "Hello, World!", None, {"href": "https://example.com"})
        string_repr = """<a href="https://example.com">Hello, World!</a>"""
        self.assertEqual(node1.node_to_html(), string_repr)

if __name__ == "__main__":
    unittest.main()



