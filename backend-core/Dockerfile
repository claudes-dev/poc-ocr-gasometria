# Dockerfile para API Python de OCR de Gasometria
FROM python:3.12-slim

# Instala dependências do sistema (Tesseract OCR, libs OpenCV e build tools)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1 \
    curl \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências Python
COPY backend-core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação backend
COPY backend-core/ .

# Copia código do OCR service
COPY ocr-service/ ./ocr-service/

# Expõe porta da API
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação (usando gunicorn em produção)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
