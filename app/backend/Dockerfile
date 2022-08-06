FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get update -y
RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /usr/src/app
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80"]