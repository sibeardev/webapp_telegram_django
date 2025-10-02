FROM node:lts-alpine AS build-node
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build:css


FROM python:3.12-slim AS runtime-python
WORKDIR /app
RUN pip install --no-cache-dir "poetry>=2.0.0" poetry-plugin-export
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --only main --without-hashes -o requirements.txt \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip
COPY . .
COPY --from=build-node /app/static/css/dist.css /app/static/css/dist.css

ENV PYTHONUNBUFFERED=1

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]