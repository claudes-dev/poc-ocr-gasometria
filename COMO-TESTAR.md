# 🧪 Como Testar a API de Gasometria

## 📦 Pré-requisitos

- Docker Desktop instalado e rodando
- OU Python 3.12+ instalado localmente

---

## 🚀 Opção 1: Rodar com Docker (Recomendado)

### 1. Subir o container
```bash
docker-compose up
```

**Primeira vez?** Vai demorar ~3 minutos instalando Tesseract, GCC, etc.  
**Próximas vezes?** Leva ~5 segundos! 🚀

### 2. Verificar se subiu
```bash
# PowerShell
Invoke-WebRequest http://localhost:5000/health

# Bash/CMD
curl http://localhost:5000/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "ocr": "tesseract_disponivel",
  "versao": "1.0.0"
}
```

### 3. Testar análise de imagem

#### PowerShell:
```powershell
$form = @{
    imagem = Get-Item "caminho\para\imagem.png"
}

Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
    -Method Post -Form $form | Select-Object -ExpandProperty Content
```

#### CMD/Bash:
```bash
curl -X POST http://localhost:5000/api/gasometria/analisar?validar=true `
  -F "imagem=@caminho/para/imagem.png"
```

### 4. Parar o container
```bash
docker-compose down
```

---

## 💻 Opção 2: Rodar com Python Direto (Desenvolvimento)

### 1. Instalar dependências
```bash
cd backend-core
pip install -r requirements.txt
```

**⚠️ Importante:** Você precisa ter o Tesseract OCR instalado:
- Windows: [UB-Mannheim Installer](https://github.com/UB-Mannheim/tesseract/wiki)
- Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-por`
- Mac: `brew install tesseract tesseract-lang`

### 2. Rodar aplicação
```bash
python run.py
```

Ou com Gunicorn (produção):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Testar igual ao Docker
Use os mesmos comandos da seção anterior! ✅

---

## 📍 Endpoints Disponíveis

### `GET /health`
Verifica status da API e do Tesseract.

### `GET /api/gasometria/parametros`
Lista todos os parâmetros de gasometria disponíveis.

**Resposta:**
```json
{
  "sucesso": true,
  "parametros": ["pH", "pCO2", "pO2", "HCO3", "BE", "SatO2", "Lactato"]
}
```

### `GET /api/gasometria/ranges`
Retorna os ranges de validação para cada parâmetro.

**Resposta:**
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

### `POST /api/gasometria/analisar`
Analisa uma imagem de gasometria e extrai valores.

**Parâmetros:**
- `imagem` (form-data): arquivo de imagem (PNG, JPG, JPEG)
- `?validar=true` (query): valida os valores extraídos
- `?debug=true` (query): inclui o texto OCR bruto

**Resposta de sucesso:**
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    "pCO2": 40,
    "pO2": 95,
    "HCO3": 24,
    "BE": 0,
    "SatO2": 98,
    "Lactato": 1.2
  },
  "validacao": {
    "pH": true,
    "pCO2": true,
    ...
  }
}
```

---

## 🐛 Troubleshooting

### "Docker container não inicia"
1. Verifique se o Docker Desktop está rodando
2. Verifique se a porta 5000 está livre: `netstat -an | findstr :5000`
3. Limpe e rebuild: `docker-compose down && docker-compose up --build`

### "ModuleNotFoundError: No module named 'main'"
- Verifique se o diretório `ocr-service/` está presente
- Rebuilde o container: `docker-compose up --build`

### "Tesseract not found"
Se rodando localmente (sem Docker):
1. Instale o Tesseract OCR
2. Configure o path em `ocr-service/main.py` nas linhas:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
```

### "Imagem não reconhecida"
- A imagem deve ter boa qualidade e resolução
- Texto deve estar legível
- Preferência por fundo claro e texto escuro

---

## 📊 Exemplo Completo (PowerShell)

```powershell
# 1. Subir API
docker-compose up -d

# 2. Aguardar 5 segundos
Start-Sleep -Seconds 5

# 3. Health check
Invoke-WebRequest http://localhost:5000/health

# 4. Ver parâmetros disponíveis
Invoke-WebRequest http://localhost:5000/api/gasometria/parametros

# 5. Analisar imagem
$resultado = Invoke-WebRequest `
    -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" `
    -Method Post `
    -Form @{ imagem = Get-Item "teste.png" }

$resultado.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# 6. Parar
docker-compose down
```

---

## 🎯 Resumo Rápido

```bash
# 🐳 Docker (jeito mais fácil)
docker-compose up          # Subir
docker-compose down        # Parar
docker-compose logs        # Ver logs

# 🐍 Python direto
cd backend-core
python run.py             # Rodar

# ✅ Testar
curl http://localhost:5000/health
```

**Dúvidas?** Verifique os logs: `docker-compose logs -f`
