FROM gcr.io/gcp-runtimes/python/gen-dockerfile
COPY . /app/flask-web
WORKDIR /app/flask-web
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/bin/python3", "main.py"]
