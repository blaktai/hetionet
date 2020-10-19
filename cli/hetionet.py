import pprint

import click 
from utils.reader import read_text
from utils.graph_parser import parse_nodes, build_subgraphs    

@click.command()
@click.argument("node_file", type=click.File("r"))
@click.argument('edge_file', type=click.File("r"))
def cli(node_file, edge_file):
    """This script prints the sub graphs of a hetionet.
    \b
    Print hetionet sub graphs to stdout:
        hetionet nodes.tsv edges.tsv
    """
    node_list = read_text(node_file, delimiter='\t', skip_header=True)
    nodes = parse_nodes(node_list)
    edges = read_text(edge_file, delimiter='\t', skip_header=True)
    for graph in build_subgraphs(nodes, edges):
        pprint.pprint(graph)
