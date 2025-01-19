FROM python:3.10

WORKDIR /app

COPY requirements/ requirements/

ARG REQUIREMENTS_FILE=requirements/base.txt
RUN pip install -r ${REQUIREMENTS_FILE}

COPY . .
