"""
Script de teste para a API de gasometria.
Testa todos os endpoints disponíveis.
"""
import requests
import os
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa endpoint de health check."""
    print("\n" + "="*60)
    print("🔍 Testando Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_api_health():
    """Testa endpoint de health check detalhado."""
    print("\n" + "="*60)
    print("🔍 Testando API Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_parametros():
    """Testa endpoint de listagem de parâmetros."""
    print("\n" + "="*60)
    print("📋 Testando Lista de Parâmetros")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/gasometria/parametros")
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get("sucesso"):
            print(f"✅ {len(data['parametros'])} parâmetros disponíveis:")
            for param in data['parametros'][:3]:  # Mostra os 3 primeiros
                print(f"   - {param['nome']}: {param['descricao']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_ranges():
    """Testa endpoint de ranges de validação."""
    print("\n" + "="*60)
    print("📊 Testando Ranges de Validação")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/gasometria/ranges")
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get("sucesso"):
            print(f"✅ Ranges disponíveis:")
            for param, ranges in list(data['ranges'].items())[:3]:  # Mostra os 3 primeiros
                print(f"   - {param}: {ranges['min']} - {ranges['max']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_analisar_imagem(imagem_path):
    """Testa endpoint de análise de imagem."""
    print("\n" + "="*60)
    print(f"🖼️  Testando Análise de Imagem: {imagem_path}")
    print("="*60)
    
    if not os.path.exists(imagem_path):
        print(f"❌ Arquivo não encontrado: {imagem_path}")
        return False
    
    try:
        with open(imagem_path, 'rb') as f:
            files = {'imagem': f}
            data = {
                'validar': 'true',
                'debug': 'false'
            }
            response = requests.post(
                f"{BASE_URL}/api/gasometria/analisar",
                files=files,
                data=data
            )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get("sucesso"):
            print("✅ Processamento bem-sucedido!")
            print(f"\n📊 Valores extraídos:")
            for param, valor in result.get('valores', {}).items():
                print(f"   - {param}: {valor}")
            
            if 'validacao' in result:
                validacao = result['validacao']
                print(f"\n🔍 Validação:")
                print(f"   - Todas válidas: {validacao.get('todas_validas')}")
                if validacao.get('fora_faixa'):
                    print(f"   - Fora da faixa: {validacao.get('fora_faixa')}")
        else:
            print(f"❌ Erro no processamento: {result.get('erro')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES DA API OCR GASOMETRIA")
    print("="*60)
    
    resultados = []
    
    # Testa endpoints básicos
    resultados.append(("Health Check", test_health()))
    resultados.append(("API Health Check", test_api_health()))
    resultados.append(("Lista Parâmetros", test_parametros()))
    resultados.append(("Ranges Validação", test_ranges()))
    
    # Testa análise de imagem (se houver arquivo)
    imagem_path = "../ocr-service/gasometria.png"
    if os.path.exists(imagem_path):
        resultados.append(("Análise de Imagem", test_analisar_imagem(imagem_path)))
    else:
        print(f"\n⚠️  Imagem de teste não encontrada: {imagem_path}")
        print("   Pulando teste de análise de imagem.")
    
    # Resumo
    print("\n" + "="*60)
    print("📋 RESUMO DOS TESTES")
    print("="*60)
    for nome, sucesso in resultados:
        status = "✅" if sucesso else "❌"
        print(f"{status} {nome}")
    
    total = len(resultados)
    sucesso_count = sum(1 for _, s in resultados if s)
    print(f"\n🎯 Total: {sucesso_count}/{total} testes passaram")
    print("="*60 + "\n")
    
    return sucesso_count == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
