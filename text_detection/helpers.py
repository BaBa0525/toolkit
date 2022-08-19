from google.cloud import vision

from statistics import mean


def filename_to_image(filename: str):
    """Return a vision.Image instance according to filename."""

    with open(filename, mode="rb") as image_file:
        content = image_file.read()

    return vision.Image(content=content)


def get_text_of_word(word: vision.Word) -> str:
    """Return the text in a vision.Word instance."""

    return "".join(symbol.text for symbol in word.symbols)


def mean_of_bounding_box(boundingBox: vision.BoundingPoly) -> int:
    """Return the mean of y-coordinates of a bounding box rounded to nearest integer."""

    yCoords = [vertex.y for vertex in boundingBox.vertices]
    return round(mean(yCoords))


def to_regex_string(string: str) -> str:
    """Convert string to a valid regex string by replacing all preserved symbols."""

    return (
        string.replace("$", r"\$")
        .replace("^", r"\^")
        .replace("+", r"\+")
        .replace("(", r"\(")
        .replace(")", r"\)")
    )


def to_regex_string_list(oldList: "list[str]") -> "list[str]":
    """Convert all strings in list to a valid regex string."""

    return [to_regex_string(string) for string in oldList]
