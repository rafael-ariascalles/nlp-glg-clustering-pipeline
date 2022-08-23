# create a container with the following image fro streamlit app
FROM python:3.7

EXPOSE 8888
COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r /requirements.txt

WORKDIR /app
COPY . .

# Setup env SERCIVE_IP from .env file
ENV SERVICE_IP 0.0.0.0

CMD ["streamlit","run", "app.py"]