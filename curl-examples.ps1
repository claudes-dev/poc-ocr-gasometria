# Exemplos de curl/Invoke-WebRequest para testar a API de OCR Gasometria
# URL base: http://localhost:5000

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Testes da API OCR Gasometria" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Health Check
Write-Host "`n1️⃣  GET /health - Verifica status da API" -ForegroundColor Yellow
curl -X GET http://localhost:5000/health

# Alternativa PowerShell nativa:
# Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing

# 2. Listar Parâmetros
Write-Host "`n`n2️⃣  GET /api/gasometria/parametros - Lista parâmetros disponíveis" -ForegroundColor Yellow
curl -X GET http://localhost:5000/api/gasometria/parametros

# Alternativa PowerShell:
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/parametros" -UseBasicParsing

# 3. Obter Ranges de Validação
Write-Host "`n`n3️⃣  GET /api/gasometria/ranges - Ranges de validação" -ForegroundColor Yellow
curl -X GET http://localhost:5000/api/gasometria/ranges

# Alternativa PowerShell:
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/ranges" -UseBasicParsing

# 4. Analisar Imagem (substitua o caminho da imagem)
Write-Host "`n`n4️⃣  POST /api/gasometria/analisar - Análise de imagem" -ForegroundColor Yellow
Write-Host "   (substitua 'imagem.png' pelo caminho real da sua imagem)" -ForegroundColor Gray

# Com curl:
curl -X POST http://localhost:5000/api/gasometria/analisar `
  -F "imagem=@imagem.png"

# Alternativa PowerShell:
# $form = @{ imagem = Get-Item "imagem.png" }
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar" -Method Post -Form $form

# 5. Analisar com Validação
Write-Host "`n`n5️⃣  POST /api/gasometria/analisar?validar=true - Com validação" -ForegroundColor Yellow

# Com curl:
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" `
  -F "imagem=@imagem.png"

# Alternativa PowerShell:
# $form = @{ imagem = Get-Item "imagem.png" }
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true" -Method Post -Form $form

# 6. Analisar com Debug (mostra texto OCR)
Write-Host "`n`n6️⃣  POST /api/gasometria/analisar?debug=true - Com debug" -ForegroundColor Yellow

# Com curl:
curl -X POST "http://localhost:5000/api/gasometria/analisar?debug=true" `
  -F "imagem=@imagem.png"

# Alternativa PowerShell:
# $form = @{ imagem = Get-Item "imagem.png" }
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?debug=true" -Method Post -Form $form

# 7. Analisar com Validação + Debug
Write-Host "`n`n7️⃣  POST /api/gasometria/analisar?validar=true&debug=true - Completo" -ForegroundColor Yellow

# Com curl:
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
  -F "imagem=@imagem.png"

# Alternativa PowerShell:
# $form = @{ imagem = Get-Item "imagem.png" }
# Invoke-WebRequest -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" -Method Post -Form $form

Write-Host "`n`n==========================================" -ForegroundColor Cyan
Write-Host "  📝 Exemplo Completo PowerShell" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host @'

# Exemplo completo com PowerShell:
$imagemPath = "C:\caminho\para\sua\imagem.png"

# 1. Verificar se a imagem existe
if (Test-Path $imagemPath) {
    
    # 2. Criar formulário multipart
    $form = @{
        imagem = Get-Item $imagemPath
    }
    
    # 3. Fazer requisição
    $response = Invoke-WebRequest `
        -Uri "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" `
        -Method Post `
        -Form $form `
        -UseBasicParsing
    
    # 4. Exibir resultado formatado
    $resultado = $response.Content | ConvertFrom-Json
    $resultado | ConvertTo-Json -Depth 10
    
} else {
    Write-Host "❌ Imagem não encontrada: $imagemPath" -ForegroundColor Red
}

'@ -ForegroundColor White

Write-Host "`n`n==========================================" -ForegroundColor Cyan
Write-Host "  ✅ Comandos prontos para uso!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
