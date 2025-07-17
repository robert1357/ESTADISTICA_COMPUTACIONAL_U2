import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns

def create_visualizations(data):
    """
    Crea un conjunto completo de visualizaciones para el dataset
    """
    visualizations = {}
    
    # Variables numéricas y categóricas
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Histogramas para variables numéricas
    if numeric_cols:
        visualizations['histograms'] = create_histograms(data, numeric_cols)
    
    # 2. Boxplots para detección de outliers
    if numeric_cols:
        visualizations['boxplots'] = create_boxplots(data, numeric_cols)
    
    # 3. Mapa de calor de correlaciones
    if len(numeric_cols) > 1:
        visualizations['correlation_heatmap'] = create_correlation_heatmap(data, numeric_cols)
    
    # 4. Gráficos de dispersión
    if len(numeric_cols) >= 2:
        visualizations['scatter_plots'] = create_scatter_plots(data, numeric_cols)
    
    # 5. Gráficos de barras para variables categóricas
    if categorical_cols:
        visualizations['categorical_plots'] = create_categorical_plots(data, categorical_cols)
    
    # 6. Gráficos de violín
    if numeric_cols:
        visualizations['violin_plots'] = create_violin_plots(data, numeric_cols)
    
    # 7. Visualizaciones avanzadas
    visualizations['advanced_plots'] = create_advanced_plots(data, numeric_cols, categorical_cols)
    
    return visualizations

def create_histograms(data, numeric_cols):
    """
    Crea histogramas para variables numéricas
    """
    n_cols = len(numeric_cols)
    n_rows = (n_cols + 2) // 3  # 3 columnas por fila
    
    fig = make_subplots(
        rows=n_rows, 
        cols=min(3, n_cols),
        subplot_titles=numeric_cols,
        vertical_spacing=0.1
    )
    
    for i, col in enumerate(numeric_cols):
        row = (i // 3) + 1
        col_pos = (i % 3) + 1
        
        # Crear histograma
        hist_data = data[col].dropna()
        
        fig.add_trace(
            go.Histogram(
                x=hist_data,
                name=col,
                nbinsx=30,
                opacity=0.7
            ),
            row=row, col=col_pos
        )
    
    fig.update_layout(
        title="Distribución de Variables Numéricas",
        height=300 * n_rows,
        showlegend=False
    )
    
    return fig

def create_boxplots(data, numeric_cols):
    """
    Crea boxplots para detectar valores atípicos
    """
    fig = go.Figure()
    
    for col in numeric_cols:
        fig.add_trace(
            go.Box(
                y=data[col],
                name=col,
                boxpoints='outliers'
            )
        )
    
    fig.update_layout(
        title="Boxplots para Detección de Valores Atípicos",
        yaxis_title="Valores",
        height=500
    )
    
    return fig

def create_correlation_heatmap(data, numeric_cols):
    """
    Crea mapa de calor de correlaciones
    """
    corr_matrix = data[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Mapa de Calor - Matriz de Correlación",
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1
    )
    
    fig.update_layout(height=600)
    
    return fig

def create_scatter_plots(data, numeric_cols):
    """
    Crea gráficos de dispersión para pares de variables
    """
    # Seleccionar las dos variables con mayor correlación
    corr_matrix = data[numeric_cols].corr()
    
    # Encontrar el par con mayor correlación absoluta
    max_corr = 0
    best_pair = (numeric_cols[0], numeric_cols[1]) if len(numeric_cols) >= 2 else None
    
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            corr_val = abs(corr_matrix.iloc[i, j])
            if not np.isnan(corr_val) and corr_val > max_corr:
                max_corr = corr_val
                best_pair = (numeric_cols[i], numeric_cols[j])
    
    if best_pair:
        fig = px.scatter(
            data,
            x=best_pair[0],
            y=best_pair[1],
            title=f"Gráfico de Dispersión: {best_pair[0]} vs {best_pair[1]}",
            trendline="ols"
        )
        
        fig.update_layout(height=500)
        return fig
    
    return None

def create_categorical_plots(data, categorical_cols):
    """
    Crea gráficos de barras para variables categóricas
    """
    plots = []
    
    for col in categorical_cols[:5]:  # Limitar a 5 variables
        value_counts = data[col].value_counts().head(10)  # Top 10 valores
        
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=f"Distribución de {col}",
            labels={'x': col, 'y': 'Frecuencia'}
        )
        
        fig.update_layout(height=400)
        plots.append(fig)
    
    return plots

