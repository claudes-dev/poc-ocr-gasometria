"""
Serviço OCR para processamento de imagens de gasometria.
Wrapper em torno do código principal de OCR com funcionalidades adicionais.
"""
import sys
import os

# Adiciona o diretório ocr-service ao path para importar o módulo main
# No Docker: /app/ocr-service/main.py
# Local: ../ocr-service/main.py (relativo ao backend-core)
ocr_service_path = os.path.join(os.path.dirname(__file__), '..', 'ocr-service')
if not os.path.exists(ocr_service_path):
    # Fallback para ambiente local (fora do container)
    ocr_service_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ocr-service')

sys.path.insert(0, ocr_service_path)

try:
    from main import processar_foto, RANGES_GASOMETRIA
    import pytesseract
except ImportError as e:
    print(f"❌ Erro ao importar módulos do OCR: {e}")
    print(f"📁 Path do OCR service: {ocr_service_path}")
    print(f"📂 Conteúdo do diretório: {os.listdir(ocr_service_path) if os.path.exists(ocr_service_path) else 'diretório não existe'}")
    print(f"🔍 sys.path: {sys.path[:3]}")
    raise

class OcrService:
    """Serviço de OCR para processamento de gasometrias."""
    
    def __init__(self):
        """Inicializa o serviço OCR."""
        self.ranges_gasometria = RANGES_GASOMETRIA
    
    def check_health(self):
        """
        Verifica se o serviço está operacional.
        
        Returns:
            Dict com status do serviço
        """
        try:
            # Tenta obter versão do Tesseract
            versao = pytesseract.get_tesseract_version()
            
            return {
                "status": "healthy",
                "service": "OCR Gasometria",
                "tesseract_version": str(versao),
                "ocr_ready": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": "OCR Gasometria",
                "ocr_ready": False,
                "erro": str(e)
            }
    
    def processar_imagem(self, imagem_bytes, validar=True, debug=False):
        """
        Processa uma imagem de gasometria.
        
        Args:
            imagem_bytes: Bytes da imagem
            validar: Se deve validar valores extraídos
            debug: Se deve incluir informações de debug
            
        Returns:
            String JSON com resultado do processamento
        """
        return processar_foto(imagem_bytes, validar=validar, debug=debug)
    
    def obter_parametros_disponiveis(self):
        """
        Retorna lista de parâmetros disponíveis para análise.
        
        Returns:
            Lista de dicts com informações dos parâmetros
        """
        parametros = [
            {
                "nome": "pH",
                "descricao": "Potencial hidrogeniônico",
                "unidade": "",
                "faixa": f"{self.ranges_gasometria['pH'][0]} - {self.ranges_gasometria['pH'][1]}"
            },
            {
                "nome": "pCO2",
                "descricao": "Pressão parcial de CO2",
                "unidade": "mmHg",
                "faixa": f"{self.ranges_gasometria['pCO2'][0]} - {self.ranges_gasometria['pCO2'][1]}"
            },
            {
                "nome": "pO2",
                "descricao": "Pressão parcial de O2",
                "unidade": "mmHg",
                "faixa": f"{self.ranges_gasometria['pO2'][0]} - {self.ranges_gasometria['pO2'][1]}"
            },
            {
                "nome": "HCO3",
                "descricao": "Bicarbonato",
                "unidade": "mEq/L",
                "faixa": f"{self.ranges_gasometria['HCO3'][0]} - {self.ranges_gasometria['HCO3'][1]}"
            },
            {
                "nome": "BE",
                "descricao": "Base Excess (Excesso de base)",
                "unidade": "mEq/L",
                "faixa": f"{self.ranges_gasometria['BE'][0]} - {self.ranges_gasometria['BE'][1]}"
            },
            {
                "nome": "SaO2",
                "descricao": "Saturação de oxigênio",
                "unidade": "%",
                "faixa": f"{self.ranges_gasometria['SaO2'][0]} - {self.ranges_gasometria['SaO2'][1]}"
            },
            {
                "nome": "lactato",
                "descricao": "Lactato sérico",
                "unidade": "mmol/L",
                "faixa": f"{self.ranges_gasometria['lactato'][0]} - {self.ranges_gasometria['lactato'][1]}"
            },
            {
                "nome": "Na",
                "descricao": "Sódio",
                "unidade": "mEq/L",
                "faixa": f"{self.ranges_gasometria['Na'][0]} - {self.ranges_gasometria['Na'][1]}"
            },
            {
                "nome": "K",
                "descricao": "Potássio",
                "unidade": "mEq/L",
                "faixa": f"{self.ranges_gasometria['K'][0]} - {self.ranges_gasometria['K'][1]}"
            },
            {
                "nome": "Ca",
                "descricao": "Cálcio iônico",
                "unidade": "mmol/L",
                "faixa": f"{self.ranges_gasometria['Ca'][0]} - {self.ranges_gasometria['Ca'][1]}"
            },
            {
                "nome": "Cl",
                "descricao": "Cloreto",
                "unidade": "mEq/L",
                "faixa": f"{self.ranges_gasometria['Cl'][0]} - {self.ranges_gasometria['Cl'][1]}"
            },
            {
                "nome": "Glicose",
                "descricao": "Glicose sanguínea",
                "unidade": "mg/dL",
                "faixa": f"{self.ranges_gasometria['Glicose'][0]} - {self.ranges_gasometria['Glicose'][1]}"
            }
        ]
        return parametros
    
    def obter_ranges_validacao(self):
        """
        Retorna as faixas de validação para todos os parâmetros.
        
        Returns:
            Dict com ranges de validação
        """
        return {
            param: {
                "min": faixa[0],
                "max": faixa[1]
            }
            for param, faixa in self.ranges_gasometria.items()
        }
