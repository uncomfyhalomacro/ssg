from src.markdown.export import markdown_to_block_and_block_types
from src.markdown.blocktypes import BlockType
import os

cwd = os.path.realpath(os.getcwd())
content_root_path = os.path.realpath(os.path.join(cwd, "content"))
template_html_path = os.path.realpath(os.path.join(cwd, "template.html"))

def extract_title(markdown):
    blocks_and_block_types = markdown_to_block_and_block_types(markdown)
    if blocks_and_block_types == []:
        raise Exception("Error: file contains no content")
    title, block_type = blocks_and_block_types[0]
    if block_type == BlockType.HEADING1:
        return title.removeprefix("# ")
    raise Exception(f"Error: no title found for page. Block type is {block_type}")

