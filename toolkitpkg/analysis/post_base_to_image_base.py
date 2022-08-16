from itertools import accumulate
import csv

from attr import define, field, asdict
from attr.converters import to_bool

from . import constants
from ..csvops import read_csv

@define
class Dimension:
    width: int = field(converter=int)
    height: int = field(converter=int)

with open('./testing-data/first_inference_official2.csv', mode='r') as csvfile:
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
    percentage: 'list[float]' = field(converter=lambda x: [x])
    postNumber: 'list[int]' = field(converter=lambda x: [x])

    def add_post(self, row: PostBasedRow):
        self.isCorrect = self.isCorrect and row.isCorrect
        self.percentage.append(row.percentage)
        self.postNumber.append(row.postNumber)

    @staticmethod
    def keys():
        return ['image', 'isComment', 'isExternal','isCorrect','border', 'postNumber']
    
    def borders_in_pixel(self, imageHeight: int) -> 'list[int]':
        # put [1:-1] to drop the INVISIBLE_HEIGHT
        accumulatedPercentage = list(accumulate(self.percentage, initial=constants.INVISIBLE_HEIGHT))[1:-1]

        def get_pixel(percentage: float, imageHeight: int):
            return round(percentage * imageHeight)
        
        return [get_pixel(percentage, imageHeight) for percentage in accumulatedPercentage]

    def as_dict(self):
        border = self.borders_in_pixel(imageToSize[self.image].height)

        return {
            'image': self.image,
            'isComment': int(self.isComment),
            'isExternal': int(self.isExternal),
            'isCorrect': int(self.isCorrect),
            'border': '_'.join(map(str, border)), 
            'postNumber': '_'.join(map(str, self.postNumber)), 
        }


def read_csv_to_dict(filename: str) -> 'dict[str, ImageBasedRow]':
    imageToRow: 'dict[str, ImageBasedRow]' = {}

    data = read_csv(filename)

    for d in data:
        post = PostBasedRow(
            image=d['images'],
            percentage=d['percent'],
            postNumber=d['code_id'],
            isComment=d['comment'],
            isExternal=d['outer_link'],
            isCorrect=d['correct']
        )

        if (imageRow := imageToRow.get(post.image)) is not None:
            imageRow.add_post(post)
        else:
            imageToRow[post.image] = ImageBasedRow(**asdict(post))
    
    return imageToRow