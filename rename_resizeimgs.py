import os
import re
import urllib.parse
from pathlib import Path


def sanitize_filename(name):
    # URLdecode
    name = urllib.parse.unquote(name)

    base, ext = os.path.splitext(name)

    # remove notion-ID (32文字の16進数 + 任意でスペース)
    match = re.search(r"\s+([a-f0-9]{32})$", base)
    if match:
        base = base[: match.start()]

    base = base.replace(" ", "").replace("　", "")
    chars_to_remove = r'[\\/*?:"<>|!@#$%^&(),.;\']'
    base = re.sub(chars_to_remove, "", base)

    base = "".join(c for c in base if c.isprintable())

    return base + ext


def rename_dir_file(dir_name, doc_name, folder_path):
    """
    make new dir
    rename markdown file to README.md and move it to new dir.
    rename image dir to "imgs" and move it to new dir.
    """
    # print(f"Renaming: Dir='{dir_name}', Doc='{doc_name}' in Folder='{folder_path}'")

    base_new = os.path.splitext(sanitize_filename(doc_name))[0]
    doc_name_new = "README.md"

    # move to parent directory
    parent = Path(folder_path).parent
    os.chdir(parent)

    folder_path_new = os.path.join(parent, base_new)
    os.makedirs(folder_path_new, exist_ok=True)

    # rename doc file
    old_path = os.path.join(folder_path, doc_name)
    new_path = os.path.join(folder_path_new, doc_name_new)
    os.rename(old_path, new_path)

    # rename dir if exists
    if dir_name:
        dir_name_new = "imgs"
        old_path = os.path.join(folder_path, dir_name)
        new_path = os.path.join(folder_path_new, dir_name_new)
        os.makedirs(new_path, exist_ok=True)
        os.system(f"cp -r '{old_path}'/* '{new_path}/'")
    else:
        dir_name_new = None

    os.system(f"rm -rf '{folder_path}'")

    return dir_name_new, doc_name_new, folder_path_new


def update_image_links(file_path, img_dir_name):
    """
    Update image links in the markdown file to use <img> tags with specified width.
     - file_path: Path to the markdown file to update.
     - img_dir_name: Name of the image directory (e.g., "imgs"). If None, it assumes images are in the same directory as the markdown file.
     - The function looks for markdown image links in the format ![alt](url) and replaces them with <img> tags, setting the width to 50%. It also preserves the original indentation of the line.
    """
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    img_ratio = 60

    new_lines = []
    for line in lines:
        match = re.search(r"^(\s*)!\[(.*?)\]\((.*?)\)", line)
        if match:
            indent = match.group(1)
            original_url = match.group(3)

            img_filename = os.path.basename(urllib.parse.unquote(original_url))

            if img_dir_name:
                new_line = f"{indent}<img src='./{img_dir_name}/{img_filename}' width='{img_ratio}%'> <br>\n"
            else:
                new_line = (
                    f"{indent}<img src='./{img_filename}' width='{img_ratio}%'> <br>\n"
                )

            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)


def main():
    folder_path = os.getcwd()

    all_files = os.listdir(folder_path)

    dirs = []
    for f in all_files:
        if os.path.isdir(os.path.join(folder_path, f)):
            dirs.append(f)
        elif (
            os.path.isfile(os.path.join(folder_path, f))
            and f.endswith(".md")
            and f != "README.md"
        ):
            doc = f
        else:
            continue

    target_dir = dirs[0] if dirs else None
    target_doc = doc

    print(f"Processing: File='{target_doc}', Dir='{target_dir}'")

    dir_name_new, doc_name_new, folder_path_new = rename_dir_file(
        target_dir, target_doc, folder_path
    )

    if doc_name_new:
        update_image_links(os.path.join(folder_path_new, doc_name_new), dir_name_new)
        print("Done.")

    os.system(f"rm -rf '{folder_path}'")


if __name__ == "__main__":
    main()
