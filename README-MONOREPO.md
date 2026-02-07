# 🐾 Sistema de Gasometria Veterinária - Monorepo

Sistema completo para análise automática de exames de gasometria veterinária usando OCR.

## 📁 Estrutura

```
poc-ocr-gasometria/
├── backend-core/         # Python API REST (Flask)
├── ocr-service/          # Python OCR Core
└── docker-compose.yml    # Orquestração
```

### Componentes

- **backend-core/**: API REST completa em Python/Flask
- **ocr-service/**: Módulo core de processamento OCR

## 🚀 Quick Start

```bash
docker-compose up --build
```

**Serviços:**
- � API Backend: http://localhost:5000

## 📡 API Principal

```bash
POST /api/gasometria/analisar
```

**Exemplo:**
```bash
curl -X POST http://localhost:5000/api/gasometria/analisar \
  -F "imagem=@teste.jpg"
```

## 🔬 Parâmetros Extraídos

pH, pCO2, pO2, HCO3, BE, SaO2, lactato, Na, K, Ca, Cl, Glicose

## 🛠️ Tech Stack

- Python 3.11+ (Flask, OpenCV, Tesseract)
- Docker
- CORS enabled para integração frontend

## 📦 Desenvolvimento

### Backend Python (Flask)

```bash
cd backend-core
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

### Testes

```bash
cd backend-core
python test_api.py
```

Ver README completo em cada serviço:
- [backend-core/README.md](backend-core/README.md) - API Python REST
- [ocr-service/README.md](ocr-service/README.md) - Core OCR
