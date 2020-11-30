FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /
RUN \
 apk add --no-cache postgresql-libs postgresql-client && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY wait-for /
RUN chmod +x /wait-for

RUN mkdir /app
WORKDIR /app
COPY app /app

RUN adduser -D user
RUN chown -R user /app
RUN chown user /wait-for
USER user