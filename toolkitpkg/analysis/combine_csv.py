from typing import Dict, List

from ..csvops import read_csv, write_csv

idStringToNewNumber = {}

def reassignPostNumber(data: List[Dict[str, str]], id: int) -> List[dict]:
    newList = []

    for d in data:
        # 1_2 => ['1', '2']
        postNumbers = d['postNumber'].split('_')
        newPostNumbers = []

        for number in postNumbers:
            idString = f'{id}-{number}'
            # '1-1' '1-2'
            
            if (newNumber := idStringToNewNumber.get(idString)) is not None:
                newPostNumbers.append(newNumber)
                continue

            newNumber = len(idStringToNewNumber) + 1
            idStringToNewNumber[idString] = newNumber
            newPostNumbers.append(newNumber)

        newList.append({
            **d,
            'postNumber': '_'.join(map(str, newPostNumbers))
        })

    return newList


def main():
    test1Data = read_csv('./testing-data/test-1-corrected.csv')
    test2Data = read_csv('./testing-data/test-2-corrected.csv')

    allData = reassignPostNumber(test1Data, 1) + reassignPostNumber(test2Data, 2)

    print(idStringToNewNumber)

    write_csv('./testing-data/all-data-corrected.csv', fields=allData[0].keys(), data=allData)


if __name__ == '__main__':
    main()