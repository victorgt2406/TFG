#!/bin/bash

if [ ! -f /ollama_preconfigurated ]; then
    ollama serve &
    sleep 5
    echo -e "\nFirst time...\n---\nInitializing Ollama...\n"
    ollama pull llama2
    ollama create llm_assitant -f /Modelfiles/assistant.Modelfile
    ollama create llm_terms -f /Modelfiles/terms.Modelfile

    touch /ollama_preconfigurated
else
    echo -e "\nSkipping initialization...\n"
    ollama serve
fi