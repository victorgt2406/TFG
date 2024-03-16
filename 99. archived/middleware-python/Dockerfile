FROM python:latest

WORKDIR /app

COPY ./app /app

RUN pip install -r ./requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
