import csv
import os
import sys
import re

def main():

    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} filename', file=sys.stderr)
        exit(-1)

    fields = ['image', 'fb_external_1', 'fb_external_2', 'fb_external_3', 'fb_external_4', 'fb_external_5', 'fb_comment_1', 'fb_comment_2', 'fb_home', 'fb_post', 'fb_post_top_y']
    csv_dicts = []

    with open(sys.argv[1], 'r') as f:
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

    file, _ = os.path.splitext(sys.argv[1])
    output = f'{file}.csv'
    print(output)
    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_dicts)
                

if __name__ == '__main__':
    main()