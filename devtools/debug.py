from src.htmlnode import HTMLNode

class DebugError(Exception):
    def get_default_message(self) -> str:
        return "A debugging error has occurred"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.get_default_message())

def gen_tree(node: HTMLNode, level: int = 0) -> str:
    '''generates a tree structure principally for debugging purposes'''
    if not isinstance(node, HTMLNode):
        raise DebugError(message = "\n".join((
            "Invalid node provided.",
            "Expected node type = HTMLNode.",
            f"Provided node type = {type(node).__name__}"
        )))
    
    indent = "  " * level
    
    lines = [] #hold the lines we're producing
    display_tag = node.tag if node.tag else "[No tag]"
    
    # We use props_to_html() to get the string of attributes
    props_str = node.props_to_html()
    
    # We show the tag and its attributes on the first line
    lines.append(f"{indent}<{display_tag}{props_str}>")
    
    # If there's a value, show it indented even further
    if node.value:
        lines.append(f"{indent}  Value: {node.value!r}")
        
    # Recursively read children
    if node.children:
        for child in node.children:
            lines.append(gen_tree(child, level + 1))
            
    # Show the closing tag for clarity
    lines.append(f"{indent}</{display_tag}>")

    # Join and return
    return "\n".join(lines)

