def get_top_performing_pages(df_input, top_n=10):
    """Devuelve las URLs con mayor frecuencia de entrada"""
    return df_input['direccion_url_entrada'].value_counts().head(top_n)

def analyze_user_engagement(df_input):
    """Calcula promedios de interacción y duración"""
    stats = {
        'avg_session_duration': df_input['duracion_sesion_segundos'].mean(),
        'avg_clicks': df_input['clics_sesion'].mean(),
        'max_engagement': df_input['standarized_engagement_score'].max()
    }
    return pd.Series(stats)

def detect_frustration_hotspots(df_metrics_long, threshold=0.7):
    """Identifica URLs donde las métricas de frustración superan un umbral normalizado"""
    frustration_metrics = ['RageClickCount', 'DeadClickCount', 'ErrorClickCount']
    mask = (df_metrics_long['metricName'].isin(frustration_metrics)) & (df_metrics_long['normalized_value'] > threshold)
    return df_metrics_long[mask][['Url', 'metricName', 'normalized_value']].sort_values(by='normalized_value', ascending=False)

def get_device_distribution(df_input):
    """Retorna la distribución porcentual por dispositivo"""
    return df_input['dispositivo'].value_counts(normalize=True) * 100

# Ejecución de prueba rápida
print("--- Vista Rápida de Estadísticas ---")
print("Distribución de Dispositivos:")
display(get_device_distribution(df_normalized))
print("\nResumen de Engagement:")
display(analyze_user_engagement(df_normalized))
