import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class _HTMLTestNode(HTMLNode):
    '''minimal concrete subclass for testing shared HTMLNode behavior'''
    def html_generator(self):
        '''includes a stub render implementation so tests remain
        compatible if the render hook becomes abstract'''
        super().html_generator()

INITIAL_ESC_DEFAULT = HTMLNode.DEFAULT_ESCAPE_BEHAVIOUR
INITIAL_VOID_DEFAULT = LeafNode.VOID_TAG_HANDLING

class TestHTMLNode(unittest.TestCase):
    
    #def test_base_node_instantiation(self):
    #    with self.assertRaises(TypeError) as cm:
    #        HTMLNode()
    #    self.assertIn("abstract class", str(cm.exception))
    
    def test_blank_tag(self):
        self.assertEqual(None, _HTMLTestNode().tag)
        
    def test_blank_value(self):
        self.assertEqual(None, _HTMLTestNode().value)
    
    def test_no_children(self):
        self.assertEqual(None, _HTMLTestNode().children)

    def test_empty_repr(self):
        expected = "_HTMLTestNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(expected, repr(_HTMLTestNode()))

    def test_props_to_html(self):
        test = _HTMLTestNode(props={"href":"www.google.com", "target":"_blank"})
        expected = ' href="www.google.com" target="_blank"'
        
        self.assertEqual(test.props_to_html(), expected)

    def test_props_to_html_default(self):
        # Testing the default (unescaped) behavior for the autograder
        node = _HTMLTestNode(
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
        node = _HTMLTestNode(
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
        node_none = _HTMLTestNode(tag="div", props=None)
        node_empty = _HTMLTestNode(tag="div", props={})
        
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr(self):
        # Verifying  !r formatting in __repr__
        node = _HTMLTestNode(tag="p", value="Hello", props={"class": "greeting"})
        # Strings are wrapped in quotes because of the !r flag
        expected = "_HTMLTestNode(tag='p', value='Hello', children=None, props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_imp(self):
        with self.assertRaises(NotImplementedError):
            _HTMLTestNode("p").to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_repr(self):
        '''confirm that children are not included in LeafNode __repr__'''
        # Verifying  !r formatting in __repr__
        node = LeafNode(tag="p", value="Hello", props={"class": "greeting"})
        # Strings are wrapped in quotes because of the !r flag
        expected = "LeafNode(tag='p', value='Hello', props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected)
    
    def test_no_tag(self):
        raw_text = "This is raw text"
        node = LeafNode(tag=None, value=raw_text)
        self.assertEqual(node.to_html(), raw_text)

    def test_link(self):
        '''tests link generation AND multiple props at same time'''
        link_text = "Link Text"
        url = "www.google.com"
        frame = "_blank"
        
        node = LeafNode(tag="a",
                        value=link_text,
                        props={"href": url,
                               "target": frame})
        expected = (f'<a href="{url}" target="{frame}">'
                    f'{link_text}</a>'
                    )
        
        self.assertEqual(expected, node.to_html())

    def test_empty_val(self):
        node = LeafNode("p","")
        expected = "<p></p>"

        self.assertEqual(node.to_html(),expected)

    def test_no_val(self):
        with self.assertRaisesRegex(ValueError,
                                    "Leaf Node MUST have a value"):
            LeafNode("p", None).to_html()

    def test_leaf_repr_correct_from_parent(self):
        child1 = LeafNode(tag="p", value="Child_text")
        child2 = _HTMLTestNode()
        children = [child1, child2]
        parent = _HTMLTestNode(tag="a", children=children)

        expected = ("_HTMLTestNode(tag='a', value=None, "
                    "children=[LeafNode(tag='p', "
                    "value='Child_text', props=None), "
                    "_HTMLTestNode(tag=None, value=None, "
                    "children=None, props=None)], props=None)"
        )
        self.assertEqual(repr(parent), expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                     "<div><span>child</span></div>"
                     )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_repr_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        expected = ("ParentNode(tag='div', value=None, "
                    "children=[ParentNode(tag='span', "
                    "value=None, children=[LeafNode(tag='b', "
                    "value='grandchild', props=None)], "
                    "props=None)], props=None)"
        )
        self.assertEqual(repr(parent_node), expected)

    def test_no_tag(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have tag"
            ):
            child = LeafNode("b", "text")
            node = ParentNode(None,[child])

    def test_empty_tag(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have tag"
            ):
            child = LeafNode("b", "text")
            node = ParentNode("",[child])

    def test_no_children(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have list of children"
            ):
            node = ParentNode("b", None)

    def test_empty_children(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have list of children"
            ):
            node = ParentNode("b", [])

    def test_unlisted_children(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have list of children"
            ):
            node = ParentNode("b", LeafNode(None, None))

class TestNodesSafeMode(unittest.TestCase):
    def setUp(self):
        # Force "test mode" before every test
        HTMLNode.DEFAULT_ESCAPE_BEHAVIOUR = False
        LeafNode.VOID_TAG_HANDLING = False

    def tearDown(self):
        HTMLNode.DEFAULT_ESCAPE_BEHAVIOUR = INITIAL_ESC_DEFAULT
        LeafNode.VOID_TAG_HANDLING = INITIAL_VOID_DEFAULT

    def test_no_escape(self):
        child_node = LeafNode(
            tag="a",
            value = "What's 'taters' precious?",
            props={
                "href": "https://www.google.com?q=fish&chips",
                "title": 'The "Great" Gatsby',
            },
        )
        node = ParentNode(
            tag="p",
            children = [child_node]
        )
        # Should NOT escape the & or the "
        expected = '<p><a href="https://www.google.com?q=fish&chips" title="The "Great" Gatsby">What\'s \'taters\' precious?</a></p>'
        self.assertEqual(node.to_html(), expected)

    def test_no_void(self):
        node = LeafNode(
            tag="img",
            value="",
            props={
                "src": "https://www.google.com/google.jpg",
                "alt": "Google Logo"
            }
        )
        expected = '<img src="https://www.google.com/google.jpg" alt="Google Logo"></img>'
        self.assertEqual(node.to_html(), expected)

class TestNodesSafeModeOff(unittest.TestCase):
    def setUp(self):
        HTMLNode.DEFAULT_ESCAPE_BEHAVIOUR = True
        LeafNode.VOID_TAG_HANDLING = True

    def tearDown(self):
        HTMLNode.DEFAULT_ESCAPE_BEHAVIOUR = INITIAL_ESC_DEFAULT
        LeafNode.VOID_TAG_HANDLING = INITIAL_VOID_DEFAULT

    def test_escape(self):
        child_node = LeafNode(
            tag="a",
            value = "What's 'taters' precious?",
            props={
                "href": "https://www.google.com?q=fish&chips",
                "title": 'The "Great" Gatsby',
            },
        )
        node = ParentNode(
            tag="p",
            children = [child_node]
        )
        # Should escape the & and the "
        expected = '<p><a href="https://www.google.com?q=fish&amp;chips" title="The &quot;Great&quot; Gatsby">What&#x27;s &#x27;taters&#x27; precious?</a></p>'
        self.assertEqual(node.to_html(), expected)

    def test_void(self):
        node = LeafNode(
            tag="img",
            value="",
            props={
                "src": "https://www.google.com/google.jpg",
                "alt": "Google Logo"
            }
        )
        expected = '<img src="https://www.google.com/google.jpg" alt="Google Logo">'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()

