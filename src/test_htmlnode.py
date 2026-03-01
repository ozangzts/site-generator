from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest

from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(tag="div", value=None, children=None, props={"class": "container"})
        node2 = HTMLNode(tag="div", value=None, children=None, props={"class": "container"})
        node3 = HTMLNode(tag="p", value=None, children=None)
        node4 = HTMLNode(tag="p")

        self.assertEqual(repr(node1), repr(node2))
        self.assertNotEqual(repr(node1), repr(node3))
        self.assertNotEqual(repr(node2), repr(node3))
        self.assertEqual(repr(node3), repr(node4))


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://example.com">Click here</a>')


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

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode(None, "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span>child2<span>child3</span></div>",
        )

    


