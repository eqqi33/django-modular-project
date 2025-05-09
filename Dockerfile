FROM python:3.11-slim AS base

# DEVELOPMENT
FROM base AS dev
CMD [ "" ]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Rename .env_docker to .env inside the container
COPY .env_docker .env

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]