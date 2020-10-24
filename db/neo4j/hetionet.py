from py2neo import Node, Relationship, Graph, Subgraph
from pprint import pprint
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

def store_graph(compounds, diseases, anatomies, genes):
    context = {RELATIONSHIPS_KEY: []}
    process_nodes(context, genes, process_gene)
    process_nodes(context, anatomies, process_anatomy)
    process_nodes(context, diseases, process_disease)
    process_nodes(context, compounds, process_compound)
    graph = Subgraph(relationships = context.get(RELATIONSHIPS_KEY))
    print(graph.labels)
    repr(graph.nodes)
    print(.nodes)

def process_nodes(context, nodes, process_node):
    return [process_node(context, node) for _, node in nodes.items()]

def process_edges(node, edges, create_relationship):
    return [create_relationship(node, edge) for edge in edges]

def store_compounds(compounds):
    process_nodes(compounds, process_compound)


def process_node(context, node, node_type, edge_processor):
    node_id, node_name, edges = node.get('id'), node.get('name'), node.get('edges')
    new_node = Node(node_type, name=node_name, id=node_id)
    context[node_id] = new_node
    process_edges(new_node, edges, edge_processor)

def process_anatomy(context, anatomy):
    def create_anatomy_relationship(anatomy_node, edge):
        edge_type = edge.get('metaedge')
        target_node = context.get(edge.get('target'))
        if edge_type == 'AuG':
            context.get(RELATIONSHIPS_KEY).append(UPREGULATES_REL(anatomy, target_node))
        elif edge_type == 'AdG':
            context.get(RELATIONSHIPS_KEY).append(DOWNREGULATES_REL(anatomy, target_node))
        # elif edge_type == '': 
        
        # elif edge_type == ''
    process_node(context, anatomy, ANATOMY, create_anatomy_relationship)

def process_compound(context, compound):

    def create_compound_relationship(compound, edge):
        edge_type = edge.get('metaedge')
        target_node = context.get(edge.get('target'))
        if edge_type == 'CrC':
            context.get(RELATIONSHIPS_KEY).append(RESEMBLES_REL(compound, target_node))
        elif edge_type == 'CtD':
            context.get(RELATIONSHIPS_KEY).append(TREATS_REL(compound, target_node))
        elif edge_type == 'CpD': 
            context.get(RELATIONSHIPS_KEY).append(PALLIATES_REL(compound, target_node))
        elif edge_type == 'CuG':
            context.get(RELATIONSHIPS_KEY).append(UPREGULATES_REL(compound, target_node))
        elif edge_type == 'CdG':
            context.get(RELATIONSHIPS_KEY).append(DOWNREGULATES_REL(compound, target_node))

    process_node (context, compound, COMPOUND, create_compound_relationship)

def process_disease(context, disease):
    def create_disease_relationship(disease, edge):
        edge_type = edge.get('metaedge')
        target_node = context.get(edge.get('target'))
        if edge_type == 'DrD':
            context.get(RELATIONSHIPS_KEY).append(RESEMBLES_REL(disease, target_node))
        elif edge_type == 'DlA':
            context.get(RELATIONSHIPS_KEY).append(LOCALIZES_REL(disease, target_node))
        # elif edge_type == '': 
        
        # elif edge_type == ''

    process_node(context, disease, DISEASE, create_disease_relationship)


def process_gene(context, gene):
    def create_gene_relationship(gene, edge):
        pass
    #     edge_type = edge.get('metaedge')
    #     if edge_type == '':
        
    #     elif edge_type == '':

    #     elif edge_type == '': 
        
    #     elif edge_type == ''
    process_node(context, gene, GENE, create_gene_relationship)
