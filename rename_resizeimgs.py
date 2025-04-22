import os


def rename_dir_file(dir_name, doc_name, folder_path):
    idx_remove_from = -32
    dir_name_new = dir_name[:idx_remove_from][:-1] + "-imgs"

    # chunk_to_remove = dir_name[idx_remove_from:]
    # doc_name_new = doc_name.split(chunk_to_remove)[0] + ".md"
    doc_name_new = "README.md"

    # remove " "
    dir_name_new = dir_name_new.replace(" ", "")
    doc_name_new = doc_name_new.replace(" ", "")

    # assign new name to the folder/file
    os.rename(
        os.path.join(folder_path, dir_name), os.path.join(folder_path, dir_name_new)
    )
    os.rename(
        os.path.join(folder_path, doc_name), os.path.join(folder_path, doc_name_new)
    )
    return dir_name_new, doc_name_new


def main(folder_name=None):
    folder_path = (
        os.path.join(os.getcwd(), folder_name)
        if folder_name is not None
        else os.getcwd()
    )

    dir_name = [
        filename_one
        for filename_one in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, filename_one))
    ]
    doc_name = [
        filename_one
        for filename_one in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, filename_one))
        and filename_one != ".DS_Store"
        and ".py" not in filename_one
    ]

    dir_name_new, doc_name_new = rename_dir_file(dir_name[0], doc_name[0], folder_path)

    # open doc_name_new
    with open(os.path.join(folder_path, doc_name_new), "r") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if "![" in line:
            spaces = line.split("!")[0]
            img_name = line.split("/")[-1].split(")")[0]

            img_ratio = 50

            breakpoint()

            lines[idx] = (
                f"{spaces}<img src='./{dir_name_new}/{img_name}' width='{str(img_ratio)}%'> <br>"
            )

    # write to doc_name_new
    with open(os.path.join(folder_path, doc_name_new), "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    main()
