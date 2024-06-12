FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

COPY . .

COPY requirements.txt .
RUN pip install pip==20.1.1
RUN pip install -r requirements.txt
