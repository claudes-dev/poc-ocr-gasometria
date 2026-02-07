"""
Controller para endpoints de gasometria.
Processa requisições e delega lógica para o serviço OCR.
"""
from flask import jsonify
from services.ocr_service import OcrService
import traceback
import json

class GasometriaController:
    """Controller responsável por gerenciar requisições de gasometria."""
    
    def __init__(self):
        """Inicializa o controller com o serviço OCR."""
        self.ocr_service = OcrService()
    
    def health_check(self):
        """
        Verifica saúde do serviço OCR.
        
        Returns:
            Response JSON com status do serviço
        """
        try:
            health_status = self.ocr_service.check_health()
            return jsonify(health_status), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "erro": str(e)
            }), 503
    
    def analisar_imagem(self, request):
        """
        Analisa uma imagem de gasometria enviada via POST.
        
        Args:
            request: Objeto Flask request contendo arquivo de imagem
            
        Returns:
            Response JSON com resultado da análise
        """
        try:
            # Valida presença do arquivo
            if 'imagem' not in request.files:
                return jsonify({
                    "sucesso": False,
                    "erro": "Nenhuma imagem enviada. Use o campo 'imagem'."
                }), 400
            
            arquivo = request.files['imagem']
            
            # Valida nome do arquivo
            if arquivo.filename == '':
                return jsonify({
                    "sucesso": False,
                    "erro": "Nome de arquivo vazio."
                }), 400
            
            # Log da requisição
            print(f"📷 Processando imagem: {arquivo.filename}")
            
            # Lê bytes da imagem
            imagem_bytes = arquivo.read()
            
            # Obtém parâmetros opcionais
            validar = request.form.get('validar', 'true').lower() == 'true'
            debug = request.form.get('debug', 'false').lower() == 'true'
            
            # Processa imagem através do serviço
            resultado = self.ocr_service.processar_imagem(
                imagem_bytes, 
                validar=validar, 
                debug=debug
            )
            
            # Parse do JSON retornado pelo serviço
            resultado_dict = json.loads(resultado)
            
            # Log do resultado
            if resultado_dict.get("sucesso"):
                print(f"✅ Processamento concluído com sucesso")
                if "valores" in resultado_dict:
                    print(f"📊 Parâmetros extraídos: {len(resultado_dict['valores'])}")
            else:
                print(f"❌ Erro no processamento: {resultado_dict.get('erro', 'Desconhecido')}")
            
            # Retorna resultado
            status_code = 200 if resultado_dict.get("sucesso") else 400
            return jsonify(resultado_dict), status_code
            
        except Exception as e:
            print(f"❌ Erro ao processar imagem: {e}")
            traceback.print_exc()
            return jsonify({
                "sucesso": False,
                "erro": "Erro interno ao processar imagem",
                "detalhes": str(e)
            }), 500
    
    def listar_parametros(self):
        """
        Lista todos os parâmetros disponíveis de gasometria.
        
        Returns:
            Response JSON com lista de parâmetros
        """
        try:
            parametros = self.ocr_service.obter_parametros_disponiveis()
            return jsonify({
                "sucesso": True,
                "parametros": parametros
            }), 200
        except Exception as e:
            return jsonify({
                "sucesso": False,
                "erro": str(e)
            }), 500
    
    def obter_ranges(self):
        """
        Retorna as faixas de valores normais para cada parâmetro.
        
        Returns:
            Response JSON com ranges de validação
        """
        try:
            ranges = self.ocr_service.obter_ranges_validacao()
            return jsonify({
                "sucesso": True,
                "ranges": ranges
            }), 200
        except Exception as e:
            return jsonify({
                "sucesso": False,
                "erro": str(e)
            }), 500
