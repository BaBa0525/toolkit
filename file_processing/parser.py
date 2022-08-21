import pandas as pd

from collections import namedtuple
import re

from utils.csv import write_csv

FIELD_NAMES = (
    "image",
    "fb_external_1",
    "fb_external_2",
    "fb_external_3",
    "fb_external_4",
    "fb_external_5",
    "fb_comment_1",
    "fb_comment_2",
    "fb_home",
    "fb_post",
    "fb_post_top_y",
)

Row = namedtuple("Row", FIELD_NAMES)


class DetectionResultParser:
    @staticmethod
    def _read_detection_result_to_dicts(filename: str) -> "list[dict[str, str]]":
        dicts = []

        with open(filename, "r") as file:
            for line in file:
                arr = line.split(":")

                if (field := arr[0]) == "Enter Image Path":
                    image = arr[1].strip()
                    dicts.append({**dict.fromkeys(FIELD_NAMES, ""), "image": image})

                elif field == "fb_post":
                    d = dicts[-1]
                    x = arr[1].split("%")

                    if d[field] != "":
                        d["fb_post"] += ","
                        d["fb_post_top_y"] += ","

                    d["fb_post"] += x[0].strip()

                    match = re.search(r"top_y:\s*\d+", line)
                    if match is None:
                        continue

                    d["fb_post_top_y"] += match.group().split()[1]

                elif field in FIELD_NAMES:
                    if d[field] != "":
                        continue

                    d = dicts[-1]
                    x = arr[1].split("%")
                    d[field] += x[0]

        return dicts

    def __init__(self, inputFile: str):
        """Parses the detection result from YOLO to desired format."""

        self.dicts = DetectionResultParser._read_detection_result_to_dicts(inputFile)

    def to_csv(self, outputFile: str):
        write_csv(outputFile, FIELD_NAMES, self.dicts)

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame([Row(**d) for d in self.dicts])
