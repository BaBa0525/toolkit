import os


def replace_extension(path: str, newExtension: str):
    """Replace the file extension in path."""

    filename, _ = os.path.splitext(path)

    if newExtension.startswith("."):
        return f"{filename}{newExtension}"

    return f"{filename}.{newExtension}"
