from pymongo import MongoClient
import networkx as nx
import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

client = MongoClient('mongodb://localhost:27017/')
db = client['cybersecurity']
collection = db['graph_data']

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key, model = "gpt-3.5-turbo")

def parse_response_to_graph_command(response):
    if "port" in response:
        return {"type": "ports"}
    
    elif "outdated" in response:
        return {"type": "outdated_services"}
    
    elif "vulnerabilities" in response:
        return {"type": "vulnerabilities"}
    
    elif "common services" in response:
        return {"type": "common_services"}
    
    elif "login forms" in response:
        return {"type": "login_forms"}
    
    return {}

def execute_graph_query(graph, structured_query):
    if structured_query["type"] == "ports":
        return [node for node, attr in graph.nodes(data=True) if attr.get("type") == "Port"]
    
    elif structured_query["type"] == "outdated_services":
        return [node for node, attr in graph.nodes(data=True) if attr.get("status") == "outdated"]

    elif structured_query["type"] == "vulnerabilities":
        return [node for node, attr in graph.nodes(data=True) if attr.get("type") == "Vulnerability"]

    elif structured_query["type"] == "common_services":
        target1_services = set(node for node, attr in graph.nodes(data=True) if attr.get("target") == "target1.com" and attr.get("type") == "Service")
        target2_services = set(node for node, attr in graph.nodes(data=True) if attr.get("target") == "target2.com" and attr.get("type") == "Service")
        return list(target1_services.intersection(target2_services))
    
    elif structured_query["type"] == "login_forms":
        return [node for node, attr in graph.nodes(data=True) if attr.get("type") == "LoginForm"]
    
    return "No relevant data found"

def query_graph(graph_id, query):
    graph_data = collection.find_one({"_id": graph_id})
    if not graph_data:
        raise ValueError("Graph not found.")

    graph = nx.node_link_graph(graph_data)

    prompt_template = """
    Given a network graph containing information on vulnerabilities, services, and ports, answer the following question in detail:
    Question: {query}
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["query"])
    chain = LLMChain(prompt=prompt, llm=llm)

    llm_response = chain.run(query=query)
    
    structured_query = parse_response_to_graph_command(llm_response)
    
    result = execute_graph_query(graph, structured_query)
    return result