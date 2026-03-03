from __future__ import annotations
from html import escape

class HTMLNode:
    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict[str, str] | None = None
                 ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self, use_escape: bool = False):
        '''if use_escape is True, will convert properties to ensure HTML safety.
        (Optional, Default = False)
        Defaults to false to account for unit tests where results are expected to not be escaped'''
        if not self.props:
            return ""
        
        return f" {' '.join(f'{k}="{escape(v) if use_escape else v}"'
                            for k,v in self.props.items())}"
    
    def __repr__(self):
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"value={self.value!r}, "
                  f"children={self.children!r}, "
                  f"props={self.props!r})"
        )
        return output
    
    def gen_tree(self, level=0):
        '''generates a tree structure principally for debugging purposes'''
        indent = "  " * level
        
        lines = [] #hold the lines we're producing
        
        
        # We use props_to_html() to get the string of attributes
        props_str = self.props_to_html()
        
        # We show the tag and its attributes on the first line
        lines.append(f"{indent}<{self.tag}{props_str}>")
        
        # If there's a value, show it indented even further
        if self.value:
            lines.append(f"{indent}  Value: {self.value!r}")
            
        # Recursively read children
        if self.children:
            for child in self.children:
                lines.append(child.gen_tree(level + 1))
                
        # Show the closing tag for clarity
        lines.append(f"{indent}</{self.tag}>")

        # Join and return
        return "\n".join(lines)
    
class LeafNode(HTMLNode):

    def __init__(self,
                 tag: str | None,
                 value: str,
                 props: dict[str, str] | None = None
                 ):
        super().__init__(tag = tag,
                         value = value,
                         props = props
                         )

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf Node MUST have a value")
        
        if self.tag is None:
            return self.value
        
        else:
            return (f"<{self.tag}"
                    f"{self.props_to_html()}>"
                    f"{self.value}"
                    f"</{self.tag}>"
            )

    def __repr__(self):
        '''override HTMLNode _repr_ to exclude children'''
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"value={self.value!r}, "
                  f"props={self.props!r})"
        )
        return output

class ParentNode(HTMLNode):
    def __init__(self,
                 tag : str,
                 children: list[HTMLNode],
                 props: dict[str, str] | None = None
                 ):
        super().__init__(tag=tag,
                         children=children,
                         props=props
                         )
        self._validate()
        
    def _validate(self):
        '''screens for empty/none inputs
        Used at initialisation time and also at use time
        to meet spec and guard against outside mutation'''

        if not self.tag:
            raise ValueError("ParentNode must have tag")
        if not isinstance(self.children, list) or len(self.children) == 0:
            raise ValueError("ParentNode must have list of children")
        
    def to_html(self):
        self._validate()
        
        components = []

        # We use props_to_html() to get the string of attributes
        props_str = self.props_to_html()
        components.append(f"<{self.tag}{props_str}>")

        for child in self.children:
            components.append(child.to_html())

        components.append(f"</{self.tag}>")

        return "".join(components)
