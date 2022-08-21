from google.cloud import vision

from bisect import bisect
import re

from .helpers import mean_of_bounding_box, get_text_of_word, to_regex_string_list
from . import typed_generators as tg


def split_posts_by_height(
    document: vision.TextAnnotation, bordersInPixel: "list[int]"
) -> "list[str]":
    """Split the text in document with the given borders.

    Args:
        document: The attribute full_text_annotation from the return value of text_detection.detect_image().
            example: `document = text_detection.detect_image('my_image.png').full_text_annotation`

        bordersInPixel: The position of each border in pixel.

    Returns:
        list[str]: The text of each post.
            Normally, the length of the list should be len(bordersInPixel) + 1.
    """

    sortedBorders = sorted(bordersInPixel)  # make sure that borders are fit to bisect()
    result: "list[list[str]]" = [[] for _ in range(len(bordersInPixel) + 1)]

    for word in tg.get_words_from_document(document):
        index = bisect(sortedBorders, mean_of_bounding_box(word.bounding_box))
        result[index].append(get_text_of_word(word))

    posts: "list[str]" = []

    for postWords in result:
        pattern = r"\s*".join(to_regex_string_list(postWords))
        text: str = document.text

        if (match := re.search(pattern, text)) is not None:
            posts.append(match.group())

    return posts
