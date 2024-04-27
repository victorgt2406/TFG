import os
from ollama import AsyncClient as OllamaClient

class OllamaSingleton:
    "Ollama Singleton"
    _client = None

    @classmethod
    def get_url(cls):
        host = os.getenv("OLLAMA_HOST") or "ollama-node"
        port = int(os.getenv("OLLAMA_PORT") or 11434)

        return f"{host}:{port}"

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            cls._client = cls._create_client()
        return cls._client

    @staticmethod
    def _create_client():
        host = os.getenv("OLLAMA_HOST") or "ollama-node"
        port = int(os.getenv("OLLAMA_PORT") or 11434)

        return OllamaClient(host=f"{host}:{port}")

    @classmethod
    async def test_connection(cls):
        try:
            llm_list = await cls._client.list()
            if len(llm_list)>=0:
                print("✅ Connection to 🦙 Ollama successful")
        except Exception as e:
            print(f"❌ Not connected to 🦙 Ollama {e}")
ollama_client = OllamaSingleton.get_instance()
