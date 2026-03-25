import unittest

from markdown import split_nodes_delimiter, MDtype
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        src_node = TextNode.plain("This is text with a `code block` word")

        split_nodes= split_nodes_delimiter(
            old_nodes=[src_node],
            delimiter=MDtype.CODE, 
            text_type=TextType.CODE
        )
        expected = [
            TextNode.plain("This is text with a "),
            TextNode.code("code block"),
            TextNode.plain(" word"),
            ]
        self.assertEqual(split_nodes, expected)

    def test_end_tags(self):
        node_list = [
            TextNode.plain("This is text with a `code block`"),
            TextNode.plain("`This text is code` and then text at the end"),
            TextNode.plain("`This is all code``But in two blocks`"),
        ]

        split_nodes = split_nodes_delimiter(
            old_nodes=node_list,
            delimiter=MDtype.CODE, 
            text_type=TextType.CODE
        )
        expected = [
            TextNode.plain("This is text with a "),
            TextNode.code("code block"),
            TextNode.code("This text is code"),
            TextNode.plain(" and then text at the end"),
            TextNode.code("This is all code"),
            TextNode.code("But in two blocks"),
            ]
        self.assertEqual(split_nodes, expected)

    def test_no_split(self):
        node = [TextNode.plain("nothing to split here!")]
        after_split_attempt = split_nodes_delimiter(node, MDtype.BOLD, TextType.BOLD)

        self.assertEqual(node, after_split_attempt)

    def test_empty_list(self):
        result = split_nodes_delimiter([], MDtype.ITALIC, TextType.ITALIC)
        self.assertEqual([], result)

    def test_not_list(self):
        with self.assertRaisesRegex(ValueError, "Nodes should be given as a list"):
            node = TextNode.plain("This should be rejected")
            split_nodes_delimiter(node, MDtype.CODE, TextType.CODE)
            


