"""
🚀 Teste Rápido da API - Versão Simplificada
Rode: python test_simple.py
"""
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "OCR Gasometria API",
        "version": "1.0.0"
    })

@app.route('/api/gasometria/analisar', methods=['POST'])
def analisar():
    return jsonify({
        "sucesso": True,
        "mensagem": "API funcionando! (OCR será integrado depois)",
        "valores": {
            "pH": 7.35,
            "pCO2": 45.0,
            "pO2": 98.0,
            "HCO3": 24.0,
            "BE": -2.0,
            "SaO2": 98.0
        }
    })

@app.route('/api/gasometria/parametros')
def parametros():
    return jsonify({
        "sucesso": True,
        "parametros": ["pH", "pCO2", "pO2", "HCO3", "BE", "SaO2"]
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 API OCR Gasometria - TESTE SIMPLIFICADO")
    print("="*60)
    print("\n🌐 Rodando em: http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /health")
    print("   POST /api/gasometria/analisar")
    print("   GET  /api/gasometria/parametros")
    print("\n💡 Teste com: curl http://localhost:5000/health")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
