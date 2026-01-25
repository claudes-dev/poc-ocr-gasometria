# 🚀 Backend Core - Sistema de Gasometria

Backend Node.js/Express responsável pela API REST do sistema de gasometria veterinária.

## 📦 Tecnologias

- Node.js 20
- Express.js
- Axios (comunicação com OCR)
- Multer (upload de arquivos)

## 🚀 Como executar

### 1. Instalar dependências:
```bash
npm install
```

### 2. Configurar variáveis de ambiente:
```bash
cp .env.example .env
```

### 3. Executar:
```bash
# Desenvolvimento (com hot reload)
npm run dev

# Produção
npm start
```

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Analisar Gasometria
```
POST /api/gasometria/analisar
Content-Type: multipart/form-data

Body:
- imagem: arquivo de imagem
```

### Listar Parâmetros
```
GET /api/gasometria/parametros
```

## 🧪 Testar API

```bash
# Com curl
curl -X POST http://localhost:3000/api/gasometria/analisar \
  -F "imagem=@/caminho/para/imagem.jpg"

# Com Postman/Insomnia
POST http://localhost:3000/api/gasometria/analisar
Body: form-data
Key: imagem (type: File)
```

## 🐳 Docker

```bash
docker build -t backend-gasometria .
docker run -p 3000:3000 -e OCR_SERVICE_URL=http://ocr-service:5000 backend-gasometria
```
