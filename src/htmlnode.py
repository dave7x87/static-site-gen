from __future__ import annotations
from typing import Iterator
#from abc import ABC, abstractmethod
from html import escape

class HTMLNode:#(ABC):  #ABC achieves nothing until abstractmethod activated
    __slots__ = ("tag", "value", "children", "props")
    
    # All additional behaviour currently defaults to off
    # to ensure compatibility with external tests 
    
    # Set Default HTML Escape Behaviour if not specified.
    # (i.e. convert characters which may cause HTML issues)
    DEFAULT_ESCAPE_BEHAVIOUR = False

    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict[str, str] | None = None
                 ) -> None:
        self.tag = tag.lower() if tag else None
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self) -> str:
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"value={self.value!r}, "
                  f"children={self.children!r}, "
                  f"props={self.props!r})"
        )
        return output
    
    def to_html(self,
                use_escape: bool | None = None
                ):    
        '''use_escape is used by sub-classes
        for HTML escaping (optional)'''
        raise NotImplementedError("to_html method not implemented")
    
    #@abstractmethod #currently disallowed by spec
    def iter_html(self):
        raise NotImplementedError("iter_html method not implemented")
    
    def _iter_props_to_html(self, use_escape: bool | None = None) -> Iterator[str]:
        '''Yields html property fragments.
        May yield zero fragments if no props assigned
        use_escape (optional) defines if html escaping is enabled'''
        if use_escape is None:
            use_escape = self.DEFAULT_ESCAPE_BEHAVIOUR

        if self.props:
            yield from (f' {k}="{escape(v) if use_escape else v}"'
                    for k,v in self.props.items()
            )

    def _open_tag(self, use_escape: bool | None = None) -> Iterator[str]:
        '''use_escape defines optional html escape behaviour'''
        yield f"<{self.tag}"
        yield from self._iter_props_to_html(use_escape = use_escape)
        yield ">"


    def _close_tag(self) -> str:
        return f"</{self.tag}>"

    def props_to_html(self, use_escape: bool | None = None) -> str:
        '''use_escape defines optional html escape behaviour'''
        return "".join(self._iter_props_to_html(use_escape = use_escape))
    
class LeafNode(HTMLNode):
    __slots__ = ()
    # Additional behaviour toggle
    # Disabled by default for external testing

    VOID_TAG_HANDLING = False
    void_tags = {"img", "br", "hr"}

    def __init__(self,
                 tag: str | None,
                 value: str,
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag = tag,
                         value = value,
                         props = props
                         )

    def __repr__(self) -> str:
        '''override HTMLNode _repr_ to exclude children'''
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"value={self.value!r}, "
                  f"props={self.props!r})"
        )
        return output
    
    def to_html(self, use_escape: bool | None = None):
        if use_escape is None:
            use_escape = self.DEFAULT_ESCAPE_BEHAVIOUR
        
        if self.value is None:
            raise ValueError("Leaf Node MUST have a value")
        
        if self.tag is None:
            return self.value
        
        else:
            parts = [f"<{self.tag}",
                    f"{self.props_to_html(use_escape)}>",
                    f"{escape(self.value) if use_escape else self.value}",
                    ]
            if (not self.VOID_TAG_HANDLING
                or self.tag not in self.void_tags
            ):
                parts.append(f"</{self.tag}>")
            return "".join(parts)



class ParentNode(HTMLNode):
    __slots__ = ()
    def __init__(self,
                 tag : str,
                 children: list[HTMLNode],
                 props: dict[str, str] | None = None
                 ) -> None:
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
        
    def to_html(self, use_escape: bool | None = None):
        self._validate()
        
        if use_escape is None:
            use_escape = self.DEFAULT_ESCAPE_BEHAVIOUR
                
        components = []

        # We use props_to_html() to get the string of attributes
        props_str = self.props_to_html(use_escape)
        components.append(f"<{self.tag}{props_str}>")

        for child in self.children:
            components.append(child.to_html(use_escape))

        components.append(f"</{self.tag}>")

        return "".join(components)
