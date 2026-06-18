FROM python:3.10-slim

WORKDIR /app

# Mun cire neman Hausa don sabar ta tashi lafiya ba tare da Error 404 ba
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    espeak \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
