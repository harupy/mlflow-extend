FROM python:3.7.6

ARG WORKDIR=/mlflow-extend

WORKDIR ${WORKDIR}

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt -r /tmp/requirements-dev.txt
