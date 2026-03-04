from enum import Enum
from dataclasses import dataclass
from typing import Optional
from htmlnode import LeafNode

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
    url: Optional[str] = None

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
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
            return LeafNode(tag="img",
                            value="",
                            props={
                                "src": text_node.url,
                                "alt": text_node.text,
                                }
                                )
        case _:
            raise ValueError("Unknown TextType")
