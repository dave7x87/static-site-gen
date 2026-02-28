
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class HTMLNode:
    tag: Optional[str] = None
    value: Optional[str] = None
    children: Optional[list[HTMLNode]] = None
    props: Optional[dict[str, str]] = None

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return " " + " ".join(f'{k}="{v}"' for k,v in self.props.items())
