FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python3-pip python3-setuptools python3.6-venv && \
    apt-get install build-essential automake libtool pkg-config libffi-dev -y

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && \
    ln -sfn /usr/bin/pip3 /usr/bin/pip

RUN pip3 install --upgrade setuptools && pip3 install --upgrade pip

WORKDIR /remme-client-python
COPY . /remme-client-python

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt

CMD sleep 7200
