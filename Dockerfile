FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN mkdir /app
WORKDIR /app
COPY app /app

RUN adduser -D user
RUN chown -R user /app
USER user