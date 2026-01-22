FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# --- system deps (rarely change) ---
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# --- python deps (cached unless requirements.txt changes) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- runtime files (change often) ---
COPY pytest.ini .
COPY app app
COPY tests tests
