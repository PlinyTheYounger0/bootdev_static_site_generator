import os
import shutil
import sys

from copy_static import copy_files_recursive
from generate_page import generate_page_recursive


dir_path_static = './static'
dir_path_public = './docs'
dir_path_content = './content'
template_path = './template.html'
defalut_base_path = '/'

def main():
    base_path = defalut_base_path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print(f' Deleting public directory')
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print(f'Copying static files to public directory...')
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page_recursive(
        dir_path_content,
        './template.html', 
        dir_path_public,
        base_path
    )

if __name__ == '__main__':
    main()