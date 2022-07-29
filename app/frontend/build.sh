# command to stop the container with name streamlit-app
docker stop streamlit-app
# build the image with name streamlit-app
docker build -t streamlit-app .
# start the container with name streamlit-app, remove if stop. with interactive mode
docker run -it --rm --name streamlit-app -p 8888:8501 streamlit-app