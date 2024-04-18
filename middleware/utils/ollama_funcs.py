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
            "content": """You are tasked with identifying specific symptoms or relevant features mentioned in a text and listing them in a comma-separated format. Ensure consistency in identifying and listing these terms regardless of the language of the input (English or Spanish).

            Example:
            - Input: "Yesterday, I started feeling a sore throat and a fever. This morning, my symptoms included a runny nose and a cough."
            - Output: "sore throat, fever, runny nose, cough

            Example:
            - Input: "Ayer, empecé a sentir dolor de garganta y fiebre. Esta mañana, mis síntomas incluían secreción nasal y tos."
            - Output: "dolor de garganta, fiebre, secreción nasal, tos

            Please ensure that your output strictly adheres to the language of the input text.
            """
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


async def ollama_get_conclusion(url: str, message: str, terms: list[str], docs: list[dict]) -> str:
    messages = [
        {
            "role": "system",
            "content": """You are an assistant programmed to analyze a given text and several JSON documents to determine which of these documents best fits the particular situation described in the problem. Explain why the selected document is the best choice, or, if all provided documents are incorrect, mention that no reliable solutions are found. If you receive a message in Spanish, respond in Spanish; if the message is in English, respond in English.

            The input you will receive is structured as follows:
            "Message: ...\nTerms: ...\nDocuments: ...\n

            Your response should be direct and based on the data you have. It should include your choice of the most appropriate document or advise that no suitable documents are available, depending on the symptoms and other data provided by the LLM.

            Example:
            - Input: Message: Yesterday, I started feeling a sore throat and a fever. This morning, my symptoms included a runny nose and a cough.
            Terms['sore-throat', 'fever', 'runny-nose', 'cough']
            Documents: [
            {
                "_id": "Tamiflu",
                "_score": 23.665468,
                "drug_name": "Tamiflu",
                "medical_condition": "Swine Flu",
                "side_effects": "sudden confusion; tremors or shaking; unusual behavior; or hallucinations (hearing or seeing things that are not there). Common Tamiflu side effects may include: nausea, vomiting ; headache ; or pain.",
                "generic_name": "oseltamivir",
                "drug_classes": "Neuraminidase inhibitors",
                "brand_names": "",
                "activity": "100%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "amantadine: https://www.drugs.com/amantadine.html | oseltamivir: https://www.drugs.com/oseltamivir.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html | Relenza: https://www.drugs.com/relenza.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 7.3,
                "no_of_reviews": 18,
                "drug_link": "https://www.drugs.com/tamiflu.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            },
            {
                "_id": "oseltamivir",
                "_score": 23.665468,
                "drug_name": "oseltamivir",
                "medical_condition": "Swine Flu",
                "side_effects": "sudden confusion; tremors or shaking; unusual behavior; or hallucinations (hearing or seeing things that are not there). Common oseltamivir side effects may include: nausea, vomiting ; headache ; or pain.",
                "generic_name": "oseltamivir",
                "drug_classes": "Neuraminidase inhibitors",
                "brand_names": "Tamiflu",
                "activity": "41%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "Tamiflu: https://www.drugs.com/tamiflu.html | amantadine: https://www.drugs.com/amantadine.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html | Relenza: https://www.drugs.com/relenza.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 7.3,
                "no_of_reviews": 18,
                "drug_link": "https://www.drugs.com/oseltamivir.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            },
            {
                "_id": "Relenza",
                "_score": 23.665468,
                "drug_name": "Relenza",
                "medical_condition": "Swine Flu",
                "side_effects": "hives ; difficult breathing; swelling of your face, lips, tongue, or throat. Some people using Relenza (especially children) have had sudden unusual changes in mood or behavior. It is not certain that zanamivir is the exact cause of these symptoms. Even without using Relenza, anyone with influenza can have neurologic or behavioral symptoms. Call your doctor right away if the person using this medicine has: sudden confusion; trouble speaking; tremors or shaking; a seizure; or hallucinations (hearing or seeing things that are not there). Stop using this medicine and call your doctor at once if you have wheezing or severe breathing problems, or if you feel like you might pass out. Common Relenza side effects may include: headache , dizziness ; nausea , vomiting , diarrhea ; cough, wheezing, trouble breathing; ear pain; or cold symptoms such as stuffy nose, sneezing, sore throat.",
                "generic_name": "zanamivir",
                "drug_classes": "Inhaled anti-infectives, Neuraminidase inhibitors",
                "brand_names": "",
                "activity": "13%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "Tamiflu: https://www.drugs.com/tamiflu.html | amantadine: https://www.drugs.com/amantadine.html | oseltamivir: https://www.drugs.com/oseltamivir.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 10,
                "no_of_reviews": 1,
                "drug_link": "https://www.drugs.com/relenza.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            }
            ]
            - Output: The symptoms mentioned, sore-throat, fever, runny-nose, and cough are consistent with those of Swine Flu (H1N1 Influenza). The documents reference medications like Tamiflu (oseltamivir) and Relenza (zanamivir), which are prescribed for Swine Flu. These drugs are part of the neuraminidase inhibitors class and are known to be effective against the symptoms described. It is advisable for individuals experiencing such symptoms to consult with a healthcare provider for proper diagnosis and treatment.
            """
        },
        {
            "role": "user",
            "content": """Message: Yesterday, I started feeling a sore throat and a fever. This morning, my symptoms included a runny nose and a cough.
            Terms['sore-throat', 'fever', 'runny-nose', 'cough']
            Documents: [
            {
                "_id": "Tamiflu",
                "_score": 23.665468,
                "drug_name": "Tamiflu",
                "medical_condition": "Swine Flu",
                "side_effects": "sudden confusion; tremors or shaking; unusual behavior; or hallucinations (hearing or seeing things that are not there). Common Tamiflu side effects may include: nausea, vomiting ; headache ; or pain.",
                "generic_name": "oseltamivir",
                "drug_classes": "Neuraminidase inhibitors",
                "brand_names": "",
                "activity": "100%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "amantadine: https://www.drugs.com/amantadine.html | oseltamivir: https://www.drugs.com/oseltamivir.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html | Relenza: https://www.drugs.com/relenza.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 7.3,
                "no_of_reviews": 18,
                "drug_link": "https://www.drugs.com/tamiflu.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            },
            {
                "_id": "oseltamivir",
                "_score": 23.665468,
                "drug_name": "oseltamivir",
                "medical_condition": "Swine Flu",
                "side_effects": "sudden confusion; tremors or shaking; unusual behavior; or hallucinations (hearing or seeing things that are not there). Common oseltamivir side effects may include: nausea, vomiting ; headache ; or pain.",
                "generic_name": "oseltamivir",
                "drug_classes": "Neuraminidase inhibitors",
                "brand_names": "Tamiflu",
                "activity": "41%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "Tamiflu: https://www.drugs.com/tamiflu.html | amantadine: https://www.drugs.com/amantadine.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html | Relenza: https://www.drugs.com/relenza.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 7.3,
                "no_of_reviews": 18,
                "drug_link": "https://www.drugs.com/oseltamivir.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            },
            {
                "_id": "Relenza",
                "_score": 23.665468,
                "drug_name": "Relenza",
                "medical_condition": "Swine Flu",
                "side_effects": "hives ; difficult breathing; swelling of your face, lips, tongue, or throat. Some people using Relenza (especially children) have had sudden unusual changes in mood or behavior. It is not certain that zanamivir is the exact cause of these symptoms. Even without using Relenza, anyone with influenza can have neurologic or behavioral symptoms. Call your doctor right away if the person using this medicine has: sudden confusion; trouble speaking; tremors or shaking; a seizure; or hallucinations (hearing or seeing things that are not there). Stop using this medicine and call your doctor at once if you have wheezing or severe breathing problems, or if you feel like you might pass out. Common Relenza side effects may include: headache , dizziness ; nausea , vomiting , diarrhea ; cough, wheezing, trouble breathing; ear pain; or cold symptoms such as stuffy nose, sneezing, sore throat.",
                "generic_name": "zanamivir",
                "drug_classes": "Inhaled anti-infectives, Neuraminidase inhibitors",
                "brand_names": "",
                "activity": "13%",
                "rx_otc": "Rx",
                "pregnancy_category": "C",
                "csa": "N",
                "alcohol": "",
                "related_drugs": "Tamiflu: https://www.drugs.com/tamiflu.html | amantadine: https://www.drugs.com/amantadine.html | oseltamivir: https://www.drugs.com/oseltamivir.html | Vicks DayQuil Severe Cold & Flu: https://www.drugs.com/mtm/dayquil-severe-cold-flu.html | Xofluza: https://www.drugs.com/xofluza.html | Fluzone: https://www.drugs.com/cdi/fluzone.html | influenza virus vaccine, inactivated: https://www.drugs.com/mtm/influenza-virus-vaccine-injection.html | Coricidin HBP Cold & Flu: https://www.drugs.com/coricidin.html | Afluria: https://www.drugs.com/afluria.html | zanamivir: https://www.drugs.com/mtm/zanamivir.html",
                "medical_condition_description": "Swine Flu Other names: H1N1 Influenza; Novel H1N1 Flu; Swine Influenza Swine Influenza (swine flu) is a respiratory disease of pigs caused by type A influenza virus that regularly causes outbreaks of influenza in pigs. People do not normally get swine flu, but human infections can and do happen. The virus is contagious and can spread from human to human. The symptoms of swine flu in people are similar to the symptoms of regular human seasonal influenza and include fever, lethargy, lack of appetite and coughing. Some people with swine flu also have reported runny nose, sore throat, nausea, vomiting and diarrhea.",
                "rating": 10,
                "no_of_reviews": 1,
                "drug_link": "https://www.drugs.com/relenza.html",
                "medical_condition_url": "https://www.drugs.com/condition/swine-flu.html"
            }
            ]"""
        },
        {
            "role": "user",
            "content": "It can be concluded that the symptoms mentioned: sore throat, fever, runny nose, and cough, are consistent with those of Swine Flu (H1N1 Influenza). The documents reference medications like Tamiflu (oseltamivir) and Relenza (zanamivir), which are prescribed for Swine Flu. These drugs are part of the neuraminidase inhibitors class and are known to be effective against the symptoms described. It is advisable for individuals experiencing such symptoms to consult with a healthcare provider for proper diagnosis and treatment."
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

    print("input: ",conclusion_msg)
    conclusion = await ollama_simple_chat(url, conclusion_msg, messages=messages)
    print("output: ",conclusion)
    return conclusion
