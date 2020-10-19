def parse_nodes(node_list):
    result = {}
    for node in node_list:
        result[node['id']] = node
    return result

def build_subgraphs(nodes, edges):
    diseases, genes, compounds, anatomies = {}, {}, {}, {}

    for edge in edges:
        source_node =  edge.get('source')
        node = nodes[source_node]
        if node.get('kind') == 'Disease':
            add_disease(node, diseases, edge)
        elif node.get('kind') == 'Gene':
            add_gene(node, genes, edge)
        elif node.get('kind') == 'Compound':
            add_compound(node, compounds, edge)
        elif node.get('kind') == 'Anatomy':
            add_anatomy(node, anatomies, edge)
        else:
            pass
    return diseases, genes, compounds, anatomies

def add_to_graph(node, graph, edge):
    id = node.get('id')
    graph_node = graph.get(id)
    if graph_node is not None:
        if graph_node.get('edges') is None:
            graph_node['edges'] = [edge]
        else:
            graph_node['edges'].append(edge)
    else:
        node['edges'] = [edge]
        graph[id] = node

def add_disease(disease, disease_graph, edge):
    add_to_graph(disease, disease_graph, edge)


def add_gene(gene, gene_graph, edge):
    add_to_graph(gene, gene_graph, edge)

def add_compound(compound, compound_graph, edge):
    add_to_graph(compound, compound_graph, edge)

def add_anatomy(anatomy, anatomy_graph, edge):
    add_to_graph(anatomy, anatomy_graph, edge)
