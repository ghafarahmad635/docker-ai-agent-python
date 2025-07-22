FROM python:3.13.4-slim-bullseye
WORKDIR /app
# copy local folder to container
# RUN mkdir -p /static_folder
COPY ./src /app
# RUN echo "Hello, World!" > index.html
CMD [ "python", "-m", "http.server", "8000" ]