"Ollama functions"

import json
from typing import Literal
import aiohttp

LlmModels = Literal["llm_terms", "llm_assistant"]


async def ollama_simple_chat(url: str, message: str, model: LlmModels, messages: list[dict] = []) -> str:
    "Send a simple text message to the LLM and get text response"
    url += "/api/chat"
    messages.append(
        {
            "role": "user",
            "content": message
        }
    )
    body = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    json_body = json.dumps(body)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json_body,
                                headers={"Content-Type": "application/json"}) as response:
            if response.status == 200:
                res_json = await response.json()
                return res_json["message"]["content"]
            else:
                raise ConnectionError(
                    f"ERROR connecting with ollama\n{response.text}")


async def ollama_get_terms(url: str, message: str) -> list[str]:
    context = [
        {
            "role": "system",
            "content": "Tú eres un asistente programado para extraer términos específicos de un texto dado. Te preguntarán tanto en Español como en inglés Tu tarea es identificar términos clave relacionados con el enunciado y listarlos separados por comas, como en este ejemplo: \"user: Me duele mucho la cabeza.\nassistant: dolor, cabeza\". Sin explicaciones, interpretaciones, ni información suplementaria. Solo listar los términos como se solicitan."
        },
        {
            "role": "user",
            "content": "Yesterday, I started feeling a sore throat and a fever. This morning, my symptoms included a runny nose and a cough."
        },
        {
            "role": "assistant",
            "content": "sore-throat, fever, runny-nose, cough"
        },
        {
            "role": "user",
            "content": "Ayer, empecé a sentir dolor de garganta y fiebre. Esta mañana, mis síntomas incluían secreción nasal y tos."
        },
        {
            "role": "assistant",
            "content": "dolor-de-garganta, fiebre, secreción-nasal, tos"
        },
        {
            "role": "user",
            "content": "Yesterday, I started feeling a sore throat and a fever. This morning, my symptoms included a runny nose and a cough."
        }
    ]
    str_term_list = await ollama_simple_chat(url, message, "llm_terms", messages=context)
    str_term_list = str_term_list.lower()
    str_term_list = str_term_list.replace(" ", "")
    term_list: list[str] = str_term_list.split(",")
    return term_list


async def ollama_get_conclusion(url: str, message: str, docs: list[dict[str, any]]) -> str:
    conclusion_msg = f"""From these options : {json.dumps(docs)}
    Which of them is the best for this situation: {message}"""
    conclusion = await ollama_simple_chat(url, conclusion_msg, "llm_assistant")
    return conclusion
