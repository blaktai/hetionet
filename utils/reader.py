import csv
import os 

import pandas as pd
import numpy as np

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

def read_files(fileName, type):
    file = pd.read_csv(fileName, sep = "\t", error_bad_lines=False)
    if type == "nodes":
        file = filter_nodes(file)
    elif type == "edges":
        file = filter_edges(file)
    return file        

def filter_nodes(df):
    kinds = ["Disease", "Compound", "Gene", "Anatomy"] 
    df.kind.isin(kinds)
    return df

def filter_edges(df):
    del df['metaedge']
    df = df.dropna()
    return df