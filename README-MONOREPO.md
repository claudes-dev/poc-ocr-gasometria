# 🐾 Sistema de Gasometria Veterinária - Monorepo

Sistema completo para análise automática de exames de gasometria veterinária usando OCR.

## 📁 Estrutura

```
poc-ocr-gasometria/
├── ocr-service/          # Python OCR
├── backend-core/         # Node.js API
└── docker-compose.yml    # Orquestração
```

## 🚀 Quick Start

```bash
docker-compose up --build
```

**Serviços:**
- 🔬 OCR: http://localhost:5000
- 🚀 API: http://localhost:3000

## 📡 API Principal

```bash
POST /api/gasometria/analisar
```

**Exemplo:**
```bash
curl -X POST http://localhost:3000/api/gasometria/analisar \
  -F "imagem=@teste.jpg"
```

## 🔬 Parâmetros Extraídos

pH, pCO2, pO2, HCO3, BE, SaO2, lactato, Na, K, Ca, Cl, Glicose

## 🛠️ Tech Stack

- Python 3.14 + OpenCV + Tesseract
- Node.js 20 + Express
- Docker

## 📦 Desenvolvimento

Ver README em cada serviço:
- [ocr-service/README.md](ocr-service/README.md)
- [backend-core/README.md](backend-core/README.md)
