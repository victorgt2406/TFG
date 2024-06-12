# Ollama Dockerfile

This dockerfile does the next:
```Dockerfile
FROM ollama/ollama:latest

COPY ./start.sh /start-ollama/start.sh

WORKDIR /start-ollama

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]
```

So it basically uses the official Ollama Image and runs a start file which makes sure to install the necessary LLMs.

*The test directory is meant to test conversations with Ollama REST API.*