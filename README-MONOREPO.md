# 🔬 Sistema de OCR para Gasometria - Monorepo

Sistema completo para análise automática de exames de gasometria usando OCR (Reconhecimento Óptico de Caracteres).

## 🎯 Visão Geral

Arquitetura **monolítica** onde o backend Flask importa diretamente o módulo OCR como biblioteca Python.

## 📁 Estrutura

```
poc-ocr-gasometria/
├── backend-core/           # API REST Flask + Controllers + Services
│   ├── app.py             # Aplicação Flask principal
│   ├── run.py             # Script de inicialização simplificado
│   ├── controllers/       # Controllers da API
│   ├── services/          # Serviços (ponte com ocr-service)
│   ├── requirements.txt   # Dependências Python
│   ├── Dockerfile         # Container com Flask + OCR
│   └── README.md          # Documentação detalhada
├── ocr-service/           # Módulo Python de OCR (biblioteca)
│   ├── main.py            # Core: preprocessamento + OCR + extração
│   ├── testar_ocr.py      # Teste CLI simples
│   ├── testar_interativo.py  # Teste interativo
│   └── requirements.txt   # Dependências do módulo OCR
├── docker-compose.yml     # Orquestração Docker
├── curl-examples.sh       # Exemplos de teste (Bash)
├── curl-examples.ps1      # Exemplos de teste (PowerShell)
├── curl-examples.md       # Documentação completa de testes
├── COMO-TESTAR.md         # Guia de testes
└── README.md              # README principal simplificado
```

## 🛠️ Stack Completa Necessária

### 🐳 Opção 1: Docker (RECOMENDADO)

Mais simples! Tudo já vem configurado no container.

**Requisitos:**
- **Docker Desktop** 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** 2.0+ (já vem com Docker Desktop)

**Sistemas Operacionais Suportados:**
- Windows 10/11 (com WSL2)
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 10+, etc.)

---

### 💻 Opção 2: Execução Local (sem Docker)

#### Requisitos de Sistema

