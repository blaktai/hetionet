from pymongo import MongoClient
from utils.reader import load_dataframes


def create_hetionet(node_file_path, edge_file_path):
    network_df, _, _ = load_dataframes(node_file_path, edge_file_path)
    node_types = ['Anatomy', 'Compound', 'Disease', 'Gene']
    client = MongoClient()

def find_all_treatments():
    """
    Returns compound documents for all diseases where there is no treatment but possible treatments exists.
    """
    client = MongoClient()
    db = client.get_database(name="hetionet")
    return 

def find_disease_treatments(disease_name):
    """
    Returns compound documents for :param disease_name where there is no treatments but possible treatments exists. 

    :param disease_name: name of the disease which has possible new treatments.
    """
    client = MongoClient()
    db = client.get_database(name="hetionet")
    return 