import os
import shutil

from copy_static import copy_files_recursive
from generate_page import generate_page_recursive


dir_path_static = './static'
dir_path_public = './public'
dir_path_content = './content'
template_path = './template.html'


def main():
    print(f' Deleting public directory')
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print(f'Copying static files to public directory...')
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page_recursive(
        dir_path_content,
        './template.html', 
        dir_path_public
    )

if __name__ == '__main__':
    main()