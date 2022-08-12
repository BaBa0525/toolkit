import csv
from functools import partial

from csvOperations import write_csv

LOG_DETAILS = False
ACCEPTABLE_PERCENTAGE = 5

def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    return next(filter(pred, iterable), default)


def acceptable(actual: int, predict: int, height: int):
    return abs(actual - predict) < height * (ACCEPTABLE_PERCENTAGE / 100)



def borderMapping(actualData, predictData, confidences, height):

    matches = []

    predict = list(map(int, predictData.split('_'))) if predictData else []
    actual = list(map(int, actualData.split('_'))) if actualData else []
    confidence = list(map(float, confidences.split('_'))) if confidences else []

    for pred, conf in zip(predict, confidence):
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

    unmatched = [{'predict': 0, 'actual': 1}] * len(actual)

    return matches + unmatched


def readCSVasDict(filename: str, key: str) -> dict:
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        result = { row[key]: row for row in reader }
    
    return result


def main():
    predictData = readCSVasDict('./testing-data/first_inference_official2.csv', 'img')
    actualData = readCSVasDict('./testing-data/all-data-corrected.csv', 'image')

    processed = []

    for image in actualData.keys():
        actual = actualData[image]['border']
        predict = predictData[image]['edge']
        confidence = predictData[image]['fb_post']
        height = int(predictData[image]['height'])
        
        matches = borderMapping(actual, predict, confidence, height)
        processed += matches

        if LOG_DETAILS:
            print(f'{image=}')
            print(f'{actual=}')
            print(f'{predict=}')
            print(f'{confidence=}')
            print(f'{height=}px')
            print(f'{matches=}')
            print('=' * 50)


    write_csv(
        './testing-data/border.csv',
        fields=['actual', 'predict'],
        data=processed
    )


if __name__ == '__main__':
    main()