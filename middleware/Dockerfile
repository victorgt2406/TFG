FROM alpine:latest

RUN apk add --no-cache nodejs npm python3 python3-dev py3-pip build-base

COPY . /app
WORKDIR /app

RUN python3 -m venv middleware \
    && source middleware/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

RUN cd ./client && npm install && npm run build && cd ..

WORKDIR /app

ENTRYPOINT ["./middleware/bin/python3", "main.py"]