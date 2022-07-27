from dataclasses import dataclass
import csv
import re

import pandas as pd


@dataclass
class Row:    
    image: str
    fb_external_1: str
    fb_external_2: str
    fb_external_3: str
    fb_external_4: str
    fb_external_5: str
    fb_comment_1: str
    fb_comment_2: str
    fb_home: str
    fb_post: str
    fb_post_top_y: str


class DetectionResultParser:
    FIELDS = ['image', 'fb_external_1', 'fb_external_2', 'fb_external_3', 'fb_external_4', 'fb_external_5', 'fb_comment_1', 'fb_comment_2', 'fb_home', 'fb_post', 'fb_post_top_y']
    
    def __init__(self, inputFile: str):
        self.dicts = DetectionResultParser.to_dicts(inputFile)

    @staticmethod
    def to_dicts(filename: str) -> list[dict]:
        dicts = []

        with open(filename, 'r') as file:
            for line in file:
                arr = line.split(':')
                
                if (field := arr[0]) == 'Enter Image Path':
                    image = arr[1].strip()
                    dicts.append({ **dict.fromkeys(DetectionResultParser.FIELDS, ''), 'image': image })
                elif field == 'fb_post':
                    d = dicts[-1]
                    x = arr[1].split('%')
                    
                    if d[field] != '':
                        d['fb_post'] += ','
                        d['fb_post_top_y'] += ','

                    d['fb_post'] += x[0].strip()

                    start, end = re.search(r'top_y:\s*\d+', line).span()
                    d['fb_post_top_y'] += line[start:end].split()[1]
                elif field in DetectionResultParser.FIELDS:
                    if d[field] != '':
                        continue

                    d = dicts[-1]
                    x = arr[1].split('%')
                    d[field] += x[0]

        return dicts

    def to_csv(self, output: str) -> None:
        with open(output, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(self.dicts)


    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame([Row(**d) for d in self.dicts])


if __name__ == "__main__":
    parser = DetectionResultParser(inputFile='result_example.txt')

    # getting a pandas.DataFreame object
    df = parser.to_df()

    # or, alternatively, output to a .csv file
    parser.to_csv(ouptut='result_example.csv')
