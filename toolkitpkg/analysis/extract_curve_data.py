from typing import Dict, List
from functools import partial
from . import ACCEPTABLE_PERCENTAGE, MAXIMUM_HEIGHT, MINIMUM_HEIGHT


def extract_field(corrected: List[Dict[str, str]], inference: List[Dict[str, str]], truthField: str, predictField: str) -> List[dict]:
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


def acceptable(actual: int, predict: int, height: int):
    return abs(actual - predict) < height * (ACCEPTABLE_PERCENTAGE / 100)


def border_mapping(actualData, predictData, confidences, height):

    matches = []

    predict = list(map(int, predictData.split('_'))) if predictData else []
    actual = list(map(int, actualData.split('_'))) if actualData else []
    confidence = list(map(float, confidences.split('_'))) if confidences else []

    for pred, conf in zip(predict, confidence):
        if not (MINIMUM_HEIGHT <= (pred/height)  <= MAXIMUM_HEIGHT):
            continue
        match = first_true(actual, default=None, pred=partial(acceptable, predict=pred, height=height))
        
        if match is None:
            matches.append({
                'predict': conf,
                'actual': 0
            })
            continue

        matches.append({
            'predict': conf,
            'actual': 1
        })
        actual.remove(match)

    unmatched = [{'predict': 0, 'actual': 1} for _ in actual] 

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



