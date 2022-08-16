from functools import partial
from typing import Callable

from . import constants

def extract_field(corrected: 'list[dict[str, str]]', inference: 'list[dict[str, str]]', truthField: str, predictField: str) -> 'list[dict]':
    imageToFields = {}

    for data in corrected:
        imageToFields[data['image']] = {
            'actual': data[truthField]
        }
 
    for data in inference:
        imageToFields[data['img']].update({
            'predict': data[predictField]
        })

    return list(imageToFields.values())


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    return next(filter(pred, iterable), default)


def is_acceptable(actual: int, predict: int, height: int):
    return abs(actual - predict) < height * (constants.ACCEPTABLE_PERCENTAGE / 100)

def is_visible(predict: int, height: int):
    return constants.MINIMUM_HEIGHT <= (predict / height)  <= constants.MAXIMUM_HEIGHT

def split_str_to_list(data: str, func: Callable = int) -> list:
    return list(map(func, data.split('_'))) if data else []

def border_mapping(actualData: str, predictData: str, confidences: str, height: int):

    matches = []

    predict = split_str_to_list(predictData)
    actual = split_str_to_list(actualData)
    confidence = split_str_to_list(confidences, func=float)

    for pred, conf in zip(predict, confidence):
        if not is_visible(pred, height):
            continue

        match = first_true(actual, default=None, pred=partial(is_acceptable, predict=pred, height=height))
        
        if match is None:
            matches.append({ 'predict': conf, 'actual': 0 })
            continue

        matches.append({ 'predict': conf, 'actual': 1 })
        actual.remove(match)

    unmatched = [{ 'predict': 0, 'actual': 1 } for _ in actual] 

    return matches + unmatched


def process_border(predictData: dict, actualData: dict):

    processed = []

    for image in actualData.keys():
        actual = actualData[image]['border']
        predict = predictData[image]['edge']
        confidence = predictData[image]['fb_post']
        height = int(predictData[image]['height'])
        
        matches = border_mapping(actual, predict, confidence, height)
        processed += matches

    return processed