def create_violin_plots(data, numeric_cols):
    """
    Crea gráficos de violín para mostrar distribuciones
    """
    fig = go.Figure()
    
    for col in numeric_cols[:6]:  # Limitar a 6 variables
        fig.add_trace(
            go.Violin(
                y=data[col],
                name=col,
                box_visible=True,
                meanline_visible=True
            )
        )
    
    fig.update_layout(
        title="Gráficos de Violín - Distribuciones Detalladas",
        yaxis_title="Valores",
        height=500
    )
    
    return fig

def create_advanced_plots(data, numeric_cols, categorical_cols):
    """
    Crea visualizaciones avanzadas adicionales
    """
    plots = []
    
    # 1. Matriz de dispersión si hay múltiples variables numéricas
    if len(numeric_cols) >= 3:
        scatter_matrix = create_scatter_matrix(data, numeric_cols[:4])  # Máximo 4 variables
        if scatter_matrix:
            plots.append(scatter_matrix)
    
    # 2. Gráfico de densidad para variables numéricas
    if len(numeric_cols) >= 2:
        density_plot = create_density_plot(data, numeric_cols[:3])
        if density_plot:
            plots.append(density_plot)
    
    # 3. Análisis de variables categóricas vs numéricas
    if categorical_cols and numeric_cols:
        cat_num_plot = create_categorical_numeric_plot(data, categorical_cols[0], numeric_cols[0])
        if cat_num_plot:
            plots.append(cat_num_plot)
    
    return plots

def create_scatter_matrix(data, numeric_cols):
    """
    Crea una matriz de dispersión
    """
    try:
        fig = px.scatter_matrix(
            data[numeric_cols],
            title="Matriz de Dispersión",
            height=600
        )
        return fig
    except:
        return None

def create_density_plot(data, numeric_cols):
    """
    Crea gráfico de densidad
    """
    fig = go.Figure()
    
    for col in numeric_cols:
        try:
            # Crear datos para el gráfico de densidad
            col_data = data[col].dropna()
            
            fig.add_trace(
                go.Histogram(
                    x=col_data,
                    name=col,
                    opacity=0.6,
                    histnorm='probability density'
                )
            )
        except:
            continue
    
    fig.update_layout(
        title="Gráficos de Densidad",
        xaxis_title="Valores",
        yaxis_title="Densidad",
        height=400
    )
    
    return fig

def create_categorical_numeric_plot(data, cat_col, num_col):
    """
    Crea gráfico que relaciona variable categórica con numérica
    """
    try:
        # Limitar categorías para evitar sobrecarga visual
        top_categories = data[cat_col].value_counts().head(8).index
        filtered_data = data[data[cat_col].isin(top_categories)]
        
        fig = px.box(
            filtered_data,
            x=cat_col,
            y=num_col,
            title=f"Distribución de {num_col} por {cat_col}"
        )
        
        fig.update_layout(height=500)
        return fig
    except:
        return None

def create_time_series_plot(data, date_col, value_cols):
    """
    Crea gráfico de series temporales si hay columnas de fecha
    """
    try:
        fig = go.Figure()
        
        for col in value_cols:
            fig.add_trace(
                go.Scatter(
                    x=data[date_col],
                    y=data[col],
                    mode='lines',
                    name=col
                )
            )
        
        fig.update_layout(
            title="Análisis de Series Temporales",
            xaxis_title="Fecha",
            yaxis_title="Valores",
            height=500
        )
        
        return fig
    except:
        return None
