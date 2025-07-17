import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st

def get_descriptive_stats(data):
    """
    Calcula estadísticas descriptivas completas para el dataset
    """
    results = {}
    
    # Variables numéricas
    numeric_data = data.select_dtypes(include=[np.number])
    if len(numeric_data.columns) > 0:
        # Estadísticas básicas
        basic_stats = numeric_data.describe()
        
        # Estadísticas adicionales
        additional_stats = pd.DataFrame({
            'Media': numeric_data.mean(),
            'Mediana': numeric_data.median(),
            'Moda': numeric_data.mode().iloc[0] if len(numeric_data.mode()) > 0 else np.nan,
            'Desviación Estándar': numeric_data.std(),
            'Varianza': numeric_data.var(),
            'Rango': numeric_data.max() - numeric_data.min(),
            'Coef. Variación': (numeric_data.std() / numeric_data.mean()) * 100,
            'Asimetría': numeric_data.skew(),
            'Curtosis': numeric_data.kurtosis()
        })
        
        # Percentiles
        percentiles = numeric_data.quantile([0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95])
        
        results['numeric_stats'] = pd.concat([basic_stats, additional_stats.T])
        results['percentiles'] = percentiles
        results['additional_stats'] = additional_stats
    
    # Variables categóricas
    categorical_data = data.select_dtypes(include=['object', 'category'])
    if len(categorical_data.columns) > 0:
        cat_stats = {}
        for col in categorical_data.columns:
            cat_stats[col] = {
                'unique_values': categorical_data[col].nunique(),
                'most_frequent': categorical_data[col].mode().iloc[0] if len(categorical_data[col].mode()) > 0 else None,
                'most_frequent_count': categorical_data[col].value_counts().iloc[0] if len(categorical_data[col].value_counts()) > 0 else 0,
                'value_counts': categorical_data[col].value_counts(),
                'percentages': categorical_data[col].value_counts(normalize=True) * 100
            }
        results['categorical_stats'] = cat_stats
    
    return results

def detect_outliers(data, column, methods=['iqr', 'zscore']):
    """
    Detecta valores atípicos usando diferentes métodos
    """
    if column not in data.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el dataset")
    
    col_data = data[column].dropna()
    outliers_info = {}
    
    if 'iqr' in methods:
        # Método IQR
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        iqr_outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)].index.tolist()
        outliers_info['iqr_outliers'] = iqr_outliers
        outliers_info['iqr_bounds'] = {'lower': lower_bound, 'upper': upper_bound}
    
    if 'zscore' in methods:
        # Método Z-score
        z_scores = np.abs(stats.zscore(col_data))
        zscore_outliers = data[np.abs(stats.zscore(data[column].fillna(col_data.mean()))) > 3].index.tolist()
        outliers_info['zscore_outliers'] = zscore_outliers
        outliers_info['z_threshold'] = 3
    
    return outliers_info

def clean_data(data, null_strategy="No aplicar", outlier_strategy="No aplicar"):
    """
    Aplica estrategias de limpieza de datos
    """
    cleaned_data = data.copy()
    
    # Tratamiento de valores nulos
    if null_strategy == "Eliminar filas":
        cleaned_data = cleaned_data.dropna()
    elif null_strategy == "Imputar con media":
        numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            cleaned_data[col].fillna(cleaned_data[col].mean(), inplace=True)
    elif null_strategy == "Imputar con mediana":
        numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            cleaned_data[col].fillna(cleaned_data[col].median(), inplace=True)
    elif null_strategy == "Imputar con moda":
        for col in cleaned_data.columns:
            if cleaned_data[col].isnull().sum() > 0:
                mode_value = cleaned_data[col].mode()
                if len(mode_value) > 0:
                    cleaned_data[col].fillna(mode_value.iloc[0], inplace=True)
    
    # Tratamiento de valores atípicos
    if outlier_strategy != "No aplicar":
        numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if outlier_strategy == "Eliminar valores atípicos":
                # Usar método IQR para eliminar
                Q1 = cleaned_data[col].quantile(0.25)
                Q3 = cleaned_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                cleaned_data = cleaned_data[
                    (cleaned_data[col] >= lower_bound) & 
                    (cleaned_data[col] <= upper_bound)
                ]
            
            elif outlier_strategy == "Transformar con log":
                if (cleaned_data[col] > 0).all():  # Solo si todos los valores son positivos
                    cleaned_data[col] = np.log1p(cleaned_data[col])
            
            elif outlier_strategy == "Winsorización":
                # Winsorización al 5% y 95%
                lower_percentile = cleaned_data[col].quantile(0.05)
                upper_percentile = cleaned_data[col].quantile(0.95)
                
                cleaned_data[col] = np.clip(
                    cleaned_data[col], 
                    lower_percentile, 
                    upper_percentile
                )
    
    return cleaned_data

def correlation_analysis(data):
    """
    Realiza análisis de correlación detallado
    """
    numeric_data = data.select_dtypes(include=[np.number])
    
    if len(numeric_data.columns) < 2:
        return None
    
    # Matriz de correlación
    corr_matrix = numeric_data.corr()
    
    # Correlaciones significativas (filtrar las más altas)
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if not np.isnan(corr_value):
                corr_pairs.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlación': corr_value,
                    'Interpretación': interpret_correlation(corr_value)
                })
    
    corr_df = pd.DataFrame(corr_pairs)
    corr_df = corr_df.sort_values('Correlación', key=abs, ascending=False)
    
    return {
        'correlation_matrix': corr_matrix,
        'significant_correlations': corr_df,
        'strongest_positive': corr_df[corr_df['Correlación'] > 0].head(3),
        'strongest_negative': corr_df[corr_df['Correlación'] < 0].head(3)
    }

def interpret_correlation(corr_value):
    """
    Interpreta el valor de correlación
    """
    abs_corr = abs(corr_value)
    
    if abs_corr >= 0.9:
        strength = "Muy fuerte"
    elif abs_corr >= 0.7:
        strength = "Fuerte"
    elif abs_corr >= 0.5:
        strength = "Moderada"
    elif abs_corr >= 0.3:
        strength = "Débil"
    else:
        strength = "Muy débil"
    
    direction = "positiva" if corr_value > 0 else "negativa"
    
    return f"{strength} {direction}"

def statistical_tests(data):
    """
    Realiza pruebas estadísticas básicas
    """
    results = {}
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # Prueba de normalidad (Shapiro-Wilk) para variables numéricas
    if len(numeric_cols) > 0:
        normality_tests = {}
        for col in numeric_cols[:5]:  # Limitar a 5 variables para evitar sobrecarga
            if len(data[col].dropna()) > 3:  # Mínimo de datos requerido
                statistic, p_value = stats.shapiro(data[col].dropna()[:5000])  # Máximo 5000 datos
                normality_tests[col] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'is_normal': p_value > 0.05
                }
        results['normality_tests'] = normality_tests
    
    return results
