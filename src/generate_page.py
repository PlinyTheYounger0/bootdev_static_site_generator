import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            title = line.strip('#')
            clean_title = title.strip()
            return clean_title
    raise Exception('No title found. Make sure you have an h1 in your markdown.')

def generate_page(src_path, template_path, dest_path, base_path):
    print(f'Generating page from {src_path} to {dest_path} using {template_path}')

    with open(src_path, 'r', encoding='utf8') as f:
        markdown = f.read()

    with open(template_path, 'r', encoding='utf8') as f:
        html_template = f.read()

    content = markdown_to_html_node(markdown)
    html_content = content.to_html()
    title = extract_title(markdown)

    title_no_content_html = html_template.replace('{{ Title }}', title)
    title_content_html = title_no_content_html.replace('{{ Content }}', html_content)
    title_content_html = title_content_html.replace('href="/', 'href="' + base_path)
    title_content_html = title_content_html.replace('src="/', 'src="' + base_path)

    dest_dirs_path = os.path.dirname(dest_path)
    os.makedirs(dest_dirs_path, exist_ok=True)

    with open(dest_path, 'w', encoding='utf8') as f:
        f.write(title_content_html)

def generate_page_recursive(src_dir, template_path, dest_dir, base_path):
    files = os.listdir(src_dir)
    print(files)
    for file in files:
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file)
        if os.path.isfile(src_path):
             if file.endswith('md'):
                 file = file.replace('md', 'html')
                 dest_path = os.path.join(dest_dir, file)
             generate_page(src_path, template_path, dest_path, base_path)
        if os.path.isdir(src_path):
            generate_page_recursive(src_path, template_path, dest_path, base_path)
        