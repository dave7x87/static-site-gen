from __future__ import annotations

class HTMLNode:
    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None,
                 children: list[HTMLNode] | None = None,
                 props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return f" {' '.join(f'{k}="{v}"' for k,v in self.props.items())}"
    
    def __repr__(self):
        output = (f"{type(self).__name__}"
                  f"(tag={self.tag}, "
                  f"value={self.value}, "
                  f"children={self.children}, "
                  f"props={self.props})"
        )
        return output