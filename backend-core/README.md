# Backend Core - API Flask + OCR

API REST completa em Python/Flask para processamento OCR de resultados de gasometria arterial.

## 📋 Estrutura do Projeto

```
backend-core/
├── app.py                          # Aplicação Flask principal (configuração CORS, rotas)
├── run.py                          # Script de inicialização simplificado
├── controllers/
│   ├── __init__.py
│   └── gasometria_controller.py    # Controller: processa requisições HTTP
├── services/
│   ├── __init__.py
│   └── ocr_service.py              # Service: ponte com módulo ocr-service
├── requirements.txt                # Dependências Python
├── Dockerfile                      # Container Docker (Python 3.12 + Tesseract)
└── README.md                       # Este arquivo
```

## 🛠️ Stack

- **Python 3.12** (não use 3.14+ - incompatibilidade com Gunicorn)
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - CORS para APIs
- **NumPy 1.26+** - Computação numérica
- **OpenCV 4.8+** - Processamento de imagens
- **pytesseract 0.3.10** - Wrapper Tesseract OCR
- **Gunicorn 21.2.0** - Servidor WSGI de produção
- **Tesseract OCR 5.0+** - Motor de OCR (idiomas: por, eng)

## 🚀 Quick Start

### Pré-requisitos

**Para rodar com Docker:**
- Docker Desktop 20.10+

**Para rodar localmente:**
- Python 3.12+
- Tesseract OCR instalado ([Download Windows](https://github.com/UB-Mannheim/tesseract/wiki))
- Idiomas: `por` (Português) e `eng` (Inglês)
- Compiladores C/C++ (para instalar NumPy)

### Opção 1: Docker (Recomendado)

Da raiz do projeto:

```bash
docker-compose up --build
```

✅ API disponível em: `http://localhost:5000`

### Opção 2: Execução Local

1. **Configure Tesseract (Windows):**
   
   Edite `../ocr-service/main.py` e descomente as linhas 11-12:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
   ```

2. **Instale dependências:**
   ```bash
   cd backend-core
   pip install -r requirements.txt
   ```

3. **Execute:**
   ```bash
   python run.py
   ```

✅ API disponível em: `http://localhost:5000`

## 📡 Endpoints

### Health Check

#### `GET /health`
Health check simples.

**Response:**
```json
{
  "status": "healthy",
  "service": "OCR Gasometria API",
  "version": "1.0.0"
}
```

### Listar Parâmetros

#### `GET /api/gasometria/parametros`
Lista todos os parâmetros de gasometria que podem ser extraídos.

**Response:**
```json
{
  "sucesso": true,
  "parametros": [
    {
      "nome": "pH",
      "descricao": "Potencial hidrogenionico",
      "unidade": "",
      "faixa": "6.8 - 7.8"
    },
    ...
  ]
}
```

### Obter Ranges de Validação

#### `GET /api/gasometria/ranges`
Retorna os valores mínimos e máximos aceitos para cada parâmetro.

**Response:**
```json
{
  "sucesso": true,
  "ranges": {
    "pH": {"min": 6.8, "max": 7.8},
    "pCO2": {"min": 10, "max": 100},
    ...
  }
}
```

### Análise de Gasometria

#### `POST /api/gasometria/analisar`
Processa imagem de gasometria e extrai valores.

**Query Parameters:**
- `validar` (boolean, opcional, default: `false`) - Valida valores extraídos
- `debug` (boolean, opcional, default: `false`) - Inclui texto OCR na resposta

**Request:**
```http
POST /api/gasometria/analisar?validar=true&debug=false
Content-Type: multipart/form-data

imagem=<arquivo>
```

**Response (sucesso):**
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    "pCO2": 40,
    "pO2": 95,
    "HCO3": 24,
    "BE": 0,
    "SaO2": 98,
    "lactato": 1.2,
    "Na": 140,
    "K": 4.0,
    "Ca": 1.2,
    "Cl": 105,
    "Glicose": 90
  },
  "validacao": {
    "pH": true,
    "pCO2": true,
    ...
  }
}
```

**Response (erro):**
```json
{
  "sucesso": false,
  "erro": "Nenhuma imagem foi enviada"
}
```

## 🧪 Exemplos de Uso

### cURL (Bash)

```bash
# Health check
curl http://localhost:5000/health

# Listar parâmetros
curl http://localhost:5000/api/gasometria/parametros

# Analisar imagem
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@imagem.png"
```

### PowerShell

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing

# Analisar imagem
$form = @{ imagem = Get-Item "imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" `
    -Method Post -Form $form -UseBasicParsing
```

## 🏗️ Arquitetura

**Camadas:**
1. **Controller** (`gasometria_controller.py`) - Processa requisições HTTP, valida input
2. **Service** (`ocr_service.py`) - Lógica de negócio, importa módulo OCR
3. **OCR Module** (`../ocr-service/main.py`) - Core: preprocessamento, OCR, extração

**Fluxo:**
```
Cliente → Flask → Controller → Service → OCR Module → Tesseract
```

## 🔧 Desenvolvimento

### Estrutura de Arquivos

- **app.py** - Configuração do Flask, CORS, registro de rotas
- **run.py** - Entry point simplificado
- **controllers/** - Endpoints da API (lógica HTTP)
- **services/** - Lógica de negócio e integração com OCR

### Adicionar Novo Endpoint

1. Crie método no controller (`controllers/gasometria_controller.py`)
2. Registre rota no `app.py`
3. Teste com curl ou Postman

### Modificar Lógica de OCR

Edite `../ocr-service/main.py` para ajustar:
- Preprocessamento de imagem (`preprocessar_imagem`)
- Regex de extração (`extrair_valores`)
- Ranges de validação (`RANGES_GASOMETRIA`)

## 📚 Documentação Adicional

- **[../README.md](../README.md)** - Guia de início rápido
- **[../README-MONOREPO.md](../README-MONOREPO.md)** - Documentação técnica completa
- **[../curl-examples.md](../curl-examples.md)** - Exemplos completos de uso da API
- **[../COMO-TESTAR.md](../COMO-TESTAR.md)** - Guia de testes

## 🐛 Troubleshooting

Ver seção de Troubleshooting em [../README-MONOREPO.md](../README-MONOREPO.md#-troubleshooting)

## 📝 Notas

- Arquitetura monolítica para simplificar POC
- `ocr-service` é módulo Python, não serviço HTTP separado
- Tesseract deve estar no PATH ou configurado no `main.py`
