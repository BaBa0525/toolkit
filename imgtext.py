"""Provides a command line tool for detecting text in images.

usage: imgtext.py [-h] [-d DIRECTORY] [-i IMAGE] -o OUTPUT [-f FORMAT [FORMAT ...]]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        detect all images with the specified file format in the directory
  -i IMAGE, --image IMAGE
                        detect the text in the image
  -o OUTPUT, --output OUTPUT
                        <Required> output file (if '-i' is set) or directory (if '-d' is set)
  -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        image file format to detect (when '-d' option is set, default=['.jpg'])
"""

import argparse
import imghdr
import os
import pathlib
import sys

from text_detection import setup_credential, detect_image, dump_json, batch_detect
from utils.path import replace_extension


def configure_args(**kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument(
        "-d",
        "--directory",
        required=False,
        help="detect all images with the specified file format in the directory",
    )
    parser.add_argument(
        "-i", "--image", required=False, help="detect the text in the image"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="<Required> output file (if '-i' is set) or directory (if '-d' is set)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default=[".jpg"],
        nargs="+",
        required=False,
        help="image file format to detect (when '-d' option is set, default=['.jpg'])",
    )
    return parser


def detect_all(args: argparse.Namespace):
    """Make call to Google OCR API with all images in args.directory and dump one JSON file for each image into args.output."""

    if not pathlib.Path(args.directory).is_dir():
        raise NotADirectoryError(f"{args.directory} is not a directory")

    os.makedirs(args.output, exist_ok=True)

    if not pathlib.Path(args.output).is_dir():
        raise NotADirectoryError(f"{args.output} is not a directory")

    def is_specified(filename: str):
        _, ext = os.path.splitext(filename)
        return ext in args.format

    # open only accepts relative path, so use os.path.join instead of os.path.abspath
    images = [
        os.path.join(args.directory, filename)
        for filename in os.listdir(args.directory)
        if is_specified(filename)
    ]

    responses = batch_detect(images)

    for image, response in zip(images, responses):
        _, filename = os.path.split(image)
        jsonFile = replace_extension(filename, "json")
        dump_json(response, os.path.join(args.output, jsonFile))


def detect_one(args: argparse.Namespace):
    """Make call to Google OCR API with args.image and dump JSON file at args.output."""

    if imghdr.what(args.image) is None:
        raise TypeError(f"{args.image} unsupported file type")

    path, _ = os.path.split(args.output)
    os.makedirs(path, exist_ok=True)

    if pathlib.Path(args.output).is_dir():
        _, imgInput = os.path.split(args.image)
        file, _ = os.path.splitext(imgInput)
        args.output = os.path.join(args.output, f"{file}.json")

    response = detect_image(args.image)
    dump_json(response, args.output)


def main():
    parser = configure_args()
    args = parser.parse_args()

    setup_credential()

    if args.directory:
        detect_all(args)

    elif args.image:
        detect_one(args)

    else:
        parser.print_help()
        print(file=sys.stderr)
        print("No image or directory provided.", file=sys.stderr)


if __name__ == "__main__":
    main()
