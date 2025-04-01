import unittest

from htmlnode import HTMLNode
from parser import markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="my_paragraph")
        node2 = HTMLNode(tag="p", value="my_paragraph")
        self.assertEqual(node, node2)

    def test_inline_node_has_no_children(self):
        node = HTMLNode(tag="span", value="some text")
        self.assertFalse(node.children)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="p",
            value="This is paragraph",
            props={
                "class": "bold color-red",
            },
        )
        expected = 'class="bold color-red"'
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
