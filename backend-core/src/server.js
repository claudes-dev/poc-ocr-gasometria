const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const gasometriaRoutes = require('./routes/gasometria.routes');

// Carrega variáveis de ambiente
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rotas
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'backend-core',
    timestamp: new Date().toISOString()
  });
});

app.use('/api/gasometria', gasometriaRoutes);

// Tratamento de erro 404
app.use((req, res) => {
  res.status(404).json({ 
    sucesso: false, 
    erro: 'Rota não encontrada' 
  });
});

// Tratamento de erros gerais
app.use((err, req, res, next) => {
  console.error('❌ Erro:', err);
  res.status(500).json({ 
    sucesso: false, 
    erro: 'Erro interno do servidor',
    mensagem: err.message 
  });
});

// Inicia servidor
app.listen(PORT, () => {
  console.log(`🚀 Backend rodando em http://localhost:${PORT}`);
  console.log(`📡 Health check: http://localhost:${PORT}/health`);
  console.log(`🔬 API Gasometria: http://localhost:${PORT}/api/gasometria`);
});

module.exports = app;
