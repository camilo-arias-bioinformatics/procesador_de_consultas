#cargar librerias basicas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

#carga de datos
from google.colab import file
uploaded = files.upload()

file_name = next(iter(uploaded))
df = pd.read_csv(file_name)

print("Archivo cargado:", file_name)
print("Columnas disponibles:")
print(df.columns.tolist())
df.head()

# Verificación de nulos y tipos
print("Valores nulos por columna:")
display(df.isnull().sum())

# Limpieza básica
# Convertir fechas y horas si es necesario
df['fecha'] = pd.to_datetime(df['fecha'])

# Llenar nulos en 'referente' con 'directo'
df['referente'] = df['referente'].fillna('directo')

# Eliminar filas con nulos críticos si existen (ej. id_usuario_clarity)
df = df.dropna(subset=['id_usuario_clarity'])

print("\nLimpieza inicial completada. Dimensiones actuales:", df.shape)

# Normalización de variables numéricas
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
numerical_cols = ['duracion_sesion_segundos', 'clics_sesion', 'clicks_por_pagina', 'interaccion_total', 'standarized_engagement_score']

# Asegurarnos de que las columnas existen antes de normalizar
existing_cols = [col for col in numerical_cols if col in df.columns]

df_normalized = df.copy()
df_normalized[existing_cols] = scaler.fit_transform(df[existing_cols])

print("Variables normalizadas:", existing_cols)
display(df_normalized[existing_cols].head())

# Verificación final de limpieza
print("Resumen de valores nulos finales:")
print(df.isnull().sum())

print("\nEstadísticas descriptivas de las columnas numéricas:")
display(df.describe())

print(f"\nTotal de registros limpios: {len(df)}")

# Guardar el DataFrame normalizado a CSV
output_filename = 'Data_Recordings_Cleaned_Normalized.csv'
df_normalized.to_csv(output_filename, index=False)

print(f"Archivo '{output_filename}' creado exitosamente.")

# Código para descargar el archivo en Colab
from google.colab import files
files.download(output_filename)

def run_marketing_analytics_engine(df):
    insights = {}

    # 1. Páginas y productos top
    # Usamos la URL de entrada y salida para identificar las páginas más visitadas
    insights['top_pages'] = df['direccion_url_entrada'].value_counts().head(10)

    # 2. Puntos críticos de abandono (Tasa de salida)
    # Calculamos cuántas veces una URL fue la 'direccion_url_salida'
    exit_counts = df['direccion_url_salida'].value_counts()
    total_presence = df['direccion_url_entrada'].value_counts() + exit_counts
    insights['exit_rate'] = (exit_counts / total_presence).dropna().sort_values(ascending=False).head(10)

    # 3. Flujo de navegación común
    # Identificamos pares comunes de Entrada -> Salida
    df['navigation_flow'] = df['direccion_url_entrada'] + ' >> ' + df['direccion_url_salida']
    insights['common_flows'] = df['navigation_flow'].value_counts().head(5)

    # 4. Interacción promedio por página
    insights['avg_interaction'] = df.groupby('direccion_url_entrada').agg({
        'clics_sesion': 'mean',
        'duracion_sesion_segundos': 'mean',
        'interaccion_total': 'mean'
    }).sort_values(by='interaccion_total', ascending=False).head(10)

    # 5. Patrones de conversión o intención
    # Identificamos páginas clave como 'request-demo', 'pricing', 'contact'
    keywords = ['demo', 'request', 'pricing', 'contact', 'product']
    intent_filter = df['direccion_url_entrada'].str.contains('|'.join(keywords), case=False, na=False)
    insights['intent_analysis'] = df[intent_filter]['direccion_url_entrada'].value_counts()

    return insights

# Ejecutar el motor
results = run_marketing_analytics_engine(df)

# Visualización de resultados clave
print("=== MOTOR DE ANÁLISIS DE MARKETING ===\n")
print("1. Top 5 Flujos de Navegación:")
display(results['common_flows'])

