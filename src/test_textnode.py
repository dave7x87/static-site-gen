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
    
    def test_no_url(self):
        with self.assertRaisesRegex(ValueError, "No URL provided"):
            node = TextNode(DEFAULT_TEXT, TextType.LINK)

    def test_no_img_source(self):
        with self.assertRaisesRegex(ValueError, "No image source provided"):
            node = TextNode(DEFAULT_TEXT, TextType.IMAGE)
    
    def test_empty_img_source(self):
        with self.assertRaisesRegex(ValueError, "No image source provided"):
            node = TextNode(DEFAULT_TEXT, TextType.IMAGE, "")
    

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
        expected = "TextNode('This is a text node', 'text', 'https://www.boot.dev')"
        self.assertEqual(expected,repr(node))

class test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode(
            "This is a link node",
            TextType.LINK,
            "www.google.com"
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
        node = TextNode(
            "This is an image node",
            TextType.IMAGE,
            "www.google.com/logo.jpg"
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
        with self.assertRaisesRegex(ValueError, "Unknown TextType"):
            text_node_to_html_node(node)

    def test_empty_val(self):
        node = text_node_to_html_node(TextNode(
            text="",
            text_type=TextType.TEXT
            ))
        node_html = node.to_html()
        expected = ""
        self.assertEqual(node_html, expected)

    def test_empty_url(self):
        node = TextNode(DEFAULT_TEXT, TextType.LINK, "")
        expected = '<a href="">This is a text node</a>'
        self.assertEqual(text_node_to_html_node(node).to_html(), expected)

    def test_img_alt(self):
        node = text_node_to_html_node(TextNode("", TextType.IMAGE, "logo.jpg"))
        node.VOID_TAG_HANDLING = True
        expected = '<img src="logo.jpg" alt="">'
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()