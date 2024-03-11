FROM victorgtutad/python-ubuntucuda:3.12-ubuntu22.04

COPY ./api /llm_app

WORKDIR /llm_app

RUN pip install -r requirements.txt

RUN ./tranformers-hface.sh