print("\n2. Páginas con Mayor Tasa de Abandono (Críticas):")
display(results['exit_rate'])

print("\n3. Análisis de Intención (Páginas Clave):")
display(results['intent_analysis'].head(5))

import seaborn as sns

# Visualizar la interacción promedio en las top páginas
plt.figure(figsize=(12, 6))
sns.barplot(x=results['avg_interaction']['interaccion_total'], y=results['avg_interaction'].index, palette='viridis')
plt.title('Top 10 Páginas por Nivel de Interacción Promedio')
plt.xlabel('Puntaje de Interacción Total')
plt.ylabel('URL de Página')
plt.show()

print("=== 1. FLUJO DE NAVEGACIÓN COMÚN (Secuencias frecuentes) ===")
display(results['common_flows'].to_frame(name='Frecuencia de la Ruta'))

print("\n=== 2. PATRONES DE CONVERSIÓN O INTENCIÓN (Páginas de Alto Interés) ===")
if not results['intent_analysis'].empty:
    display(results['intent_analysis'].to_frame(name='Visitas a páginas de conversión'))
else:
    print("No se detectaron visitas a páginas con las palabras clave: demo, request, pricing, contact.")

#carga de datos
from google.colab import files
uploaded = files.upload()

file_name = next(iter(uploaded))
df = pd.read_csv(file_name)

print("Archivo cargado:", file_name)
print("Columnas disponibles:")
print(df.columns.tolist())
df.head()

# 1. Identificar métricas únicas
unique_metrics = df['metricName'].unique()
print(f"Métricas encontradas: {unique_metrics}\n")

# 2. Crear un diccionario para almacenar los datos separados
metrics_dict = {metric: df[df['metricName'] == metric].copy() for metric in unique_metrics}

# 3. Mostrar un resumen de cada métrica separada
for metric, data in metrics_dict.items():
    print(f"Métrica: {metric} | Registros: {len(data)}")
    # Mostramos las primeras filas de la métrica 'Traffic' como ejemplo
    if metric == 'Traffic':
        print("Ejemplo de datos para Traffic:")
        display(data.head())
        print("-" * 30)

from sklearn.preprocessing import MinMaxScaler

# Diccionario para guardar los datos procesados
metrics_processed = {}
scaler = MinMaxScaler()

print("=== PROCESANDO SUBGRUPOS DE MÉTRICAS ===\n")

for metric, data in metrics_dict.items():
    # 1. Identificar columnas que NO son todas nulas para esta métrica
    cols_with_data = data.columns[data.notnull().any()].tolist()
    # Filtrar solo las columnas numéricas relevantes para normalizar (excluyendo IDs y nombres)
    numeric_cols = data[cols_with_data].select_dtypes(include=[np.number]).columns.tolist()

    # 2. Limpieza: Llenar nulos con 0 solo en las columnas con datos
    clean_data = data.copy()
    clean_data[numeric_cols] = clean_data[numeric_cols].fillna(0)

    # 3. Normalización: Solo si hay columnas numéricas y más de una fila
    if numeric_cols and len(clean_data) > 1:
        clean_data[numeric_cols] = scaler.fit_transform(clean_data[numeric_cols])

    metrics_processed[metric] = clean_data

    print(f"Métrica: {metric}")
    print(f"- Columnas procesadas: {numeric_cols}")
    print(f"- Registros: {len(clean_data)}\n")

print("Procesamiento completado para todos los subgrupos.")

# 1. Consolidar todos los subgrupos procesados en un solo DataFrame
df_consolidated = pd.concat(metrics_processed.values(), axis=0).sort_index()

# 2. Definir el nombre del archivo
output_csv = 'Metrics_Subgroups_Cleaned_Normalized.csv'

# 3. Guardar a CSV
df_consolidated.to_csv(output_csv, index=False)

print(f"Archivo '{output_csv}' creado con éxito con todos los subgrupos procesados.")

# 4. Descargar el archivo
from google.colab import files
files.download(output_csv)
