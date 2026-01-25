const axios = require('axios');
const FormData = require('form-data');

/**
 * Serviço responsável por comunicar com o microserviço de OCR
 */
class OcrService {
  constructor() {
    // URL do serviço OCR (pode vir de variável de ambiente)
    this.ocrServiceUrl = process.env.OCR_SERVICE_URL || 'http://ocr-service:5000';
  }

  /**
   * Processa uma imagem através do serviço OCR
   * @param {Buffer} imagemBuffer - Buffer da imagem
   * @returns {Promise<Object>} Resultado do OCR
   */
  async processarImagem(imagemBuffer) {
    try {
      // Prepara FormData para enviar ao serviço OCR
      const formData = new FormData();
      formData.append('imagem', imagemBuffer, {
        filename: 'gasometria.jpg',
        contentType: 'image/jpeg'
      });
      formData.append('validar', 'true');

      console.log(`🔗 Chamando serviço OCR: ${this.ocrServiceUrl}/processar`);

      // Faz requisição ao serviço OCR
      const response = await axios.post(
        `${this.ocrServiceUrl}/processar`,
        formData,
        {
          headers: {
            ...formData.getHeaders()
          },
          timeout: 30000 // 30 segundos
        }
      );

      console.log('✅ OCR processado com sucesso');
      
      // Se o resultado for string JSON, faz parse
      if (typeof response.data === 'string') {
        return JSON.parse(response.data);
      }
      
      return response.data;

    } catch (error) {
      console.error('❌ Erro ao chamar serviço OCR:', error.message);
      
      // Trata erros específicos
      if (error.code === 'ECONNREFUSED') {
        throw new Error('Serviço OCR indisponível. Verifique se está rodando.');
      }
      
      if (error.response) {
        throw new Error(`OCR retornou erro: ${error.response.status} - ${error.response.data}`);
      }
      
      throw new Error(`Erro ao processar imagem: ${error.message}`);
    }
  }

  /**
   * Verifica se o serviço OCR está saudável
   * @returns {Promise<boolean>}
   */
  async verificarSaude() {
    try {
      const response = await axios.get(`${this.ocrServiceUrl}/health`, { timeout: 5000 });
      return response.status === 200;
    } catch (error) {
      console.error('❌ Serviço OCR não está saudável:', error.message);
      return false;
    }
  }
}

module.exports = new OcrService();
