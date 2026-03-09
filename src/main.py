from textnode import TextNode, TextType
import shutil
import os
from markdown_blocks import markdown_to_html_node



def main():
    
    src_folder = "static"
    dst_folder = "public"

    copy_folder(src_folder, dst_folder)
    generate_pages_recursive("content", "template.html", "public")
    


def copy_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
            print(f"Copied folder: {s} to {d}")
        else:
            shutil.copy2(s, d)
            print(f"Copied file: {s} to {d}")
    

def extract_title(markdown):
    lines = markdown.splitlines()
    h1_index = -1
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h1_index = i
            break
    if h1_index == -1:
        raise ValueError("No h1 header found in the markdown content.")
    return lines[h1_index][2:].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with (open(from_path, 'r') as f):
        markdown_content = f.read()
    with (open(template_path, 'r') as f):
        template_content = f.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with (open(dest_path, 'w') as f):
        f.write(final_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        s = os.path.join(dir_path_content, item)
        d = os.path.join(dest_dir_path, item)
        if os.path.isdir(s):
            generate_pages_recursive(s, template_path, d)
        elif s.endswith(".md"):
            generate_page(s, template_path, d.replace(".md", ".html"))

if __name__ == "__main__":
    main()

