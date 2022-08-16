from typing import Callable


from utils.decorators import static_vars
from . import config


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    return next(filter(pred, iterable), default)


def is_acceptable(actual: int, predict: int, height: int):
    return abs(actual - predict) < height * (config.ACCEPTABLE_PERCENTAGE / 100)


def is_visible(predict: int, height: int):
    return config.MINIMUM_HEIGHT <= (predict / height) <= config.MAXIMUM_HEIGHT


def split_str_to_list(data: str, func: Callable = int) -> list:
    return list(map(func, data.split("_"))) if data else []


@static_vars(idStringToNewNumber={})
def reassign_post_number(data: "list[dict[str, str]]", identifier: int) -> "list[dict]":
    idStringToNewNumber: "dict[str, int]" = reassign_post_number.idStringToNewNumber

    newList = []

    for d in data:
        postNumbers = d["postNumber"].split("_")
        newPostNumbers = []

        for number in postNumbers:
            idString = f"{identifier}-{number}"

            if (newNumber := idStringToNewNumber.get(idString)) is not None:
                newPostNumbers.append(newNumber)
                continue

            newNumber = len(idStringToNewNumber) + 1
            idStringToNewNumber[idString] = newNumber
            newPostNumbers.append(newNumber)

        newList.append({**d, "postNumber": "_".join(map(str, newPostNumbers))})

    return newList
