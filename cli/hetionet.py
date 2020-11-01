import pprint

import click 
from utils.reader import read_text
from utils.graph_parser import parse_nodes, build_subgraphs    
from db.neo4j.hetionet_pandas import create_hetionet

@click.command()
@click.argument("node_file_path", type=click.Path(exists=True), required=True)
@click.argument('edge_file_path', type=click.Path(exists=True), required=True)
@click.option("--delimiter", default="\t", help="Delimiter of file format")
# @click.parameter()
def cli(node_file_path, edge_file_path, delimiter):
    """This script prints the sub graphs of a hetionet.
    \b
    Print hetionet sub graphs to stdout:
        hetionet nodes.tsv edges.tsv
    """
    print(node_file_path, edge_file_path, delimiter)
    create_hetionet(node_file_path, edge_file_path, delimiter)
