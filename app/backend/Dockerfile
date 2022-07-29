FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update -y
RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
