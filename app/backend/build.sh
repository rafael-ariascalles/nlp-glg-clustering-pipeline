docker build -t fast-app .
docker run -it --rm --name fast-app -e WORKERS_PER_CORE="2" -p 9898:80 fast-app