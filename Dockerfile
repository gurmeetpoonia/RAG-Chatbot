FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Working directory backend set karein
WORKDIR /app/backend

# Requirements copy aur install karein
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Baaki poora code copy karein
COPY . /app

EXPOSE 10000

# Ab 'main:app' directly import ho jayega!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]