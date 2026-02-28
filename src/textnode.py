from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TextType(Enum):
    plain = "plain"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: Optional[str] = None

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    