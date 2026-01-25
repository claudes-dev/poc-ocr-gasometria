const ocrService = require('../services/ocr.service');

/**
 * Controller para endpoints de gasometria
 */
class GasometriaController {
  /**
   * Analisa uma imagem de gasometria
   */
  async analisarImagem(req, res) {
    try {
      // Verifica se há arquivo
      if (!req.file) {
        return res.status(400).json({
          sucesso: false,
          erro: 'Nenhuma imagem enviada. Use o campo "imagem".'
        });
      }

      console.log(`📷 Processando imagem: ${req.file.originalname} (${req.file.size} bytes)`);

      // Envia para o serviço OCR
      const resultado = await ocrService.processarImagem(req.file.buffer);

      // Retorna resultado
      return res.json(resultado);

    } catch (error) {
      console.error('❌ Erro ao analisar imagem:', error.message);
      return res.status(500).json({
        sucesso: false,
        erro: 'Erro ao processar imagem',
        detalhes: error.message
      });
    }
  }

  /**
   * Lista parâmetros disponíveis para análise
   */
  listarParametros(req, res) {
    const parametros = {
      sucesso: true,
      parametros: [
        { nome: 'pH', descricao: 'Potencial hidrogeniônico', faixa: '6.8 - 7.8' },
        { nome: 'pCO2', descricao: 'Pressão parcial de CO2', faixa: '10 - 100 mmHg' },
        { nome: 'pO2', descricao: 'Pressão parcial de O2', faixa: '40 - 500 mmHg' },
        { nome: 'HCO3', descricao: 'Bicarbonato', faixa: '10 - 50 mEq/L' },
        { nome: 'BE', descricao: 'Base Excess', faixa: '-20 - 20 mEq/L' },
        { nome: 'SaO2', descricao: 'Saturação de oxigênio', faixa: '50 - 100 %' },
        { nome: 'lactato', descricao: 'Lactato', faixa: '0.5 - 20 mmol/L' },
        { nome: 'Na', descricao: 'Sódio', faixa: '100 - 180 mEq/L' },
        { nome: 'K', descricao: 'Potássio', faixa: '2.0 - 8.0 mEq/L' },
        { nome: 'Ca', descricao: 'Cálcio', faixa: '0.5 - 3.0 mmol/L' },
        { nome: 'Cl', descricao: 'Cloro', faixa: '80 - 130 mEq/L' },
        { nome: 'Glicose', descricao: 'Glicose', faixa: '20 - 600 mg/dL' }
      ]
    };

    res.json(parametros);
  }
}

module.exports = new GasometriaController();
