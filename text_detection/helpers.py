from google.cloud import vision

from statistics import mean


def get_text_of_word(word: vision.Word) -> str:
    return "".join(symbol.text for symbol in word.symbols)


def mean_of_bounding_box(boundingBox: vision.BoundingPoly) -> int:
    yCoords = [vertex.y for vertex in boundingBox.vertices]
    return round(mean(yCoords))


def to_regex_string(oldString: str) -> str:
    return (
        oldString.replace("$", r"\$")
        .replace("^", r"\^")
        .replace("+", r"\+")
        .replace("(", r"\(")
        .replace(")", r"\)")
    )


def to_regex_string_list(oldList: "list[str]") -> "list[str]":
    return [to_regex_string(string) for string in oldList]
