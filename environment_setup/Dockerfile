FROM python:3.7-slim-stretch

# LABEL org.label-schema.vendor = "Microsoft" \
#       org.label-schema.url = "https://hub.docker.com/r/microsoft/mlopspython" \
#       org.label-schema.vcs-url = "https://github.com/microsoft/MLOpsPython"

COPY requirements.txt  /setup/
	
RUN apt-get update && apt-get install gcc -y && pip install --upgrade -r /setup/requirements.txt && \
    chmod -R 777 /usr/local/lib/python3.7

CMD ["python"]