FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

COPY docker/prod/requirements.txt /
RUN apk add --no-cache postgresql-libs postgresql-client && \
	apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
	python3 -m pip install --upgrade pip && \
	python3 -m pip install -r /requirements.txt --no-cache-dir && \
	apk --purge del .build-deps


RUN mkdir /app
WORKDIR /app
COPY app /app

RUN mkdir /files
RUN mkdir /files/staticfiles
COPY ./docker/prod/entrypoint.sh /files
RUN chmod +x /files/entrypoint.sh

COPY wait-for /files
RUN chmod +x /files/wait-for

RUN addgroup app && adduser -D user -G app
RUN chown -R user:app /app
RUN chown -R user:app /files
USER user