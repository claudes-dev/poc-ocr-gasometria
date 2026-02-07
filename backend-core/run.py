"""
🚀 Modo Simples - Just Run!
Execute: python run.py
"""
import subprocess
import sys
import os

def check_dependencies():
    """Verifica se dependências estão instaladas."""
    try:
        import flask
        import cv2
        import pytesseract
        print("✅ Dependências OK!")
        return True
    except ImportError as e:
        print(f"❌ Faltam dependências: {e}")
        print("\n📦 Instalando dependências automaticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas!")
        return True

def main():
    print("=" * 60)
    print("🚀 Iniciando API OCR Gasometria (Modo Simples)")
    print("=" * 60)
    print()
    
    # Verifica/instala dependências
    check_dependencies()
    
    print("\n🌐 API rodando em: http://localhost:5000")
    print("📋 Pressione Ctrl+C para parar\n")
    print("=" * 60)
    print()
    
    # Inicia a aplicação
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
