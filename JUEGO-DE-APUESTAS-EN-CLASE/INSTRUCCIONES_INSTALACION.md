# Instrucciones de Instalación - Streamlit CSV Analyzer

## Instalación en VS Code

### Paso 1: Preparar el ambiente
1. Abre VS Code
2. Descomprime el archivo `streamlit_csv_analyzer.zip` en tu carpeta de proyectos
3. Abre la carpeta del proyecto en VS Code: `File > Open Folder`

### Paso 2: Crear ambiente virtual (Recomendado)
```bash
# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación
```bash
# Opción 1: Usando Streamlit directamente
streamlit run app.py

# Opción 2: Usando el script de ejecución
python run.py
```

## Verificación de la Instalación

### Verificar que Python está instalado
```bash
python --version
# Debería mostrar Python 3.8 o superior
```

### Verificar que pip está instalado
```bash
pip --version
```

### Verificar que Streamlit funciona
```bash
streamlit --version
```

## Solución de Problemas Comunes

### Error: "streamlit: command not found"
```bash
# Asegúrate de que el ambiente virtual esté activado
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstala Streamlit
pip install streamlit
```

### Error: "No module named 'streamlit'"
```bash
# Verifica que estés en el ambiente virtual correcto
which python  # Debería mostrar la ruta del ambiente virtual

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error de permisos en Windows
```bash
# Ejecuta como administrador o usa:
python -m pip install -r requirements.txt
```

### Error con weasyprint en Windows
```bash
# Instala GTK+ para Windows o omite weasyprint:
pip install streamlit pandas numpy matplotlib seaborn plotly scikit-learn scipy chardet reportlab
```

## Uso de la Aplicación

### Acceder a la aplicación
- Una vez ejecutada, la aplicación estará disponible en: `http://localhost:8501`
- Se abrirá automáticamente en tu navegador predeterminado

### Cargar datos
1. Ve a la sección "📂 Carga y Exploración"
2. Haz clic en "Browse files" para seleccionar tu archivo CSV
3. La aplicación detectará automáticamente la codificación

### Navegar por las secciones
- Usa el menú lateral para moverte entre las diferentes secciones
- Cada sección construye sobre los análisis anteriores

## Archivos Incluidos

- `app.py`: Aplicación principal de Streamlit
- `requirements.txt`: Lista de dependencias
- `run.py`: Script de ejecución alternativo
- `README.md`: Documentación completa
- `utils/`: Módulos de análisis especializados
- `Enaho01-2022-100.csv`: Archivo de muestra (si incluido)
- `ejemplo_con_nulos.csv`: Archivo de ejemplo con valores nulos (si incluido)

## Características del Sistema

### Archivos Soportados
- Archivos CSV con cualquier codificación
- Separadores: coma, punto y coma, tabulación
- Tamaño recomendado: menos de 100MB

### Navegadores Compatibles
- Chrome (recomendado)
- Firefox
- Safari
- Edge

### Requisitos del Sistema
- Python 3.8+
- 4GB RAM recomendado
- Conexión a internet para la primera instalación

## Notas Adicionales

- La aplicación se ejecuta localmente en tu computadora
- Los datos no se envían a ningún servidor externo
- Para detener la aplicación, presiona `Ctrl+C` en la terminal
- Los archivos de análisis se guardan localmente