# Graph-based Retrieval Augment Generation (RAG) System

---
**Project Overview:**

This project involves implementing a graph-based RAG system using Langgraph and Langchain for a cybersecurity use case. It builds a dynamic graph from cybersecurity data, which can answer specific penetration testing-related questions.

---
**Requirements:**

- Language: ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
- Dependency: ![Poetry](https://img.shields.io/badge/Package%20Manager-Poetry-blue?logo=poetry)
- API: ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
- Database: Chroma Vector Database, with ingestion support from ![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?logo=mongodb)

---
**Implementation:**

- *Graph Entity Design:* Defining entities (hosts, ports, services) and relationships dynamically based on the HackTheBox data and walkthroughs.
- *Data Ingestion:* Building an ingestion pipeline to handle irregular data updates.
- *Inference Pipeline:* Answering Cybersecurity-related queries using graph-based RAG with optimized response times.

---
**Usage:**

- Setup the Python environment with Poetry.
- Run the graph pipeline and ingestion process.
- Query the graph for penetration testing insights.
