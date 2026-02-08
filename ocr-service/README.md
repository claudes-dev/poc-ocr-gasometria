# 🔬 OCR Service - Gasometria

Serviço Python responsável pelo OCR (Reconhecimento Óptico de Caracteres) de exames de gasometria.

## 🚀 Como executar localmente

### 1. Instalar dependências:
```bash
pip install -r requirements.txt
```

### 2. Executar API:
```bash
python api.py
```

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Processar Imagem
```
POST /processar
Content-Type: multipart/form-data

Body:
- imagem: arquivo de imagem
- validar: true/false (opcional, padrão: true)
- debug: true/false (opcional, padrão: false)
```

## 🧪 Testar localmente (sem API)

```bash
python testar_ocr.py <caminho_imagem>
```

ou

```bash
python testar_interativo.py
```

## 🐳 Docker

```bash
docker build -t ocr-gasometria .
docker run -p 5000:5000 ocr-gasometria
```
