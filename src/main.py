from textnode import TextNode
from textnode import TextType


def main():
    textnode = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(textnode)

main()
