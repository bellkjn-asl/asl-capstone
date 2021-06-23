FROM gcr.io/gcp-runtimes/python/gen-dockerfile
COPY . /app/flask-web
WORKDIR /app/flask-web
ENTRYPOINT ["/bin/python3", "main.py"]
