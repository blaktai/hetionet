import csv
import os 
import re 
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

def load(filename, delimiter = '\t'):
    return pd.read_csv(filename, delimiter=delimiter)

def clean_up(node_df, edge_df, edge_types, cols = ['Anatomy', 'Compound', 'Disease', 'Gene']):
    node_df = clean_up_nodes(node_df, cols)
    edge_df = clean_up_edges(edge_df, cols, edge_types)
    node_cols = node_df.columns
    edge_cols = edge_df.columns
    df = edge_df.merge(node_df, how='inner', left_on='source', right_on='id')
    edge_df = df[edge_cols]
    return df, node_df, edge_df

def clean_up_edges(edge_df, cols, edge_types):
    regex = re.compile('(.+)::.+')
    edge_cols = edge_df.columns
    edge_df['target_kind'] = edge_df.target.str.replace(regex, r'\1')
    f = (edge_df.target_kind.isin(cols) & edge_df.metaedge.isin(edge_types))
    subset_edges_df = edge_df[edge_df.target_kind.isin(cols)]
    subset_edges_df = subset_edges_df[subset_edges_df.metaedge.isin(edge_types)]
    return subset_edges_df[edge_cols]

def clean_up_nodes(node_df, cols):
    return node_df[node_df.kind.isin(cols)]

def load_dataframes(node_file_path, edge_file_path, delimiter='\t',
    edge_types = ['AuG', 'AdG', 'CrC', 'CtD', 'CpD', 'CuG', 'CdG', 'DrD', 'DlA'],
    node_types = ['Anatomy', 'Compound', 'Disease', 'Gene']):
    nodes_df = load(node_file_path, delimiter=delimiter)
    edges_df = load(edge_file_path, delimiter=delimiter)
    return clean_up(nodes_df, edges_df, edge_types, node_types)