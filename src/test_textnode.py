import unittest

from textnode import TextNode, TextType, text_node_to_html_node

DEFAULT_TEXT = "This is a text node"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode(DEFAULT_TEXT, TextType.BOLD)
        node2 = TextNode(DEFAULT_TEXT, TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode(DEFAULT_TEXT, TextType.LINK, "https://www.boot.dev")
        node2 = TextNode(DEFAULT_TEXT, TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_empty_url_not_eq(self):
        node = TextNode(DEFAULT_TEXT, TextType.LINK)
        node2 = TextNode(DEFAULT_TEXT, TextType.LINK, "")
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode(DEFAULT_TEXT, TextType.PLAIN)
        node2 = TextNode("This text node is different", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_text_case(self):
        node = TextNode(DEFAULT_TEXT, TextType.CODE)
        node2 = TextNode(DEFAULT_TEXT.lower(), TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode(DEFAULT_TEXT, TextType.ITALIC)
        node2 = TextNode(DEFAULT_TEXT, TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")
        expected = "TextNode(This is a text node, text, https://www.boot.dev)"
        self.assertEqual(expected,repr(node))

class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()