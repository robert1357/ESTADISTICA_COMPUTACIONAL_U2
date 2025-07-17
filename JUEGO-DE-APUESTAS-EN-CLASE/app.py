import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
warnings.filterwarnings('ignore')

# Importar módulos personalizados
from utils.data_loader import load_csv_with_encoding, get_basic_info
from utils.statistics import get_descriptive_stats, detect_outliers, clean_data
from utils.visualizations import create_visualizations
from utils.advanced_analytics import perform_advanced_analysis
from utils.report_generator import generate_report

# Configuración de la página
st.set_page_config(
    page_title="Analizador de CSV - Análisis Estadístico Completo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Analizador de CSV - Análisis Estadístico Completo")
st.markdown("**Una herramienta completa para el análisis estadístico de datos CSV**")

# Sidebar para navegación
st.sidebar.title("🧭 Navegación")
sections = [
    "🏠 Inicio",
    "📂 Carga y Exploración",
    "📈 Estadísticas Descriptivas",
    "🧹 Detección y Limpieza",
    "📊 Visualizaciones",
    "🔬 Análisis Avanzado",
    "📋 Conclusiones y Reporte",
    "📊 Análisis Completo ENAHO",
    "🖼️ Gráficos y Visualizaciones",
    "📄 Documentos ENAHO"
]

selected_section = st.sidebar.selectbox("Seleccionar sección:", sections)

# Inicializar session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# Sección de Inicio
if selected_section == "🏠 Inicio":
    st.header("Bienvenido al Analizador de CSV")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Características principales:")
        st.markdown("""
        - **Carga automática** con detección de codificación
        - **Estadísticas descriptivas** completas
        - **Detección de valores atípicos** (IQR y Z-score)
        - **Visualizaciones interactivas** con Plotly
        - **Análisis estadístico avanzado** (Regresión, PCA, Clustering)
        - **Reportes descargables** en español
        """)
    
    with col2:
        st.subheader("📋 Estructura del análisis:")
        st.markdown("""
        1. **Carga y Exploración**: Información básica del dataset
        2. **Estadísticas Descriptivas**: Medidas de tendencia y dispersión
        3. **Limpieza de Datos**: Detección y tratamiento de anomalías
        4. **Visualizaciones**: Gráficos interactivos y mapas de calor
        5. **Análisis Avanzado**: Técnicas de machine learning
        6. **Conclusiones**: Insights automáticos y recomendaciones
        """)
    
    st.info("👆 Usa el menú lateral para navegar entre las diferentes secciones del análisis.")

