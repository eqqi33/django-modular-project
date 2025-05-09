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

# Optional .env_docker copy
COPY .env_docker /tmp/.env_docker
RUN if [ -f /tmp/.env_docker ]; then cp /tmp/.env_docker .env; else echo ".env_docker not found, skipping copy"; fi

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]