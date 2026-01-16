from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError('Invalid markdown. Formatted section not closed.')
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        orignal_text = old_node.text
        image_list = extract_markdown_images(orignal_text)
        if len(image_list) == 0:
            new_nodes.append(old_node)
            continue
        for image in image_list:
            alt_text, image_url = image
            sections = orignal_text.split(f'![{alt_text}]({image_url})', 1)
            if len(sections) != 2:
                raise ValueError('Invalid Markdown. Image section not closed')
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            orignal_text = sections[1]
        if orignal_text != '':
            new_nodes.append(TextNode(orignal_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        orignal_text = old_node.text
        link_list = extract_markdown_links(orignal_text)
        if not link_list:
            new_nodes.append(old_node)
            continue
        for link in link_list:
            anchor_text, link_url = link
            sections = orignal_text.split(f'[{anchor_text}]({link_url})', 1)
            if len(sections) != 2:
                raise ValueError('Invalid Markdown. Link section not closed')
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
            orignal_text = sections[1]
        if orignal_text != '':
            new_nodes.append(TextNode(orignal_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes