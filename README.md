# (TFG) The integration of a LLM with a Search Engine
By *Víctor Gutiérrez Tovar*

2023/2024

# Introduction
This is the last project of my journey studying for the bachelors degree of Software Engineering.

The main goal of this project is create a prototype tha can use the advantages of the Search Engines and the LLMs. To do so, the prototype will do a cicle to be able to get some data from the search engine from the original question, and using that specific data from the search engine answer that question.

# The cicle
This cicle can be explain in the next steps:
1. Get the message as the only input.
2. From that message process it with the llm and get the terms needed to make the search to the search engine
3. Get those terms and make the query to the search engine getting at the end the documents with the highest scoring.
4. From those docs and the original message the llm will answer based on the information added.

# Architecture
## Containers
- Search engine **OpenSearch**
- search engine dashboard **OpenSearch Dashboard**
- Middleware  **fastAPI**
- LLM **Ollama**

# Getting started
## Requirements
- A System with a Docker Engine installed.
## Set up:
1. Clone the repository
2. In the relative root where the repository was cloned execute:
```bash
docker compose up -d
```
3. Open a browser and paste this url: `http://localhost:2002`

# Variables del entorno `.env`
It will be required to declare a .env file, this is a example to getting started.
```bash
OS_HOST=opensearch-node
OS_PORT=9200
OPENSEARCH_INITIAL_ADMIN_PASSWORD=opensearchPsw1

MDW_PORT=2002

OLLAMA_PORT=11434
OLLAMA_HOST=ollama-node
```