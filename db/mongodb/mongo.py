from pymongo import MongoClient
from utils.reader import load_dataframes

CLIENT = MongoClient()


def load(filename, delimiter):
    return pd.read_csv(filename, delimiter=delimiter)

def create_hetionet(node_file_path, edge_file_path):
    network_df, _, _ = load_dataframes(node_file_path, edge_file_path)
    node_types = ['Anatomy', 'Compound', 'Disease', 'Gene']