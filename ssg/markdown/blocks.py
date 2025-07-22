def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return blocks
