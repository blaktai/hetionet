import csv

def read_text(file, delimiter=',', skip_header=False):
    text_file = csv.DictReader(file, delimiter=delimiter)
    result = []
    for row in text_file:
        result.append(row)
    return result       
