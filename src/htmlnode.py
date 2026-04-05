from __future__ import annotations
from typing import Iterator
#from abc import ABC, abstractmethod
from html import escape
import src.errors as errors

class HTMLNode:#(ABC):  #ABC achieves nothing until abstractmethod activated
    __slots__ = ("tag", "value", "children", "props")
    
    # All additional behaviour currently defaults to off
    # to ensure compatibility with external tests 
    
    # Set HTML Escape Behaviour
    # (i.e. convert characters which may cause HTML issues)
    USE_HTML_ESCAPE = False

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
    
    def to_html(self) -> str:    
        return "".join(self.iter_html())
    
    #@abstractmethod #currently disallowed by spec
    def iter_html(self) -> Iterator[str]:
        raise NotImplementedError("iter_html method not implemented")
    
    def _iter_props_to_html(self) -> Iterator[str]:
        '''Yields html property fragments. May yield zero fragments if no props assigned'''

        if self.props:
            yield from (f' {k}="{self._escape_text(v)}"'for k, v in self.props.items())

    def _open_tag(self) -> Iterator[str]:
        yield f"<{self.tag}"
        yield from self._iter_props_to_html()
        yield ">"

    def _escape_text(self, text: str) -> str:
        '''checks compatibility flag and handles escaping text'''
        return escape(text) if self.USE_HTML_ESCAPE else text
    
    def _close_tag(self) -> str:
        return f"</{self.tag}>"

    def props_to_html(self) -> str:
        return "".join(self._iter_props_to_html()) if self.props else ""
    
    @staticmethod #factory support
    def _check_props(protected: set[str], props_to_check: dict[str, str]) -> None:
        '''Checks for issues and conflicting props keys in factory methods'''
        
        normalised_protected = {prop.lower() for prop in protected}
        
        if not isinstance(props_to_check, dict):
            raise errors.HTMLNodePropError(message = "Props not passed within dict")        
        
        for prop in props_to_check:
            if prop.lower() in normalised_protected:
                raise errors.HTMLNodePropConflict(prop = prop)
            if not isinstance(props_to_check[prop], str):
                raise errors.HTMLNodePropTypeError(prop = prop)
            
    @staticmethod
    def _is_missing(attribute : str | None) -> bool:
        '''Returns true if provided attribute is missing or an empty string'''
        return (attribute is None or attribute == "")


class VoidNode(HTMLNode):
    __slots__ = ()

    # Additional behaviour toggle
    # Disabled by default for external testing
    VOID_TAG_HANDLING = False

    def __init__(self,
                 tag: str,
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag = tag, props = props)
        self._validate()

    def __repr__(self) -> str:
        '''override HTMLNode _repr_ to exclude children/value'''
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"props={self.props!r})"
        )
        return output
    
    def _validate(self) -> None:
        '''screens for empty/none inputs
        Used at initialisation time and also at use time
        to meet spec and guard against outside mutation'''
        if self._is_missing(self.tag):
            raise errors.HTMLNodeMissingAttributeError(attribute="tag")
        
    def iter_html(self) -> Iterator[str]:
        self._validate()
        yield from self._open_tag()

    ## VoidNode Compatibility helper method
    @classmethod
    def _compat_from_void(
        cls,
        tag: str,
        props: dict[str, str] | None = None
    ) -> VoidNode | LeafNode :
        if not cls.VOID_TAG_HANDLING:
            return LeafNode.from_void(tag = tag, props = props)
        return cls(tag = tag, props = props)
     
    ## VoidNode Factory Methods
    @classmethod
    def image(cls,
              source: str,
              alt_text: str | None = None,
              other_props: dict[str, str] | None = None
              ) -> VoidNode:

        if cls._is_missing(source):
            raise errors.HTMLNodeMissingAttributeError(attribute = "image source")
        
        props = {"src": source}
        if alt_text is not None:
            props["alt"] = alt_text
        
        if other_props:
            protected = {"src", "alt"}
            cls._check_props(protected = protected, props_to_check = other_props)
            props.update(other_props)

        return cls._compat_from_void(tag="img", props=props)
    
    @classmethod
    def hr(cls):
        return cls._compat_from_void(tag="hr")

    @classmethod
    def br(cls):
        return cls._compat_from_void(tag="br")


class LeafNode(HTMLNode):
    __slots__ = ()

    def __init__(self,
                 tag: str | None,
                 value: str,
                 props: dict[str, str] | None = None
                 ) -> None:
        super().__init__(tag = tag,
                         value = value,
                         props = props
                         )
        self._validate()

    def __repr__(self) -> str:
        '''override HTMLNode _repr_ to exclude children'''
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag!r}, "
                  f"value={self.value!r}, "
                  f"props={self.props!r})"
        )
        return output

    def _validate(self) -> None:
        '''screens for empty/none inputs
        Used at initialisation time and also at use time
        to meet spec and guard against outside mutation'''
        if self.value is None:
            raise errors.HTMLNodeMissingAttributeError(attribute="value")
    
    def iter_html(self) -> Iterator[str]:
        self._validate()
        
        if self._is_missing(self.tag):
            yield self._escape_text(self.value)
        else:
            yield from self._open_tag()
            yield self._escape_text(self.value)
            yield self._close_tag()
    
    @classmethod
    def from_void(
        cls,
        tag: str, props: dict[str, str] | None = None
        ) -> LeafNode:
        '''Compatibility Helper'''
        return cls(
            tag = tag,
            value = "",
            props = props
        )
    
    ## LeafNode Factory Methods

    @classmethod
    def text(cls, text: str) -> LeafNode:
        return cls(tag=None, value=text)
    
    @classmethod
    def bold(cls, text: str) -> LeafNode:
        return cls(tag="b", value=text)
    
    @classmethod
    def italic(cls, text: str) -> LeafNode:
        return cls(tag="i", value=text)
    
    @classmethod
    def code(cls, text: str) -> LeafNode:
        return cls(tag="code", value=text)
    
    @classmethod
    def link(cls,
              url: str,
              text: str,
              other_props: dict[str, str] | None = None
              ) -> LeafNode:

        if cls._is_missing(url):
            raise errors.HTMLNodeMissingAttributeError(attribute = "link URL")
        
        if cls._is_missing(text):
            raise errors.HTMLNodeMissingAttributeError(attribute = "link text")
        
        props = {"href": url}
        
        if other_props:
            protected = {"href"}
            cls._check_props(protected = protected, props_to_check = other_props)
            props.update(other_props)

        return cls(tag="a", value=text, props=props)

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

        if self._is_missing(self.tag):
            raise errors.HTMLNodeMissingAttributeError(attribute="tag")
        if not isinstance(self.children, list) or len(self.children) == 0:
            raise errors.HTMLNodeChildrenListError()
        bad_children = [child for child in self.children if not isinstance(child, HTMLNode)]
        if bad_children:
            raise errors.HTMLNodeChildrenTypeError(children = bad_children)
        
    def iter_html(self) -> Iterator[str]:
        
        self._validate()
        yield from self._open_tag()
        for child in self.children:
            yield from child.iter_html()
        yield self._close_tag()

