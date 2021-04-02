FROM python:3.9.2-alpine3.13
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && \
    apk add --no-cache \
    gcc \
    mariadb \
    mariadb-dev \
    mariadb-connector-c \
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
VOLUME /code/static-files
ENV API_PORT=8000
EXPOSE 8000
ENTRYPOINT ["/startup/prod-entrypoint.sh"]
