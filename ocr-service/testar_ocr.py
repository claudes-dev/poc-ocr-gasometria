"""
Script para testar o OCR de gasometria com uma imagem local.
"""
from main import processar_foto
import sys

def testar_com_arquivo(caminho_imagem: str, debug: bool = True):
    """
    Testa o OCR com uma imagem do disco.
    
    Args:
        caminho_imagem: Caminho para a imagem (ex: "gasometria.jpg")
        debug: Se True, mostra o texto OCR completo
    """
    print(f"🔍 Processando imagem: {caminho_imagem}")
    print("-" * 60)
    
    try:
        # Lê a imagem como bytes
        with open(caminho_imagem, "rb") as f:
            imagem_bytes = f.read()
        
        # Processa
        resultado = processar_foto(imagem_bytes, validar=True, debug=debug)
        
        print("\n📊 RESULTADO:")
        print(resultado)
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{caminho_imagem}' não encontrado!")
        print("\nCertifique-se de que o arquivo existe no diretório atual.")
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")

if __name__ == "__main__":
    # Você pode passar o caminho da imagem como argumento
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        testar_com_arquivo(caminho, debug=True)
    else:
        print("=" * 60)
        print("🧪 TESTE DE OCR - GASOMETRIA")
        print("=" * 60)
        print("\nUSO:")
        print("  python testar_ocr.py <caminho_da_imagem>")
        print("\nEXEMPLOS:")
        print('  python testar_ocr.py gasometria.jpg')
        print('  python testar_ocr.py "C:/Users/nome/Desktop/foto.png"')
        print('  python testar_ocr.py ./imagens/gasometria.jpg')
        print("\n" + "=" * 60)
        
        # Tenta usar uma imagem de exemplo se existir
        import os
        exemplos = ["gasometria.jpg", "gasometria.png", "teste.jpg", "teste.png"]
        
        for exemplo in exemplos:
            if os.path.exists(exemplo):
                print(f"\n✅ Encontrei '{exemplo}' no diretório atual!")
                resposta = input(f"Deseja processar esta imagem? (s/n): ")
                if resposta.lower() in ['s', 'sim', 'y', 'yes']:
                    testar_com_arquivo(exemplo, debug=True)
                    break
        else:
            print("\n💡 Coloque uma imagem de gasometria neste diretório e execute:")
            print("   python testar_ocr.py <nome_da_imagem>")
