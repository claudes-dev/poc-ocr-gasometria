# API Python - OCR Gasometria

API REST completa em Python/Flask para processamento OCR de resultados de gasometria arterial.

## 📋 Estrutura do Projeto

```
python-api/
├── app.py                          # Aplicação Flask principal
├── controllers/
│   ├── __init__.py
│   └── gasometria_controller.py    # Controller de gasometria
├── services/
│   ├── __init__.py
│   └── ocr_service.py              # Serviço de OCR
├── requirements.txt                # Dependências Python
├── Dockerfile                      # Container Docker
├── .env.example                    # Exemplo de configuração
└── README.md                       # Este arquivo
```

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- Tesseract OCR instalado ([Download Windows](https://github.com/UB-Mannheim/tesseract/wiki))
- Idiomas: `por` (Português) e `eng` (Inglês)

### Instalação Local

1. **Clone o repositório** (se ainda não fez):
   ```bash
   git clone <repo-url>
   cd poc-ocr-gasometria/python-api
   ```

2. **Crie ambiente virtual**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite .env com seus caminhos do Tesseract
   ```

5. **Execute a API**:
   ```bash
   python app.py
   ```

A API estará disponível em: `http://localhost:5000`

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

#### `GET /api/health`
Health check detalhado com status do Tesseract.

**Response:**
```json
{
  "status": "healthy",
  "service": "OCR Gasometria",
  "tesseract_version": "5.3.0",
  "ocr_ready": true
}
```

### Análise de Gasometria

#### `POST /api/gasometria/analisar`
Processa imagem de gasometria e extrai valores.

**Request:**
- Content-Type: `multipart/form-data`
- Campo obrigatório: `imagem` (arquivo de imagem)
- Parâmetros opcionais:
  - `validar` (true/false) - Valida valores extraídos
  - `debug` (true/false) - Inclui texto OCR bruto na resposta

**Exemplo com cURL:**
```bash
curl -X POST http://localhost:5000/api/gasometria/analisar \
  -F "imagem=@gasometria.png" \
  -F "validar=true" \
  -F "debug=false"
```

**Response (Sucesso):**
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    "pCO2": 45.0,
    "pO2": 98.0,
    "HCO3": 24.0,
    "BE": -2.0,
    "SaO2": 98.0,
    "lactato": 1.2,
    "Na": 140.0,
    "K": 4.4,
    "Ca": 1.2,
    "Cl": 105.0,
    "Glicose": 110.0
  },
  "validacao": {
    "todas_validas": true,
    "fora_faixa": []
  }
}
```

**Response (Erro):**
```json
{
  "sucesso": false,
  "erro": "Descrição do erro",
  "detalhes": "Detalhes adicionais"
}
```

#### `GET /api/gasometria/parametros`
Lista todos os parâmetros disponíveis.

**Response:**
```json
{
  "sucesso": true,
  "parametros": [
    {
      "nome": "pH",
      "descricao": "Potencial hidrogeniônico",
      "unidade": "",
      "faixa": "6.8 - 7.8"
    },
    {
      "nome": "pCO2",
      "descricao": "Pressão parcial de CO2",
      "unidade": "mmHg",
      "faixa": "10 - 100"
    }
    // ... outros parâmetros
  ]
}
```

#### `GET /api/gasometria/ranges`
Retorna faixas de validação para cada parâmetro.

**Response:**
```json
{
  "sucesso": true,
  "ranges": {
    "pH": { "min": 6.8, "max": 7.8 },
    "pCO2": { "min": 10, "max": 100 },
    "pO2": { "min": 40, "max": 500 }
    // ... outros ranges
  }
}
```

## 🐳 Docker

### Build da Imagem

```bash
docker build -t ocr-gasometria-api .
```

### Executar Container

```bash
docker run -p 5000:5000 ocr-gasometria-api
```

## 🧪 Testes

### Teste Manual com cURL

```bash
# Health check
curl http://localhost:5000/health

# Processar imagem
curl -X POST http://localhost:5000/api/gasometria/analisar \
  -F "imagem=@../ocr-service/gasometria.png"

# Listar parâmetros
curl http://localhost:5000/api/gasometria/parametros
```

### Teste com Python

```python
import requests

# Enviar imagem
url = "http://localhost:5000/api/gasometria/analisar"
files = {"imagem": open("gasometria.png", "rb")}
data = {"validar": "true", "debug": "false"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FLASK_DEBUG` | Modo debug do Flask | `true` |
| `HOST` | Host do servidor | `0.0.0.0` |
| `PORT` | Porta do servidor | `5000` |
| `TESSERACT_CMD` | Caminho do executável Tesseract | (detecta automaticamente) |
| `TESSDATA_PREFIX` | Diretório de dados do Tesseract | (detecta automaticamente) |

### Gunicorn (Produção)

Para rodar em produção com Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

## 📚 Arquitetura

### Camadas

1. **app.py**: Define rotas Flask e configuração da aplicação
2. **Controllers**: Processam requisições HTTP e validam entrada
3. **Services**: Implementam lógica de negócio e integração com OCR
4. **OCR Core**: Módulo `main.py` do ocr-service (processamento de imagem)

### Fluxo de Processamento

```
Cliente → Flask Route → Controller → Service → OCR Core
                                              ↓
Cliente ← JSON Response ← Controller ← Service ← Resultado
```

## 🛠️ Desenvolvimento

### Estrutura de Código

- **app.py**: Aplicação principal Flask
- **controllers/gasometria_controller.py**: Lógica de controle de requisições
- **services/ocr_service.py**: Wrapper do módulo OCR com funcionalidades adicionais

### Adicionando Novos Endpoints

1. Adicione rota em `app.py`
2. Implemente método no controller apropriado
3. Se necessário, adicione lógica ao service
4. Atualize documentação

## 📄 Licença

Projeto de POC para fins educacionais e de teste.

## 🤝 Contribuindo

Este é um projeto de demonstração. Para contribuições:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
