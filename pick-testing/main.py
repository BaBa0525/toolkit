import os
import random
import shutil


IMAGE_ROOT_PATH = "/mnt/c/Users/Alan/Documents/ig"
OUTPUT_PATH = "./pick-testing/picked-images"

USED_IMAGES_FILE = "./pick-testing/used-images.txt"

GROUP_SIZE = 25
NUM_GROUPS = 40


def load_used_images():
    with open(USED_IMAGES_FILE, mode="r") as f:
        return [line.strip("\n") for line in f]


def main():
    used_images = set(load_used_images())

    users = os.listdir(IMAGE_ROOT_PATH)

    testing_images: "set[str]" = set()
    grouped_images: "list[tuple[str, str, set[str]]]" = []

    for _ in range(NUM_GROUPS):
        while True:
            user = random.choice(users)
            user_path = os.path.join(IMAGE_ROOT_PATH, user)

            sessions = os.listdir(user_path)
            session = random.choice(sessions)
            session_path = os.path.join(user_path, session)

            images = sorted(
                [
                    os.path.join(session_path, image)
                    for image in os.listdir(session_path)
                ]
            )
            num_images = len(images)

            if num_images < GROUP_SIZE:
                continue

            start_index = random.randint(0, num_images - GROUP_SIZE - 1)
            picked_images = set(images[start_index : start_index + GROUP_SIZE])

            if (
                len(testing_images & picked_images) != 0
                or len(used_images & picked_images) != 0
            ):
                continue

            testing_images.update(picked_images)
            grouped_images.append((user, session, picked_images))
            break

    for group, (user, session, images) in enumerate(grouped_images):
        output_dir = os.path.join(OUTPUT_PATH, f"group-{group + 1:02d}")
        os.makedirs(output_dir, exist_ok=True)

        for image in images:

            shutil.move(
                image,
                os.path.join(output_dir, f"{user}-{session}-{os.path.split(image)[1]}"),
            )

    with open(os.path.join(OUTPUT_PATH, ".gitignore"), mode="w") as f:
        print("*", file=f)


if __name__ == "__main__":
    main()
