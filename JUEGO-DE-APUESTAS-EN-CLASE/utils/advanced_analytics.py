import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, silhouette_score
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def perform_advanced_analysis(data, analysis_type):
    """
    Ejecuta análisis estadístico avanzado según el tipo seleccionado
    """
    results = {}
    
    try:
        if analysis_type == "Análisis de Correlación Detallado":
            results = detailed_correlation_analysis(data)
        
        elif analysis_type == "Regresión Lineal/Múltiple":
            results = regression_analysis(data)
        
        elif analysis_type == "Clustering (K-means)":
            results = clustering_analysis(data)
        
        elif analysis_type == "Análisis de Componentes Principales (PCA)":
            results = pca_analysis(data)
        
        elif analysis_type == "Pruebas de Hipótesis":
            results = hypothesis_testing(data)
        
        return results
    
    except Exception as e:
        raise Exception(f"Error en el análisis avanzado: {str(e)}")

def detailed_correlation_analysis(data):
    """
    Análisis de correlación detallado con interpretaciones
    """
    numeric_data = data.select_dtypes(include=[np.number])
    
    if len(numeric_data.columns) < 2:
        raise ValueError("Se necesitan al menos 2 variables numéricas para el análisis de correlación")
    
    # Matriz de correlación
    corr_matrix = numeric_data.corr()
    
    # Identificar correlaciones significativas
    significant_correlations = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if not np.isnan(corr_value):
                significance = interpret_correlation_strength(abs(corr_value))
                significant_correlations.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlación': round(corr_value, 4),
                    'Fuerza': significance,
                    'Interpretación': generate_correlation_interpretation(
                        corr_matrix.columns[i], 
                        corr_matrix.columns[j], 
                        corr_value
                    )
                })
    
    significant_df = pd.DataFrame(significant_correlations)
    significant_df = significant_df.sort_values('Correlación', key=abs, ascending=False)
    
    return {
        'correlation_matrix': corr_matrix,
        'significant_correlations': significant_df,
        'summary': generate_correlation_summary(significant_df)
    }

def regression_analysis(data):
    """
    Análisis de regresión lineal/múltiple
    """
    numeric_data = data.select_dtypes(include=[np.number]).dropna()
    
    if len(numeric_data.columns) < 2:
        raise ValueError("Se necesitan al menos 2 variables numéricas para regresión")
    
    # Seleccionar variable dependiente (la que tenga mayor correlación promedio)
    corr_matrix = numeric_data.corr()
    avg_correlations = corr_matrix.abs().mean().sort_values(ascending=False)
    
    target_col = avg_correlations.index[0]
    feature_cols = [col for col in numeric_data.columns if col != target_col]
    
    if len(feature_cols) == 0:
        raise ValueError("No hay variables predictoras disponibles")
    
    X = numeric_data[feature_cols]
    y = numeric_data[target_col]
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Entrenar modelo
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predicciones
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Métricas
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    # Importancia de características
    feature_importance = pd.DataFrame({
        'Variable': feature_cols,
        'Coeficiente': model.coef_,
        'Importancia_Abs': np.abs(model.coef_)
    }).sort_values('Importancia_Abs', ascending=False)
    
    # Gráfico de predicciones vs valores reales
    predictions_plot = create_regression_plot(y_test, y_pred_test, target_col)
    
    return {
        'r2_score': r2_test,
        'r2_train': r2_train,
        'rmse': rmse_test,
        'feature_importance': feature_importance,
        'predictions_plot': predictions_plot,
        'model_summary': {
            'target_variable': target_col,
            'n_features': len(feature_cols),
            'n_samples': len(y),
            'intercept': model.intercept_
        }
    }

