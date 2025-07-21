import unittest

from src.markdown.blocks import markdown_to_blocks
from src.markdown.blocktypes import block_to_block_type, BlockType


class BlockTypesTest(unittest.TestCase):
    def test_block_to_blocktypes(self):
        md = """This is supposed to be a paragraph

# This is a heading

## This is also another heading

> Oh this is a quote block
and it's so nice!

```bash
echo "This is a code block!!!"
```

- An unordered list item
- Next to another item

1. This is also a list but this is ordered

Another paragraph that does not make sense at all!
But all is good!
"""
        md_blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is supposed to be a paragraph",
                "# This is a heading",
                "## This is also another heading",
                "> Oh this is a quote block\nand it's so nice!",
                '```bash\necho "This is a code block!!!"\n```',
                "- An unordered list item\n- Next to another item",
                "1. This is also a list but this is ordered",
                "Another paragraph that does not make sense at all!\nBut all is good!",
            ],
            md_blocks,
        )
        all_block_types = [block_to_block_type(md_block) for md_block in md_blocks]
        self.assertEqual(
            [
                BlockType.PARAGRAPH,
                BlockType.HEADING1,
                BlockType.HEADING2,
                BlockType.QUOTE,
                BlockType.CODE_BLOCK,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
            ],
            all_block_types,
        )


if __name__ == "__main__":
    unittest.main()
