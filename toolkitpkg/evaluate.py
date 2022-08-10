from typing import Dict, List
import csv

from attr import define, field, asdict
from attr.converters import to_bool

INVISIBLE_PERCENTAGE = 0.13

@define
class PostBasedRow:
    image: str
    percentage: float = field(converter=float)
    postNumber: int = field(converter=int)
    isComment: bool = field(converter=to_bool)
    isExternal: bool = field(converter=to_bool)
    isCorrect: bool = field(converter=lambda x: not to_bool(x))

@define
class ImageBasedRow:
    image: str
    isComment: bool
    isExternal: bool
    isCorrect: bool
    percentage: List[float] = field(converter=lambda x: [x])
    postNumber: List[int] = field(converter=lambda x: [x])

    def addPost(self, row: PostBasedRow):
        self.isCorrect = self.isCorrect and row.isCorrect
        self.percentage.append(row.percentage)
        self.postNumber.append(row.postNumber)


def main():
    imageToRow: Dict[str, ImageBasedRow] = {}

    with open('testing-data/test-1.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for csvdata in reader:
            postRow = PostBasedRow(
                image=csvdata['images'],
                percentage=csvdata['percent'],
                postNumber=csvdata['code_id'],
                isComment=csvdata['comment'],
                isExternal=csvdata['outer_link'],
                isCorrect=csvdata['correct'],
            )

            if (imageRow := imageToRow.get(postRow.image)) is not None:
                imageRow.addPost(postRow) 
            else:
                imageToRow[postRow.image] = ImageBasedRow(**asdict(postRow))

    print(len(imageToRow))

if __name__ == '__main__':
    main()
