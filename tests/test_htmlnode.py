import unittest
import types

from src.htmlnode import HTMLNode, VoidNode, LeafNode, ParentNode
import src.errors as errors

class _HTMLTestNode(HTMLNode):
    '''minimal concrete subclass for testing shared HTMLNode behavior'''
    def iter_html(self, use_escape = None):
        '''includes a stub render implementation so tests remain
        compatible if the render hook becomes abstract'''
        super().iter_html(use_escape = use_escape)

INITIAL_ESC_DEFAULT = HTMLNode.USE_HTML_ESCAPE
INITIAL_VOID_DEFAULT = VoidNode.VOID_TAG_HANDLING

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

    def test_props_generator(self):
        node = _HTMLTestNode(
            tag="a",
            value="click me",
            props={"href": "http://boot.dev",
                   "target": "_blank"
                   }
        )
        result = node._iter_props_to_html()
        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(next(result), ' href="http://boot.dev"')
        self.assertEqual(next(result), ' target="_blank"')
        with self.assertRaises(StopIteration):
            next(result)

    def test_open_tag(self):
        node = _HTMLTestNode(
            tag="a",
            value="click me",
            props={"href": "http://boot.dev",
                   "target": "_blank"
                   }
        )
        result = node._open_tag()
        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual("".join(result), '<a href="http://boot.dev" target="_blank">')

    def test_close_tag(self):
        node = _HTMLTestNode(
            tag="a",
            value="click me",
            props={"href": "http://boot.dev",
                   "target": "_blank"
                   }
        )
        self.assertEqual(node._close_tag(),"</a>")

class TestVoidNode(unittest.TestCase):
    def setUp(self):
        VoidNode.VOID_TAG_HANDLING = True

    def tearDown(self):
        VoidNode.VOID_TAG_HANDLING = INITIAL_VOID_DEFAULT
    
    def test_repr(self):
        '''confirm that children and value are not included in VoidNode __repr__'''

        # Verifying  !r formatting in __repr__
        node = VoidNode.image(source="logo.png", alt_text="")

        # Strings are wrapped in quotes because of the !r flag
        expected = "VoidNode(tag='img', props={'src': 'logo.png', 'alt': ''})"
        self.assertEqual(repr(node), expected)

    def test_no_tag(self):
        with self.assertRaises(errors.HTMLNodeMissingAttributeError):
            VoidNode(tag=None)

    def test_empty_tag(self):
        with self.assertRaises(errors.HTMLNodeMissingAttributeError):
            VoidNode(tag="")

    def test_image_tag(self):
        node = VoidNode.image(source="logo.png", alt_text="")
        expected = '<img src="logo.png" alt="">'

        self.assertEqual(node.to_html(), expected)

    def test_image_no_source(self):
        with self.assertRaises(errors.HTMLNodeMissingAttributeError):
            VoidNode.image(source=None)

    def test_image_empty_source(self):
        with self.assertRaises(errors.HTMLNodeMissingAttributeError):
            VoidNode.image(source="")

    def test_image_no_alt(self):
        node = VoidNode.image(source="logo.png")
        expected = '<img src="logo.png">'

        self.assertEqual(node.to_html(), expected)

    def test_image_props(self):
        node = VoidNode.image(source="logo.png", other_props={"width": "200"})
        expected = {'src': 'logo.png', 'width': "200"}

        self.assertEqual(node.props, expected)

    def test_image_extra_src(self):
        with self.assertRaises(errors.HTMLNodePropConflict):
             VoidNode.image(source="logo.png", other_props={"SRC": "image.png"})

    def test_image_extra_alt(self):
        with self.assertRaises(errors.HTMLNodePropConflict):
             VoidNode.image(source="logo.png", other_props={"Alt": "alt text"})

    def test_image_bad_prop_type(self):
        with self.assertRaises(errors.HTMLNodePropTypeError):
            VoidNode.image(source="logo.png", other_props={"width": 200})

    def test_image_bad_prop_dict(self):
        with self.assertRaises(errors.HTMLNodePropError):
            VoidNode.image(source="logo.png", other_props='"width": 200')

    def test_hr_tag(self):
        node = VoidNode.hr()
        expected = '<hr>'

        self.assertEqual(node.to_html(), expected)

    def test_br_tag(self):
        node = VoidNode.br()
        expected = '<br>'

        self.assertEqual(node.to_html(), expected)

class TestVoidNodeCompatibility(unittest.TestCase):
    def setUp(self):
        VoidNode.VOID_TAG_HANDLING = False

    def tearDown(self):
        VoidNode.VOID_TAG_HANDLING = INITIAL_VOID_DEFAULT
    
    def test_image_tag(self):
        node = VoidNode.image(source="logo.png", alt_text="")
        expected = '<img src="logo.png" alt=""></img>'

        self.assertEqual(node.to_html(), expected)

    def test_image_no_alt(self):
        node = VoidNode.image(source="logo.png")
        expected = '<img src="logo.png"></img>'

        self.assertEqual(node.to_html(), expected)

    def test_hr_tag(self):
        node = VoidNode.hr()
        expected = '<hr></hr>'

        self.assertEqual(node.to_html(), expected)

    def test_br_tag(self):
        node = VoidNode.br()
        expected = '<br></br>'

        self.assertEqual(node.to_html(), expected)

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
        with self.assertRaises(errors.HTMLNodeMissingAttributeError):
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
            ParentNode(None,[child])

    def test_empty_tag(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have tag"
            ):
            child = LeafNode("b", "text")
            ParentNode("",[child])

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
            ParentNode("b", [])

    def test_unlisted_children(self):
        with self.assertRaisesRegex(
            ValueError,
            "ParentNode must have list of children"
            ):
            ParentNode("b", LeafNode(tag="", value=""))

class TestNodesSafeMode(unittest.TestCase):
    def setUp(self):
        # Force "test mode" before every test
        HTMLNode.USE_HTML_ESCAPE = False
        LeafNode.VOID_TAG_HANDLING = False

    def tearDown(self):
        HTMLNode.USE_HTML_ESCAPE = INITIAL_ESC_DEFAULT
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
        HTMLNode.USE_HTML_ESCAPE = True
        LeafNode.VOID_TAG_HANDLING = True

    def tearDown(self):
        HTMLNode.USE_HTML_ESCAPE = INITIAL_ESC_DEFAULT
        LeafNode.VOID_TAG_HANDLING = INITIAL_VOID_DEFAULT

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

