# ---- build runtime ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# OS deps (si besoin de mysqlclient, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copier deps
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le code
COPY src ./src
COPY .env.example ./.env.example  # optionnel, juste pour doc
# si tu as des fichiers nécessaires (alembic.ini etc.), copie-les ici

# Expose & cmd
ENV PYTHONPATH=src
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
