FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

# Install requirements
COPY docker/dev/requirements.txt /
RUN apk add --no-cache postgresql-libs postgresql-client && \
 	apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 	python3 -m pip install --upgrade pip && \
 	python3 -m pip install -r /requirements.txt --no-cache-dir && \
 	apk --purge del .build-deps


# Copy files to container
COPY wait-for /
RUN chmod +x /wait-for

RUN mkdir /app
WORKDIR /app
COPY app /app


# Create a non-root user to run the application
RUN adduser -D user
RUN chown -R user /app
RUN chown user /wait-for
USER user