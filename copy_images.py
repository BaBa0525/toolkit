import shutil


def main():
    with open("label/images.md", mode="r") as f:
        images = f.readlines()

    for image in images:
        arr = image.split()
        shutil.copy2(arr[-1], f"label/image/")


if __name__ == "__main__":
    main()
