FROM victorgtutad/python-ubuntucuda:3.12-ubuntu22.04
# https://github.com/victorgt2406/containers/tree/main/python-ubuntucuda

COPY ./api /llm_app

WORKDIR /llm_app

RUN pip install -r requirements.txt

RUN ./tranformers-hface.sh

ENTRYPOINT ["python", "./app.py"]