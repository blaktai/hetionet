import pandas as pd

def fileReader(fileName):
    return pd.read_csv(fileName, sep = "\t")