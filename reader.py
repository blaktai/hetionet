import pandas as pd
import numpy as np

def read_files(fileName, type):
    file = pd.read_csv(fileName, sep = "\t")
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
