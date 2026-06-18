# 1. Dauko asalin tsarin Python
FROM python:3.9-slim

# 2. Saka ainihin injin karatu na Tesseract a cikin Linux din sabar
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-hau espeak

# 3. Tsara wajen aiki
WORKDIR /app

# 4. Kawo fayil din requirements sannan a saka masarrafan Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kawo sauran code din gaba daya cikin sabar
COPY . .

# 6. Kunna sabar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
```
*(Lura: A layi na ƙarshe, na yi amfani da `main:app`. Idan ainihin fayil ɗinka da ke da FastAPI sunansa `main.py` ne, toh wannan daidai ne. Idan sunansa wani daban ne, misali `api.py`, sai ka canza kalmar `main` ta koma `api`).
