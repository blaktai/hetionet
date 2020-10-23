import csv
import os 

def read_text(file, delimiter=',', skip_header=False):
    text_file = csv.DictReader(file, delimiter=delimiter)
    result = []
    for row in text_file:
        result.append(row)
    return result       

def read_text_from_disk(filename, delimiter, skip_header):
    path = os.path.join("./data")
    data_dir = os.path.normpath(path)
    file_path = f"{data_dir}/{filename}"
    node_list = []
    with open(file_path, 'r') as file:
        node_list = read_text(file, delimiter='\t', skip_header=True)
    return node_list