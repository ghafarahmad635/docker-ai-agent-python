FROM python:3.13.4-slim-bullseye
WORKDIR /app

# host.docker.internal -> localhost
# curl -X POST -d '{"message": "Hello world"}'  -H "Content-Type: application/json" http://host.docker.internal:8080/api/chats/
RUN apt-get update && apt-get install -y curl

RUN python -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

COPY ./src .
COPY requirements.txt tmp/requirements.txt
RUN pip install  -r tmp/requirements.txt

CMD [ "python", "-m", "http.server", "8000" ]
