from functools import partial

from utils.csv import read_csv
from .classes import PostBasedRow, ImageBasedRow
from .utils import (
    reassign_post_number,
    split_str_to_list,
    is_visible,
    is_acceptable,
    first_true,
)


def post_based_to_image_based(filename: str) -> "dict[str, ImageBasedRow]":
    imageToRow: "dict[str, ImageBasedRow]" = {}

    data = read_csv(filename)

    for d in data:
        post = PostBasedRow(
            image=d["images"],
            percentage=d["percent"],
            postNumber=d["code_id"],
            isComment=d["comment"],
            isExternal=d["outer_link"],
            isCorrect=d["correct"],
        )

        if (imageRow := imageToRow.get(post.image)) is not None:
            imageRow.add_post(post)
        else:
            imageToRow[post.image] = ImageBasedRow(**post.__dict__)

    return imageToRow


def combine_csv_data(*csvData: "list[dict]"):
    allData = []

    for index, data in enumerate(csvData):
        allData += reassign_post_number(index, identifier=data)

    return allData


def extract_field(
    corrected: "list[dict[str, str]]",
    inference: "list[dict[str, str]]",
    truthField: str,
    predictField: str,
) -> "list[dict]":
    imageToFields = {}

    for data in corrected:
        imageToFields[data["image"]] = {"actual": data[truthField]}

    for data in inference:
        imageToFields[data["img"]].update({"predict": data[predictField]})

    return list(imageToFields.values())


def map_borders(actualData: str, predictData: str, confidences: str, height: int):

    matches = []

    predict = split_str_to_list(predictData)
    actual = split_str_to_list(actualData)
    confidence = split_str_to_list(confidences, func=float)

    for pred, conf in zip(predict, confidence):
        if not is_visible(pred, height):
            continue

        match = first_true(
            actual,
            default=None,
            pred=partial(is_acceptable, predict=pred, height=height),
        )

        if match is None:
            matches.append({"predict": conf, "actual": 0})
            continue

        matches.append({"predict": conf, "actual": 1})
        actual.remove(match)

    unmatched = [{"predict": 0, "actual": 1} for _ in actual]

    return matches + unmatched


def extract_border_data(predictData: dict, actualData: dict):

    processed = []

    for image in actualData.keys():
        actual = actualData[image]["border"]
        predict = predictData[image]["edge"]
        confidence = predictData[image]["fb_post"]
        height = int(predictData[image]["height"])

        matches = map_borders(actual, predict, confidence, height)
        processed += matches

    return processed
