const express = require('express');
const router = express.Router();
const multer = require('multer');
const gasometriaController = require('../controllers/gasometria.controller');

// Configuração do multer para upload de arquivos (em memória)
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB
});

/**
 * POST /api/gasometria/analisar
 * Envia imagem para análise OCR
 */
router.post('/analisar', upload.single('imagem'), gasometriaController.analisarImagem);

/**
 * GET /api/gasometria/parametros
 * Retorna lista de parâmetros disponíveis
 */
router.get('/parametros', gasometriaController.listarParametros);

module.exports = router;