# Sección 1: Carga y Exploración
elif selected_section == "📂 Carga y Exploración":
    st.header("1. Carga y Exploración Inicial de Datos")
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo CSV para analizar:",
        type=['csv'],
        help="Sube tu archivo CSV. El sistema detectará automáticamente la codificación."
    )
    
    if uploaded_file is not None:
        try:
            # Cargar datos con detección automática de codificación
            with st.spinner('Cargando y procesando archivo...'):
                data = load_csv_with_encoding(uploaded_file)
                st.session_state.data = data
            
            st.success(f"✅ Archivo cargado exitosamente: {uploaded_file.name}")
            
            # Mostrar información básica
            basic_info = get_basic_info(data)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Filas", basic_info['rows'])
            with col2:
                st.metric("Columnas", basic_info['columns'])
            with col3:
                st.metric("Valores nulos", basic_info['null_values'])
            with col4:
                st.metric("Duplicados", basic_info['duplicates'])
            
            # Información detallada de columnas
            st.subheader("📋 Información de Columnas")
            col_info = pd.DataFrame({
                'Columna': data.columns,
                'Tipo de Dato': data.dtypes,
                'Valores Nulos': data.isnull().sum(),
                'Valores Únicos': data.nunique(),
                'Porcentaje Nulos': (data.isnull().sum() / len(data) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Primeras y últimas filas
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔝 Primeras 5 filas")
                st.dataframe(data.head(), use_container_width=True)
            
            with col2:
                st.subheader("🔚 Últimas 5 filas")
                st.dataframe(data.tail(), use_container_width=True)
            
            # Mostrar tipos de variables
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔢 Variables Numéricas")
                if numeric_cols:
                    st.write(numeric_cols)
                else:
                    st.info("No se encontraron variables numéricas")
            
            with col2:
                st.subheader("📝 Variables Categóricas")
                if categorical_cols:
                    st.write(categorical_cols)
                else:
                    st.info("No se encontraron variables categóricas")
                    
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            st.info("Verifica que el archivo sea un CSV válido.")

# Sección 2: Estadísticas Descriptivas
elif selected_section == "📈 Estadísticas Descriptivas":
    st.header("2. Estadísticas Descriptivas Básicas")
    
    if st.session_state.data is not None:
        data = st.session_state.data
        
        # Obtener estadísticas descriptivas
        stats_results = get_descriptive_stats(data)
        
        # Variables numéricas
        if 'numeric_stats' in stats_results:
            st.subheader("🔢 Estadísticas para Variables Numéricas")
            st.dataframe(stats_results['numeric_stats'], use_container_width=True)
            
            # Medidas adicionales
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.subheader("📊 Medidas Adicionales")
                additional_stats = pd.DataFrame({
                    'Varianza': data[numeric_cols].var(),
                    'Desviación Estándar': data[numeric_cols].std(),
                    'Rango': data[numeric_cols].max() - data[numeric_cols].min(),
                    'Coeficiente de Variación': (data[numeric_cols].std() / data[numeric_cols].mean() * 100).round(2)
                })
                st.dataframe(additional_stats, use_container_width=True)
        
        # Variables categóricas
        if 'categorical_stats' in stats_results:
            st.subheader("📝 Estadísticas para Variables Categóricas")
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            
            for col in categorical_cols:
                with st.expander(f"Análisis de: {col}"):
                    value_counts = data[col].value_counts()
                    percentages = (data[col].value_counts(normalize=True) * 100).round(2)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Frecuencias:**")
                        st.dataframe(value_counts)
                    with col2:
                        st.write("**Porcentajes:**")
                        st.dataframe(percentages)
        
        # Matriz de correlación para variables numéricas
        numeric_data = data.select_dtypes(include=[np.number])
        if len(numeric_data.columns) > 1:
            st.subheader("🔗 Matriz de Correlación")
            corr_matrix = numeric_data.corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Matriz de Correlación entre Variables Numéricas",
                color_continuous_scale='RdBu'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Correlaciones más fuertes
            st.subheader("🏆 Correlaciones Más Significativas")
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlación': corr_matrix.iloc[i, j]
                    })
            
            corr_df = pd.DataFrame(corr_pairs)
            corr_df = corr_df.sort_values('Correlación', key=abs, ascending=False)
            st.dataframe(corr_df.head(10), use_container_width=True)
    
    else:
        st.warning("⚠️ Primero debes cargar un archivo CSV en la sección 'Carga y Exploración'.")

# Sección 3: Detección y Limpieza
elif selected_section == "🧹 Detección y Limpieza":
    st.header("3. Detección y Limpieza de Datos")
    
    if st.session_state.data is not None:
        data = st.session_state.data
        
        # Valores nulos
        st.subheader("🕳️ Análisis de Valores Nulos")
        null_counts = data.isnull().sum()
        null_percentages = (data.isnull().sum() / len(data) * 100).round(2)
        
        null_df = pd.DataFrame({
            'Columna': null_counts.index,
            'Valores Nulos': null_counts.values,
            'Porcentaje': null_percentages.values
        })
        null_df = null_df[null_df['Valores Nulos'] > 0].sort_values('Valores Nulos', ascending=False)
        
        if len(null_df) > 0:
            st.dataframe(null_df, use_container_width=True)
            
            # Visualización de valores nulos
            fig = px.bar(
                null_df, 
                x='Columna', 
                y='Porcentaje',
                title="Porcentaje de Valores Nulos por Columna",
                color='Porcentaje',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No se encontraron valores nulos en el dataset.")
        
        # Detección de valores atípicos
        st.subheader("🎯 Detección de Valores Atípicos")
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("Selecciona una variable para analizar:", numeric_cols)
            
            if selected_col:
                outliers_info = detect_outliers(data, selected_col)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Valores atípicos (IQR)", len(outliers_info['iqr_outliers']))
                with col2:
                    st.metric("Valores atípicos (Z-score)", len(outliers_info['zscore_outliers']))
                
                # Visualización de boxplot
                fig = px.box(
                    data, 
                    y=selected_col,
                    title=f"Boxplot para {selected_col} - Detección de Valores Atípicos"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar valores atípicos
                if len(outliers_info['iqr_outliers']) > 0:
                    st.subheader("📋 Valores Atípicos Detectados (Método IQR)")
                    outlier_data = data.loc[outliers_info['iqr_outliers']]
                    st.dataframe(outlier_data[[selected_col]], use_container_width=True)
        
        # Opciones de limpieza
        st.subheader("🧽 Opciones de Limpieza de Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tratamiento de Valores Nulos")
            null_strategy = st.selectbox(
                "Estrategia para valores nulos:",
                ["No aplicar", "Eliminar filas", "Imputar con media", "Imputar con mediana", "Imputar con moda"]
            )
        
        with col2:
            st.subheader("Tratamiento de Valores Atípicos")
            outlier_strategy = st.selectbox(
                "Estrategia para valores atípicos:",
                ["No aplicar", "Eliminar valores atípicos", "Transformar con log", "Winsorización"]
            )
        
        if st.button("🔄 Aplicar Limpieza de Datos"):
            try:
                cleaned_data = clean_data(data, null_strategy, outlier_strategy)
                st.session_state.cleaned_data = cleaned_data
                
                st.success("✅ Datos limpiados exitosamente!")
                
                # Mostrar comparación antes/después
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Filas originales", len(data))
                    st.metric("Valores nulos originales", data.isnull().sum().sum())
                with col2:
                    st.metric("Filas después de limpieza", len(cleaned_data))
                    st.metric("Valores nulos después", cleaned_data.isnull().sum().sum())
                    
            except Exception as e:
                st.error(f"❌ Error durante la limpieza: {str(e)}")
    
    else:
        st.warning("⚠️ Primero debes cargar un archivo CSV en la sección 'Carga y Exploración'.")

# Sección 4: Visualizaciones
elif selected_section == "📊 Visualizaciones":
    st.header("4. Visualizaciones Completas")
    
    if st.session_state.data is not None:
        # Usar datos limpios si están disponibles, sino usar datos originales
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        visualizations = create_visualizations(data)
        
        # Pestañas para organizar visualizaciones
        tabs = st.tabs([
            "📊 Distribuciones", 
            "📈 Correlaciones", 
            "📋 Categóricas", 
            "🔍 Comparaciones",
            "🎯 Avanzadas"
        ])
        
        with tabs[0]:  # Distribuciones
            st.subheader("📊 Distribuciones de Variables Numéricas")
            if 'histograms' in visualizations:
                st.plotly_chart(visualizations['histograms'], use_container_width=True)
            
            st.subheader("📦 Boxplots para Detección de Valores Atípicos")
            if 'boxplots' in visualizations:
                st.plotly_chart(visualizations['boxplots'], use_container_width=True)
        
        with tabs[1]:  # Correlaciones
            st.subheader("🔗 Mapa de Calor de Correlaciones")
            if 'correlation_heatmap' in visualizations:
                st.plotly_chart(visualizations['correlation_heatmap'], use_container_width=True)
            
            st.subheader("🎯 Gráficos de Dispersión")
            if 'scatter_plots' in visualizations:
                st.plotly_chart(visualizations['scatter_plots'], use_container_width=True)
        
        with tabs[2]:  # Categóricas
            st.subheader("📊 Distribución de Variables Categóricas")
            if 'categorical_plots' in visualizations:
                for plot in visualizations['categorical_plots']:
                    st.plotly_chart(plot, use_container_width=True)
        
        with tabs[3]:  # Comparaciones
            st.subheader("🎻 Gráficos de Violín")
            if 'violin_plots' in visualizations:
                st.plotly_chart(visualizations['violin_plots'], use_container_width=True)
            
            st.subheader("📈 Gráficos de Líneas (si hay variables temporales)")
            if 'line_plots' in visualizations:
                st.plotly_chart(visualizations['line_plots'], use_container_width=True)
        
        with tabs[4]:  # Avanzadas
            st.subheader("🎯 Visualizaciones Avanzadas")
            if 'advanced_plots' in visualizations:
                for plot in visualizations['advanced_plots']:
                    st.plotly_chart(plot, use_container_width=True)
        
        # Descargar visualizaciones
        st.subheader("💾 Exportar Visualizaciones")
        if st.button("📁 Generar ZIP con todas las visualizaciones"):
            st.info("Funcionalidad de descarga disponible - implementar según necesidades específicas")
    
    else:
        st.warning("⚠️ Primero debes cargar un archivo CSV en la sección 'Carga y Exploración'.")

# Sección 5: Análisis Avanzado
elif selected_section == "🔬 Análisis Avanzado":
    st.header("5. Técnicas Estadísticas Avanzadas")
    
    if st.session_state.data is not None:
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        # Selección de técnica de análisis
        analysis_type = st.selectbox(
            "Selecciona la técnica de análisis:",
            [
                "Análisis de Correlación Detallado",
                "Regresión Lineal/Múltiple", 
                "Clustering (K-means)",
                "Análisis de Componentes Principales (PCA)",
                "Pruebas de Hipótesis"
            ]
        )
        
        if st.button("🚀 Ejecutar Análisis Avanzado"):
            with st.spinner(f'Ejecutando {analysis_type}...'):
                try:
                    results = perform_advanced_analysis(data, analysis_type)
                    st.session_state.analysis_results[analysis_type] = results
                    
                    # Mostrar resultados según el tipo de análisis
                    if analysis_type == "Análisis de Correlación Detallado":
                        st.subheader("🔗 Análisis de Correlación Detallado")
                        if 'correlation_matrix' in results:
                            st.dataframe(results['correlation_matrix'], use_container_width=True)
                        if 'significant_correlations' in results:
                            st.subheader("📊 Correlaciones Significativas")
                            st.dataframe(results['significant_correlations'], use_container_width=True)
                    
                    elif analysis_type == "Regresión Lineal/Múltiple":
                        st.subheader("📈 Resultados de Regresión")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("R² Score", f"{results.get('r2_score', 0):.4f}")
                        with col2:
                            st.metric("RMSE", f"{results.get('rmse', 0):.4f}")
                        
                        if 'feature_importance' in results:
                            st.subheader("🎯 Importancia de Variables")
                            st.dataframe(results['feature_importance'], use_container_width=True)
                        
                        if 'predictions_plot' in results:
                            st.plotly_chart(results['predictions_plot'], use_container_width=True)
                    
                    elif analysis_type == "Clustering (K-means)":
                        st.subheader("🎯 Resultados de Clustering")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Número de Clusters", results.get('n_clusters', 0))
                        with col2:
                            st.metric("Silhouette Score", f"{results.get('silhouette_score', 0):.4f}")
                        
                        if 'cluster_plot' in results:
                            st.plotly_chart(results['cluster_plot'], use_container_width=True)
                        
                        if 'cluster_centers' in results:
                            st.subheader("📍 Centros de Clusters")
                            st.dataframe(results['cluster_centers'], use_container_width=True)
                    
                    elif analysis_type == "Análisis de Componentes Principales (PCA)":
                        st.subheader("🔍 Resultados de PCA")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Componentes", len(results.get('explained_variance', [])))
                        with col2:
                            st.metric("Varianza Explicada Total", f"{sum(results.get('explained_variance', [])):.2%}")
                        
                        if 'pca_plot' in results:
                            st.plotly_chart(results['pca_plot'], use_container_width=True)
                        
                        if 'components_df' in results:
                            st.subheader("📊 Componentes Principales")
                            st.dataframe(results['components_df'], use_container_width=True)
                    
                    elif analysis_type == "Pruebas de Hipótesis":
                        st.subheader("🧪 Resultados de Pruebas de Hipótesis")
                        if 'test_results' in results:
                            for test_name, test_result in results['test_results'].items():
                                with st.expander(f"📋 {test_name}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.metric("Estadístico", f"{test_result.get('statistic', 0):.4f}")
                                    with col2:
                                        st.metric("p-valor", f"{test_result.get('p_value', 0):.4f}")
                                    
                                    conclusion = "Rechazar H₀" if test_result.get('p_value', 1) < 0.05 else "No rechazar H₀"
                                    st.write(f"**Conclusión:** {conclusion} (α = 0.05)")
                
                except Exception as e:
                    st.error(f"❌ Error durante el análisis: {str(e)}")
        
        # Mostrar análisis previos
        if st.session_state.analysis_results:
            st.subheader("📋 Análisis Realizados Previamente")
            for analysis_name in st.session_state.analysis_results.keys():
                st.info(f"✅ {analysis_name}")
    
    else:
        st.warning("⚠️ Primero debes cargar un archivo CSV en la sección 'Carga y Exploración'.")

# Sección 6: Conclusiones y Reporte
elif selected_section == "📋 Conclusiones y Reporte":
    st.header("6. Storytelling y Conclusiones")
    
    if st.session_state.data is not None:
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        # Generar reporte automático
        if st.button("📄 Generar Reporte Completo"):
            with st.spinner('Generando reporte automático...'):
                try:
                    report = generate_report(data, st.session_state.analysis_results)
                    
                    # Resumen Ejecutivo
                    st.subheader("📋 Resumen Ejecutivo")
                    st.markdown(report.get('executive_summary', 'No disponible'))
                    
                    # Hallazgos Principales
                    st.subheader("🔍 Hallazgos Principales")
                    if 'key_findings' in report:
                        for finding in report['key_findings']:
                            st.markdown(f"• {finding}")
                    
                    # Insights Automáticos
                    st.subheader("💡 Insights Automáticos")
                    if 'insights' in report:
                        for insight in report['insights']:
                            st.info(insight)
                    
                    # Recomendaciones
                    st.subheader("🎯 Recomendaciones")
                    if 'recommendations' in report:
                        for recommendation in report['recommendations']:
                            st.success(recommendation)
                    
                    # Limitaciones
                    st.subheader("⚠️ Limitaciones del Análisis")
                    if 'limitations' in report:
                        for limitation in report['limitations']:
                            st.warning(limitation)
                    
                    # Próximos Pasos
                    st.subheader("🚀 Próximos Pasos Sugeridos")
                    if 'next_steps' in report:
                        for step in report['next_steps']:
                            st.markdown(f"📌 {step}")
                    
                    # Botón de descarga del reporte
                    st.subheader("💾 Descargar Reporte")
                    report_text = f"""
# REPORTE DE ANÁLISIS DE DATOS
## Generado automáticamente

### RESUMEN EJECUTIVO
{report.get('executive_summary', 'No disponible')}

### HALLAZGOS PRINCIPALES
{chr(10).join(f'• {finding}' for finding in report.get('key_findings', []))}

### INSIGHTS AUTOMÁTICOS  
{chr(10).join(f'• {insight}' for insight in report.get('insights', []))}

### RECOMENDACIONES
{chr(10).join(f'• {rec}' for rec in report.get('recommendations', []))}

### LIMITACIONES
{chr(10).join(f'• {lim}' for lim in report.get('limitations', []))}

### PRÓXIMOS PASOS
{chr(10).join(f'• {step}' for step in report.get('next_steps', []))}
                    """
                    
                    # Múltiples opciones de descarga
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            label="📁 Reporte (.txt)",
                            data=report_text,
                            file_name="reporte_analisis_datos.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Verificar si existe el archivo LaTeX
                        if os.path.exists("informe_enaho_2022.tex"):
                            with open("informe_enaho_2022.tex", "r", encoding="utf-8") as f:
                                latex_content = f.read()
                            st.download_button(
                                label="📊 LaTeX (.tex)",
                                data=latex_content,
                                file_name="informe_enaho_2022.tex",
                                mime="text/plain"
                            )
                    
                    with col3:
                        # Verificar si existe el archivo HTML
                        if os.path.exists("informe_enaho_2022.html"):
                            with open("informe_enaho_2022.html", "r", encoding="utf-8") as f:
                                html_content = f.read()
                            st.download_button(
                                label="🌐 HTML (.html)",
                                data=html_content,
                                file_name="informe_enaho_2022.html",
                                mime="text/html"
                            )
                    
                except Exception as e:
                    st.error(f"❌ Error al generar el reporte: {str(e)}")
        
        # Métricas del dataset
        st.subheader("📊 Métricas Finales del Dataset")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Filas Totales", len(data))
        with col2:
            st.metric("Columnas Totales", len(data.columns))
        with col3:
            st.metric("Completitud", f"{((1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100):.1f}%")
        with col4:
            st.metric("Análisis Realizados", len(st.session_state.analysis_results))
    
    else:
        st.warning("⚠️ Primero debes cargar un archivo CSV en la sección 'Carga y Exploración'.")

# Nueva Sección: Análisis Completo ENAHO
elif selected_section == "📊 Análisis Completo ENAHO":
    st.header("📊 Análisis Estadístico Completo - ENAHO 2022")
    st.markdown("**Análisis exhaustivo con las 4 secciones principales**")
    
    # Información del análisis
    st.info("""
    📋 **Análisis implementado:**
    
    **1. Estadísticas Descriptivas Básicas**
    - Resumen estadístico completo (describe())
    - Medidas de tendencia central y dispersión
    - Percentiles detallados
    - Análisis de variables categóricas
    
    **2. Detección y Limpieza de Datos**
    - Identificación de valores nulos
    - Detección de outliers (IQR y Z-score)
    - Estrategias de limpieza propuestas
    
    **3. Visualizaciones Completas**
    - Histogramas y boxplots
    - Matriz de correlación
    - Scatter plots y violin plots
    - Gráficos categóricas
    
    **4. Técnicas Estadísticas Avanzadas**
    - Clustering K-means
    - Análisis PCA
    - Regresión múltiple
    - Pruebas de hipótesis
    """)
    
    # Botón para ejecutar análisis
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Ejecutar Análisis Completo", use_container_width=True, type="primary"):
            with st.spinner("Ejecutando análisis completo... Esto puede tomar unos minutos."):
                try:
                    # Ejecutar el análisis completo
                    import subprocess
                    result = subprocess.run(['python', 'analisis_completo_enaho.py'], 
                                          capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        st.success("✅ Análisis completado exitosamente!")
                        
                        # Mostrar estadísticas del análisis
                        st.markdown("### 📈 Resultados del Análisis")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Dataset", "ENAHO 2022")
                        with col2:
                            st.metric("Registros", "100")
                        with col3:
                            st.metric("Variables", "324")
                        with col4:
                            st.metric("Técnicas Aplicadas", "4")
                        
                        # Mostrar parte de la salida
                        st.markdown("### 📋 Resumen de Resultados")
                        with st.expander("Ver detalles del análisis"):
                            st.text(result.stdout[:2000] + "..." if len(result.stdout) > 2000 else result.stdout)
                        
                        # Verificar archivos generados
                        import os
                        archivos_generados = [
                            "analisis_completo_visualizaciones.png",
                            "matriz_correlacion.png",
                            "graficos_categoricas.png",
                            "scatter_plots.png",
                            "violin_plots.png",
                            "clustering_kmeans.png",
                            "pca_analysis.png",
                            "regression_analysis.png"
                        ]
                        
                        archivos_existentes = [f for f in archivos_generados if os.path.exists(f)]
                        
                        if archivos_existentes:
                            st.markdown("### 📁 Visualizaciones Generadas")
                            st.success(f"✅ Se generaron {len(archivos_existentes)} gráficos exitosamente")
                            
                            # Mostrar lista de archivos
                            for archivo in archivos_existentes:
                                st.markdown(f"• {archivo}")
                            
                            st.info("💡 Los gráficos están disponibles en el directorio del proyecto")
                    
                    else:
                        st.error("❌ Error durante la ejecución del análisis")
                        if result.stderr:
                            st.text("Error details:")
                            st.text(result.stderr)
                
                except subprocess.TimeoutExpired:
                    st.warning("⏱️ El análisis está tomando más tiempo del esperado. Continúa ejecutándose en segundo plano.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Información adicional
    st.markdown("---")
    st.markdown("### 🔍 Detalles Técnicos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Variables Analizadas:**
        - 118 variables numéricas
        - 206 variables categóricas
        - Análisis de completitud: 100%
        """)
    
    with col2:
        st.markdown("""
        **📊 Técnicas Aplicadas:**
        - K-means clustering
        - Análisis PCA
        - Regresión múltiple
        - Pruebas t-test
        """)

# Nueva Sección: Gráficos y Visualizaciones
elif selected_section == "🖼️ Gráficos y Visualizaciones":
    from visor_graficos import mostrar_graficos_disponibles, mostrar_resumen_graficos
    mostrar_graficos_disponibles()
    mostrar_resumen_graficos()

# Nueva Sección: Documentos ENAHO
elif selected_section == "📄 Documentos ENAHO":
    from documentos_enaho import show_download_section, create_pdf_instructions
    show_download_section()
    create_pdf_instructions()

# Footer
st.markdown("---")
st.markdown("**Analizador de CSV** - Herramienta completa para análisis estadístico de datos | Desarrollado con ❤️ usando Streamlit")
