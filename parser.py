import numpy as np
import warnings
warnings.filterwarnings('ignore')

from data_cleaner import dataCleaner
from reader import fileReader

def parseTsv(edges, nodes):
    edges = fileReader(edges)
    nodes = fileReader(nodes)

    base_df = dataCleaner.createBaseDataFrame(edges, nodes)

    new_edges = dataCleaner.createGuideDataFrame(edges)
    new_edges["disease"] = dataCleaner.replaceColumn(new_edges, "disease", "Disease", "source")
    new_edges["compound"] = dataCleaner.replaceColumn(new_edges, "compound", "Compound", "source")
    new_edges["anatomy"] = dataCleaner.replaceColumn(new_edges, "anatomy", "Anatomy", "source")

    copy_gid = new_edges
    gene_disease = copy_gid[['target','disease']]
    gene_compound = copy_gid[['target','compound']]
    gene_anatomy = copy_gid[['target','anatomy']]

    merged = gene_disease.join(gene_anatomy.set_index('target'), on='target')
    merged = merged.join(gene_compound.set_index('target'), on='target')
    merged = merged.join(base_df.set_index('gene_id'), on='target')
    merged = merged.drop_duplicates()
    merged = merged.dropna()

    findNames = dataCleaner.nodeDict(nodes)
    merged = merged.rename(columns={"target": "gene"})
    merged = dataCleaner.replaceValues(merged, "anatomy", findNames)
    merged = dataCleaner.replaceValues(merged, "compound", findNames)
    merged = dataCleaner.replaceValues(merged, "gene", findNames)
    del merged['disease']

    df = merged.groupby(['disease_id']).agg(lambda x: x.tolist())

    for i in range(len(df['disease_name'])):
        df['disease_name'][i] = list(dict.fromkeys(df['disease_name'][i]))
    for i in range(len(df['gene'])):
        df['gene'][i] = list(dict.fromkeys(df['gene'][i]))
    for i in range(len(df['anatomy'])):
        df['anatomy'][i] = list(dict.fromkeys(df['anatomy'][i]))
    for i in range(len(df['compound'])):
        df['compound'][i] = list(dict.fromkeys(df['compound'][i]))

    df = df[['disease_name', 'compound', 'gene', 'anatomy']]
    df = df.transpose()
    return df.to_dict()