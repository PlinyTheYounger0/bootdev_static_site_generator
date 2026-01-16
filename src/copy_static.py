import os
import shutil



def copy_files_recursive(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

        for filename in os.listdir(src_dir):
            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            print(f" * {src_path} -> {dest_path}")
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
            else:
                copy_files_recursive(src_path, dest_path)