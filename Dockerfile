# 1. Official Python 3.11 Slim image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. Install Tesseract OCR and system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy requirements from backend subfolder and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy all source code
COPY . .

EXPOSE 10000

# 5. Run FastAPI app from backend module
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]