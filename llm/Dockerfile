FROM victorgtutad/python-ubuntucuda:3.12-ubuntu22.04
# https://github.com/victorgt2406/containers/tree/main/python-ubuntucuda

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN ./tranformers-hface.sh

ENTRYPOINT ["python", "./main.py"]