def clustering_analysis(data):
    """
    Análisis de clustering usando K-means
    """
    numeric_data = data.select_dtypes(include=[np.number]).dropna()
    
    if len(numeric_data.columns) < 2:
        raise ValueError("Se necesitan al menos 2 variables numéricas para clustering")
    
    # Estandarizar datos
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)
    
    # Determinar número óptimo de clusters (método del codo)
    inertias = []
    silhouette_scores = []
    k_range = range(2, min(11, len(numeric_data) // 2))
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_data)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(scaled_data, kmeans.labels_))
    
    # Seleccionar mejor k (mayor silhouette score)
    best_k = k_range[np.argmax(silhouette_scores)]
    
    # Clustering final
    final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    clusters = final_kmeans.fit_predict(scaled_data)
    
    # Agregar clusters al dataset original
    clustered_data = numeric_data.copy()
    clustered_data['Cluster'] = clusters
    
    # Crear visualización
    cluster_plot = create_cluster_plot(clustered_data, numeric_data.columns[:2], best_k)
    
    # Centros de clusters (en escala original)
    cluster_centers = pd.DataFrame(
        scaler.inverse_transform(final_kmeans.cluster_centers_),
        columns=numeric_data.columns,
        index=[f'Cluster {i}' for i in range(best_k)]
    )
    
    return {
        'n_clusters': best_k,
        'silhouette_score': silhouette_scores[best_k - 2],
        'cluster_plot': cluster_plot,
        'cluster_centers': cluster_centers,
        'clustered_data': clustered_data,
        'inertias': inertias,
        'silhouette_scores': silhouette_scores
    }

def pca_analysis(data):
    """
    Análisis de Componentes Principales
    """
    numeric_data = data.select_dtypes(include=[np.number]).dropna()
    
    if len(numeric_data.columns) < 3:
        raise ValueError("Se necesitan al menos 3 variables numéricas para PCA")
    
    # Estandarizar datos
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)
    
    # Aplicar PCA
    pca = PCA()
    pca_result = pca.fit_transform(scaled_data)
    
    # Varianza explicada
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    # Número de componentes que explican al menos 80% de la varianza
    n_components_80 = np.argmax(cumulative_variance >= 0.8) + 1
    
    # Crear DataFrame con componentes principales
    pca_columns = [f'PC{i+1}' for i in range(len(explained_variance))]
    pca_df = pd.DataFrame(pca_result, columns=pca_columns)
    
    # Cargas de los componentes
    components_df = pd.DataFrame(
        pca.components_[:3].T,  # Primeras 3 componentes
        columns=['PC1', 'PC2', 'PC3'],
        index=numeric_data.columns
    )
    
    # Crear visualización
    pca_plot = create_pca_plot(pca_df, explained_variance)
    
    return {
        'explained_variance': explained_variance.tolist(),
        'cumulative_variance': cumulative_variance.tolist(),
        'n_components_80': n_components_80,
        'pca_plot': pca_plot,
        'components_df': components_df,
        'pca_data': pca_df
    }

def hypothesis_testing(data):
    """
    Realiza pruebas de hipótesis estadísticas
    """
    results = {'test_results': {}}
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Prueba de normalidad (Shapiro-Wilk)
    if len(numeric_cols) > 0:
        normality_results = {}
        for col in numeric_cols[:3]:  # Limitar a 3 variables
            col_data = data[col].dropna()
            if len(col_data) > 3 and len(col_data) <= 5000:
                statistic, p_value = stats.shapiro(col_data)
                normality_results[f'Normalidad - {col}'] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'interpretation': 'Los datos siguen distribución normal' if p_value > 0.05 else 'Los datos NO siguen distribución normal'
                }
        results['test_results'].update(normality_results)
    
    # 2. Prueba t de una muestra (comparar con la media)
    if len(numeric_cols) > 0:
        for col in numeric_cols[:2]:
            col_data = data[col].dropna()
            if len(col_data) > 1:
                mean_value = col_data.mean()
                statistic, p_value = stats.ttest_1samp(col_data, mean_value)
                results['test_results'][f'T-test - {col}'] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'interpretation': f'La media de {col} es significativamente diferente del valor testado' if p_value < 0.05 else f'No hay diferencia significativa en la media de {col}'
                }
    
    # 3. Prueba chi-cuadrado para variables categóricas
    if len(categorical_cols) >= 2:
        cat1, cat2 = categorical_cols[:2]
        contingency_table = pd.crosstab(data[cat1], data[cat2])
        if contingency_table.size > 1:
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
            results['test_results'][f'Chi-cuadrado - {cat1} vs {cat2}'] = {
                'statistic': chi2,
                'p_value': p_value,
                'interpretation': f'Existe asociación significativa entre {cat1} y {cat2}' if p_value < 0.05 else f'No existe asociación significativa entre {cat1} y {cat2}'
            }
    
    return results

