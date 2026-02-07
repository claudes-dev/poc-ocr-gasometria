# 🧪 Exemplos de Comandos cURL para API OCR Gasometria

Base URL: `http://localhost:5000`

---

## 📍 1. Health Check

Verifica se a API está funcionando.

### cURL
```bash
curl -X GET http://localhost:5000/health
```

### PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing
```

### Resposta Esperada
```json
{
  "service": "OCR Gasometria API",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 📋 2. Listar Parâmetros Disponíveis

Lista todos os parâmetros de gasometria que podem ser extraídos.

### cURL
```bash
curl -X GET http://localhost:5000/api/gasometria/parametros
```

### PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/parametros" -UseBasicParsing
```

### Resposta Esperada
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
    {
      "nome": "pCO2",
      "descricao": "Pressão parcial de CO2",
      "unidade": "mmHg",
      "faixa": "10 - 100"
    },
    ...
  ]
}
```

---

## 🎯 3. Obter Ranges de Validação

Retorna os valores mínimos e máximos aceitos para cada parâmetro.

### cURL
```bash
curl -X GET http://localhost:5000/api/gasometria/ranges
```

### PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/ranges" -UseBasicParsing
```

### Resposta Esperada
```json
{
  "sucesso": true,
  "ranges": {
    "pH": {"min": 6.8, "max": 7.8},
    "pCO2": {"min": 10, "max": 100},
    "pO2": {"min": 40, "max": 500},
    ...
  }
}
```

---

## 🖼️ 4. Analisar Imagem (Básico)

Envia uma imagem para análise OCR.

### cURL
```bash
curl -X POST http://localhost:5000/api/gasometria/analisar \
  -F "imagem=@/caminho/para/imagem.png"
```

### Windows (CMD)
```cmd
curl -X POST http://localhost:5000/api/gasometria/analisar ^
  -F "imagem=@C:\caminho\para\imagem.png"
```

### PowerShell
```powershell
$form = @{
    imagem = Get-Item "C:\caminho\para\imagem.png"
}
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar" `
    -Method Post -Form $form -UseBasicParsing
```

### Resposta Esperada
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
    "lactato": 1.2
  }
}
```

---

## ✅ 5. Analisar com Validação

Analisa a imagem e valida os valores extraídos.

### cURL
```bash
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@/caminho/para/imagem.png"
```

### PowerShell
```powershell
$form = @{ imagem = Get-Item "C:\caminho\para\imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" `
    -Method Post -Form $form -UseBasicParsing
```

### Resposta Esperada
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    "pCO2": 40,
    ...
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

## 🐛 6. Analisar com Debug

Inclui o texto OCR bruto na resposta para debug.

### cURL
```bash
curl -X POST "http://localhost:5000/api/gasometria/analisar?debug=true" \
  -F "imagem=@/caminho/para/imagem.png"
```

### PowerShell
```powershell
$form = @{ imagem = Get-Item "C:\caminho\para\imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?debug=true" `
    -Method Post -Form $form -UseBasicParsing
```

### Resposta Esperada
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    ...
  },
  "texto_ocr": "pH 7.35\npCO2 40 mmHg\npO2 95 mmHg\n..."
}
```

---

## 🚀 7. Analisar Completo (Validação + Debug)

Análise completa com validação e texto OCR.

### cURL
```bash
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" \
  -F "imagem=@/caminho/para/imagem.png"
```

### PowerShell
```powershell
$form = @{ imagem = Get-Item "C:\caminho\para\imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
    -Method Post -Form $form -UseBasicParsing
```

### Resposta Esperada
```json
{
  "sucesso": true,
  "valores": {
    "pH": 7.35,
    "pCO2": 40,
    ...
  },
  "validacao": {
    "pH": true,
    "pCO2": true,
    ...
  },
  "texto_ocr": "pH 7.35\npCO2 40 mmHg\n..."
}
```

---

## 📊 Exemplo Completo PowerShell

```powershell
# Caminho da imagem
$imagemPath = "C:\caminho\para\sua\imagem.png"

# Verificar se existe
if (Test-Path $imagemPath) {
    
    # Criar formulário
    $form = @{
        imagem = Get-Item $imagemPath
    }
    
    # Fazer requisição
    $response = Invoke-WebRequest `
        -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
        -Method Post `
        -Form $form `
        -UseBasicParsing
    
    # Parsear JSON
    $resultado = $response.Content | ConvertFrom-Json
    
    # Exibir formatado
    Write-Host "`n✅ Análise Concluída!" -ForegroundColor Green
    Write-Host "`nValores Extraídos:" -ForegroundColor Cyan
    $resultado.valores | ConvertTo-Json
    
    Write-Host "`nValidação:" -ForegroundColor Cyan
    $resultado.validacao | ConvertTo-Json
    
    if ($resultado.texto_ocr) {
        Write-Host "`nTexto OCR:" -ForegroundColor Cyan
        Write-Host $resultado.texto_ocr
    }
    
} else {
    Write-Host "❌ Imagem não encontrada: $imagemPath" -ForegroundColor Red
}
```

---

## 🔥 Testando Rápido (Todos os Endpoints)

### Bash
```bash
# Health
curl http://localhost:5000/health

# Parâmetros
curl http://localhost:5000/api/gasometria/parametros

# Ranges
curl http://localhost:5000/api/gasometria/ranges

# Analisar (substitua o caminho)
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" \
  -F "imagem=@imagem.png"
```

### PowerShell
```powershell
# Health
curl http://localhost:5000/health

# Parâmetros
curl http://localhost:5000/api/gasometria/parametros

# Ranges
curl http://localhost:5000/api/gasometria/ranges

# Analisar
$form = @{ imagem = Get-Item "imagem.png" }
Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
    -Method Post -Form $form
```

---

## 📝 Formatos de Imagem Aceitos

- PNG
- JPG / JPEG
- Outros formatos suportados pelo OpenCV

---

## ❌ Tratamento de Erros

### Imagem não enviada
```json
{
  "sucesso": false,
  "erro": "Nenhuma imagem foi enviada"
}
```

### Formato inválido
```json
{
  "sucesso": false,
  "erro": "Formato de arquivo não suportado"
}
```

### Erro no OCR
```json
{
  "sucesso": false,
  "erro": "Erro ao processar imagem: [detalhes do erro]"
}
```

---

## 🎯 Dicas

1. **Use `?validar=true`** para ter certeza que os valores estão dentro dos ranges esperados
2. **Use `?debug=true`** quando os valores não estiverem sendo extraídos corretamente
3. **Imagens com melhor qualidade** = resultados mais precisos
4. **Prefira fundo claro** com texto escuro para melhor OCR

---

## 🚀 Quick Start

```bash
# 1. Subir API
docker-compose up

# 2. Testar health
curl http://localhost:5000/health

# 3. Analisar imagem
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@sua_imagem.png"
```

✅ **Pronto para usar!**
