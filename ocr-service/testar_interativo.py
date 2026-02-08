"""
Script interativo para testar OCR de gasometria.
Permite arrastar e soltar arquivo ou digitar o caminho.
"""
from main import processar_foto
import os
import json

def limpar_caminho(caminho: str) -> str:
    """Remove aspas e espaços extras do caminho."""
    return caminho.strip().strip('"').strip("'")

def main():
    print("=" * 70)
    print("🧪 TESTE INTERATIVO DE OCR - GASOMETRIA")
    print("=" * 70)
    
    while True:
        print("\n" + "-" * 70)
        print("📁 Cole o caminho da imagem (ou 'sair' para encerrar):")
        print("   💡 Dica: Você pode arrastar o arquivo para a janela do terminal")
        print("-" * 70)
        
        caminho = input("\n➤ Caminho da imagem: ").strip()
        
        if caminho.lower() in ['sair', 'exit', 'q', 'quit']:
            print("\n👋 Encerrando...")
            break
        
        if not caminho:
            continue
        
        # Limpa o caminho (remove aspas se houver)
        caminho = limpar_caminho(caminho)
        
        if not os.path.exists(caminho):
            print(f"\n❌ Arquivo não encontrado: {caminho}")
            print("   Verifique se o caminho está correto.")
            continue
        
        # Verifica se é uma imagem
        extensoes_validas = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        if not any(caminho.lower().endswith(ext) for ext in extensoes_validas):
            print(f"\n⚠️  Aviso: O arquivo pode não ser uma imagem válida")
            print(f"   Extensões suportadas: {', '.join(extensoes_validas)}")
            continuar = input("   Deseja continuar mesmo assim? (s/n): ")
            if continuar.lower() not in ['s', 'sim', 'y', 'yes']:
                continue
        
        print(f"\n🔍 Processando: {os.path.basename(caminho)}")
        print("   Aguarde...")
        
        try:
            # Lê a imagem
            with open(caminho, "rb") as f:
                imagem_bytes = f.read()
            
            # Processa com validação e debug
            resultado_json = processar_foto(imagem_bytes, validar=True, debug=True)
            resultado = json.loads(resultado_json)
            
            # Exibe resultado formatado
            print("\n" + "=" * 70)
            print("📊 RESULTADOS DA ANÁLISE")
            print("=" * 70)
            
            if resultado.get("sucesso"):
                print(f"\n✅ Status: Sucesso")
                print(f"📈 Parâmetros encontrados: {resultado['parametros_encontrados']}/{resultado['total_parametros']}")
                
                print("\n📋 VALORES EXTRAÍDOS:")
                print("-" * 70)
                
                dados = resultado["dados"]
                for parametro, info in dados.items():
                    if isinstance(info, dict):
                        valor = info.get("valor")
                        valido = info.get("valido")
                        mensagem = info.get("mensagem")
                        
                        if valor is not None:
                            status_icon = "✅" if valido else "⚠️"
                            print(f"  {status_icon} {parametro:12s}: {valor:>8} - {mensagem}")
                        else:
                            print(f"  ❌ {parametro:12s}: Não encontrado")
                    else:
                        if info is not None:
                            print(f"  • {parametro:12s}: {info}")
                
                # Mostra texto OCR se debug estiver ativo
                if "texto_ocr" in resultado:
                    print("\n" + "-" * 70)
                    print("📄 TEXTO OCR COMPLETO:")
                    print("-" * 70)
                    print(resultado["texto_ocr"][:500])  # Primeiros 500 caracteres
                    if len(resultado["texto_ocr"]) > 500:
                        print(f"\n... (texto truncado, total: {len(resultado['texto_ocr'])} caracteres)")
            else:
                print(f"\n❌ Erro: {resultado.get('erro')}")
            
            print("\n" + "=" * 70)
            
            # Pergunta se quer salvar o resultado
            salvar = input("\n💾 Deseja salvar o resultado em JSON? (s/n): ")
            if salvar.lower() in ['s', 'sim', 'y', 'yes']:
                nome_saida = f"resultado_{os.path.splitext(os.path.basename(caminho))[0]}.json"
                with open(nome_saida, 'w', encoding='utf-8') as f:
                    f.write(resultado_json)
                print(f"✅ Resultado salvo em: {nome_saida}")
            
        except Exception as e:
            print(f"\n❌ Erro ao processar imagem: {e}")
            import traceback
            print("\nDetalhes do erro:")
            traceback.print_exc()
        
        # Pergunta se quer processar outra imagem
        print("\n" + "-" * 70)
        continuar = input("🔄 Processar outra imagem? (s/n): ")
        if continuar.lower() not in ['s', 'sim', 'y', 'yes']:
            print("\n👋 Encerrando...")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário. Encerrando...")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
