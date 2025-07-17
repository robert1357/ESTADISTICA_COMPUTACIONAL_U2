import pandas as pd
import numpy as np
from datetime import datetime

def generate_report(data, analysis_results):
    """
    Genera un reporte completo del análisis de datos
    """
    report = {
        'executive_summary': generate_executive_summary(data),
        'key_findings': generate_key_findings(data, analysis_results),
        'insights': generate_insights(data, analysis_results),
        'recommendations': generate_recommendations(data, analysis_results),
        'limitations': generate_limitations(data),
        'next_steps': generate_next_steps(data, analysis_results)
    }
    
    return report

def generate_executive_summary(data):
    """
    Genera el resumen ejecutivo del análisis
    """
    n_rows, n_cols = data.shape
    numeric_cols = len(data.select_dtypes(include=[np.number]).columns)
    categorical_cols = len(data.select_dtypes(include=['object', 'category']).columns)
    completeness = ((1 - data.isnull().sum().sum() / (n_rows * n_cols)) * 100)
    
    summary = f"""
**Resumen Ejecutivo del Análisis de Datos**

Se analizó un dataset con {n_rows:,} registros y {n_cols} variables, compuesto por {numeric_cols} variables numéricas y {categorical_cols} variables categóricas. 

**Calidad de los datos:** El dataset presenta un {completeness:.1f}% de completitud, con {data.isnull().sum().sum()} valores faltantes en total. Se identificaron {data.duplicated().sum()} registros duplicados.

**Alcance del análisis:** Se realizó un análisis estadístico completo que incluye estadísticas descriptivas, detección de valores atípicos, análisis de correlaciones, visualizaciones interactivas y técnicas de análisis avanzado.

**Fecha del análisis:** {datetime.now().strftime('%d de %B de %Y')}
    """
    
    return summary.strip()

def generate_key_findings(data, analysis_results):
    """
    Genera los hallazgos principales
    """
    findings = []
    
    # Hallazgos sobre la estructura de datos
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    
    findings.append(f"El dataset contiene {len(data)} observaciones distribuidas en {len(data.columns)} variables")
    
    # Hallazgos sobre valores nulos
    null_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
    if null_percentage > 10:
        findings.append(f"Se detectó un {null_percentage:.1f}% de valores faltantes, lo que requiere atención especial")
    elif null_percentage > 0:
        findings.append(f"El dataset presenta {null_percentage:.1f}% de valores faltantes, un nivel manejable")
    else:
        findings.append("El dataset está completo sin valores faltantes")
    
    # Hallazgos sobre variables numéricas
    if len(numeric_cols) > 0:
        # Variable con mayor variabilidad
        cv_values = (data[numeric_cols].std() / data[numeric_cols].mean()) * 100
        high_var_col = cv_values.idxmax()
        findings.append(f"La variable '{high_var_col}' presenta la mayor variabilidad (CV: {cv_values.max():.1f}%)")
        
        # Correlaciones fuertes
        if len(numeric_cols) > 1:
            corr_matrix = data[numeric_cols].corr()
            max_corr = 0
            corr_vars = None
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = abs(corr_matrix.iloc[i, j])
                    if not np.isnan(corr_val) and corr_val > max_corr:
                        max_corr = corr_val
                        corr_vars = (corr_matrix.columns[i], corr_matrix.columns[j])
            
            if max_corr > 0.7:
                findings.append(f"Se identificó una correlación fuerte ({max_corr:.3f}) entre '{corr_vars[0]}' y '{corr_vars[1]}'")
    
    # Hallazgos sobre variables categóricas
    if len(categorical_cols) > 0:
        for col in categorical_cols[:2]:  # Analizar primeras 2 variables categóricas
            unique_count = data[col].nunique()
            total_count = len(data[col].dropna())
            if unique_count / total_count > 0.5:
                findings.append(f"La variable '{col}' presenta alta diversidad con {unique_count} categorías únicas")
            else:
                most_common = data[col].mode().iloc[0] if len(data[col].mode()) > 0 else "N/A"
                findings.append(f"En '{col}', la categoría más frecuente es '{most_common}'")
    
    # Hallazgos de análisis avanzados
    for analysis_type, results in analysis_results.items():
        if analysis_type == "Regresión Lineal/Múltiple" and 'r2_score' in results:
            r2 = results['r2_score']
            if r2 > 0.8:
                findings.append(f"El modelo de regresión explica {r2:.1%} de la varianza, indicando una relación predictiva fuerte")
            elif r2 > 0.5:
                findings.append(f"El modelo de regresión explica {r2:.1%} de la varianza, mostrando una relación moderada")
        
        elif analysis_type == "Clustering (K-means)" and 'n_clusters' in results:
            n_clusters = results['n_clusters']
            silhouette = results.get('silhouette_score', 0)
            findings.append(f"Se identificaron {n_clusters} grupos naturales en los datos con calidad de separación de {silhouette:.3f}")
    
    return findings

