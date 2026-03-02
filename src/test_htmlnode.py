import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_blank_tag(self):
        self.assertEqual(None, HTMLNode().tag)
        
    def test_blank_value(self):
        self.assertEqual(None, HTMLNode().value)
    
    def test_no_children(self):
        self.assertEqual(None, HTMLNode().children)

    def test_repr(self):
        expected = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(expected, repr(HTMLNode()))

    def test_props_to_html(self):
        test = HTMLNode(props={"href":"www.google.com", "target":"_blank"})
        expected = ' href="www.google.com" target="_blank"'
        
        self.assertEqual(test.props_to_html(), expected)

    def test_props_to_html_default(self):
        # Testing the default (unescaped) behavior for the autograder
        node = HTMLNode(
            tag="div",
            props={
                "href": "https://www.google.com?q=fish&chips",
                "title": 'The "Great" Gatsby',
            },
        )
        # Should NOT escape the & or the "
        expected = ' href="https://www.google.com?q=fish&chips" title="The "Great" Gatsby"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_escaped(self):
        # Testing safeguard
        node = HTMLNode(
            tag="div",
            props={
                "href": "https://www.google.com?q=fish&chips",
                "title": 'The "Great" Gatsby',
            },
        )
        # Should escape & to &amp; and " to &quot;
        expected = (' href="https://www.google.com?q=fish&amp;chips" '
                    'title="The &quot;Great&quot; Gatsby"'
        )
        self.assertEqual(node.props_to_html(use_escape=True), expected)

    def test_props_to_html_no_props(self):
        # Testing the edge case of None or empty props
        node_none = HTMLNode(tag="div", props=None)
        node_empty = HTMLNode(tag="div", props={})
        
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr(self):
        # Verifying  !r formatting in __repr__
        node = HTMLNode(tag="p", value="Hello", props={"class": "greeting"})
        # Strings are wrapped in quotes because of the !r flag
        expected = "HTMLNode(tag='p', value='Hello', children=None, props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()

