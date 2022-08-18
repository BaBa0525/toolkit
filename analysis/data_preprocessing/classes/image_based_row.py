from attr import define

from itertools import accumulate

from utils.csv import read_csv
from . import Dimension, PostBasedRow
from .. import config


INFERENCE_FILE = "data/official-two/first_inference_official.csv"


IMAGE_NAME_TO_DIMENSION: "dict[str, Dimension]" = {
    row["img"]: Dimension(row["width"], row["height"])
    for row in read_csv(INFERENCE_FILE)
}


@define
class ImageBasedRow:
    """A class that contains the detection data within a image."""

    image: str
    isComment: bool
    isExternal: bool
    isCorrect: bool
    percentage: "list[float]"
    postNumber: "list[int]"

    @classmethod
    def from_post(cls, row: PostBasedRow):
        """Create a ImageBasedRow based on a PostBasedRow instance.

        The new object is created without adding the border and post number.
        (Intended, for simplifying dictionary setdefault)
        """

        obj = cls.__new__(cls)
        obj.image = row.image
        obj.isComment = row.isComment
        obj.isExternal = row.isExternal
        obj.isCorrect = row.isCorrect
        obj.percentage = []
        obj.postNumber = []
        return obj

    def add_post(self, row: PostBasedRow):
        """Add a post record into the image row record if they're inside the same image."""

        if self.image != row.image:
            return

        self.isCorrect = self.isCorrect and row.isCorrect
        self.percentage.append(row.percentage)
        self.postNumber.append(row.postNumber)

    def borders_in_pixel(self, imageHeight: int) -> "list[int]":
        """Convert the borders in percentages into a list of pixels."""

        accumulatedPercentage = list(
            accumulate(self.percentage, initial=config.INVISIBLE_HEIGHT)
        )[1:-1]
        # [1:-1] => drop the INVISIBLE_HEIGHT

        def get_pixel(percentage: float, imageHeight: int):
            return round(percentage * imageHeight)

        return [
            get_pixel(percentage, imageHeight) for percentage in accumulatedPercentage
        ]

    def as_dict(self):
        """Return a dictionary that can represent a row of this image in csv.DictWriter."""

        border = self.borders_in_pixel(IMAGE_NAME_TO_DIMENSION[self.image].height)

        return {
            "image": self.image,
            "isComment": int(self.isComment),
            "isExternal": int(self.isExternal),
            "isCorrect": int(self.isCorrect),
            "border": "_".join(map(str, border)),
            "postNumber": "_".join(map(str, self.postNumber)),
        }
