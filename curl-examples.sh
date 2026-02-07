#!/bin/bash
# Exemplos de curl para testar a API de OCR Gasometria
# URL base: http://localhost:5000

echo "=========================================="
echo "  Testes da API OCR Gasometria"
echo "=========================================="

# 1. Health Check
echo ""
echo "1️⃣  GET /health - Verifica status da API"
curl -X GET http://localhost:5000/health

# 2. Listar Parâmetros
echo ""
echo ""
echo "2️⃣  GET /api/gasometria/parametros - Lista parâmetros disponíveis"
curl -X GET http://localhost:5000/api/gasometria/parametros

# 3. Obter Ranges de Validação
echo ""
echo ""
echo "3️⃣  GET /api/gasometria/ranges - Ranges de validação"
curl -X GET http://localhost:5000/api/gasometria/ranges

# 4. Analisar Imagem (substitua o caminho da imagem)
echo ""
echo ""
echo "4️⃣  POST /api/gasometria/analisar - Análise de imagem"
echo "   (substitua 'imagem.png' pelo caminho real da sua imagem)"
curl -X POST http://localhost:5000/api/gasometria/analisar \
  -F "imagem=@imagem.png"

# 5. Analisar com Validação
echo ""
echo ""
echo "5️⃣  POST /api/gasometria/analisar?validar=true - Com validação"
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true" \
  -F "imagem=@imagem.png"

# 6. Analisar com Debug (mostra texto OCR)
echo ""
echo ""
echo "6️⃣  POST /api/gasometria/analisar?debug=true - Com debug"
curl -X POST "http://localhost:5000/api/gasometria/analisar?debug=true" \
  -F "imagem=@imagem.png"

# 7. Analisar com Validação + Debug
echo ""
echo ""
echo "7️⃣  POST /api/gasometria/analisar?validar=true&debug=true - Completo"
curl -X POST "http://localhost:5000/api/gasometria/analisar?validar=true&debug=true" \
  -F "imagem=@imagem.png"

echo ""
echo ""
echo "=========================================="
echo "  Testes concluídos!"
echo "=========================================="
