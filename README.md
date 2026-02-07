# 🔬 API OCR Gasometria - Python

Extrai automaticamente dados de exames de gasometria arterial usando OCR (Reconhecimento Óptico de Caracteres).

## 🚀 Quick Start

### ⚡ Opção 1: Docker (RECOMENDADO)

**Requisitos:** [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado

```bash
docker-compose up --build
```

✅ **Pronto!** → http://localhost:5000

---

### 💻 Opção 2: Python Local

**Requisitos:**
- Python 3.12+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) instalado (Windows)
  - Linux/Mac: `brew install tesseract` ou `apt install tesseract-ocr`

**⚠️ Windows:** Descomente linhas 11-12 no `ocr-service/main.py` e configure o caminho do Tesseract

```bash
cd backend-core
pip install -r requirements.txt
python run.py
```

✅ **Pronto!** → http://localhost:5000

---

## 📡 Usar a API

### Health Check
```bash
curl http://localhost:5000/health
```

### Analisar Imagem

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

---

## 📊 Parâmetros Extraídos

**12 parâmetros de gasometria:**
- **pH** (6.8 - 7.8)
- **pCO2** (10 - 100 mmHg)
- **pO2** (40 - 500 mmHg)
- **HCO3** (10 - 50 mEq/L)
- **BE** (-20 - 20 mEq/L)
- **SaO2** (50 - 100%)
- **lactato** (0.5 - 20 mmol/L)
- **Na, K, Ca, Cl, Glicose**

---

## 🛠️ Stack Tecnológica

- **Python 3.12** - Linguagem base
- **Flask 3.0** - Framework web
- **OpenCV 4.8+** - Processamento de imagens
- **Tesseract OCR 5.0+** - Motor de OCR
- **NumPy 1.26+** - Computação numérica
- **Docker** - Containerização

---

## 📁 Estrutura do Projeto

```
poc-ocr-gasometria/
├── backend-core/           # API REST Flask
│   ├── app.py             # Aplicação principal
│   ├── run.py             # Script de inicialização
│   ├── controllers/       # Controllers da API
│   ├── services/          # Camada de serviços
│   └── requirements.txt   # Dependências Python
├── ocr-service/           # Módulo OCR (biblioteca Python)
│   ├── main.py            # Core: OCR + extração + validação
│   ├── testar_ocr.py      # Teste CLI
│   └── testar_interativo.py  # Teste interativo
├── docker-compose.yml     # Orquestração Docker
├── curl-examples.md       # 📚 Exemplos completos de uso
└── COMO-TESTAR.md         # 📚 Guia de testes
```

---

## 🧪 Testes

### Teste Rápido (3 comandos)

```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Ver parâmetros disponíveis
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

---

## 📚 Documentação Completa

### 📖 Guias Principais
- **[README-MONOREPO.md](README-MONOREPO.md)** - 📘 **Documentação técnica completa** (stacks, dependências, troubleshooting)
- **[COMO-TESTAR.md](COMO-TESTAR.md)** - Guia passo-a-passo de testes
- **[curl-examples.md](curl-examples.md)** - Todos os exemplos de uso da API

### 📄 Documentação dos Módulos
- **[backend-core/README.md](backend-core/README.md)** - Detalhes da API Flask
- **[ocr-service/README.md](ocr-service/README.md)** - Detalhes do módulo OCR

### 🚀 Scripts de Teste
- **[curl-examples.sh](curl-examples.sh)** - Script Bash executável
- **[curl-examples.ps1](curl-examples.ps1)** - Script PowerShell executável

---

## 🐛 Problemas Comuns

### ❌ "tesseract is not installed or it's not in your PATH"

**Solução Windows (rodando localmente):**
1. Baixe e instale [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. Edite `ocr-service/main.py` e **descomente** as linhas 11-12:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata"
   ```

**No Docker:** Não deve acontecer (Tesseract já vem instalado no container)

### ❌ Erro ao instalar NumPy/OpenCV

**Solução:** Instale compiladores C/C++
- Windows: [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Linux: `sudo apt install build-essential gcc g++`
- macOS: `xcode-select --install`

### ❌ Porta 5000 já em uso

**Solução:** Altere a porta no `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Usar porta 8080
```

Acesse: http://localhost:8080

---

## 💡 Dicas

✅ **Use Docker** - É a forma mais simples, tudo já vem configurado

✅ **Teste com imagens de boa qualidade** - Melhor OCR = resultados mais precisos

✅ **Use `?validar=true`** - Para garantir que valores estão nos ranges esperados

✅ **Use `?debug=true`** - Para ver o texto OCR bruto quando algo não funcionar

---

## 🎯 Próximos Passos

1. ✅ **Rode o Quick Start** acima
2. 📖 **Leia [README-MONOREPO.md](README-MONOREPO.md)** para entender dependências e stacks
3. 🧪 **Teste com suas imagens** usando exemplos em [curl-examples.md](curl-examples.md)
4. 🔧 **Ajuste regex/ranges** em `ocr-service/main.py` conforme necessário

---

**Desenvolvido em Python 🐍 | Rodando em Docker 🐳 | OCR com Tesseract 🔬**
