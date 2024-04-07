FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt
