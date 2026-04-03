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
        self.text_type = text_type
        if message is None:
            message = self.get_default_message()
            if text_type:
                message = f"{message}: (type:{self.text_type})"
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
        self.attribute = attribute
        if message is None:
            message = self.get_default_message()
            if attribute:
                message = f"{message}: (attribute:{self.attribute})"
        super().__init__(message)
    
    
class HTMLNodeMissingAttributeError(HTMLNodeAttributeError):
    def get_default_message(self) -> str:
        return "Missing required attribute for this node type"
    
class HTMLNodePropError(HTMLNodeError):
    def get_default_message(self) -> str:
        return "Issue with prop provided"
    
    def __init__(self,
                message: str | None = None,
                prop: str | None = None,
                ) -> None:
        self.prop = prop
        if message is None:
            message = self.get_default_message()
            if prop:
                message = f"{message}: (prop:{self.prop})"
        super().__init__(message)

class HTMLNodePropConflict(HTMLNodePropError):
    def get_default_message(self) -> str:
        return "Protected prop passed as other prop"

class HTMLNodePropTypeError(HTMLNodePropError):
    def get_default_message(self) -> str:
        return "Prop provided is wrong type"

class HTMLNodeChildrenError(HTMLNodeError):
    def get_default_message(self) -> str:
        return "Error with HTMLNode children"
    
    def __init__(self,
                message: str | None = None,
                children: list[str] | str | None = None,
                ) -> None:
        self.children = children
        if message is None:
            message = self.get_default_message()
            if children:
                message = f"{message}: (children:{self.children})"
        super().__init__(message)

class HTMLNodeChildrenTypeError(HTMLNodeChildrenError):
    def get_default_message(self) -> str:
        return "Provided children are not HTMLNodes"
    
class HTMLNodeChildrenListError(HTMLNodeChildrenError):
    def get_default_message(self) -> str:
        return "Must supply children in a list"  
