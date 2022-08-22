import os
import random
from typing import Union


ROOT_DIRECTORY = "/mnt/d/IG"
NUMBER_OF_IMAGES = 100


def get_user_id_index(routes: "list[str]") -> Union[int, None]:
    """Return index of user id in the given path list

    Args:
        routes (list[str]): path to image pre-splitted according to `os.path.sep`

    Returns:
        Union[int, None]: index of user id find in the list, `None` if not found.
    """

    for index, route in enumerate(routes):
        if route.startswith("U"):
            return index

    return None


def sample_sorting_key(pathToImage: str) -> "tuple[int, int, str]":
    """Sorting key of images.

    Args:
        pathToImage (str): path to chosen image

    Returns:
        int: user id (e.g. U123 -> 123)
        int: folder id (e.g. U123/456 -> 456)
        str: name of the image file
    """

    path = os.path.normpath(pathToImage)
    routes = path.split(os.path.sep)

    userIdIndex = get_user_id_index(routes)

    userId, folderId, imageName = routes[userIdIndex:]

    return int(userId[1:]), int(folderId), imageName


def main():
    if not os.path.isdir(ROOT_DIRECTORY):
        raise NotADirectoryError(f"{ROOT_DIRECTORY!r} is not a directory.")

    allImages: "list[str]" = []

    for root, _, files in os.walk(ROOT_DIRECTORY):
        allImages.extend(os.path.join(root, file) for file in files)

    filteredImages = list(filter(lambda imageName: "crop" not in imageName, allImages))

    results = sorted(
        random.sample(filteredImages, k=NUMBER_OF_IMAGES), key=sample_sorting_key
    )

    for result in results:
        print(f"- [ ] {result}")


if __name__ == "__main__":
    main()
