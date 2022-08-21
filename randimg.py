import os
import random


ROOT_DIRECTORY = ""
NUMBER_OF_IMAGES = 100


def get_user_id_index(routes: "list[str]") -> int:
    for index, route in enumerate(routes):
        if "U" in route:
            return index


def sample_sorting_key(sample: str) -> "tuple[int, int, str]":
    path = os.path.normpath(sample)
    routes = path.split(os.path.sep)

    userIdIndex = get_user_id_index(routes)

    userId, folderId, imageName = routes[userIdIndex:]

    # userId: 'Uxxx'
    return int(userId[1:]), int(folderId), imageName


def main():
    if not os.path.isdir(ROOT_DIRECTORY):
        raise NotADirectoryError(f"{ROOT_DIRECTORY!r} is not a directory.")

    allImages: "list[str]" = []

    for root, _, files in os.walk(ROOT_DIRECTORY):
        allImages.extend(os.path.join(root, file) for file in files)

    filteredImages = list(filter(lambda x: "crop" not in x, allImages))

    samples = random.sample(filteredImages, k=NUMBER_OF_IMAGES)

    results = sorted(samples, key=sample_sorting_key)

    print("\n".join(results))


if __name__ == "__main__":
    main()
