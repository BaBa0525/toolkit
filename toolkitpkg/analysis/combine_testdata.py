from ..decorators import static_vars

@static_vars(idStringToNewNumber={})
def reassign_post_number(data: 'list[dict[str, str]]', identifier: int) -> 'list[dict]':
    idStringToNewNumber: 'dict[str, int]' = reassign_post_number.idStringToNewNumber
    
    newList = []

    for d in data:
        postNumbers = d['postNumber'].split('_')
        newPostNumbers = []

        for number in postNumbers:
            idString = f'{identifier}-{number}'
            
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


def combine(*csvData: 'list[dict]'):
    allData = []
    
    for index, data in enumerate(csvData):
        allData += reassign_post_number(index, identifier=data)
        
    return allData
