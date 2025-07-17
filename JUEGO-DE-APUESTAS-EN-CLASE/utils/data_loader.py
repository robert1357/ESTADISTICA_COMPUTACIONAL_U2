import pandas as pd
import chardet
import streamlit as st
from io import StringIO

def detect_encoding(file_bytes):
    """
    Detecta la codificación de un archivo usando chardet
    """
    try:
        result = chardet.detect(file_bytes)
        encoding = result['encoding']
        confidence = result['confidence']
        
        # Si la confianza es baja, intentar con codificaciones comunes
        if confidence < 0.7:
            common_encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            for enc in common_encodings:
                try:
                    file_bytes.decode(enc)
                    return enc
                except:
                    continue
        
        return encoding if encoding else 'utf-8'
    except:
        return 'utf-8'

def load_csv_with_encoding(uploaded_file):
    """
    Carga un archivo CSV con detección automática de codificación
    """
    # Leer bytes del archivo
    file_bytes = uploaded_file.read()
    
    # Detectar codificación
    encoding = detect_encoding(file_bytes)
    
    # Intentar diferentes separadores
    separators = [',', ';', '\t', '|']
    
    for separator in separators:
        try:
            # Resetear el puntero del archivo
            uploaded_file.seek(0)
            
            # Convertir bytes a string con la codificación detectada
            string_data = file_bytes.decode(encoding)
            string_io = StringIO(string_data)
            
            # Intentar leer el CSV
            df = pd.read_csv(string_io, sep=separator, encoding=None)
            
            # Verificar que el DataFrame tiene sentido (más de una columna o datos válidos)
            if len(df.columns) > 1 or (len(df.columns) == 1 and len(df) > 0):
                return df
                
        except Exception as e:
            continue
    
    # Si todo falla, intentar con configuración por defecto
    try:
        uploaded_file.seek(0)
        string_data = file_bytes.decode('utf-8', errors='ignore')
        string_io = StringIO(string_data)
        return pd.read_csv(string_io)
    except Exception as e:
        raise Exception(f"No se pudo cargar el archivo CSV: {str(e)}")

def get_basic_info(data):
    """
    Obtiene información básica del dataset
    """
    info = {
        'rows': len(data),
        'columns': len(data.columns),
        'null_values': data.isnull().sum().sum(),
        'duplicates': data.duplicated().sum(),
        'memory_usage': f"{data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
        'numeric_columns': len(data.select_dtypes(include=['number']).columns),
        'categorical_columns': len(data.select_dtypes(include=['object', 'category']).columns)
    }
    
    return info

def preview_data(data, n_rows=5):
    """
    Genera una vista previa del dataset
    """
    preview = {
        'head': data.head(n_rows),
        'tail': data.tail(n_rows),
        'sample': data.sample(min(n_rows, len(data))) if len(data) > 0 else pd.DataFrame(),
        'dtypes': data.dtypes,
        'describe': data.describe(include='all')
    }
    
    return preview

def get_column_info(data):
    """
    Obtiene información detallada de cada columna
    """
    column_info = []
    
    for col in data.columns:
        col_data = data[col]
        
        info = {
            'column': col,
            'dtype': str(col_data.dtype),
            'null_count': col_data.isnull().sum(),
            'null_percentage': (col_data.isnull().sum() / len(data)) * 100,
            'unique_values': col_data.nunique(),
            'unique_percentage': (col_data.nunique() / len(data)) * 100
        }
        
        # Información específica según el tipo de dato
        if col_data.dtype in ['int64', 'float64']:
            info.update({
                'min': col_data.min(),
                'max': col_data.max(),
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std()
            })
        else:
            # Para variables categóricas
            top_value = col_data.mode().iloc[0] if len(col_data.mode()) > 0 else None
            info.update({
                'most_frequent': top_value,
                'most_frequent_count': col_data.value_counts().iloc[0] if len(col_data.value_counts()) > 0 else 0
            })
        
        column_info.append(info)
    
    return pd.DataFrame(column_info)
