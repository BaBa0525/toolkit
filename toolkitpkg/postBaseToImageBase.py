from itertools import accumulate
from typing import Dict, List
import csv

from attr import define, field, asdict
from attr.converters import to_bool

INVISIBLE_PERCENTAGE = 0.13

@define
class Dimension:
    width: int = field(converter=int)
    height: int = field(converter=int)

with open('./testing-data/first_inference_official2 - first_inference_official2.csv', mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    imageToSize = { row['img']: Dimension(row['width'], row['height']) for row in reader }


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

    @staticmethod
    def keys():
        return [
            'image', 
            'isComment', 
            'isExternal',
            'isCorrect',
            'border', 
            'postNumber',
        ]
    
    def bordersInPixel(self, imageHeight: int) -> List[int]:
        # the reason to put [1:] is to drop the INVISIBLE_PERCENTAGE
        accumulatedPercentage = list(accumulate(self.percentage, initial=INVISIBLE_PERCENTAGE))[1:]

        def getPixel(percentage: float, imageHeight: int):
            return round(percentage * imageHeight)
        
        return [getPixel(percentage, imageHeight) for percentage in accumulatedPercentage]

    def asDict(self):
        border = self.bordersInPixel(imageToSize[self.image].height)

        return {
            'image': self.image,
            'isComment': int(self.isComment),
            'isExternal': int(self.isExternal),
            'isCorrect': int(self.isCorrect),
            'border': '_'.join(map(str, border)), 
            'postNumber': '_'.join(map(str, self.postNumber)), 
        }


def readCSVToDict(filename: str) -> Dict[str, ImageBasedRow]:
    imageToRow: Dict[str, ImageBasedRow] = {}
    
    with open(filename, mode='r') as csvfile:
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
    
    return imageToRow

def main():
    imageToRow = readCSVToDict('./testing-data/test-1.csv')
    imageToRow.update(readCSVToDict('./testing-data/test-2.csv'))

    with open('./testing-data/all-data.csv', mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ImageBasedRow.keys())
        writer.writeheader()
        writer.writerows(row.asDict() for row in imageToRow.values())

if __name__ == '__main__':
    main()
