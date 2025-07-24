FROM python:3.13.4-slim-bullseye
WORKDIR /app

RUN python -m venv /opt/venv/
ENV PATH=/opt/venv/bin:$PATH

COPY ./src .
COPY requirements.txt tmp/requirements.txt
RUN pip install -r tmp/requirements.txt

# add a non-root user for security and Choreo compliance
RUN groupadd -r appgroup && useradd -r -g appgroup --uid 10001 appuser
USER 10001

CMD [ "python", "-m", "http.server", "8000" ]
