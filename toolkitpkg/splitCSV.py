from typing import Dict, List
from csvOperations import read_csv, write_csv

'''
all-data-corrected.csv 
first_inference...

external.csv (actual, predict)
comment.csv (actual, predict)
border.csv (actual, predict)
'''

def extract_field(corrected: List[Dict[str, str]], inference: List[Dict[str, str]], truthField: str, predictField: str) -> List[dict]:
    imageToFields = {}

    for data in corrected:
        imageToFields[data['image']] = {
            'image': data['image'],
            'actual': data[truthField]
        }
 
    for data in inference:
        imageToFields[data['img']].update({
            'predict': data[predictField]
        })

    return list(imageToFields.values())


def main():
    correctedData = read_csv('./testing-data/all-data-corrected.csv')
    firstInference = read_csv('./testing-data/first_inference_official2.csv')

    commentData = extract_field(correctedData, firstInference, truthField='isComment', predictField='comment')
    externalData = extract_field(correctedData, firstInference, truthField='isExternal', predictField='external')
    borderData = extract_field(correctedData, firstInference, truthField='border', predictField='edge')

    write_csv('comment.csv', fields=commentData[0].keys(), data=commentData)
    write_csv('external.csv', fields=externalData[0].keys(), data=externalData)
    write_csv('border.csv', fields=borderData[0].keys(), data=borderData)


if __name__ == "__main__":
    main()
