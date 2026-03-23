import unittest

from debug import gen_tree, DebugError
from htmlnode import LeafNode, ParentNode
from textnode import TextNode

class TestGenTree(unittest.TestCase):
    def test_invalid_node(self):
        with self.assertRaises(DebugError):
            gen_tree(TextNode.plain("Plain node"))
    
    def test_not_a_node(self):
        with self.assertRaises(DebugError):
            gen_tree("just a string")

    def test_leaf_node(self):
        self.assertNotEqual(
            None,
            gen_tree(
                LeafNode(
                    "a",
                    "link",
                    {"href":"http://www.google.com"}
                )
            )
        )

    def test_parent_node(self):
        self.assertNotEqual(
            None,
            gen_tree(
                ParentNode(
                    "parent",
                    [LeafNode(
                        "img",
                        "",
                        {"src":"logo.png"}
                )]
                )
            )
        )

