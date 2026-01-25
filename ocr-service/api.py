"""
API Flask para o serviço de OCR de gasometria.
"""
from flask import Flask, request, jsonify
from main import processar_foto
import traceback

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check."""
    return jsonify({"status": "healthy", "service": "ocr-gasometria"}), 200

@app.route('/processar', methods=['POST'])
def processar():
    """
    Processa uma imagem de gasometria e retorna os valores extraídos.
    
    Espera um arquivo de imagem no campo 'imagem'.
    """
    try:
        # Verifica se há arquivo na requisição
        if 'imagem' not in request.files:
            return jsonify({
                "sucesso": False,
                "erro": "Nenhuma imagem enviada. Use o campo 'imagem'."
            }), 400
        
        arquivo = request.files['imagem']
        
        # Verifica se o arquivo não está vazio
        if arquivo.filename == '':
            return jsonify({
                "sucesso": False,
                "erro": "Nome de arquivo vazio."
            }), 400
        
        # Lê os bytes da imagem
        imagem_bytes = arquivo.read()
        
        # Obtém parâmetros opcionais
        validar = request.form.get('validar', 'true').lower() == 'true'
        debug = request.form.get('debug', 'false').lower() == 'true'
        
        # Processa a imagem
        resultado = processar_foto(imagem_bytes, validar=validar, debug=debug)
        
        # Retorna resultado (já está em formato JSON string)
        return resultado, 200
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        traceback.print_exc()
        return jsonify({
            "sucesso": False,
            "erro": f"Erro interno ao processar imagem: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando serviço OCR Gasometria...")
    print("📡 Endpoints disponíveis:")
    print("   GET  /health - Health check")
    print("   POST /processar - Processar imagem de gasometria")
    app.run(host='0.0.0.0', port=5000, debug=True)
