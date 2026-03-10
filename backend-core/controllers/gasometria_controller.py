"""
Controller para endpoints de gasometria.
Processa requisições e delega lógica para o serviço OCR.
"""
from flask import jsonify
from services.ocr_service import OcrService
import traceback
import json
import uuid

# Unidades por parâmetro
_UNITS = {
    "pH": "", "pCO2": "mmHg", "pO2": "mmHg", "HCO3": "mEq/L",
    "BE": "mEq/L", "SaO2": "%", "lactato": "mmol/L",
    "Na": "mEq/L", "K": "mEq/L", "Ca": "mmol/L", "Cl": "mEq/L", "Glicose": "mg/dL"
}

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
    
    def _transform_result(self, resultado_dict, species):
        """Transforma resultado OCR interno no formato padronizado da API."""
        exam_id = str(uuid.uuid4())
        species = species or "unknown"

        if not resultado_dict.get("sucesso"):
            return {
                "examId": exam_id,
                "species": species,
                "status": "OCR_ERROR",
                "error": resultado_dict.get("erro", "Erro desconhecido")
            }, 400

        dados = resultado_dict.get("dados", {})
        extracted = []

        for param, info in dados.items():
            if isinstance(info, dict):
                valor = info.get("valor")
                valido = info.get("valido")
            else:
                valor = info
                valido = None

            if valor is None:
                continue

            confidence = 0.90 if valido is True else (0.65 if valido is False else 0.75)

            extracted.append({
                "code": param.lower(),
                "valueRaw": str(valor),
                "valueNumber": valor,
                "unit": _UNITS.get(param, ""),
                "confidence": confidence
            })

        return {
            "examId": exam_id,
            "species": species,
            "status": "OCR_DONE",
            "parametros_encontrados": len(extracted),
            "total_parametros": len(dados),
            "extracted": extracted
        }, 200

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
                    "examId": str(uuid.uuid4()),
                    "status": "OCR_ERROR",
                    "error": "Nenhuma imagem enviada. Use o campo 'imagem'."
                }), 400
            
            arquivo = request.files['imagem']
            
            # Valida nome do arquivo
            if arquivo.filename == '':
                return jsonify({
                    "examId": str(uuid.uuid4()),
                    "status": "OCR_ERROR",
                    "error": "Nome de arquivo vazio."
                }), 400
            
            # Log da requisição
            print(f"📷 Processando imagem: {arquivo.filename}")
            
            # Lê bytes da imagem
            imagem_bytes = arquivo.read()
            
            # Obtém parâmetros opcionais
            species = request.form.get('species') or request.args.get('species', 'unknown')
            debug = request.form.get('debug', 'false').lower() == 'true'
            
            # Processa sempre com validar=True para calcular confidence
            resultado = self.ocr_service.processar_imagem(
                imagem_bytes,
                validar=True,
                debug=debug
            )
            
            # Parse do JSON retornado pelo serviço
            resultado_dict = json.loads(resultado)
            
            # Log do resultado
            if resultado_dict.get("sucesso"):
                dados = resultado_dict.get("dados", {})
                encontrados = sum(1 for v in dados.values()
                                  if (isinstance(v, dict) and v.get("valor") is not None)
                                  or (not isinstance(v, dict) and v is not None))
                print(f"✅ Processamento concluído — {encontrados} parâmetros extraídos")
            else:
                print(f"❌ Erro no processamento: {resultado_dict.get('erro', 'Desconhecido')}")

            if debug:
                resultado_dict["texto_ocr"] = resultado_dict.get("texto_ocr")

            resposta, status_code = self._transform_result(resultado_dict, species)

            if debug and "texto_ocr" in resultado_dict:
                resposta["texto_ocr"] = resultado_dict["texto_ocr"]

            return jsonify(resposta), status_code
            
        except Exception as e:
            print(f"❌ Erro ao processar imagem: {e}")
            traceback.print_exc()
            return jsonify({
                "examId": str(uuid.uuid4()),
                "status": "OCR_ERROR",
                "error": "Erro interno ao processar imagem"
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
