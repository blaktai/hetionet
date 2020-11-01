from utils.reader import read_files
from utils.dictionary import create_dictionary

import redis
import pandas as pd
import numpy as np 

import warnings
warnings.filterwarnings('ignore')

def create_redis_store(node_file_path, edge_file_path):
    # Creates edges and nodes dataframes from tsv files
    edges = read_files(edge_file_path, "edges")
    nodes = read_files(node_file_path, "nodes")

    # Create id:name dictionaries 
    disease_dictionary = create_dictionary(nodes, 'Disease')
    gene_dictionary = create_dictionary(nodes, 'Gene')
    compound_dictionary = create_dictionary(nodes, 'Compound')
    anatomy_dictionary = create_dictionary(nodes, 'Anatomy')

    # Create disease to gene dataframe
    disease_to_gene = edges.loc[(edges['source'].str.contains("Disease")) & (edges['target'].str.contains("Gene"))]
    disease_to_gene = disease_to_gene.replace({'target':gene_dictionary})
    disease_to_gene = disease_to_gene.rename(columns={'source':'disease_id', 'target':'gene'})

    # Create disease to anatomy dataframe
    disease_to_anatomy = edges.loc[(edges['source'].str.contains("Disease")) & (edges['target'].str.contains("Anatomy"))]
    disease_to_anatomy = disease_to_anatomy.replace({'target':anatomy_dictionary})
    disease_to_anatomy = disease_to_anatomy.rename(columns={'source':'disease_id', 'target':'anatomy'})

    # Create gene to compound dataframe 
    gene_to_compound = edges.loc[(edges['source'].str.contains("Compound")) & (edges['target'].str.contains("Gene"))]
    gene_to_compound = gene_to_compound.replace({'source':compound_dictionary})
    gene_to_compound = gene_to_compound.replace({'target':gene_dictionary})
    gene_to_compound = gene_to_compound.rename(columns={'source':'compound', 'target':'gene'})

    # Match disease to compound using gene to compound dataframe
    dgc = pd.merge(disease_to_gene, gene_to_compound, on='gene')
    dgca = pd.merge(dgc, disease_to_anatomy, on='disease_id')

    # Create disease name column using disease_dictionary
    dgca['disease'] = dgca['disease_id'].map(disease_dictionary).fillna(np.nan)

    # Group columns by disease_id and remove duplicates
    dgca = dgca.groupby(['disease_id']).agg(lambda x: ','.join(x.unique()))

    # Reorder dataframe keys
    dgca = dgca[['disease', 'compound', 'gene', 'anatomy']]

    # Convert dgca dataframe to dictionary
    dgca = dgca.transpose()
    dgca = dgca.to_dict()

    # Start Redis
    r = redis.Redis()

    # Parse dictionary keys and values and add to Redis database
    for key in dgca.keys():
        r.mset({str(key): str(dgca[key])})


def find_disease(disease_id):
    r = redis.Redis()
    return r.get(disease_id)
