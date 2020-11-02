import pandas as pd
import re
from py2neo import Node, Relationship, Graph, Subgraph
import logging
from utils.reader import load_dataframes

LOG = logging.Logger(__name__, level=logging.WARNING)

ANATOMY = 'ANATOMY'
DISEASE = 'DISEASE'
COMPOUND = 'COMPOUND'
GENE = 'GENE'
TREATS = 'TREATS'
RESEMBLES = 'RESEMBLES'
PALLIATES = 'PALLIATES'
UPREGULATES = 'UPREGULATES'
DOWNREGULATES = 'DOWNREGULATES'
LOCALIZES = 'LOCALIZES'
RELATIONSHIPS_KEY = 'RELATIONSHIPS'
RESEMBLES_REL = Relationship.type(RESEMBLES)
TREATS_REL = Relationship.type(TREATS)
PALLIATES_REL = Relationship.type(PALLIATES)
UPREGULATES_REL= Relationship.type(UPREGULATES)
DOWNREGULATES_REL = Relationship.type(DOWNREGULATES)
LOCALIZES_REL = Relationship.type(LOCALIZES)
PARTITION_SIZE = 5

def create_relationships(mappings, context, edge):
    source_id, target_id, edge_type = edge.get('source'), edge.get('target'), edge.get('metaedge')
    node_type = context.get('kind').get(source_id)
    nodes_map = context.get('node')
    source_node, target_node = nodes_map.get(source_id), nodes_map.get(target_id)
    relationship_func = mappings.get(node_type)
    return relationship_func(source_node, target_node, edge_type)

def create_anatomy_relationship(anatomy, target_node, edge_type):
        if edge_type == 'AuG':
            return UPREGULATES_REL(anatomy, target_node)
        elif edge_type == 'AdG':
            return DOWNREGULATES_REL(anatomy, target_node)

def create_compound_relationship(compound, target_node, edge_type):
    if edge_type == 'CrC':
        return RESEMBLES_REL(compound, target_node)
    elif edge_type == 'CtD':
        return TREATS_REL(compound, target_node)
    elif edge_type == 'CpD': 
        return PALLIATES_REL(compound, target_node)
    elif edge_type == 'CuG':
        return UPREGULATES_REL(compound, target_node)
    elif edge_type == 'CdG':
        return DOWNREGULATES_REL(compound, target_node)

def create_disease_relationship(disease, target_node, edge_type):
    if edge_type == 'DrD':
        return RESEMBLES_REL(disease, target_node)
    elif edge_type == 'DlA':
        return LOCALIZES_REL(disease, target_node)

def create_hetionet(node_filepath, edge_filepath, delimiter):
    """
    Create Neo4j Node and Relationship objects with the appropriate labels, names, and ids
    from file path to the underlying text files. 

    :param node_filepath: path to the hetionet nodes file
    :param edge_filepath: path to the hetionet edges file
    :param delimiter: The separator between fields of the file
    """
    _, nodes_df, edges_df = load_dataframes(node_filepath, edge_filepath)
    nodes_df['node'] = nodes_df.apply(lambda x: Node(x['kind'], name=x['name'], id=x['id']), axis=1)
    nodes_df = nodes_df.set_index('id')
    mappings = {'Disease': create_disease_relationship, 'Anatomy': create_anatomy_relationship, 'Compound': create_compound_relationship}
    context = nodes_df[['node', 'kind']].to_dict()
    

    edges_df['relationships'] = edges_df.apply(lambda x: create_relationships(mappings, context, x), axis=1)

    relationships = edges_df.relationships.unique().tolist()
    graph = Graph()
    num_relationships = len(relationships)
    batch_size = num_relationships // PARTITION_SIZE
    num_batches = PARTITION_SIZE if num_relationships // PARTITION_SIZE > 0 else 1
    for partition in range(num_batches):
        sub_relationship_graph = relationships[:partition * batch_size]
        if num_batches == partition + 1:
            sub_relationship_graph = relationships[batch_size * partition:]
        if len(sub_relationship_graph) > 0:
            relationships_graph = Subgraph(relationships=relationships)
            graph.create(relationships_graph)

def find_all_treatments():
    """
    Returns compound nodes for all disease where there is no treatment but possible treatments exists.
    """

    cypher_query = """ MATCH (:Disease)-[:LOCALIZES]-(:Anatomy)-[:UPREGULATES|DOWNREGULATES]-(g:Gene)
                       OPTIONAL MATCH (c)-[:RESEMBLES]-(c2:Compound)
                       WHERE NOT EXISTS((c)--(:Disease)) AND ((c)--(g) OR (c2)--(g))
                       RETURN distinct c  
                   """
    graph = Graph()
    return graph.run(cypher_query)

def find_disease_treatments(disease_name):
    """
    Returns compound nodes for :param disease_name where there is no treatments but possible treatments exists. 

    :param disease_name: name of the disease which has possible new treatments.
    """
    cypher_query = f"""MATCH (d:Disease{{name: '{disease_name}'}})-[:LOCALIZES]->(:Anatomy)-[:UPREGULATES|DOWNREGULATES]->(g:Gene)<-[:UPREGULATES|DOWNREGULATES]-(c:Compound)
                       MATCH (c2:Compound)-[:RESEMBLES]->(c3:Compound)
                       WHERE NOT EXISTS((c2)--(d)) AND (c = c2 OR c = c3)
                       RETURN distinct c  
                    """
    graph = Graph()
    return graph.run(cypher_query).data()

    