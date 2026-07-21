# 1. Official Python 3.11 Slim image (lightweight & fast)
FROM python:3.11-slim

# 2. Prevent Python from writing .pyc files and enable live output logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install Tesseract OCR and system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Set working directory inside container
WORKDIR /app

# 5. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy rest of the backend source code
COPY . .

# 7. Expose Render default port
EXPOSE 10000

# 8. Start FastAPI backend with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]