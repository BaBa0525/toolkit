import re
import pandas as pd
from dataclasses import dataclass

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


def todf(filename: str) -> pd.DataFrame:
    '''
    Returns a pandas DataFrame object from the input file
    '''

    fields = ['image', 'fb_external_1', 'fb_external_2', 'fb_external_3', 'fb_external_4', 'fb_external_5', 'fb_comment_1', 'fb_comment_2', 'fb_home', 'fb_post', 'fb_post_top_y']
    csv_dicts = []

    with open(filename, 'r') as f:
        for line in f:
            arr = line.split(':')

            if line.startswith('Enter Image Path'):
                filename = arr[1].strip()
                csv_dicts.append({**dict.fromkeys(fields, 0), 'image': filename})
            
            if (field := arr[0]) == 'fb_post':
                d = csv_dicts[-1]
                x = arr[1].split('%')
                if d['fb_post'] != 0:
                    d['fb_post'] += ',' 
                    d['fb_post_top_y']  += ','
                else: 
                    d['fb_post'] = '' 
                    d['fb_post_top_y']  = ''
                d['fb_post'] += x[0].strip()
                match = re.search(r'top_y:\s*\d+', line)
                s, e = match.span()
                d['fb_post_top_y'] += line[s:e].split()[1]
                
            elif field in fields:
                d = csv_dicts[-1]
                x = arr[1].split('%')
                if d[field] != 0:
                    d[field] += ',' 
                else:
                    d[field] = ''
                d[field] += x[0]

    return pd.DataFrame([Row(*d.values()) for d in csv_dicts])

if __name__ == '__main__':
    df = todf('result_example.txt')