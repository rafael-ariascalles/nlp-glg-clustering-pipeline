# create a container with the following image fro streamlit app
FROM python:3.7

EXPOSE 8888
COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r /requirements.txt

WORKDIR /app
COPY . .

CMD ["streamlit","run", "app.py"]