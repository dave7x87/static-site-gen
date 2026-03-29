from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from textnode import TextType

### Primary error class

class SSGError(Exception):
    def get_default_message(self) -> str:
        return "An internal SSG error has occurred"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.get_default_message())

### TextNode Errors

class TextNodeError(SSGError):
    def get_default_message(self) -> str:
        return "Error with TextNode"

class TextNodeTypeError(TextNodeError):
    def get_default_message(self) -> str:
        return "Error with provided text type"
    
    def __init__(self,
                message: str | None = None,
                text_type: str | TextType | None = None,
                ) -> None:
        if message is None:
            message = self.get_default_message()
            if text_type:
                message = f"{message}: (type:{text_type})"
        super().__init__(message)

class TextNodeNoURL(TextNodeTypeError):
    def get_default_message(self) -> str:
        return "URL required for this node type"
    
### HTML Node Errors

class HTMLNodeError(SSGError):
    def get_default_message(self) -> str:
        return "Error with HTMLNode"
    
class HTMLNodeAttributeError(HTMLNodeError):
    def get_default_message(self) -> str:
        return "Error with HTMLNode attribute"
    
    def __init__(self,
                message: str | None = None,
                attribute: str | None = None,
                ) -> None:
        if message is None:
            message = self.get_default_message()
            if attribute:
                message = f"{message}: (attribute:{attribute})"
        super().__init__(message)
    
    
class HTMLNodeMissingAttributeError(HTMLNodeAttributeError):
    def get_default_message(self) -> str:
        return "Missing required attribute for this node type"
    

