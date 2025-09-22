FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="$PATH:/root/.local/bin" && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "core.asgi:application", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
