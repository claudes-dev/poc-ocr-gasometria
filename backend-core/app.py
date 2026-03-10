"""
API Flask completa para processamento OCR de gasometria arterial.
Integra todo o pipeline de OCR em uma aplicação web RESTful.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.gasometria_controller import GasometriaController
import os
from flasgger import Swagger


app = Flask(__name__)

# Configuração do Swagger
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "OCR Gasometria API",
        "description": "API para extração de parâmetros de gasometria arterial via OCR.",
        "version": "1.0.0"
    },
    "basePath": "/",
}
swagger = Swagger(app, template=swagger_template)

# Configuração de CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Instancia o controller
gasometria_controller = GasometriaController()

# ==================== ROTAS DE HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check da API."""
    return jsonify({
        "status": "healthy",
        "service": "OCR Gasometria API",
        "version": "1.0.0"
    }), 200

@app.route('/api/health', methods=['GET'])
def api_health_check():
    """Health check detalhado da API."""
    return gasometria_controller.health_check()

# ==================== ROTAS DE GASOMETRIA ====================

@app.route('/api/gasometria/analisar', methods=['POST'])
def analisar_imagem():
    """
    Analisa uma imagem de gasometria e retorna os valores extraídos.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: imagem
        in: formData
        type: file
        required: true
        description: Imagem da gasometria arterial
      - name: species
        in: formData
        type: string
        required: false
        description: Espécie do animal (ex. dog, cat, human). Também pode ser enviado como query param.
        example: dog
      - name: debug
        in: formData
        type: boolean
        required: false
        description: Se deve retornar o texto OCR bruto no campo texto_ocr
    responses:
      200:
        description: Resultado da análise OCR
        schema:
          type: object
          properties:
            examId:
              type: string
              format: uuid
              example: "7b5f5e3c-2a0f-4c15-9b20-7c7b2d7d9a77"
            species:
              type: string
              example: "dog"
            status:
              type: string
              enum: [OCR_DONE, OCR_ERROR]
              example: "OCR_DONE"
            parametros_encontrados:
              type: integer
              example: 8
            total_parametros:
              type: integer
              example: 12
            extracted:
              type: array
              items:
                type: object
                properties:
                  code:
                    type: string
                    example: "ph"
                  valueRaw:
                    type: string
                    example: "7.38"
                  valueNumber:
                    type: number
                    example: 7.38
                  unit:
                    type: string
                    example: ""
                  confidence:
                    type: number
                    format: float
                    example: 0.9
              example:
                - code: "ph"
                  valueRaw: "7.38"
                  valueNumber: 7.38
                  unit: ""
                  confidence: 0.9
                - code: "pco2"
                  valueRaw: "42.0"
                  valueNumber: 42.0
                  unit: "mmHg"
                  confidence: 0.9
      400:
        description: Erro na requisição ou OCR falhou
        schema:
          type: object
          properties:
            examId:
              type: string
              format: uuid
            species:
              type: string
            status:
              type: string
              example: "OCR_ERROR"
            error:
              type: string
              example: "Nenhuma imagem enviada. Use o campo 'imagem'."
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            examId:
              type: string
              format: uuid
            status:
              type: string
              example: "OCR_ERROR"
            error:
              type: string
              example: "Erro interno ao processar imagem"
    """
    return gasometria_controller.analisar_imagem(request)

@app.route('/api/gasometria/parametros', methods=['GET'])
def listar_parametros():
    """
    Lista todos os parâmetros disponíveis para análise de gasometria.
    ---
    responses:
      200:
        description: Lista de parâmetros
        schema:
          type: object
          example:
            sucesso: true
            parametros:
              - pH
              - PCO2
              - PO2
              - HCO3
              - SaO2
              - Lactato
              - Glicose
      500:
        description: Erro interno
        schema:
          type: object
          example:
            sucesso: false
            erro: "Erro ao obter parâmetros"
    """
    return gasometria_controller.listar_parametros()

@app.route('/api/gasometria/ranges', methods=['GET'])
def obter_ranges():
    """
    Retorna as faixas de valores normais para cada parâmetro.
    ---
    responses:
      200:
        description: Faixas de valores normais
        schema:
          type: object
          example:
            sucesso: true
            ranges:
              pH:
                min: 7.35
                max: 7.45
              PCO2:
                min: 35
                max: 45
              PO2:
                min: 75
                max: 100
              HCO3:
                min: 22
                max: 26
              SaO2:
                min: 95
                max: 100
              Lactato:
                min: 0.5
                max: 2.0
              Glicose:
                min: 70
                max: 100
      500:
        description: Erro interno
        schema:
          type: object
          example:
            sucesso: false
            erro: "Erro ao obter ranges"
    """
    return gasometria_controller.obter_ranges()

# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    """Tratamento de rotas não encontradas."""
    return jsonify({
        "sucesso": False,
        "erro": "Endpoint não encontrado",
        "path": request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Tratamento de erros internos."""
    return jsonify({
        "sucesso": False,
        "erro": "Erro interno do servidor",
        "detalhes": str(error)
    }), 500

# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Iniciando API OCR Gasometria")
    print("=" * 60)
    print("\n📡 Endpoints disponíveis:")
    print("   GET  /health")
    print("   GET  /api/health")
    print("   POST /api/gasometria/analisar")
    print("   GET  /api/gasometria/parametros")
    print("   GET  /api/gasometria/ranges")
    print("\n" + "=" * 60)
    print(f"🌐 Servidor rodando em: http://0.0.0.0:5000")
    print("=" * 60 + "\n")
    
    # Obtém configurações do ambiente
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.run(host=host, port=port, debug=debug_mode)