def generate_insights(data, analysis_results):
    """
    Genera insights automáticos basados en el análisis
    """
    insights = []
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    
    # Insights sobre distribuciones
    if len(numeric_cols) > 0:
        # Detectar asimetría
        skewness = data[numeric_cols].skew()
        highly_skewed = skewness[abs(skewness) > 1].index.tolist()
        
        if len(highly_skewed) > 0:
            insights.append(f"Las variables {', '.join(highly_skewed)} presentan distribuciones asimétricas que podrían beneficiarse de transformaciones")
    
    # Insights sobre completitud de datos
    incomplete_cols = data.columns[data.isnull().any()].tolist()
    if len(incomplete_cols) > 0:
        worst_col = data.isnull().sum().idxmax()
        worst_percentage = (data[worst_col].isnull().sum() / len(data)) * 100
        insights.append(f"La variable '{worst_col}' tiene {worst_percentage:.1f}% de datos faltantes, considerar estrategias de imputación")
    
    # Insights sobre valores atípicos
    if len(numeric_cols) > 0:
        outlier_info = []
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
            if len(outliers) > len(data) * 0.05:  # Más del 5% son outliers
                outlier_info.append(col)
        
        if outlier_info:
            insights.append(f"Las variables {', '.join(outlier_info)} contienen una proporción significativa de valores atípicos")
    
    # Insights específicos de análisis avanzados
    for analysis_type, results in analysis_results.items():
        if analysis_type == "Análisis de Correlación Detallado":
            if 'significant_correlations' in results:
                strong_corrs = results['significant_correlations'][
                    results['significant_correlations']['Correlación'].abs() > 0.7
                ]
                if len(strong_corrs) > 0:
                    insights.append("Existen relaciones lineales fuertes entre variables que podrían indicar redundancia o causalidad")
        
        elif analysis_type == "Clustering (K-means)":
            if 'silhouette_score' in results:
                score = results['silhouette_score']
                if score > 0.7:
                    insights.append("Los datos presentan grupos naturales bien definidos, sugiriendo segmentación clara")
                elif score > 0.5:
                    insights.append("Existe cierta estructura de agrupamiento en los datos, aunque con alguna superposición")
    
    # Insights sobre escalas y rangos
    if len(numeric_cols) > 1:
        ranges = data[numeric_cols].max() - data[numeric_cols].min()
        if ranges.max() / ranges.min() > 100:
            insights.append("Las variables numéricas operan en escalas muy diferentes, considerar normalización para análisis comparativos")
    
    return insights

def generate_recommendations(data, analysis_results):
    """
    Genera recomendaciones basadas en el análisis
    """
    recommendations = []
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    
    # Recomendaciones sobre calidad de datos
    null_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
    if null_percentage > 20:
        recommendations.append("Implementar una estrategia integral de manejo de datos faltantes antes de análisis adicionales")
    elif null_percentage > 5:
        recommendations.append("Evaluar patrones de datos faltantes y aplicar técnicas de imputación apropiadas")
    
    # Recomendaciones sobre outliers
    if len(numeric_cols) > 0:
        high_outlier_cols = []
        for col in numeric_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
            if len(outliers) > len(data) * 0.1:
                high_outlier_cols.append(col)
        
        if high_outlier_cols:
            recommendations.append("Investigar y tratar valores atípicos en variables clave para mejorar la robustez del análisis")
    
    # Recomendaciones específicas por tipo de análisis
    for analysis_type, results in analysis_results.items():
        if analysis_type == "Regresión Lineal/Múltiple":
            if 'r2_score' in results:
                r2 = results['r2_score']
                if r2 < 0.3:
                    recommendations.append("Explorar variables adicionales o transformaciones no lineales para mejorar el poder predictivo")
                elif r2 > 0.8:
                    recommendations.append("Validar el modelo con datos externos para confirmar su capacidad de generalización")
        
        elif analysis_type == "Clustering (K-means)":
            if 'silhouette_score' in results:
                score = results['silhouette_score']
                if score < 0.5:
                    recommendations.append("Considerar algoritmos de clustering alternativos o diferentes números de grupos")
                else:
                    recommendations.append("Utilizar los grupos identificados para personalización o segmentación estratégica")
    
    # Recomendaciones sobre visualización y presentación
    if len(data) > 10000:
        recommendations.append("Para datasets grandes, implementar técnicas de muestreo para visualizaciones más eficientes")
    
    if len(categorical_cols) > 0:
        high_cardinality_cols = [col for col in categorical_cols if data[col].nunique() > 20]
        if high_cardinality_cols:
            recommendations.append("Considerar técnicas de codificación o agrupación para variables categóricas con alta cardinalidad")
    
    # Recomendaciones sobre análisis futuros
    if len(numeric_cols) >= 3 and "Análisis de Componentes Principales (PCA)" not in analysis_results:
        recommendations.append("Explorar análisis de componentes principales para reducción de dimensionalidad")
    
    if len(categorical_cols) >= 2 and "Pruebas de Hipótesis" not in analysis_results:
        recommendations.append("Realizar pruebas de independencia entre variables categóricas")
    
    return recommendations

