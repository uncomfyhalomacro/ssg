from ssg.markdown.export import markdown_to_block_and_block_types, markdown_to_html_node
from ssg.markdown.blocktypes import BlockType
import os

cwd = os.path.realpath(os.getcwd())
public_path = os.path.realpath(os.path.join(cwd, "public"))
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


def markdown_file_to_html(md):
    return markdown_to_html_node(md).to_html()


def transform_markdown_to_html_with_template(markdown_file, basepath=None):
    if not os.path.exists(markdown_file):
        raise FileExistsError(
            f"Error: unable to look for file at path `{markdown_file}`"
        )
    if not os.path.isfile(markdown_file):
        raise FileExistsError(f"Error: the path `{markdown_file}` is not a file.")

    if not os.path.exists(template_html_path):
        raise FileExistsError(
            f"Error: unable to look for file at path `{template_html_path}`"
        )
    if not os.path.isfile(template_html_path):
        raise FileExistsError(f"Error: the path `{template_html_path}` is not a file.")

    with open(markdown_file) as md:
        md = md.read()
        title = extract_title(md)
        content = markdown_to_html_node(md).to_html()
        with open(template_html_path) as template:
            templ = template.read()
            templ = templ.replace("{{ Title }}", title)
            templ = templ.replace("{{ Content }}", content)
            if basepath is None:
                return templ
            templ = templ.replace("""href="/""", f"""href="{basepath}""")
            templ = templ.replace("""src="/""", f"""src="{basepath}""")
            return templ
    raise Exception("Error: unknown error occured. markdown file not transformed to html")

def export_from_path_of_md_to_html(markdown_file, basepath=None):
    dst = ""
    parent_dir = os.path.dirname(markdown_file).removeprefix(content_root_path).removeprefix("/")
    if parent_dir == "" or parent_dir == "content":
        dst = os.path.realpath(os.path.join(public_path, "index.html"))
    else:
        new_parent = os.path.realpath(os.path.join(public_path, parent_dir))
        if not os.path.exists(new_parent):
            os.makedirs(new_parent, exist_ok=True)
        dst = os.path.realpath(os.path.join(new_parent, "index.html"))
    html = transform_markdown_to_html_with_template(markdown_file, basepath=basepath)
    with open(dst, "w") as f:
        f.write(html)

def export_content_to_public(content_root_path=content_root_path, basepath=None):
    list_contents = os.listdir(content_root_path)
    for content in list_contents:
        current = os.path.join(content_root_path, content)
        if current.endswith("index.md") and os.path.isfile(current):
            export_from_path_of_md_to_html(current, basepath=basepath)
        if os.path.isdir(current):
            export_content_to_public(current, basepath=basepath)

