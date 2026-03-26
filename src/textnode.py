from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from src.htmlnode import LeafNode
import src.errors as errors

class TextType(Enum):
    TEXT = "text"
    PLAIN = "text" #maintained from older builds for compat. equivalent to TEXT
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    URL = "url"     #added as compatibility option
    IMAGE = "image"

@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None
    
    def __post_init__(self) -> None:
        match self:
            # Match any node where text_type is LINK/URL and url is None
            case TextNode(text_type=(TextType.LINK | TextType.URL), url=None):
                raise errors.TextNodeNoURL(text_type=self.text_type)
                
            # Match any node where text_type is IMAGE and url is empty/None
            case TextNode(text_type=TextType.IMAGE, url=None | ""):
                raise errors.TextNodeNoURL(text_type=self.text_type)
    
    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"
    
    @classmethod
    def plain(cls, text: str) -> TextNode:
        return cls(text, TextType.TEXT)

    @classmethod
    def bold(cls, text: str) -> TextNode:
        return cls(text, TextType.BOLD)
    
    @classmethod
    def italic(cls, text: str) -> TextNode:
        return cls(text, TextType.ITALIC)
    
    @classmethod
    def code(cls, text: str) -> TextNode:
        return cls(text, TextType.CODE)
    
    @classmethod
    def link(cls, text:str, url: str) -> TextNode:
        return cls(text, TextType.LINK, url)    
    
    @classmethod
    def image(cls, text:str, url: str) -> TextNode:
        return cls(text, TextType.IMAGE, url)    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT | TextType.PLAIN:
            return LeafNode(tag=None,
                            value=text_node.text
                            )
        case TextType.BOLD:
            return LeafNode(tag="b",
                            value=text_node.text
                            )
        case TextType.ITALIC:
            return LeafNode(tag="i",
                            value=text_node.text
                            )
        case TextType.CODE:
            return LeafNode(tag="code",
                            value=text_node.text
                            )
        case TextType.LINK | TextType.URL:
            return LeafNode(tag="a",
                            value=text_node.text,
                            props={"href": text_node.url}
                            )
        case TextType.IMAGE:
            return  LeafNode(tag="img",
                            value="",
                            props={
                                "src": text_node.url,
                                "alt": text_node.text,
                                }
                                )
        case unknown_type:
            raise errors.TextNodeTypeError(text_type=unknown_type)
