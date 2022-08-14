import csv
from typing import List

def read_csv(filename: str):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    return data

def read_csv_as_dict(filename: str, key: str) -> dict:
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        result = { row[key]: row for row in reader }
    
    return result

def write_csv(filename: str, fields: List[str], data: List[dict]):
    with open(filename, mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
