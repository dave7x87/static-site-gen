from enum import Enum
from textnode import TextNode, TextType

class MD_type(Enum):
    h1 = "#"
    h2 = "##"
    h3 = "###"
    h4 = "####"
    h5 = "#####"
    h6 = "######"
    CODE = "`"
    BOLD = "**"
    ITALIC = "*"
    BLOCKQUOTE = ">"
    H_RULE = "---"
    LINK = "[link]"
    IMAGE = "!"

def split_nodes_delimiter(old_nodes: list[TextNode],
                          delimiter: str | MD_type,
                          text_type: TextType
                          ):
    if not isinstance(old_nodes, list):
        raise ValueError("Nodes should be given as a list")
    # If it's our Enum, get the string value (e.g., "**")
    actual_delimiter = (delimiter.value if isinstance(delimiter, MD_type)
                        else delimiter
    )
    
    new_nodes: list[TextNode] = []
    node_types = [TextType.TEXT, text_type]

    for node in old_nodes:
        ## move to using match/case instead of if/else. logic is clearer
        ## will need to reverse order (i.e. handle plain text first)
        if (node.text_type != TextType.TEXT
            and node.text_type != TextType.PLAIN
            ):
            new_nodes.append(node)
        else:
            split_strings = node.text.split(actual_delimiter)
            if len(split_strings) % 2 == 0:
                raise ValueError("Closing delimiter not found")
            new_nodes.extend(
                TextNode(text = t,
                         text_type = node_types[i % 2]
                         )
                         for i, t in enumerate(split_strings)
                         if t != ""
            )

    return new_nodes