def generate_limitations(data):
    """
    Genera limitaciones del análisis
    """
    limitations = []
    
    # Limitaciones por tamaño de muestra
    if len(data) < 30:
        limitations.append("El tamaño de muestra es pequeño, lo que puede afectar la validez de las pruebas estadísticas")
    elif len(data) < 100:
        limitations.append("El tamaño de muestra es limitado para ciertos análisis de machine learning")
    
    # Limitaciones por datos faltantes
    null_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
    if null_percentage > 10:
        limitations.append("La presencia significativa de datos faltantes puede introducir sesgos en los resultados")
    
    # Limitaciones por tipo de datos
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        limitations.append("Pocas variables numéricas limitan el alcance de análisis de correlación y regresión")
    
    # Limitaciones temporales
    date_cols = []
    for col in data.columns:
        if data[col].dtype == 'datetime64[ns]' or 'date' in col.lower() or 'time' in col.lower():
            date_cols.append(col)
    
    if len(date_cols) == 0:
        limitations.append("Sin variables temporales, no es posible realizar análisis de series de tiempo o tendencias")
    
    # Limitaciones de causalidad
    limitations.append("Los análisis de correlación no implican causalidad; se requiere investigación adicional para establecer relaciones causales")
    
    # Limitaciones de generalización
    limitations.append("Los resultados son específicos para este dataset y pueden no ser generalizables a poblaciones diferentes")
    
    return limitations

def generate_next_steps(data, analysis_results):
    """
    Genera próximos pasos sugeridos
    """
    next_steps = []
    
    # Pasos para mejorar calidad de datos
    null_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
    if null_percentage > 0:
        next_steps.append("Desarrollar una estrategia de recolección de datos para reducir valores faltantes")
    
    # Pasos para análisis adicionales
    if "Regresión Lineal/Múltiple" in analysis_results:
        next_steps.append("Validar modelo predictivo con datos nuevos y evaluar su desempeño en tiempo real")
    
    if "Clustering (K-means)" in analysis_results:
        next_steps.append("Caracterizar cada grupo identificado y desarrollar estrategias específicas por segmento")
    
    # Pasos para implementación
    next_steps.append("Crear un dashboard interactivo para monitoreo continuo de las métricas clave")
    next_steps.append("Establecer un proceso de actualización periódica del análisis con nuevos datos")
    
    # Pasos para análisis avanzados
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) >= 5:
        next_steps.append("Explorar algoritmos de machine learning más sofisticados (Random Forest, SVM, Neural Networks)")
    
    # Pasos para validación externa
    next_steps.append("Recolectar datos adicionales para validar patrones identificados")
    next_steps.append("Consultar con expertos del dominio para interpretar hallazgos desde perspectiva del negocio")
    
    # Pasos para automatización
    next_steps.append("Automatizar el pipeline de análisis para procesamiento regular de datos actualizados")
    
    return next_steps

def format_report_for_download(report_data):
    """
    Formatea el reporte para descarga en texto plano
    """
    formatted_report = f"""
# REPORTE COMPLETO DE ANÁLISIS DE DATOS
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## RESUMEN EJECUTIVO
{report_data.get('executive_summary', 'No disponible')}

## HALLAZGOS PRINCIPALES
{chr(10).join(['• ' + finding for finding in report_data.get('key_findings', [])])}

## INSIGHTS AUTOMÁTICOS
{chr(10).join(['• ' + insight for insight in report_data.get('insights', [])])}

## RECOMENDACIONES
{chr(10).join(['• ' + rec for rec in report_data.get('recommendations', [])])}

## LIMITACIONES DEL ANÁLISIS
{chr(10).join(['• ' + lim for lim in report_data.get('limitations', [])])}

## PRÓXIMOS PASOS SUGERIDOS
{chr(10).join(['• ' + step for step in report_data.get('next_steps', [])])}

---
Reporte generado automáticamente por el Analizador de CSV
    """
    
    return formatted_report.strip()
