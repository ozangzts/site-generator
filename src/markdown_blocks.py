from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    block_nodes = []

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        block_nodes.append(block_to_html_node(block, block_type))

    return ParentNode("div", block_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def block_to_html_node(block, block_type):
    if block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_type == BlockType.ULIST:
        return unordered_list_block_to_html_node(block)
    if block_type == BlockType.OLIST:
        return ordered_list_block_to_html_node(block)
    return paragraph_block_to_html_node(block)


def heading_block_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_block_to_html_node(block):
    if block.startswith("```\n"):
        code_text = block[4:-3]
    else:
        lines = block.split("\n")
        code_text = "\n".join(lines[1:-1])
    code_child = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [code_child])])


def quote_block_to_html_node(block):
    quote_lines = []
    for line in block.split("\n"):
        line = line[1:]
        if line.startswith(" "):
            line = line[1:]
        quote_lines.append(line)
    quote_text = " ".join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_text))


def unordered_list_block_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line[2:]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)


def ordered_list_block_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line[line.find(". ") + 2 :]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)


def paragraph_block_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))
        