import numpy as np

class dataCleaner:

    def removeListDuplicates(df, column_name):
        l = []
        for i in range(len(df[column_name])):
            l.append(list(dict.fromkeys(df[column_name][i])))

    def replaceValues(df, column_name, dict):
        return df.replace({column_name:dict})

    def nodeDict(nodes):
        del nodes['kind']
        return nodes.set_index('id').to_dict()['name']

    def replaceColumn(edges, column_name, contains_string, compare):
        modified_edges = dataCleaner.modifyEdges(edges, column_name, contains_string, compare)
        l = []
        for i in range(len(modified_edges[column_name])):
            if(modified_edges[column_name][i]):
                l.append(modified_edges[compare][i])
            else:
                l.append(np.nan)
        return l

    def modifyEdges(edges, column_name, contains_string, compare):
        new_edges = edges
        new_edges[column_name] = new_edges[compare].str.contains(contains_string)
        return new_edges

    def createGuideDataFrame(edges):
        new_edges = edges
        new_edges['gene'] = dataCleaner.replaceColumn(new_edges, "gene", "Gene", "target")
        new_edges = new_edges[new_edges['gene'] != np.nan]
        return new_edges

    def createBaseDataFrame(edges, nodes): 
        did_to_gid = nodes.join(edges.set_index('source'), on='id')
        did_to_gid = did_to_gid[did_to_gid['kind']=='Disease']
        did_to_gid = did_to_gid.rename(columns={"id": "disease_id", "name": "disease_name", "target":"gene_id"})
        return did_to_gid[['disease_id','disease_name','gene_id']]
