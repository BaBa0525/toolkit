from typing import Callable


from utils.decorators import static_vars
from . import config


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns `default`

    If `pred` is not None, returns the first item
    for which `pred(item)` is true.
    """
    return next(filter(pred, iterable), default)


def is_acceptable(actual: int, predict: int, height: int):
    """Return whether the gap between actual border and predicted border is less than `ACCEPTABLE_PERCENTAGE`."""
    return abs(actual - predict) < height * (config.ACCEPTABLE_PERCENTAGE / 100)


def is_visible(border: int, height: int):
    """Return whether the border is inside the visible area."""
    return config.MINIMUM_HEIGHT <= (border / height) <= config.MAXIMUM_HEIGHT


def split_str_to_list(data: str, func: Callable[[str], any] = str) -> list:
    """Split the underscore-separated data string into a list with each element applied by func."""
    return [func(x) if func else x for x in data.split("_")] if data else []


@static_vars(postNumbersMap={})
def reassign_post_number(data: "list[dict[str, str]]", identifier: any) -> "list[dict]":
    """Reassign unique post number in a data list read from csv in ascending order (1-based).

    The uniqueness is according to the tuple `(identifier, postNumber)` during the whole lifetime of this function.
    """

    postNumbersMap: "dict[tuple[any, str], int]" = reassign_post_number.postNumbersMap

    newList = []

    for d in data:
        postNumbers = d["postNumber"].split("_")
        newPostNumbers = []

        for number in postNumbers:
            newNumber = postNumbersMap.setdefault(
                (identifier, number), len(postNumbersMap) + 1
            )
            newPostNumbers.append(newNumber)

        newList.append({**d, "postNumber": "_".join(map(str, newPostNumbers))})

    return newList
