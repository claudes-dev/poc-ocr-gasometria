FROM python:3.14-slim

# Instala Tesseract e dependências do OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código do serviço
COPY . .

# Expõe porta do Flask
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "api.py"]
