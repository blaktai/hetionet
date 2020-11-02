import click 

from db.neo4j.neo4j import create_hetionet, find_disease_treatments
from db.redis.redis import create_redis_store, find_disease

@click.group()
def cli():
    pass

@cli.command()
@click.argument("node_file_path", type=click.Path(exists=True), required=True)
@click.argument('edge_file_path', type=click.Path(exists=True), required=True)
@click.option("--delimiter", default="\t", help="Delimiter of file format")
def store(node_file_path, edge_file_path, delimiter):
    create_redis_store(node_file_path, edge_file_path)
    create_hetionet(node_file_path, edge_file_path, delimiter)    
    
@cli.command()
@click.option('-t', "query_type", type=click.Choice(['disease', 'treatment'], case_sensitive=False))
@click.argument("disease_arg", required=True)
def find(query_type, disease_arg):
    if query_type == 'disease':
        print(find_disease(disease_arg))
    else:
        print(find_disease_treatments(disease_arg))
        