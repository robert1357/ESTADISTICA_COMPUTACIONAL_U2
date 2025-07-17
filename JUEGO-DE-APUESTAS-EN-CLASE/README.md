# Analizador de CSV - Streamlit

## Descripción
Aplicación web completa para el análisis estadístico de archivos CSV, construida con Streamlit. Incluye análisis descriptivo, detección de outliers, visualizaciones interactivas, análisis avanzado con machine learning y generación de reportes.

## Características Principales

### 📊 Análisis Completo
- **Carga automática** con detección de codificación
- **Estadísticas descriptivas** completas
- **Detección de valores atípicos** (IQR y Z-score)
- **Visualizaciones interactivas** con Plotly
- **Análisis estadístico avanzado** (Regresión, PCA, Clustering)
- **Reportes descargables** en español

### 🔧 Módulos Incluidos
- `data_loader.py`: Carga y exploración inicial de datos
- `statistics.py`: Estadísticas descriptivas y análisis básico
- `visualizations.py`: Generación de gráficos interactivos
- `advanced_analytics.py`: Machine learning y análisis avanzado
- `report_generator.py`: Generación de reportes automatizados

## Instalación

### Método 1: Usando pip
```bash
pip install -r requirements.txt
```

### Método 2: Usando ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### Estructura del Análisis
1. **Carga y Exploración**: Información básica del dataset
2. **Estadísticas Descriptivas**: Medidas de tendencia y dispersión
3. **Limpieza de Datos**: Detección y tratamiento de anomalías
4. **Visualizaciones**: Gráficos interactivos y mapas de calor
5. **Análisis Avanzado**: Técnicas de machine learning
6. **Conclusiones**: Insights automáticos y recomendaciones

## Estructura de Archivos
```
streamlit_csv_analyzer/
├── app.py                  # Aplicación principal
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── pyproject.toml         # Configuración del proyecto
└── utils/
    ├── data_loader.py     # Carga de datos
    ├── statistics.py      # Estadísticas descriptivas
    ├── visualizations.py  # Visualizaciones
    ├── advanced_analytics.py  # Análisis avanzado
    └── report_generator.py    # Generación de reportes
```

## Funcionalidades Detalladas

### 📂 Carga de Datos
- Detección automática de codificación de archivos CSV
- Análisis básico de estructura y calidad de datos
- Identificación de tipos de variables (numéricas/categóricas)

### 📈 Estadísticas Descriptivas
- Medidas de tendencia central y dispersión
- Análisis de correlaciones
- Distribuciones de frecuencia para variables categóricas

### 🧹 Limpieza de Datos
- Detección de valores nulos y estrategias de imputación
- Identificación de valores atípicos con múltiples métodos
- Opciones de transformación de datos

### 📊 Visualizaciones
- Histogramas y distribuciones
- Boxplots para detección de outliers
- Mapas de calor de correlaciones
- Gráficos de dispersión interactivos
- Análisis de variables categóricas

### 🔬 Análisis Avanzado
- Análisis de Componentes Principales (PCA)
- Clustering K-means
- Regresión lineal y evaluación de modelos
- Análisis de varianza (ANOVA)

### 📋 Reportes
- Generación automática de insights
- Recomendaciones basadas en los análisis
- Resúmenes ejecutivos descargables

## Requisitos del Sistema
- Python 3.8 o superior
- Navegador web moderno
- Memoria RAM: 4GB recomendado para datasets grandes

## Notas Importantes
- La aplicación funciona mejor con datasets en formato CSV
- Para archivos grandes (>100MB), considere usar una muestra
- Las visualizaciones interactivas requieren una conexión estable

## Soporte
Este proyecto está diseñado para ser ejecutado localmente. Para problemas específicos, revise los logs en la consola de Streamlit.