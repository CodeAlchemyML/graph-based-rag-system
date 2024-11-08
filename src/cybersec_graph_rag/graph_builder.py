import networkx as nx
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cybersecurity']
collection = db['graph_data']

def build_graph(entities, relations):
    graph = nx.Graph()

    for entity in entities:
        graph.add_node(entity['name'], type=entity['type'], description=entity.get('description', ''))
    
    for relation in relations:
        graph.add_edge(relation['source'], relation['target'], type=relation['type'])
    
    collection.insert_one(nx.node_link_data(graph))
    print("Graph data saved to MongoDB with ID:", graph.find_one()['_id'])

    return graph