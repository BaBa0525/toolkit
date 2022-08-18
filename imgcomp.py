"""This script provides a command line interface for image compression.

usage: imgcomp.py [-h] [--directory DIRECTORY] [--image IMAGE] --output OUTPUT [--size SIZE] [--quality QUALITY] [--format FORMAT [FORMAT ...]]

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        compress all images in the directory
  --image IMAGE, -i IMAGE
                        compress the image
  --output OUTPUT, -o OUTPUT
                        <Required> output file or directory
  --size SIZE, -s SIZE  image size factor (default=0.8)
  --quality QUALITY, -q QUALITY
                        image quality on save (range=[0,99], default=85)
  --format FORMAT [FORMAT ...], -f FORMAT [FORMAT ...]
                        image file types (when '-d' option is set, default=['.jpg'])
"""

import argparse
import imghdr
import pathlib
import sys

from img_processing import Compressor


def configure_args(**kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument(
        "--directory", "-d", required=False, help="compress all images in the directory"
    )
    parser.add_argument("--image", "-i", required=False, help="compress the image")
    parser.add_argument(
        "--output", "-o", required=True, help="<Required> output file or directory"
    )
    parser.add_argument(
        "--size",
        "-s",
        type=float,
        default=0.8,
        required=False,
        help="image size factor (default=0.8)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=85,
        required=False,
        help="image quality on save (range=[0,99], default=85)",
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default=[".jpg"],
        nargs="+",
        required=False,
        help="image file types (when '-d' option is set, default=['.jpg'])",
    )
    return parser


def main():
    parser = configure_args()
    args = parser.parse_args()

    compressor = Compressor(args.size, args.quality, args.format)

    if args.directory:
        if not pathlib.Path(args.directory).is_dir():
            raise NotADirectoryError(f"{args.directory} is not a directory")

        compressor.compress(args.directory, args.output)

    elif args.image:
        if imghdr.what(args.image) is None:
            raise TypeError(f"{args.image} unsupported file type")

        compressor.compress_image(args.image, args.output)

    else:
        parser.print_help()
        print(file=sys.stderr)
        print("No image or directory provided.", file=sys.stderr)


if __name__ == "__main__":
    main()