**1. Python**
- **Versão:** Python 3.12+ (testado com 3.12)
- **Download:** [python.org](https://www.python.org/downloads/)
- ⚠️ **Importante:** Não use Python 3.14+ (incompatibilidade com Gunicorn)

**2. Tesseract OCR**
- **Versão:** 5.0+
- **Idiomas necessários:** `por` (Português) e `eng` (Inglês)

**Downloads por plataforma:**

- **Windows:**
  - [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (RECOMENDADO)
  - Durante instalação, marque: "Additional language data" → Portuguese e English
  - Caminho padrão: `C:\Program Files\Tesseract-OCR\`

- **macOS:**
  ```bash
  brew install tesseract tesseract-lang
  ```

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng
  ```

- **Linux (CentOS/RHEL):**
  ```bash
  sudo yum install tesseract tesseract-langpack-por tesseract-langpack-eng
  ```

**3. Bibliotecas de Sistema (para OpenCV)**

- **Linux:**
  ```bash
  sudo apt install libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1
  ```

- **macOS:** (geralmente já incluídas)

- **Windows:** Não necessário (incluídas no opencv-python)

**4. Compiladores C/C++ (para NumPy)**

- **Windows:**
  - Visual Studio Build Tools ([Download](https://visualstudio.microsoft.com/downloads/))
  - Ou MinGW-w64

- **macOS:**
  ```bash
  xcode-select --install
  ```

- **Linux:**
  ```bash
  sudo apt install build-essential gcc g++
  ```

#### Dependências Python

Definidas em `backend-core/requirements.txt`:

```txt
flask==3.0.0               # Framework web
flask-cors==4.0.0          # CORS para APIs
numpy>=1.26.0,<2.0.0       # Computação numérica
opencv-python>=4.8.0       # Processamento de imagens
pytesseract==0.3.10        # Wrapper Python do Tesseract
gunicorn==21.2.0           # Servidor WSGI de produção
```

## 🚀 Quick Start

### Opção 1: Docker (1 comando!)

```bash
# Subir container
docker-compose up --build

# Em segundo plano (detached)
docker-compose up -d --build
```

✅ **Pronto!** API rodando em: http://localhost:5000

**Parar:**
```bash
docker-compose down
```

---

### Opção 2: Execução Local

#### Windows (PowerShell)

```powershell
# 1. Configurar Tesseract (IMPORTANTE!)
# Edite ocr-service/main.py e descomente as linhas 11-12:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"

# 2. Instalar dependências
cd backend-core
pip install -r requirements.txt

# 3. Rodar
python run.py
```

#### Linux/macOS

```bash
# 1. Tesseract já deve estar no PATH
# (não precisa descomentar nada no main.py)

# 2. Instalar dependências
cd backend-core
pip install -r requirements.txt

# 3. Rodar
python run.py
```

✅ **Pronto!** API rodando em: http://localhost:5000

## 📡 Endpoints da API

### Health Check
```bash
GET /health
```

### Listar Parâmetros
```bash
GET /api/gasometria/parametros
```

### Obter Ranges de Validação
```bash
GET /api/gasometria/ranges
```

### Analisar Imagem
```bash
POST /api/gasometria/analisar?validar=true&debug=false
Content-Type: multipart/form-data
Body: imagem=<arquivo>
```

## 🧪 Testando a API

**Exemplos completos em:**
- [curl-examples.md](curl-examples.md) - Documentação completa
- [curl-examples.sh](curl-examples.sh) - Script Bash
- [curl-examples.ps1](curl-examples.ps1) - Script PowerShell
- [COMO-TESTAR.md](COMO-TESTAR.md) - Guia passo-a-passo

**Teste rápido (PowerShell):**
```powershell
# Health
curl http://localhost:5000/health

# Analisar imagem
$form = @{ imagem = Get-Item "imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" `
    -Method Post -Form $form
```

**Teste rápido (Bash):**
```bash
# Health
curl http://localhost:5000/health

# Analisar imagem
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@imagem.png"
```

## 🔬 Parâmetros Extraídos

| Parâmetro | Descrição | Unidade | Range |
|-----------|-----------|---------|-------|
| pH | Potencial hidrogeniônico | - | 6.8 - 7.8 |
| pCO2 | Pressão parcial de CO2 | mmHg | 10 - 100 |
| pO2 | Pressão parcial de O2 | mmHg | 40 - 500 |
| HCO3 | Bicarbonato | mEq/L | 10 - 50 |
| BE | Base Excess | mEq/L | -20 - 20 |
| SaO2 | Saturação de O2 | % | 50 - 100 |
| lactato | Lactato | mmol/L | 0.5 - 20 |
| Na | Sódio | mEq/L | 100 - 180 |
| K | Potássio | mEq/L | 2.0 - 8.0 |
| Ca | Cálcio | mmol/L | 0.5 - 3.0 |
| Cl | Cloreto | mEq/L | 80 - 130 |
| Glicose | Glicose | mg/dL | 20 - 600 |

## 🏗️ Arquitetura

**Monolítica:**
- Container único executa Flask API
- `ocr-service` é importado como módulo Python (não é serviço HTTP separado)
- Simplifica deploy e desenvolvimento para POC

**Fluxo de Requisição:**
```
Cliente → Flask API (backend-core)
            ↓
       Controller (gasometria_controller.py)
            ↓
       Service (ocr_service.py)
            ↓
       OCR Module (ocr-service/main.py)
            ↓
       Tesseract OCR
```

## 📚 Documentação Adicional

- **[README.md](README.md)** - Guia simplificado de início rápido
- **[backend-core/README.md](backend-core/README.md)** - Detalhes da API Flask
- **[ocr-service/README.md](ocr-service/README.md)** - Detalhes do módulo OCR
- **[COMO-TESTAR.md](COMO-TESTAR.md)** - Guia completo de testes
- **[curl-examples.md](curl-examples.md)** - Exemplos de uso da API

## 🐛 Troubleshooting

### Erro: "tesseract is not installed or it's not in your PATH"

**No Docker:** Não deve acontecer (Tesseract já está instalado no container)

**Rodando localmente:**
- **Windows:** Descomente as linhas 11-12 no `ocr-service/main.py` e ajuste o caminho
- **Linux/macOS:** Verifique se Tesseract está instalado: `tesseract --version`

### Erro ao instalar NumPy/OpenCV

**Precisa de compiladores C/C++:**
- Windows: Instale Visual Studio Build Tools
- Linux: `sudo apt install build-essential gcc g++`
- macOS: `xcode-select --install`

### Container não inicia

```bash
# Ver logs
docker-compose logs -f

# Recriar do zero
docker-compose down
docker-compose up --build --force-recreate
```

### Porta 5000 já em uso

Edite `docker-compose.yml` e altere:
```yaml
ports:
  - "8080:5000"  # Usar porta 8080 no host
```

## 💡 Próximos Passos

1. **Teste com suas imagens** de gasometria
2. **Ajuste regex** em `ocr-service/main.py` se necessário
3. **Calibre ranges** em `RANGES_GASOMETRIA` para seus padrões
4. **Melhore preprocessamento** em `preprocessar_imagem()` se OCR não estiver preciso

## 📝 Licença

Projeto de prova de conceito (POC).