# Funciones auxiliares para visualización

def create_regression_plot(y_true, y_pred, target_col):
    """
    Crea gráfico de predicciones vs valores reales
    """
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(
        go.Scatter(
            x=y_true,
            y=y_pred,
            mode='markers',
            name='Predicciones',
            marker=dict(
                color='blue',
                opacity=0.6
            )
        )
    )
    
    # Línea perfecta (y = x)
    min_val = min(min(y_true), min(y_pred))
    max_val = max(max(y_true), max(y_pred))
    
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Predicción Perfecta',
            line=dict(color='red', dash='dash')
        )
    )
    
    fig.update_layout(
        title=f'Predicciones vs Valores Reales - {target_col}',
        xaxis_title='Valores Reales',
        yaxis_title='Predicciones',
        height=500
    )
    
    return fig

def create_cluster_plot(data, feature_cols, n_clusters):
    """
    Crea visualización de clusters
    """
    if len(feature_cols) >= 2:
        fig = px.scatter(
            data,
            x=feature_cols[0],
            y=feature_cols[1],
            color='Cluster',
            title=f'Clustering K-means (k={n_clusters})',
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
        fig.update_layout(height=500)
        return fig
    
    return None

def create_pca_plot(pca_data, explained_variance):
    """
    Crea visualización de PCA
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Varianza Explicada por Componente', 'PC1 vs PC2'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Gráfico de varianza explicada
    fig.add_trace(
        go.Bar(
            x=[f'PC{i+1}' for i in range(len(explained_variance))],
            y=explained_variance,
            name='Varianza Explicada'
        ),
        row=1, col=1
    )
    
    # Scatter plot PC1 vs PC2
    if 'PC1' in pca_data.columns and 'PC2' in pca_data.columns:
        fig.add_trace(
            go.Scatter(
                x=pca_data['PC1'],
                y=pca_data['PC2'],
                mode='markers',
                name='Observaciones',
                marker=dict(opacity=0.6)
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title='Análisis de Componentes Principales (PCA)',
        height=500
    )
    
    return fig

# Funciones auxiliares de interpretación

def interpret_correlation_strength(corr_value):
    """
    Interpreta la fuerza de correlación
    """
    if corr_value >= 0.9:
        return "Muy fuerte"
    elif corr_value >= 0.7:
        return "Fuerte"
    elif corr_value >= 0.5:
        return "Moderada"
    elif corr_value >= 0.3:
        return "Débil"
    else:
        return "Muy débil"

def generate_correlation_interpretation(var1, var2, corr_value):
    """
    Genera interpretación textual de la correlación
    """
    direction = "positiva" if corr_value > 0 else "negativa"
    strength = interpret_correlation_strength(abs(corr_value))
    
    if abs(corr_value) >= 0.7:
        return f"Correlación {strength} {direction}: {var1} y {var2} están fuertemente relacionadas"
    elif abs(corr_value) >= 0.3:
        return f"Correlación {strength} {direction}: Existe relación moderada entre {var1} y {var2}"
    else:
        return f"Correlación {strength}: Poca o ninguna relación lineal entre {var1} y {var2}"

def generate_correlation_summary(correlations_df):
    """
    Genera resumen del análisis de correlación
    """
    if len(correlations_df) == 0:
        return "No se encontraron correlaciones significativas"
    
    strong_correlations = correlations_df[correlations_df['Correlación'].abs() >= 0.7]
    moderate_correlations = correlations_df[
        (correlations_df['Correlación'].abs() >= 0.3) & 
        (correlations_df['Correlación'].abs() < 0.7)
    ]
    
    summary = f"""
    Resumen del Análisis de Correlación:
    - Total de pares analizados: {len(correlations_df)}
    - Correlaciones fuertes (|r| ≥ 0.7): {len(strong_correlations)}
    - Correlaciones moderadas (0.3 ≤ |r| < 0.7): {len(moderate_correlations)}
    - Correlación más fuerte: {correlations_df.iloc[0]['Correlación']:.3f} entre {correlations_df.iloc[0]['Variable 1']} y {correlations_df.iloc[0]['Variable 2']}
    """
    
    return summary
