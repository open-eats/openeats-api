FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && \
    apk add --no-cache \
    gcc \
    git \
    mariadb \
    mariadb-dev \
    py-mysqldb \
    musl-dev \
    libjpeg-turbo-dev \
    zlib-dev

COPY base/prod-entrypoint.sh /startup/
RUN chmod +x /startup/prod-entrypoint.sh

RUN mkdir /code
WORKDIR /code
ADD base/requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
ADD . /code/