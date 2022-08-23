# nlp-glg-clustering-pipeline

GLG Capstone project repository - Applied NLP for Text Clustering, Topic Extraction , NER implementation and Text Analytics generation - Fourthbrain  Certification

Team: 
* Jason Jones
* Rafael Arias

## General Tech stack

* Python
* Conda 
* Docker runtime

## For development 

the notebooks use specific kernerl. For test aand further development the following command should be:

```bash
conda env create -f conda-env.yml
```

for some notebooks it is necesary to crete the .env file with the following content:

```text
NEWS_DATA_PATH=<path_to_local_news21>
AUTH_TOKEN=<huggingface_auth_token>
COHERE_API_KEY = <cohere_auth_token>
HUGGINGFACE_API_KEY = <huggingface_auth_token>
```

the diference between AUTH_TOKEN and HUGGINGFACE_API_KEY is that the first one has write permision and the second only read permision.

## For deployment

After cloning the repository, the following command should be executed:

```bash
cd app/backend
bash build.sh
```

this will create the docker image with all the necesary files and dependencies.
after the building process it will run the container with an Endpoint at port 9898, this can be setup into build.sh

to have the FastAPI functionality of Autoreloading when some changes are implement into the code run the build-local.sh

for the frontend the we have to setup a .env file with the IP of the computer and the run the a bash command should be executed (make sure you are into the root folder of the repo nlp-glg-clustering-pipeline):

Enviroment:
```text
SERVICE_IP = <IPv4_local_host>
```	

command:
```bash
cd app/frontend
bash build.sh
```
