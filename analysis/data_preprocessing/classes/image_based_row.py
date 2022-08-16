from attr import define, field

from itertools import accumulate

from utils.csv import read_csv
from . import Dimension, PostBasedRow
from .. import config


INFERENCE_FILE = "data/official-two/first_inference_official.csv"


imageToSize = {
    row["img"]: Dimension(row["width"], row["height"])
    for row in read_csv(INFERENCE_FILE)
}


@define
class ImageBasedRow:
    image: str
    isComment: bool
    isExternal: bool
    isCorrect: bool
    percentage: "list[float]" = field(converter=lambda x: [x])
    postNumber: "list[int]" = field(converter=lambda x: [x])

    def add_post(self, row: PostBasedRow):
        self.isCorrect = self.isCorrect and row.isCorrect
        self.percentage.append(row.percentage)
        self.postNumber.append(row.postNumber)

    def borders_in_pixel(self, imageHeight: int) -> "list[int]":
        accumulatedPercentage = list(
            accumulate(self.percentage, initial=config.INVISIBLE_HEIGHT)
        )[1:-1]
        # [1:-1] => drop the INVISIBLE_HEIGHT

        def get_pixel(percentage: float, imageHeight: int):
            return round(percentage * imageHeight)

        return [
            get_pixel(percentage, imageHeight) for percentage in accumulatedPercentage
        ]

    @property
    def __dict__(self):
        border = self.borders_in_pixel(imageToSize[self.image].height)

        return {
            "image": self.image,
            "isComment": int(self.isComment),
            "isExternal": int(self.isExternal),
            "isCorrect": int(self.isCorrect),
            "border": "_".join(map(str, border)),
            "postNumber": "_".join(map(str, self.postNumber)),
        }
