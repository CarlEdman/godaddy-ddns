FROM python:latest

WORKDIR /app
COPY . /app

ENTRYPOINT [ "/app/godaddy_ddns.py" ]