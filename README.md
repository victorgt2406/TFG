# (TFG) Aplicaciones de los Motores de Búsqueda con los LLMs
Realizado por *Víctor Gutiérrez Tovar*

Curso 2023/2024

# Arquitectura
## Contenedores
- Opensearch
- Middleware (Python con fastAPI)
- Ollama

# Variables del entorno `.env`
Sera necesario crear un archivo .env con la configuración del entorno
```bash
OS_HOST=opensearch-node
OPENSEARCH_INITIAL_ADMIN_PASSWORD=opensearchPsw1

MDW_PORT=3000

OLLAMA_PORT=11434
OLLAMA_HOST=ollama-node
```