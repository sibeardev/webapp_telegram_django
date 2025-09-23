FROM python:3.12-slim

WORKDIR /app

# Установим poetry + плагин для export
RUN pip install --no-cache-dir "poetry>=2.0.0" poetry-plugin-export

# Копируем только файлы зависимостей (чтобы работало кэширование слоёв)
COPY pyproject.toml poetry.lock ./

# Экспортируем зависимости и ставим через pip
RUN poetry export -f requirements.txt --only main --without-hashes -o requirements.txt \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Копируем код проекта
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
