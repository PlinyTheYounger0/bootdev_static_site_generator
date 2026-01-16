import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode('This is a **bolded** word.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bolded', TextType.BOLD),
                TextNode(' word.', TextType.TEXT)
            ],
            new_nodes
        )

    def test_double_delim_bold(self):
        node = TextNode('This is a **bolded** word and **another** word.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('bolded', TextType.BOLD),
                TextNode(' word and ', TextType.TEXT),
                TextNode('another', TextType.BOLD),
                TextNode(' word.', TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode('This is a `block of code` surrounded by words.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertListEqual(
            [
                TextNode('This is a ', TextType.TEXT),
                TextNode('block of code', TextType.CODE),
                TextNode(' surrounded by words.', TextType.TEXT)
            ],
            new_nodes
        )
    def test_delim_italics(self):
        node = TextNode('This is an _italisized word_ surrounded by words.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode('This is an ', TextType.TEXT),
                TextNode('italisized word', TextType.ITALIC),
                TextNode(' surrounded by words.', TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_bold_italic_code(self):
        node = TextNode('This is an _italisized word_ surrounded by `a block of code` and some **bolded words** as well as some text.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('This is an ', TextType.TEXT),
                TextNode('italisized word', TextType.ITALIC),
                TextNode(' surrounded by ', TextType.TEXT),
                TextNode('a block of code', TextType.CODE),
                TextNode(' and some ', TextType.TEXT),
                TextNode('bolded words', TextType.BOLD),
                TextNode(' as well as some text.', TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_one_image(self):
        text = 'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)'
        image_list = extract_markdown_images(text)
        self.assertListEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif')
            ],
            image_list
        )

    def test_two_images(self):
        text = 'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)'
        image_list = extract_markdown_images(text)
        self.assertListEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            image_list
        )

    def test_one_link(self):
        text = 'This is text with a link [to boot dev](https://www.boot.dev)'
        link_list = extract_markdown_links(text)
        self.assertListEqual(
            [
                ('to boot dev', 'https://www.boot.dev')
            ],
            link_list
        )

    def test_one_link_one_image(self):
        text = 'This is text with a link [to boot dev](https://www.boot.dev) and a ![rick roll](https://i.imgur.com/aKaOqIh.gif)'
        link_list = extract_markdown_links(text)
        image_list = extract_markdown_images(text)
        self.assertListEqual(
            [
                ('to boot dev', 'https://www.boot.dev')
            ],
            link_list
        )
        self.assertListEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif')
            ],
            image_list
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_text_to_text_node(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                        [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
            )
if __name__ == "__main__":
    unittest.main()