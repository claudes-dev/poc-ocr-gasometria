# 🔬 API OCR Gasometria - Sistema Completo

Extrai automaticamente dados de exames de gasometria arterial usando OCR (Reconhecimento Óptico de Caracteres).

> 💡 **TL;DR:** `docker-compose up --build` e pronto! API em http://localhost:5000

---

## 📑 Índice

- [🚀 Quick Start](#-quick-start)
- [📡 Usando a API](#-usando-a-api)
- [🛠️ Stack Completa](#️-stack-completa-necessária)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [📊 Parâmetros Extraídos](#-parâmetros-extraídos)
- [🏗️ Arquitetura](#️-arquitetura)
- [🧪 Testando](#-testando)
- [🐛 Troubleshooting](#-troubleshooting)
- [📚 Documentação Adicional](#-documentação-adicional)

---

## 🚀 Quick Start

### ⚡ Opção 1: Docker (RECOMENDADO)

**Requisito:** [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado

```bash
# Subir container
docker-compose up --build

# Ou em segundo plano (detached)
docker-compose up -d --build
```

✅ **Pronto!** API rodando em: http://localhost:5000

**Parar:**
```bash
docker-compose down
```

---

### 💻 Opção 2: Python Local

**Pré-requisitos:**
- Python 3.12+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) instalado

**⚠️ Windows:** Descomente linhas 11-12 no `ocr-service/main.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
```

**Executar:**
```bash
cd backend-core
pip install -r requirements.txt
python run.py
```

✅ **Pronto!** API rodando em: http://localhost:5000

---

## 📡 Usando a API

### Health Check
```bash
curl http://localhost:5000/health
```

### Analisar Imagem de Gasometria

**Bash/Linux/Mac:**
```bash
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@imagem.png"
```

**PowerShell/Windows:**
```powershell
$form = @{ imagem = Get-Item "imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" `
    -Method Post -Form $form
```

### Outros Endpoints

```bash
# Listar parâmetros disponíveis
GET /api/gasometria/parametros

# Obter ranges de validação
GET /api/gasometria/ranges
```

**📚 Mais exemplos:** Veja [curl-examples.md](curl-examples.md) e [COMO-TESTAR.md](COMO-TESTAR.md)

---

## 🛠️ Stack Completa Necessária

### 🐳 Opção 1: Docker (tudo incluído)

**Requisitos:**
- **Docker Desktop** 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** 2.0+ (já vem com Docker Desktop)

**Sistemas Suportados:**
- Windows 10/11 (com WSL2)
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 10+, etc.)

---

### 💻 Opção 2: Execução Local

#### 1. Python
- **Versão:** Python 3.12+
- **Download:** [python.org](https://www.python.org/downloads/)
- ⚠️ **Não use Python 3.14+** (incompatibilidade com Gunicorn)

#### 2. Tesseract OCR
- **Versão:** 5.0+
- **Idiomas:** `por` (Português) e `eng` (Inglês)

**Downloads por plataforma:**

<details>
<summary><b>Windows</b></summary>

- [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (RECOMENDADO)
- Durante instalação: marque "Additional language data" → Portuguese e English
- Caminho padrão: `C:\Program Files\Tesseract-OCR\`
</details>

<details>
<summary><b>macOS</b></summary>

```bash
brew install tesseract tesseract-lang
```
</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng
```
</details>

<details>
<summary><b>Linux (CentOS/RHEL)</b></summary>

```bash
sudo yum install tesseract tesseract-langpack-por tesseract-langpack-eng
```
</details>

#### 3. Bibliotecas de Sistema (para OpenCV)

**Linux:**
```bash
sudo apt install libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1
```

**macOS/Windows:** Geralmente já incluídas

#### 4. Compiladores C/C++ (para NumPy)

**Windows:**
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

**macOS:**
```bash
xcode-select --install
```

**Linux:**
```bash
sudo apt install build-essential gcc g++
```

#### 5. Dependências Python

Definidas em `backend-core/requirements.txt`:

```txt
flask==3.0.0               # Framework web
flask-cors==4.0.0          # CORS para APIs
numpy>=1.26.0,<2.0.0       # Computação numérica
opencv-python>=4.8.0       # Processamento de imagens
pytesseract==0.3.10        # Wrapper Python do Tesseract
gunicorn==21.2.0           # Servidor WSGI de produção
```

---

## 📁 Estrutura do Projeto

```
poc-ocr-gasometria/
├── backend-core/              # API REST Flask
│   ├── app.py                # Aplicação Flask principal
│   ├── run.py                # Script de inicialização
│   ├── controllers/          # Controllers da API
│   │   └── gasometria_controller.py
│   ├── services/             # Camada de serviços
│   │   └── ocr_service.py   # Ponte com módulo OCR
│   ├── requirements.txt      # Dependências Python
│   ├── Dockerfile            # Container Docker
│   └── README.md             # Detalhes da API
│
├── ocr-service/              # Módulo OCR (biblioteca Python)
│   ├── main.py              # Core: preprocessamento + OCR + extração
│   ├── testar_ocr.py        # Teste CLI simples
│   ├── testar_interativo.py # Teste interativo
│   └── requirements.txt      # Dependências do módulo
│
├── docker-compose.yml        # Orquestração Docker
├── curl-examples.sh          # Scripts de teste (Bash)
├── curl-examples.ps1         # Scripts de teste (PowerShell)
├── curl-examples.md          # 📚 Documentação completa de testes
├── COMO-TESTAR.md            # 📚 Guia passo-a-passo
└── README.md                 # 📖 Este arquivo
```

### 🎯 Arquitetura: Monolítica

- Container único executa Flask API
- `ocr-service` é importado como módulo Python (não é serviço HTTP separado)
- Simplifica deploy e desenvolvimento para POC

---

## 📊 Parâmetros Extraídos

**12 parâmetros de gasometria arterial:**

| Parâmetro | Descrição | Unidade | Range Normal |
|-----------|-----------|---------|--------------|
| **pH** | Potencial hidrogeniônico | - | 6.8 - 7.8 |
| **pCO2** | Pressão parcial de CO2 | mmHg | 10 - 100 |
| **pO2** | Pressão parcial de O2 | mmHg | 40 - 500 |
| **HCO3** | Bicarbonato | mEq/L | 10 - 50 |
| **BE** | Base Excess | mEq/L | -20 - 20 |
| **SaO2** | Saturação de O2 | % | 50 - 100 |
| **lactato** | Lactato | mmol/L | 0.5 - 20 |
| **Na** | Sódio | mEq/L | 100 - 180 |
| **K** | Potássio | mEq/L | 2.0 - 8.0 |
| **Ca** | Cálcio | mmol/L | 0.5 - 3.0 |
| **Cl** | Cloreto | mEq/L | 80 - 130 |
| **Glicose** | Glicose | mg/dL | 20 - 600 |

---

## 🏗️ Arquitetura

### Fluxo de Requisição

```
Cliente (cURL/Postman/App)
    ↓
Flask API (backend-core/app.py)
    ↓
Controller (gasometria_controller.py)
    ↓
Service (ocr_service.py)
    ↓
OCR Module (ocr-service/main.py)
    ↓ preprocessamento → OCR → extração → validação
Tesseract OCR Engine
    ↓
Resposta JSON
```

### Camadas

1. **API Layer** - Flask, CORS, rotas
2. **Controller Layer** - Validação de input, processamento HTTP
3. **Service Layer** - Lógica de negócio
4. **OCR Module** - Processamento de imagem e extração
5. **Tesseract Engine** - OCR proprietário

---

## 🧪 Testando

### Teste Rápido (3 comandos)

```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Listar parâmetros
curl http://localhost:5000/api/gasometria/parametros

# 3. Analisar imagem
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@sua_imagem.png"
```

### Resposta Exemplo

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
    "pO2": true,
    ...
  }
}
```

### Mais Exemplos

- **[curl-examples.md](curl-examples.md)** - Documentação completa com todos os endpoints
- **[curl-examples.sh](curl-examples.sh)** - Script Bash executável
- **[curl-examples.ps1](curl-examples.ps1)** - Script PowerShell executável
- **[COMO-TESTAR.md](COMO-TESTAR.md)** - Guia passo-a-passo detalhado

---

## 🐛 Troubleshooting

### ❌ "tesseract is not installed or it's not in your PATH"

**No Docker:** Não deve acontecer (Tesseract já instalado no container)

**Rodando localmente:**

**Windows:**
1. Instale [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. Edite `ocr-service/main.py` e **descomente** linhas 11-12:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
   ```

**Linux/macOS:**
```bash
# Verificar se está instalado
tesseract --version

# Se não estiver, instalar
# Ubuntu/Debian:
sudo apt install tesseract-ocr tesseract-ocr-por

# macOS:
brew install tesseract tesseract-lang
```

---

### ❌ Erro ao instalar NumPy/OpenCV

**Causa:** Falta compilador C/C++

**Solução por plataforma:**

**Windows:**
- Instale [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Ou use Docker (já vem configurado)

**Linux:**
```bash
sudo apt install build-essential gcc g++
```

**macOS:**
```bash
xcode-select --install
```

---

### ❌ Container não inicia / build falha

```bash
# Ver logs completos
docker-compose logs -f

# Limpar e recriar do zero
docker-compose down
docker system prune -a  # Remove imagens antigas
docker-compose up --build --force-recreate
```

---

### ❌ Porta 5000 já em uso

**Windows (PowerShell):**
```powershell
# Ver o que está usando a porta
Get-NetTCPConnection -LocalPort 5000
```

**Solução:** Altere a porta no `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Usar porta 8080 no host
```

Acesse: http://localhost:8080

---

### ❌ OCR não extrai valores corretamente

**Dicas:**
1. Use `?debug=true` para ver o texto OCR bruto:
   ```bash
   curl -X POST "http://localhost:5000/api/gasometria/analisar?debug=true" \
     -F "imagem=@imagem.png"
   ```

2. **Melhore a qualidade da imagem:**
   - Resolução mínima: 300 DPI
   - Texto deve estar nítido
   - Bom contraste (fundo claro, texto escuro)
   - Sem rotação/inclinação

3. **Ajuste o preprocessamento** em `ocr-service/main.py`:
   - Função `preprocessar_imagem()`
   - Ajuste CLAHE, threshold, morfologia

4. **Ajuste regex** em `ocr-service/main.py`:
   - Função `extrair_valores()`
   - Adicione variações de padrões OCR comuns

---

## 📚 Documentação Adicional

### 📖 Guias e Tutoriais
- **[COMO-TESTAR.md](COMO-TESTAR.md)** - Guia completo passo-a-passo de testes
- **[curl-examples.md](curl-examples.md)** - Todos os exemplos de uso da API
- **[backend-core/README.md](backend-core/README.md)** - Documentação técnica do backend
- **[ocr-service/README.md](ocr-service/README.md)** - Documentação do módulo OCR

### 🚀 Scripts Prontos
- **[curl-examples.sh](curl-examples.sh)** - Script Bash com todos os testes
- **[curl-examples.ps1](curl-examples.ps1)** - Script PowerShell com todos os testes

---

## 💡 Dicas de Uso

✅ **Use Docker** - É plug-and-play, tudo já configurado

✅ **Imagens de qualidade** - Melhor OCR = resultados mais precisos

✅ **Use `?validar=true`** - Garante valores dentro dos ranges esperados

✅ **Use `?debug=true`** - Para diagnosticar problemas de extração

✅ **Calibre os ranges** - Ajuste `RANGES_GASOMETRIA` em `ocr-service/main.py` conforme necessário

---

## 🎯 Próximos Passos

1. ✅ **Rode o Quick Start** e teste os endpoints
2. 🧪 **Teste com suas imagens** reais de gasometria
3. 🔧 **Ajuste regex/ranges** em `ocr-service/main.py` se necessário
4. 📈 **Melhore preprocessamento** se OCR não estiver preciso
5. 🚀 **Integre com seu sistema** usando a API REST

---

## 🛠️ Stack Tecnológica Resumida

| Componente | Tecnologia | Versão |
|------------|-----------|--------|
| **Linguagem** | Python | 3.12+ |
| **Framework Web** | Flask | 3.0.0 |
| **Processamento Imagem** | OpenCV | 4.8+ |
| **Motor OCR** | Tesseract | 5.0+ |
| **Computação Numérica** | NumPy | 1.26+ |
| **Servidor Produção** | Gunicorn | 21.2.0 |
| **Containerização** | Docker | 20.10+ |
| **CORS** | Flask-CORS | 4.0.0 |

---

## 📝 Licença

Projeto de prova de conceito (POC) para extração automatizada de dados de gasometria.

---

## 🤝 Contribuindo

Para melhorias:
1. Ajuste padrões regex em `ocr-service/main.py`
2. Melhore preprocessamento de imagens
3. Adicione novos parâmetros em `RANGES_GASOMETRIA`
4. Compartilhe imagens de teste para calibração

---

**Desenvolvido em Python 🐍 | Rodando em Docker 🐳 | OCR com Tesseract 🔬**

**Status:** ✅ Pronto para uso | 🚀 Em produção | 📊 POC validado
