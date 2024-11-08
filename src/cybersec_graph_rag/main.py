from cybersec_graph_rag.data_fetcher import fetch_nvd_data, parse_nvd_data
from cybersec_graph_rag.graph_builder import build_graph
from cybersec_graph_rag.query_interface import query_graph

def main():
    print("Fetching NVD Data...")
    nvd_data = fetch_nvd_data()
    entities, relations = parse_nvd_data(nvd_data)

    graph = build_graph(entities, relations)

    while True:
        query = input("Enter your query (or type 'exit' to quit):")
        if query.lower() == 'exit':
            break

        results = query_graph(graph.graph_id, query)
        print("Results: ", results)

if __name__ == "__main__":
    main()