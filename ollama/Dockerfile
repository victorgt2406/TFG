FROM ollama/ollama:latest

COPY ./Modelfiles /Modelfiles

COPY ./start.sh /start-ollama/start.sh

WORKDIR /start-ollama

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]