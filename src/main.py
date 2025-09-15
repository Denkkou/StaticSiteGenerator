from textnode import *
import os, shutil, re, sys
from converters import markdown_to_html_node

def main():
    public_path = "docs/"
    static_path = "static/"
    content_path = "content/"
    if sys.argv:
        base_path = sys.argv[1]
    else: 
        base_path = "/"
    
    clear_directory(public_path)
    copy_static_to_public(static_path, public_path)
    generate_page_recursive(content_path, "template.html", public_path, base_path)


def copy_static_to_public(static_path, public_path):
    static_contents = os.listdir(static_path)
    for item in static_contents:
        if os.path.isfile(static_path + item):
            shutil.copy(static_path + item, public_path)
            print(f"Copying {item} from {static_path}{item} to {public_path}{item}.")
        elif os.path.isdir(static_path + item):
            os.mkdir(public_path + f"{item}")
            copy_static_to_public(static_path + item + "/", public_path + item + "/")

def clear_directory(directory_path):
    contents = os.listdir(directory_path)
    if not contents:
        print(f"Directory '{directory_path}' is already empty.")
        return
    
    for item in os.listdir(directory_path):
        if os.path.isfile(directory_path + item):
            print(f"Deleting file: {directory_path}{item}")
            os.remove(directory_path + item)
        elif os.path.isdir(directory_path + item):
            print(f"Deleting directory: {directory_path}{item}")
            shutil.rmtree(directory_path + item)

def extract_title(markdown):
    headers = re.findall(r"^# .*", markdown, re.MULTILINE)
    if headers:
        return headers[0][1:].strip()
    else:
        raise Exception("No header found in markdown document.")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        markdown = open(from_path, 'r').read()
    except:
        raise Exception("Could not open and read markdown.")
    
    try:
        template = open(template_path, 'r').read()
    except:
        raise Exception("Could not open and read template.")

    html_string = markdown_to_html_node(markdown).to_html()

    header = extract_title(markdown)

    print(base_path)
    output = template[:]
    output = output.replace("{{ Title }}", header)
    output = output.replace("{{ Content }}", html_string)
    output = output.replace('href="', f'href="{base_path}')
    output = output.replace('src="', f'src="{base_path}')

    with open(dest_path, 'w') as file:
        file.write(output)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    contents = os.listdir(dir_path_content)
    print(contents)

    for item in contents:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            file_name = os.path.splitext(item)[0] + ".html"
            generate_page(item_path, template_path, os.path.join(dest_dir_path, file_name), base_path)
        elif os.path.isdir(item_path):
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_page_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item), base_path)           

if __name__ == "__main__":
    main()