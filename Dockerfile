FROM python:3.10-slim

WORKDIR /app

# Mun cire tesseract-ocr-hau a nan, mun saka wget don mu dauko shi da kan mu
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    espeak \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Neman inda Tesseract yake a sabar da kuma zuba masa asalin fayil din Hausa kai tsaye
RUN TESSDATA_DIR=$(find /usr/share -name "tessdata" -type d | head -n 1) && \
    wget -P $TESSDATA_DIR https://github.com/tesseract-ocr/tessdata/raw/main/hau.traineddata

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
