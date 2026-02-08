"""
API Flask completa para processamento OCR de gasometria arterial.
Integra todo o pipeline de OCR em uma aplicação web RESTful.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers.gasometria_controller import GasometriaController
import os

app = Flask(__name__)

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
    
    Aceita:
    - multipart/form-data com campo 'imagem'
    - Parâmetros opcionais: validar (true/false), debug (true/false)
    """
    return gasometria_controller.analisar_imagem(request)

@app.route('/api/gasometria/parametros', methods=['GET'])
def listar_parametros():
    """Lista todos os parâmetros disponíveis para análise de gasometria."""
    return gasometria_controller.listar_parametros()

@app.route('/api/gasometria/ranges', methods=['GET'])
def obter_ranges():
    """Retorna as faixas de valores normais para cada parâmetro."""
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
