import csv
from typing import List

def read_csv(filename: str):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    return data

def write_csv(filename: str, fields: List[str], data: List[dict]):
    with open(filename, mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)