import csv


def read_csv(filename: str) -> "list[dict[str]]":
    with open(filename, mode="r") as csvfile:
        rows = csv.DictReader(csvfile)
        data = list(rows)

    return data


def read_csv_as_dict(filename: str, keyAttr: str) -> "dict[str, dict[str]]":
    with open(filename, mode="r") as csvfile:
        rows = csv.DictReader(csvfile)
        data = {row[keyAttr]: row for row in rows}

    return data


def write_csv(filename: str, fields: "list[str]", data: "list[dict[str]]"):
    with open(filename, mode="w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
