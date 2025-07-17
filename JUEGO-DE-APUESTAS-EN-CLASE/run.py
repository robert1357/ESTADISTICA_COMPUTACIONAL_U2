#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Streamlit CSV Analyzer
"""

import subprocess
import sys
import os

def main():
    """Ejecuta la aplicación Streamlit"""
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("Error: No se encontró app.py")
        print("Asegúrate de ejecutar este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar que Streamlit está instalado
    try:
        import streamlit
        print(f"Streamlit versión: {streamlit.__version__}")
    except ImportError:
        print("Error: Streamlit no está instalado")
        print("Instala las dependencias con: pip install -r requirements.txt")
        sys.exit(1)
    
    # Ejecutar la aplicación
    try:
        print("Iniciando aplicación Streamlit...")
        print("La aplicación se abrirá en tu navegador en http://localhost:8501")
        print("Presiona Ctrl+C para detener la aplicación")
        
        subprocess.run([
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            "app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
        
    except KeyboardInterrupt:
        print("\nAplicación detenida por el usuario")
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()