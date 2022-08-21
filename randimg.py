import os
import random
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int, help="number of samples")
    args = parser.parse_args()

    allImages: "list[str]" = []

    for root, _, files in os.walk("/mnt/d/IG"):
        allImages.extend(os.path.join(root, file) for file in files)

    filteredImages = filter(lambda x: "crop" not in x, allImages)

    samples = random.sample(range(len(filteredImages)), k=args.k)

    print(*[filteredImages[sample] for sample in samples], sep="\n")


if __name__ == "__main__":
    main()
