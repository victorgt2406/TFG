"Ollama functions"

import json
import aiohttp


async def ollama_simple_chat(url: str, message: str, messages: list[dict] = []) -> str:
    "Send a simple text message to the LLM and get text response"
    url += "/api/chat"
    messages.append(
        {
            "role": "user",
            "content": message
        }
    )
    body = {
        "model": "llama2",
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
    messages = [
        {
            "role": "system",
            "content": "Tú eres un asistente programado para extraer términos específicos de un texto dado. Te preguntarán tanto en Español como en inglés Tu tarea es identificar términos clave relacionados con el enunciado y listarlos separados por comas. Ahora le dare varios ejemplos"
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
            "role": "system",
            "content": "Lo estas haciendo genial al identificar el idioma. Sigue asi."
        },
        {
            "role": "user",
            "content": "For several weeks now, I've been having trouble falling asleep. Even when I do, I wake up multiple times during the night. In the morning, I don't feel rested and struggle with daytime tiredness."
        },
        {
            "role": "assistant",
            "content": "insomnia, daytime-tiredness, fatigue"
        }
    ]
    str_term_list = await ollama_simple_chat(url, message, messages=messages)
    str_term_list = str_term_list.lower()
    str_term_list = str_term_list.replace(" ", "")
    term_list: list[str] = str_term_list.split(",")
    return term_list


async def ollama_get_conclusion(url: str, message: str, terms: list[str], docs: list[dict[str, any]]) -> str:
    messages = [
        {
            "role": "system",
            "content": "Tú eres un asistente programado para segun un texto y unos documentos json, determinar cual de esos documentos json se adaptan mejor a la situación particular del problema y explicar porque ese documento en concreto es la mejor opción o en caso de que todos los documentos proporcionados sean erróneos también mencionar que no encuentras soluciones fiables."
        }
    ]

    conclusion_msg = f"""Message: {
        message
    }\nTerms{
        terms
    }\nDocuments: {
        json.dumps(docs, indent=2) if len(
            docs) > 0 else "0 docs related to this message."
    }\n"""
    conclusion = await ollama_simple_chat(url, conclusion_msg, messages=messages)
    return conclusion
