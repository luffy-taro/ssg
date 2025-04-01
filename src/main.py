import os
import shutil
import sys

from parser import extract_title, markdown_to_html_node


CURRENT_DIRECTORY = os.getcwd()
PUBLIC_DIR = os.path.join(CURRENT_DIRECTORY, 'docs')
STATIC_DIR = os.path.join(CURRENT_DIRECTORY, 'static')
CONTENT_DIR = os.path.join(CURRENT_DIRECTORY, 'content')
TEMPLATE_FILE = os.path.join(CURRENT_DIRECTORY, 'template.html')

def copy_files(src, dest):
    listings = os.listdir(src)
    for item in listings:
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest)
        else:
            dest_path = os.path.join(dest, item)
            os.mkdir(dest_path)
            copy_files(item_path, dest_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    template_file = open(template_path)

    md_text = md_file.read()
    template_string = template_file.read()

    title = extract_title(md_text)
    html_string = markdown_to_html_node(md_text).to_html()


    template_string = template_string.replace("{{ Title }}", title)
    template_string = template_string.replace("{{ Content }}", html_string)

    if basepath != "/":
        template_string = template_string.replace('href="', f"href=\"{basepath}")
        template_string = template_string.replace('src="', f"src=\"{basepath}")

    with open(dest_path, 'w') as f:
        f.write(template_string)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    listings = os.listdir(dir_path_content)
    for item in listings:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            filename = os.path.splitext(item)[0] + ".html"
            generate_page(item_path, template_path, os.path.join(dest_dir_path, filename), basepath)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path, basepath)


def main():
    # clear public directory
    if os.path.exists(PUBLIC_DIR):
        for item in os.listdir(PUBLIC_DIR):
            path = os.path.join(PUBLIC_DIR, item)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
    else:
        os.mkdir(PUBLIC_DIR)

    # copy all static files
    copy_files(STATIC_DIR, PUBLIC_DIR)


    # update basepath
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # convert md files to html and copy to public dir
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, PUBLIC_DIR, basepath)


if __name__ == "__main__":
    main()
