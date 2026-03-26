import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node
import src.errors as errors

DEFAULT_TEXT = "This is a text node"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode.bold(DEFAULT_TEXT)
        node2 = TextNode(DEFAULT_TEXT, TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode.link(DEFAULT_TEXT,"https://www.boot.dev")
        node2 = TextNode(DEFAULT_TEXT, TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_no_url(self):
        with self.assertRaises(errors.TextNodeNoURL):
            node = TextNode(DEFAULT_TEXT, TextType.URL)

    def test_no_img_source(self):
        with self.assertRaises(errors.TextNodeNoURL):
            node = TextNode(DEFAULT_TEXT, TextType.IMAGE)
    
    def test_empty_img_source(self):
        with self.assertRaises(errors.TextNodeNoURL):
            node = TextNode.image(DEFAULT_TEXT, "")
    
    def test_text_not_eq(self):
        node = TextNode.plain(DEFAULT_TEXT)
        node2 = TextNode.plain("This text node is different")
        self.assertNotEqual(node, node2)

    def test_text_case(self):
        node = TextNode.code(DEFAULT_TEXT)
        node2 = TextNode.code(DEFAULT_TEXT.lower())
        self.assertNotEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode.italic(DEFAULT_TEXT)
        node2 = TextNode.plain(DEFAULT_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")
        expected = "TextNode('This is a text node', 'text', 'https://www.boot.dev')"
        self.assertEqual(expected,repr(node))

class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode.plain("This is a text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_plain(self):
        node = TextNode.plain("This is a text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode.bold("This is a bold text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode.italic("This is an italic text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode.code("This is a code node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode.link(
            text="This is a link node",
            url="www.google.com"
            )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_url(self):
        node = TextNode(
            "This is a link node",
            TextType.URL,
            "www.google.com"
            )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_img(self):
        node = TextNode.image(
            text="This is an image node",
            url="www.google.com/logo.jpg"
            )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "www.google.com/logo.jpg",
                "alt": "This is an image node"
                }
                )
        
    def test_invalid_type(self):
        node = TextNode("This is not a text node", "not_a_type")
        with self.assertRaises(errors.TextNodeTypeError):
            text_node_to_html_node(node)

    def test_empty_val(self):
        node = text_node_to_html_node(TextNode.plain(text="",))
        node_html = node.to_html()
        expected = ""
        self.assertEqual(node_html, expected)

    def test_empty_url(self):
        node = TextNode.link(DEFAULT_TEXT, "")
        expected = '<a href="">This is a text node</a>'
        self.assertEqual(text_node_to_html_node(node).to_html(), expected)

    def test_img_alt(self):
        node = text_node_to_html_node(TextNode.image(text="", url="logo.jpg"))
        node.VOID_TAG_HANDLING = True
        expected = '<img src="logo.jpg" alt="">'
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()