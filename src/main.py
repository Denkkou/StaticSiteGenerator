from textnode import *
import os, shutil

def main():
    public_path = "public/"
    static_path = "static/"
    
    clear_directory(public_path)
    copy_static_to_public(public_path, static_path)


def copy_static_to_public(public_path, static_path):
    static_contents = os.listdir(static_path)
    for item in static_contents:
        if os.path.isfile(static_path + item):
            shutil.copy(static_path + item, public_path)
            print(f"Copying {item} from {static_path}{item} to {public_path}{item}.")
        elif os.path.isdir(static_path + item):
            os.mkdir(public_path + f"{item}")
            copy_static_to_public(public_path + item + "/", static_path + item + "/")

def clear_directory(directory_path):
    contents = os.listdir(directory_path)
    if not contents:
        print(f"Directory '{directory_path}' is already empty.")()
        return
    
    for item in os.listdir(directory_path):
        if os.path.isfile(directory_path + item):
            print(f"Deleting file: {directory_path}{item}")
            os.remove(directory_path + item)
        elif os.path.isdir(directory_path + item):
            print(f"Deleting directory: {directory_path}{item}")
            shutil.rmtree(directory_path + item)

if __name__ == "__main__":
    main()