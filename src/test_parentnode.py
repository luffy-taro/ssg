import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_node_creation(self):
        parent_node = ParentNode(tag="div", children=[
            LeafNode(tag="h1", value="Hello, world!"),
            LeafNode(tag="p", value="This is a paragraph."),
        ])
        self.assertEqual(parent_node.to_html(), "<div><h1>Hello, world!</h1><p>This is a paragraph.</p></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )