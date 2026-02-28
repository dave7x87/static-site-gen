import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_blank_tag(self):
        self.assertEqual(None, HTMLNode().tag)
        
    def test_blank_value(self):
        self.assertEqual(None, HTMLNode().value)
    
    def test_no_children(self):
        self.assertEqual(None, HTMLNode().children)

    def test_no_props(self):
        self.assertEqual(None, HTMLNode().props)

    def test_repr(self):
        expected = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(expected, repr(HTMLNode()))

    def test_props_to_html(self):
        test = HTMLNode(props={"href":"www.google.com", "target":"_blank"})
        expected = ' href="www.google.com" target="_blank"'
        
        self.assertEqual(test.props_to_html(), expected)

