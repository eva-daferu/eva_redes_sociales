import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import numpy as np
import openai
from io import BytesIO
import base64

warnings.filterwarnings('ignore')

# Configuración de la API de OpenAI
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# NUEVOS ENDPOINTS PARA GRÁFICAS
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/followers"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/pauta_anuncio"
GRAFICA1_URL = "https://pahubisas.pythonanywhere.com/grafica1"
GRAFICA2_URL = "https://pahubisas.pythonanywhere.com/grafica2"

def cargar_datos_backend():
    try:
        r = requests.get(BACKEND_URL, timeout=20)
        r.raise_for_status()
        data = r.json()

        # Data principal
        df = pd.DataFrame(data.get("data", []))

        # Normalización básica
        if "fecha_publicacion" in df.columns:
            df["fecha_publicacion"] = pd.to_datetime(
                df["fecha_publicacion"],
                dayfirst=True,
                errors="coerce"
            )

        # Convertir números
        num_cols = ["vistas", "comentarios", "me_gusta_numero", "visualizaciones", 
                   "me_gusta", "comentarios_num", "Seguidores_Totales"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Asegurar columnas estándar
        if "visualizaciones" not in df.columns and "vistas" in df.columns:
            df["visualizaciones"] = df["vistas"]
        
        if "me_gusta" not in df.columns and "me_gusta_numero" in df.columns:
            df["me_gusta"] = df["me_gusta_numero"]
        
        if "comentarios" not in df.columns and "comentarios_num" in df.columns:
            df["comentarios"] = df["comentarios_num"]

        # Filtros calculados
        if "fecha_publicacion" in df.columns:
            hoy = pd.Timestamp.now()
            df["dias"] = (hoy - df["fecha_publicacion"]).dt.days.fillna(0).astype(int)
            df["dias_desde_publicacion"] = df["dias"].apply(lambda x: max(x, 1))
            df["rendimiento_por_dia"] = df["visualizaciones"] / df["dias_desde_publicacion"]
            df["semana"] = df["fecha_publicacion"].dt.isocalendar().week.fillna(0).astype(int)
            df["meses"] = df["fecha_publicacion"].dt.month.fillna(0).astype(int)

        # Red fija si no existe
        if "red" not in df.columns and "platform" in df.columns:
            df["red"] = df["platform"]
        elif "red" not in df.columns:
            df["red"] = "desconocido"

        # Tipo fijo si no existe
        if "tipo" not in df.columns:
            df["tipo"] = "general"

        return df

    except Exception as e:
        st.error(f"Error al conectar con el backend de datos: {str(e)}")
        return pd.DataFrame()

def cargar_datos_seguidores():
    """Carga datos de seguidores desde el endpoint específico"""
    try:
        r = requests.get(FOLLOWERS_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Convertir a DataFrame
        df_followers = pd.DataFrame(data.get("data", []))
        
        # Procesar datos
        if "Fecha" in df_followers.columns:
            df_followers["Fecha"] = pd.to_datetime(
                df_followers["Fecha"],
                dayfirst=True,
                errors="coerce"
            )
        
        # Convertir números
        if "Seguidores_Totales" in df_followers.columns:
            df_followers["Seguidores_Totales"] = pd.to_numeric(df_followers["Seguidores_Totales"], errors="coerce")
        
        return df_followers
        
    except Exception as e:
        st.error(f"Error al conectar con el backend de seguidores: {str(e)}")
        return pd.DataFrame()

def cargar_datos_pauta():
    """Carga datos de pauta publicitaria"""
    try:
        r = requests.get(PAUTA_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Convertir a DataFrame
        df_pauta = pd.DataFrame(data.get("data", []))
        
        # Procesar datos si existen
        if not df_pauta.empty:
            # Asegurar nombres de columnas
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores'] = df_pauta['Seguidores']
            
            # Formatear coste anuncio (sin decimales)
            if "coste_anuncio" in df_pauta.columns:
                df_pauta["coste_anuncio"] = pd.to_numeric(df_pauta["coste_anuncio"], errors="coerce").fillna(0).astype(int)
            
            # Formatear otras columnas
            for col in ["visualizaciones_videos", "nuevos_seguidores"]:
                if col in df_pauta.columns:
                    df_pauta[col] = pd.to_numeric(df_pauta[col], errors="coerce").fillna(0).astype(int)
            
            # Procesar fecha - FORMATO CORRECTO PARA CRUCE
            if "fecha" in df_pauta.columns:
                # Intentar múltiples formatos de fecha
                df_pauta["fecha"] = pd.to_datetime(
                    df_pauta["fecha"], 
                    errors='coerce',
                    dayfirst=True  # Asumir día primero
                )
        
        return df_pauta
        
    except Exception as e:
        return pd.DataFrame()

#############################################
# NUEVAS FUNCIONES PARA MOSTRAR GRÁFICA
#############################################

def mostrar_grafica_inversion_vs_seguidores():
    """Muestra la gráfica de inversión vs seguidores desde el backend"""
    try:
        # Descargar la imagen desde el backend
        response = requests.get(GRAFICA1_URL, timeout=20)
        
        if response.status_code == 200:
            # Mostrar la imagen
            st.image(BytesIO(response.content), caption="Inversión vs Seguidores", use_container_width=True)
            
            # Mostrar información adicional
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Gráfica Generada", "Inversión vs Seguidores")
            with col2:
                st.metric("📅 Tipo de Análisis", "Regresión y Punto Óptimo")
            with col3:
                st.metric("🎯 Objetivo", "Optimizar Costo por Seguidor")
        else:
            st.error(f"Error al cargar la gráfica: {response.status_code}")
            
    except Exception as e:
        st.error(f"Error al cargar la gráfica: {str(e)}")

def cargar_metricas_excel():
    """Carga las métricas desde el Excel del backend"""
    try:
        # Descargar el archivo Excel
        response = requests.get(GRAFICA2_URL, timeout=20)
        
        if response.status_code == 200:
            # Leer el Excel en un DataFrame
            excel_data = pd.read_excel(BytesIO(response.content))
            
            # Mostrar resumen
            st.markdown("### 📊 Métricas Detalladas del Excel")
            
            # Mostrar estadísticas básicas
            col1, col2, col3, col4 = st.columns(4)
            
            if 'Costo' in excel_data.columns:
                with col1:
                    st.metric("💰 Costo Total", f"${excel_data['Costo'].sum():,.0f}")
            
            if 'Seguidores' in excel_data.columns:
                with col2:
                    st.metric("👥 Seguidores Totales", f"{excel_data['Seguidores'].sum():,.0f}")
            
            if 'CPS' in excel_data.columns:
                with col3:
                    st.metric("📈 CPS Promedio", f"${excel_data['CPS'].mean():,.2f}")
            
            if 'Visualizaciones' in excel_data.columns:
                with col4:
                    st.metric("👁️ Visualizaciones", f"{excel_data['Visualizaciones'].sum():,.0f}")
            
            # Mostrar tabla con los datos
            with st.expander("📋 Ver datos completos"):
                st.dataframe(excel_data, use_container_width=True)
            
            return excel_data
        else:
            st.error(f"Error al cargar las métricas: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error al cargar las métricas: {str(e)}")
        return None

def analizar_con_ia(metricas, pregunta):
    """Analiza las métricas usando OpenAI"""
    try:
        # Preparar el contexto con las métricas
        contexto = f"""
        DATOS DE MÉTRICAS DE SEGUIDORES VS INVERSIÓN:
        
        Estadísticas Resumidas:
        - Costo Total: ${metricas['Costo'].sum():,.0f}
        - Seguidores Totales: {metricas['Seguidores'].sum():,.0f}
        - Visualizaciones Totales: {metricas['Visualizaciones'].sum():,.0f}
        - CPS Promedio (Costo por Seguidor): ${metricas['CPS'].mean():,.2f}
        - CPS Mínimo: ${metricas['CPS'].min():,.2f}
        - CPS Máximo: ${metricas['CPS'].max():,.2f}
        
        Distribución por Día (primeras 5 filas):
        {metricas.head().to_string()}
        
        Pregunta del usuario: {pregunta}
        
        Por favor, proporciona un análisis detallado basado en estos datos, incluyendo:
        1. Eficiencia de la inversión en publicidad
        2. Recomendaciones para optimizar el costo por seguidor
        3. Análisis de tendencias y patrones
        4. Sugerencias específicas para mejorar resultados
        """
        
        # Llamar a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto analista de marketing digital y optimización de campañas publicitarias."},
                {"role": "user", "content": contexto}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error al conectar con OpenAI: {str(e)}"

# Función para cargar datos con caché
@st.cache_data(ttl=300)  # 5 minutos de caché
def cargar_datos():
    """Carga datos desde el backend y separa por plataforma"""
    df = cargar_datos_backend()
    df_followers = cargar_datos_seguidores()
    df_pauta = cargar_datos_pauta()
    
    if df.empty:
        # Datos de respaldo si falla el backend
        st.warning("Usando datos de respaldo. El backend no está disponible.")
        
        # Datos de ejemplo
        youtobe_data = pd.DataFrame({
            'titulo': ['Amazonía al borde', 'El costo oculto de botar comida'],
            'fecha_publicacion': ['01/10/2025', '23/09/2025'],
            'visualizaciones': [18, 22],
            'me_gusta': [0, 0],
            'comentarios': [0, 0],
            'Seguidores_Totales': [0, 0],
            'red': ['youtobe', 'youtobe']
        })
        
        tiktok_data = pd.DataFrame({
            'titulo': ['Especie única en Colombia', 'Una peli que te volará la mente'],
            'fecha_publicacion': ['03/12/2025', '28/11/2025'],
            'visualizaciones': [127, 5669],
            'me_gusta': [19, 211],
            'comentarios': [2, 5],
            'Seguidores_Totales': [450, 450],
            'red': ['tiktok', 'tiktok']
        })
        
        youtobe_data['fecha_publicacion'] = pd.to_datetime(youtobe_data['fecha_publicacion'], dayfirst=True)
        tiktok_data['fecha_publicacion'] = pd.to_datetime(tiktok_data['fecha_publicacion'], dayfirst=True)
        
        # Datos de seguidores de ejemplo
        df_followers = pd.DataFrame({
            'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Seguidores_Totales': range(400, 430)
        })
        
        # Datos de pauta de ejemplo
        df_pauta = pd.DataFrame({
            'coste_anuncio': [641140],
            'visualizaciones_videos': [180500],
            'nuevos_seguidores': [4170],
            'fecha': ['2025-10-19']
        })
        
    else:
        # Primero, asegurarnos de que la columna 'red' existe y está limpia
        if 'red' in df.columns:
            df['red'] = df['red'].astype(str).str.lower().str.strip()
        
        # Filtrar usando comparación exacta
        youtobe_data = df[df['red'] == 'youtobe'].copy()
        
        # Si no encuentra 'youtobe', buscar 'youtube' como alternativa
        if youtobe_data.empty:
            youtobe_data = df[df['red'] == 'youtube'].copy()
        
        # Para TikTok
        tiktok_data = df[df['red'] == 'tiktok'].copy()
    
    # Calcular métricas comunes para ambos datasets
    for df_data in [youtobe_data, tiktok_data]:
        if not df_data.empty and 'fecha_publicacion' in df_data.columns:
            hoy = pd.Timestamp.now()
            df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
            df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
            df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
    
    return df, youtobe_data, tiktok_data, df_followers, df_pauta

# Estilos CSS mejorados con reducción de espacio
st.markdown("""
<style>
/* Main container - REDUCIDO ESPACIO SUPERIOR */
.main { 
    padding: 0;
    padding-top: 0.5rem !important;
}

/* Sidebar styling - AZUL PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Social media buttons - MEJORADO */
.stButton > button {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    margin: 6px 0;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    text-align: left;
    justify-content: flex-start;
}

.stButton > button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
}

.stButton > button[kind="primary"] {
    background: rgba(59, 130, 246, 0.2);
    border-color: #3B82F6;
    color: #3B82F6;
}

/* Metrics cards - MEJORADAS */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 22px 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
}

.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #1f2937;
    margin: 12px 0 5px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.metric-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-trend {
    font-size: 12px;
    display: flex;
    align-items: center;
    margin-top: 8px;
    font-weight: 500;
}

.trend-up { color: #10b981; }
.trend-down { color: #ef4444; }

/* Tarjetas de pauta publicitaria */
.pauta-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 14px;
    padding: 20px 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.pauta-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #10b981 0%, #3B82F6 100%);
}

.pauta-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.pauta-value {
    font-size: 26px;
    font-weight: 800;
    color: #1f2937;
    margin: 10px 0 3px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.pauta-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.pauta-period {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 5px;
    font-weight: 500;
}

/* Header principal - REDUCIDO */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 18px;
    padding: 25px 30px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 12px 28px rgba(59, 130, 246, 0.25);
    position: relative;
    overflow: hidden;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    line-height: 1.2;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 30px 30px;
    opacity: 0.1;
}

/* Tabs mejorados */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    padding: 6px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 18px;
    background: transparent;
    color: #64748b;
    font-weight: 500;
    transition: all 0.3s;
}

.stTabs [aria-selected="true"] {
    background: white;
    color: #3B82F6;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    font-weight: 600;
}

/* Chart containers */
.performance-chart {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

.data-table-container {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

/* Platform-specific colors */
.youtube-color { color: #FF0000; }
.tiktok-color { color: #000000; }
.facebook-color { color: #1877F2; }
.twitter-color { color: #1DA1F2; }
.instagram-color { color: #E4405F; }
.linkedin-color { color: #0A66C2; }

/* Status indicators */
.status-connected {
    color: #10b981;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-disconnected {
    color: #ef4444;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-warning {
    color: #f59e0b;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Sidebar titles */
.sidebar-title {
    color: #cbd5e1 !important;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
    margin-top: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Status containers */
.status-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s;
}

.status-container:hover {
    background: rgba(255, 255, 255, 0.08);
}

/* Custom table */
.dataframe {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.dataframe th {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    padding: 12px 14px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
}

.dataframe td {
    padding: 10px 14px;
    border-bottom: 1px solid #e5e7eb;
    color: #4b5563;
}

.dataframe tr:hover {
    background: #f9fafb;
}

.dataframe tr:last-child td {
    border-bottom: none;
}

/* Badges */
.platform-badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 18px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
}

/* Loader */
.loader {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3B82F6;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    animation: spin 1s linear infinite;
    margin: 15px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Backend status */
.backend-status {
    padding: 8px 12px;
    border-radius: 8px;
    margin: 12px 0;
    font-size: 12px;
    font-weight: 500;
}

.backend-connected {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.backend-disconnected {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .metric-value { font-size: 26px; }
    .pauta-value { font-size: 22px; }
    .dashboard-header { padding: 20px; }
    .dashboard-header h1 { font-size: 26px; }
}

/* Data table improvements */
.full-table {
    width: 100%;
    max-height: 550px;
    overflow-y: auto;
}

.full-table th {
    position: sticky;
    top: 0;
    z-index: 10;
}

/* Filter buttons */
.filter-btn {
    margin: 2px;
    border-radius: 8px;
}

.filter-btn.active {
    background-color: #3B82F6;
    color: white;
    border-color: #3B82F6;
}

/* Platform header styles */
.platform-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 18px;
    background: rgba(var(--platform-color-rgb), 0.05);
    border-radius: 16px;
    border-left: 5px solid var(--platform-color);
}

.platform-icon {
    font-size: 28px;
    margin-right: 18px;
    color: var(--platform-color);
}

.platform-title {
    flex: 1;
}

.platform-title h2 {
    margin: 0;
    color: var(--platform-color);
    font-size: 24px;
}

.platform-title p {
    margin: 6px 0 0 0;
    color: #6b7280;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.platform-badge-container {
    margin-left: auto;
    display: flex;
    gap: 12px;
    align-items: center;
}

.platform-badge-style {
    background: rgba(var(--platform-color-rgb), 0.1);
    color: var(--platform-color);
    padding: 8px 20px;
    border-radius: 22px;
    font-size: 14px;
    font-weight: 700;
    border: 2px solid rgba(var(--platform-color-rgb), 0.2);
}

/* Gráficas avanzadas */
.grafica-container {
    background: linear-gradient(135deg, #0b1020 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.grafica-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Arial Black', sans-serif;
}

.grafica-subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 25px;
    font-family: 'Arial', sans-serif;
}

/* Tabs para gráficas */
.grafica-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 25px;
    flex-wrap: wrap;
}

.grafica-tab {
    padding: 12px 24px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    color: #cbd5e1;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-family: 'Arial', sans-serif;
}

.grafica-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.grafica-tab.active {
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    color: white;
    border-color: transparent;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

/* Botones de acción */
.action-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 8px;
    background: linear-gradient(135deg, #10b981 0%, #3B82F6 100%);
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    text-decoration: none;
    font-family: 'Arial', sans-serif;
}

.action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* Tooltips */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted #666;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #1e293b;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
    border: 1px solid #334155;
    font-family: 'Arial', sans-serif;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Etiquetas de gráficas */
.chart-label {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    color: white !important;
}

.heatmap-cell {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    font-size: 10px !important;
}

/* Leyenda mejorada */
.legend-item {
    font-family: 'Arial', sans-serif !important;
    font-weight: 600 !important;
}

/* Ejes mejorados */
.axis-label {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    color: #c7d2fe !important;
}

/* Texto en gráficas */
.chart-text {
    font-family: 'Arial', sans-serif !important;
    font-weight: 500 !important;
}

/* Chat AI Container */
.chat-container {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid #334155;
}

.chat-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 12px;
    max-width: 80%;
}

.chat-message.user {
    background: linear-gradient(135deg, #3B82F6 0%, #1e40af 100%);
    color: white;
    margin-left: auto;
}

.chat-message.assistant {
    background: rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-input-container {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Inicializar estado de chat
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 55px; height: 55px; border-radius: 14px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 12px auto; font-size: 26px;">
            📊
        </div>
        <h2 style="color: white; margin-bottom: 4px; font-size: 20px; font-family: 'Arial Black', sans-serif;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 12px; margin: 0; font-family: 'Arial', sans-serif;">Social Media Analytics v3.3</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div class="backend-status backend-connected">✅ Backend Conectado</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Error: {backend_test.status_code}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Offline</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
    # Botones de plataformas con botón GENERAL
    platforms = {
        "general": ("🌐 GENERAL", "#3B82F6"),
        "facebook": ("📘 Facebook", "#1877F2"),
        "twitter": ("🐦 Twitter", "#1DA1F2"),
        "instagram": ("📷 Instagram", "#E4405F"),
        "linkedin": ("💼 LinkedIn", "#0A66C2"),
        "youtube": ("▶️ YouTube", "#FF0000"),
        "tiktok": ("🎵 TikTok", "#000000")
    }
    
    selected_platform = st.session_state.get("selected_platform", "general")
    
    for platform_key, (platform_name, platform_color) in platforms.items():
        if st.button(platform_name, key=f"{platform_key}_btn", use_container_width=True):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
            st.rerun()
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Nueva sección para gráficas avanzadas
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📊 GRÁFICAS AVANZADAS</p>', unsafe_allow_html=True)
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        if st.button("📈 Gráfica 1", key="grafica1_btn", use_container_width=True, 
                    help="Inversión vs Seguidores - Análisis de eficiencia"):
            st.session_state["show_grafica1"] = not st.session_state.get("show_grafica1", False)
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
            if "show_ai_chat" in st.session_state:
                st.session_state["show_ai_chat"] = False
    
    with col_graf2:
        if st.button("🤖 AI Analytics", key="ai_chat_btn", use_container_width=True,
                    help="Chat con IA para análisis de métricas"):
            st.session_state["show_ai_chat"] = not st.session_state.get("show_ai_chat", False)
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
    
    # Botón para ocultar gráficas
    if st.session_state.get("show_grafica1", False) or st.session_state.get("show_ai_chat", False):
        if st.button("⬅️ Volver a Dashboard", key="back_dashboard", use_container_width=True):
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
            if "show_ai_chat" in st.session_state:
                st.session_state["show_ai_chat"] = False
            st.rerun()
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Filtros de tiempo cuando no está en modo GENERAL
    if selected_platform != "general":
        st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📅 Filtros de Tiempo</p>', unsafe_allow_html=True)
        
        tiempo_filtro = st.selectbox(
            "Seleccionar período:",
            ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Todo el período"],
            key="tiempo_filtro"
        )
    
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📈 Status Conexiones</p>', unsafe_allow_html=True)
    
    # Estado de conexiones basado en datos reales
    connection_status = []
    
    # YouTube/Youtobe
    youtube_connected = not youtobe_df.empty
    connection_status.append(("YouTube", "connected" if youtube_connected else "disconnected"))
    
    # TikTok
    tiktok_connected = not tiktok_df.empty
    connection_status.append(("TikTok", "connected" if tiktok_connected else "disconnected"))
    
    # Otras plataformas
    connection_status.extend([
        ("Facebook", "disconnected"),
        ("Twitter", "disconnected"),
        ("Instagram", "disconnected"),
        ("LinkedIn", "disconnected")
    ])
    
    for platform, status in connection_status:
        icon = "🔴" if status == "disconnected" else "🟡" if status == "warning" else "🟢"
        status_class = "status-disconnected" if status == "disconnected" else "status-warning" if status == "warning" else "status-connected"
        
        st.markdown(f"""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0; font-family: 'Arial', sans-serif;">{platform}</span>
                <span class="{status_class}" style="font-family: 'Arial', sans-serif;">{icon} {status.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div class="dashboard-header">
    <h1 style="font-family: 'Arial Black', sans-serif;">📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px; font-weight: 400; font-family: 'Arial', sans-serif;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
    <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8; font-family: 'Arial', sans-serif;">
        Actualizado: {current_time}
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# SECCIÓN: GRÁFICA 1 - INVERSIÓN VS SEGUIDORES
# ================================================================
if st.session_state.get("show_grafica1", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📈 GRÁFICA: INVERSIÓN VS SEGUIDORES</div>
        <div class="grafica-subtitle">
            Análisis de eficiencia por nivel de inversión • CPS (Costo por Seguidor) • Punto óptimo
        </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Cargando gráfica desde el backend..."):
        mostrar_grafica_inversion_vs_seguidores()
    
    # Información sobre la gráfica
    st.markdown("---")
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #3B82F6;">
            <h4 style="margin: 0 0 10px 0; color: #3B82F6;">📊 Interpretación</h4>
            <p style="margin: 0; color: #6b7280; font-size: 13px;">
                Esta gráfica muestra la relación entre la inversión publicitaria y los seguidores obtenidos.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #10b981;">
            <h4 style="margin: 0 0 10px 0; color: #10b981;">🎯 Punto Óptimo</h4>
            <p style="margin: 0; color: #6b7280; font-size: 13px;">
                El punto óptimo indica la inversión con mejor costo por seguidor (CPS).
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info3:
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #8b5cf6;">
            <h4 style="margin: 0 0 10px 0; color: #8b5cf6;">💰 Recomendaciones</h4>
            <p style="margin: 0; color: #6b7280; font-size: 13px;">
                Basado en la curva, se recomienda invertir cerca del punto óptimo para maximizar ROI.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================================================================
# SECCIÓN: CHAT CON IA PARA ANÁLISIS DE MÉTRICAS
# ================================================================
elif st.session_state.get("show_ai_chat", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">🤖 ASISTENTE DE IA - ANÁLISIS DE MÉTRICAS</div>
        <div class="grafica-subtitle">
            Analiza las métricas de seguidores vs inversión • Recomendaciones personalizadas • Insights inteligentes
        </div>
    """, unsafe_allow_html=True)
    
    # Cargar métricas del Excel
    with st.spinner("Cargando métricas del backend..."):
        metricas_excel = cargar_metricas_excel()
    
    if metricas_excel is not None:
        # Mostrar historial de chat
        st.markdown("### 💬 Historial de Conversación")
        
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <strong>👤 Tú:</strong><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <strong>🤖 Asistente IA:</strong><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input para nuevas preguntas
        st.markdown("### 💭 Haz una pregunta sobre las métricas")
        
        col_input1, col_input2 = st.columns([4, 1])
        
        with col_input1:
            user_question = st.text_area(
                "Escribe tu pregunta:",
                placeholder="Ej: ¿Cuál es el costo por seguidor óptimo? ¿Cómo puedo mejorar mi ROI?",
                height=100,
                key="user_question"
            )
        
        with col_input2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            analyze_button = st.button("📊 Analizar", use_container_width=True)
        
        if analyze_button and user_question:
            # Agregar pregunta al historial
            st.session_state.chat_messages.append({"role": "user", "content": user_question})
            
            # Mostrar indicador de procesamiento
            with st.spinner("🤖 Analizando con IA..."):
                # Obtener respuesta de la IA
                respuesta_ia = analizar_con_ia(metricas_excel, user_question)
                
                # Agregar respuesta al historial
                st.session_state.chat_messages.append({"role": "assistant", "content": respuesta_ia})
                
                # Actualizar la pantalla
                st.rerun()
        
        # Preguntas sugeridas
        st.markdown("### 💡 Preguntas sugeridas")
        
        col_q1, col_q2, col_q3 = st.columns(3)
        
        with col_q1:
            if st.button("📈 ¿Cuál es el CPS óptimo?", use_container_width=True):
                st.session_state.user_question = "¿Cuál es el costo por seguidor (CPS) óptimo según los datos?"
                st.rerun()
        
        with col_q2:
            if st.button("💰 ¿Cómo mejorar ROI?", use_container_width=True):
                st.session_state.user_question = "¿Cómo puedo mejorar el retorno de inversión (ROI) de mis campañas?"
                st.rerun()
        
        with col_q3:
            if st.button("🎯 ¿Recomendaciones?", use_container_width=True):
                st.session_state.user_question = "¿Qué recomendaciones específicas tienes para optimizar mi inversión en publicidad?"
                st.rerun()
        
        # Botón para limpiar historial
        if st.button("🗑️ Limpiar Historial", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================================================================
# DASHBOARD NORMAL (si no se están mostrando gráficas avanzadas)
# ================================================================

# Determinar datos según plataforma seleccionada
if selected_platform == "general":
    platform_name = "GENERAL"
    platform_color = "#3B82F6"
    platform_icon = "🌐"
    df = df_all
elif selected_platform == "youtube":
    platform_name = "YouTube"
    platform_color = "#FF0000"
    platform_icon = "▶️"
    df = youtobe_df
elif selected_platform == "tiktok":
    platform_name = "TikTok"
    platform_color = "#000000"
    platform_icon = "🎵"
    df = tiktok_df
else:
    # Para otras plataformas (Facebook, Twitter, etc.) usar datos de YouTube temporalmente
    platform_config = {
        "facebook": ("Facebook", "#1877F2", "📘", youtobe_df),
        "twitter": ("Twitter", "#1DA1F2", "🐦", youtobe_df),
        "instagram": ("Instagram", "#E4405F", "📷", youtobe_df),
        "linkedin": ("LinkedIn", "#0A66C2", "💼", youtobe_df)
    }
    platform_name, platform_color, platform_icon, df = platform_config.get(
        selected_platform, 
        ("YouTube", "#FF0000", "▶️", youtobe_df)
    )

# Aplicar filtro de tiempo si no está en modo GENERAL
if selected_platform != "general" and 'fecha_publicacion' in df.columns:
    hoy = pd.Timestamp.now()
    
    if 'tiempo_filtro' in st.session_state:
        if st.session_state.tiempo_filtro == "Últimos 7 días":
            fecha_limite = hoy - timedelta(days=7)
            df = df[df['fecha_publicacion'] >= fecha_limite]
        elif st.session_state.tiempo_filtro == "Últimos 30 días":
            fecha_limite = hoy - timedelta(days=30)
            df = df[df['fecha_publicacion'] >= fecha_limite]
        elif st.session_state.tiempo_filtro == "Últimos 90 días":
            fecha_limite = hoy - timedelta(days=90)
            df = df[df['fecha_publicacion'] >= fecha_limite]
        # "Todo el período" no aplica filtro

# Verificar si hay datos
if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    
    if selected_platform != "general":
        with st.expander("🔍 Información de Depuración", expanded=False):
            st.write(f"**Plataforma seleccionada:** {selected_platform}")
            st.write(f"**Total registros en dataset:** {len(df_all)}")
            st.write(f"**Total registros YouTube/Youtobe:** {len(youtobe_df)}")
            st.write(f"**Total registros TikTok:** {len(tiktok_df)}")
    
    st.info("Conectando al backend para cargar datos en tiempo real...")
    st.stop()

# Información de la plataforma
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    st.markdown(f'<div style="font-size: 38px; text-align: center; color: {platform_color};">{platform_icon}</div>', unsafe_allow_html=True)

with col_header2:
    st.markdown(f'<h2 style="margin: 0; color: {platform_color}; font-size: 26px; text-align: center; font-family: Arial Black, sans-serif;">{platform_name} ANALYTICS</h2>', unsafe_allow_html=True)
    total_posts = len(df)
    st.markdown(f'<p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; text-align: center; font-family: Arial, sans-serif;">{total_posts} contenidos analizados • Última actualización: {datetime.now().strftime("%H:%M")}</p>', unsafe_allow_html=True)
    if selected_platform != "general":
        st.markdown(f'<p style="margin: 2px 0 0 0; color: #9ca3af; font-size: 11px; text-align: center; font-family: Arial, sans-serif;">Filtro: {st.session_state.get("tiempo_filtro", "Todo el período")}</p>', unsafe_allow_html=True)

with col_header3:
    st.markdown(f'''
    <div style="background: {platform_color}15; color: {platform_color}; padding: 8px 18px; 
                border-radius: 18px; font-size: 13px; font-weight: 600; text-align: center; 
                border: 1px solid {platform_color}30; font-family: Arial Black, sans-serif;">
        {total_posts} {platform_name} Posts
    </div>
    ''', unsafe_allow_html=True)

# Calcular métricas clave
total_views = df['visualizaciones'].sum() if 'visualizaciones' in df.columns else 0
total_likes = df['me_gusta'].sum() if 'me_gusta' in df.columns else 0
total_comments = df['comentarios'].sum() if 'comentarios' in df.columns else 0

# Calcular total de seguidores (solo para GENERAL y TikTok)
total_followers = 0
if (selected_platform == "general" or selected_platform == "tiktok") and not df_followers.empty:
    if 'Seguidores_Totales' in df_followers.columns:
        total_followers = int(df_followers['Seguidores_Totales'].iloc[-1] if len(df_followers) > 0 else 0)

if 'rendimiento_por_dia' in df.columns:
    avg_daily_perf = df['rendimiento_por_dia'].mean()
else:
    avg_daily_perf = 0

if total_views > 0:
    engagement_rate = ((total_likes + total_comments) / total_views * 100)
else:
    engagement_rate = 0

# ============================================================================
# SECCIÓN: MÉTRICAS DE PAUTA PUBLICITARIA (solo para GENERAL y TikTok)
# ============================================================================
if (selected_platform == "general" or selected_platform == "tiktok") and not df_pauta.empty:
    # Calcular sumas por columnas
    coste_anuncio_sum = 0
    visualizaciones_videos_sum = 0
    nuevos_seguidores_sum = 0
    
    if 'coste_anuncio' in df_pauta.columns:
        coste_anuncio_sum = df_pauta['coste_anuncio'].sum()
    
    if 'visualizaciones_videos' in df_pauta.columns:
        visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum()
    
    if 'nuevos_seguidores' in df_pauta.columns:
        nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum()
    
    # Función para formatear números con separador de miles
    def format_number(num):
        """Formatea números con separador de miles"""
        try:
            return f"{int(num):,}".replace(",", ".")
        except:
            return "0"
    
    # Formatear valores
    coste_anuncio = format_number(coste_anuncio_sum)
    visualizaciones_videos = format_number(visualizaciones_videos_sum)
    nuevos_seguidores = format_number(nuevos_seguidores_sum)
    
    # Obtener rango de fechas si existe
    rango_fechas = 'N/D'
    if 'fecha' in df_pauta.columns and not df_pauta.empty:
        fechas = df_pauta['fecha'].dropna()
        if not fechas.empty:
            min_fecha = fechas.min().strftime('%d/%m/%Y')
            max_fecha = fechas.max().strftime('%d/%m/%Y')
            rango_fechas = f"{min_fecha} - {max_fecha}"
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                border-radius: 16px; padding: 20px; margin-bottom: 20px; 
                border-left: 5px solid #0ea5e9;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #0369a1; font-size: 20px; display: flex; align-items: center; gap: 8px; font-family: Arial Black, sans-serif;">
                📢 MÉTRICAS DE PAUTA PUBLICITARIA (SUMAS)
            </h3>
            <div style="color: #64748b; font-size: 12px; background: white; padding: 5px 12px; border-radius: 15px; border: 1px solid #cbd5e1; font-family: Arial, sans-serif;">
                Período: {rango_fechas}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar 3 tarjetas de métricas de pauta (eliminada VISUALIZACIONES PERFIL)
    col_pauta1, col_pauta2, col_pauta3 = st.columns(3)
    
    with col_pauta1:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label" style="font-family: Arial, sans-serif;">COSTE ANUNCIO</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">${coste_anuncio}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma total en pesos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta2:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES VIDEOS</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">{visualizaciones_videos}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma de reproducciones</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta3:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label" style="font-family: Arial, sans-serif;">NUEVOS SEGUIDORES</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">{nuevos_seguidores}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma de audiencia ganada</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FIN SECCIÓN PAUTA PUBLICITARIA
# ============================================================================

# Métricas principales
if selected_platform == "general" or selected_platform == "tiktok":
    # Mostrar 5 métricas cuando es GENERAL o TikTok
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL SEGUIDORES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_followers:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👥 TikTok Followers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL CONTENIDOS</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_posts}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES TOTALES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_views:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">RENDIMIENTO DIARIO</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TASA DE ENGAGEMENT</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>💬 Interacción</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Mostrar 4 métricas para otras plataformas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL CONTENIDOS</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_posts}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES TOTALES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_views:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">RENDIMIENTO DIARIO</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TASA DE ENGAGEMENT</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>💬 Interacción</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# SECCIÓN: GRÁFICA DE SEGUIDORES Y PAUTA (solo para GENERAL y TikTok)
if (selected_platform == "general" or selected_platform == "tiktok") and not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
                📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA
            </h3>
            <div style="color: #6b7280; font-size: 12px; font-family: Arial, sans-serif;">
                Total Seguidores: {:,}
            </div>
        </div>
    """.format(total_followers), unsafe_allow_html=True)
    
    try:
        # Preparar datos de pauta si existen
        if not df_pauta.empty:
            # Asegurar que tenemos las columnas necesarias de pauta
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores_pauta'] = df_pauta['Seguidores']
            
            # Convertir fecha en pauta al mismo formato que en followers
            df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
            
            # Agrupar por fecha para sumar valores duplicados
            df_pauta_agg = df_pauta.groupby('fecha').agg({
                'coste_anuncio': 'sum',
                'visualizaciones_videos': 'sum',
                'nuevos_seguidores_pauta': 'sum'
            }).reset_index()
            
            # Fusionar por fecha - CORRECCIÓN: USAR OUTER JOIN PARA VER TODAS LAS FECHAS
            df_merged = pd.merge(df_followers, df_pauta_agg, left_on='Fecha', right_on='fecha', how='outer')
            
            # Ordenar por fecha
            df_merged = df_merged.sort_values('Fecha')
            
            # Rellenar valores faltantes
            if 'Seguidores_Totales' in df_merged.columns:
                df_merged['Seguidores_Totales'] = df_merged['Seguidores_Totales'].fillna(method='ffill').fillna(0)
            
            if 'coste_anuncio' in df_merged.columns:
                df_merged['coste_anuncio'] = df_merged['coste_anuncio'].fillna(0)
            
            if 'visualizaciones_videos' in df_merged.columns:
                df_merged['visualizaciones_videos'] = df_merged['visualizaciones_videos'].fillna(0)
            
            if 'nuevos_seguidores_pauta' in df_merged.columns:
                df_merged['nuevos_seguidores_pauta'] = df_merged['nuevos_seguidores_pauta'].fillna(0)
        else:
            df_merged = df_followers.copy()
            df_merged['coste_anuncio'] = 0
            df_merged['visualizaciones_videos'] = 0
            df_merged['nuevos_seguidores_pauta'] = 0
        
        # Crear gráfica de 4 líneas
        fig_followers = go.Figure()
        
        # 1. Seguidores Totales (línea principal)
        fig_followers.add_trace(go.Scatter(
            x=df_merged['Fecha'],
            y=df_merged['Seguidores_Totales'],
            mode='lines+markers',
            name='👥 Seguidores Totales',
            marker=dict(
                size=8,
                color='#000000',
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            line=dict(color='#000000', width=3),
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores Totales: %{y:,}<extra></extra>'
        ))
        
        # 2. Seguidores Pauta (si existe)
        if 'nuevos_seguidores_pauta' in df_merged.columns:
            fig_followers.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['nuevos_seguidores_pauta'],
                mode='lines+markers',
                name='👥 Seguidores Pauta',
                marker=dict(
                    size=6,
                    color='#10b981',
                    symbol='diamond'
                ),
                line=dict(color='#10b981', width=2, dash='dot'),
                hovertemplate='Seguidores Pauta: %{y:,}<extra></extra>',
                yaxis='y1'
            ))
        
        # 3. Costo de Pauta (barras, eje secundario)
        if 'coste_anuncio' in df_merged.columns:
            fig_followers.add_trace(go.Bar(
                x=df_merged['Fecha'],
                y=df_merged['coste_anuncio'],
                name='💰 Costo Pauta',
                marker=dict(
                    color='#ef4444',
                    opacity=0.7
                ),
                hovertemplate='Costo Pauta: $%{y:,}<extra></extra>',
                yaxis='y2'
            ))
        
        # 4. Visualizaciones de Pauta (eje secundario)
        if 'visualizaciones_videos' in df_merged.columns:
            fig_followers.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['visualizaciones_videos'],
                mode='lines+markers',
                name='👁️ Visualizaciones Pauta',
                marker=dict(
                    size=6,
                    color='#3B82F6',
                    symbol='triangle-up'
                ),
                line=dict(color='#3B82F6', width=2, dash='dash'),
                hovertemplate='Visualizaciones Pauta: %{y:,}<extra></extra>',
                yaxis='y2'
            ))
        
        # Configurar layout con eje secundario
        fig_followers.update_layout(
            height=450,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Fecha",
                gridcolor='#f1f5f9',
                showgrid=True,
                tickformat='%d/%m/%Y'
            ),
            yaxis=dict(
                title="Seguidores",
                gridcolor='#f1f5f9',
                showgrid=True,
                title_font=dict(color='#000000')
            ),
            yaxis2=dict(
                title="Costo ($) / Visualizaciones",
                overlaying='y',
                side='right',
                gridcolor='rgba(241, 245, 249, 0.5)',
                showgrid=False,
                title_font=dict(color='#ef4444')
            )
        )
        
        st.plotly_chart(fig_followers, use_container_width=True)
        
        # Estadísticas de seguidores y pauta
        if len(df_merged) > 0:
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            with col_f1:
                latest_followers = df_merged['Seguidores_Totales'].iloc[-1] if len(df_merged) > 0 else 0
                st.metric("👥 Últimos seguidores", f"{latest_followers:,}")
            
            with col_f2:
                if 'nuevos_seguidores_pauta' in df_merged.columns:
                    total_nuevos_seguidores = df_merged['nuevos_seguidores_pauta'].sum()
                    st.metric("👥 Seguidores Pauta", f"{total_nuevos_seguidores:,}")
                else:
                    st.metric("👥 Seguidores Pauta", "N/D")
            
            with col_f3:
                if 'coste_anuncio' in df_merged.columns:
                    total_costo = df_merged['coste_anuncio'].sum()
                    st.metric("💰 Costo total pauta", f"${total_costo:,}")
                else:
                    st.metric("💰 Costo pauta", "N/D")
            
            with col_f4:
                if 'visualizaciones_videos' in df_merged.columns:
                    total_visualizaciones = df_merged['visualizaciones_videos'].sum()
                    st.metric("👁️ Visualizaciones pauta", f"{total_visualizaciones:,}")
                else:
                    st.metric("👁️ Visualizaciones", "N/D")
    
    except Exception as e:
        st.warning(f"Error al generar gráfica combinada: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 1: PERFORMANCE OVER TIME - GRÁFICA MULTI-LÍNEA MEJORADA
st.markdown("""
<div class="performance-chart">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
            📈 PERFORMANCE OVER TIME - EVOLUCIÓN DETALLADA
        </h3>
        <div style="color: #6b7280; font-size: 12px; font-family: Arial, sans-serif;">
            Gráfica multi-línea interactiva
        </div>
    </div>
""", unsafe_allow_html=True)

try:
    if not df.empty and 'fecha_publicacion' in df.columns:
        # Crear DataFrame para gráficas diarias
        df_sorted = df.sort_values('fecha_publicacion')
        
        # Agrupar por fecha
        daily_stats = df_sorted.groupby('fecha_publicacion').agg({
            'visualizaciones': 'sum',
            'me_gusta': 'sum',
            'comentarios': 'sum',
            'rendimiento_por_dia': 'mean'
        }).reset_index()
        
        # Crear gráfica multi-línea con subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '📊 Evolución Diaria de Visualizaciones',
                '❤️ Evolución Diaria de Likes',
                '💬 Evolución Diaria de Comentarios',
                '🚀 Rendimiento Promedio Diario'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'scatter'}],
                [{'type': 'scatter'}, {'type': 'scatter'}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Visualizaciones
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['visualizaciones'],
                mode='lines+markers',
                name='Visualizaciones',
                line=dict(color='#3B82F6', width=3),
                marker=dict(size=6, color='#3B82F6'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>👁️ Views: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ),
            row=1, col=1
        )
        
        # 2. Likes
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['me_gusta'],
                mode='lines+markers',
                name='Likes',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6, color='#10b981'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>❤️ Likes: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ),
            row=1, col=2
        )
        
        # 3. Comentarios
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['comentarios'],
                mode='lines+markers',
                name='Comentarios',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=6, color='#8b5cf6'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>💬 Comments: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.1)'
            ),
            row=2, col=1
        )
        
        # 4. Rendimiento diario
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['rendimiento_por_dia'],
                mode='lines+markers',
                name='Rendimiento/Día',
                line=dict(color='#f59e0b', width=3),
                marker=dict(size=6, color='#f59e0b'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>🚀 Perf/Día: %{y:.1f}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(245, 158, 11, 0.1)'
            ),
            row=2, col=2
        )
        
        # Actualizar layout
        fig.update_layout(
            height=750,
            showlegend=False,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=100, b=40),
            title_font=dict(size=16),
            font=dict(size=12),
            hovermode='x unified'
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Visualizaciones", row=1, col=1)
        fig.update_xaxes(title_text="Fecha", row=1, col=2)
        fig.update_yaxes(title_text="Likes", row=1, col=2)
        fig.update_xaxes(title_text="Fecha", row=2, col=1)
        fig.update_yaxes(title_text="Comentarios", row=2, col=1)
        fig.update_xaxes(title_text="Fecha", row=2, col=2)
        fig.update_yaxes(title_text="Rendimiento/Día", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas resumidas debajo del gráfico
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            max_views_day = daily_stats.loc[daily_stats['visualizaciones'].idxmax(), 'fecha_publicacion']
            max_views = daily_stats['visualizaciones'].max()
            st.metric("📅 Día con más Views", max_views_day.strftime('%d/%m/%Y'), f"{max_views:,}")
        
        with col_stats2:
            max_likes_day = daily_stats.loc[daily_stats['me_gusta'].idxmax(), 'fecha_publicacion']
            max_likes = daily_stats['me_gusta'].max()
            st.metric("📅 Día con más Likes", max_likes_day.strftime('%d/%m/%Y'), f"{max_likes:,}")
        
        with col_stats3:
            max_comments_day = daily_stats.loc[daily_stats['comentarios'].idxmax(), 'fecha_publicacion']
            max_comments = daily_stats['comentarios'].max()
            st.metric("📅 Día con más Comments", max_comments_day.strftime('%d/%m/%Y'), f"{max_comments:,}")
        
        with col_stats4:
            max_perf_day = daily_stats.loc[daily_stats['rendimiento_por_dia'].idxmax(), 'fecha_publicacion']
            max_perf = daily_stats['rendimiento_por_dia'].max()
            st.metric("📅 Mejor rendimiento/día", max_perf_day.strftime('%d/%m/%Y'), f"{max_perf:.1f}")
        
except Exception as e:
    st.warning(f"Error al generar gráficas: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 2: CONTENT PERFORMANCE DATA - TABLA COMPLETA
st.markdown("""
<div class="data-table-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
                📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA
            </h3>
            <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; font-family: Arial, sans-serif;">
                Lista completa de contenidos con todos los detalles
            </p>
        </div>
        <div style="color: #6b7280; font-size: 12px; background: #f8fafc; padding: 6px 14px; border-radius: 18px; border: 1px solid #e5e7eb; font-family: Arial, sans-serif;">
            {total_posts} contenidos totales
        </div>
    </div>
""".format(total_posts=total_posts), unsafe_allow_html=True)

if not df.empty:
    # Preparar DataFrame para mostrar
    display_df = df.copy()
    
    # Seleccionar y ordenar columnas
    column_order = []
    
    if 'titulo' in display_df.columns:
        column_order.append('titulo')
        display_df['titulo'] = display_df['titulo'].fillna('Sin título')
    
    if 'fecha_publicacion' in display_df.columns:
        column_order.append('fecha_publicacion')
        display_df['fecha_publicacion'] = display_df['fecha_publicacion'].dt.strftime('%d/%m/%Y %H:%M')
    
    if 'red' in display_df.columns:
        column_order.append('red')
    
    if 'visualizaciones' in display_df.columns:
        column_order.append('visualizaciones')
    
    if 'me_gusta' in df.columns:
        column_order.append('me_gusta')
    
    if 'comentarios' in df.columns:
        column_order.append('comentarios')
    
    # AGREGAR COLUMNA DE SEGUIDORES_TOTALES SI EXISTE
    if 'Seguidores_Totales' in display_df.columns:
        column_order.append('Seguidores_Totales')
    
    if 'rendimiento_por_dia' in display_df.columns:
        column_order.append('rendimiento_por_dia')
    
    if 'dias_desde_publicacion' in display_df.columns:
        column_order.append('dias_desde_publicacion')
    
    if 'semana' in display_df.columns:
        column_order.append('semana')
    
    if 'meses' in display_df.columns:
        column_order.append('meses')
    
    # Filtrar solo columnas existentes
    column_order = [col for col in column_order if col in display_df.columns]
    display_df = display_df[column_order]
    
    # Renombrar columnas para mejor visualización
    rename_dict = {
        'titulo': '📝 TÍTULO',
        'fecha_publicacion': '📅 FECHA PUBLICACIÓN',
        'red': '🌐 PLATAFORMA',
        'visualizaciones': '👁️ VISUALIZACIONES',
        'me_gusta': '❤️ LIKES',
        'comentarios': '💬 COMENTARIOS',
        'Seguidores_Totales': '👥 SEGUIDORES TOTALES',
        'rendimiento_por_dia': '🚀 REND/DÍA',
        'dias_desde_publicacion': '📅 DÍAS PUBLICADO',
        'semana': '📅 SEMANA',
        'meses': '📅 MES'
    }
    
    display_df = display_df.rename(columns={k: v for k, v in rename_dict.items() if k in display_df.columns})
    
    # Configurar columnas para mejor visualización
    column_config = {}
    
    if '👁️ VISUALIZACIONES' in display_df.columns:
        column_config['👁️ VISUALIZACIONES'] = st.column_config.NumberColumn(
            format="%d",
            help="Número total de visualizaciones"
        )
    
    if '❤️ LIKES' in display_df.columns:
        column_config['❤️ LIKES'] = st.column_config.NumberColumn(
            format="%d",
            help="Número total de likes"
        )
    
    if '💬 COMENTARIOS' in display_df.columns:
        column_config['💬 COMENTARIOS'] = st.column_config.NumberColumn(
            format="%d",
            help="Número total de comentarios"
        )
    
    # AGREGAR CONFIGURACIÓN PARA SEGUIDORES TOTALES
    if '👥 SEGUIDORES TOTALES' in display_df.columns:
        column_config['👥 SEGUIDORES TOTALES'] = st.column_config.NumberColumn(
            format="%d",
            help="Seguidores totales del contenido"
        )
    
    if '🚀 REND/DÍA' in display_df.columns:
        column_config['🚀 REND/DÍA'] = st.column_config.NumberColumn(
            format="%.1f",
            help="Rendimiento promedio por día"
        )
    
    if '📝 TÍTULO' in display_df.columns:
        column_config['📝 TÍTULO'] = st.column_config.TextColumn(
            width="large",
            help="Título del contenido"
        )
    
    # Mostrar tabla completa con paginación
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=550
    )
    
    # Estadísticas de la tabla
    col_table1, col_table2, col_table3, col_table4 = st.columns(4)
    
    with col_table1:
        avg_views = display_df['👁️ VISUALIZACIONES'].mean() if '👁️ VISUALIZACIONES' in display_df.columns else 0
        st.metric("📊 Views promedio", f"{avg_views:,.0f}")
    
    with col_table2:
        avg_likes = display_df['❤️ LIKES'].mean() if '❤️ LIKES' in display_df.columns else 0
        st.metric("📊 Likes promedio", f"{avg_likes:,.0f}")
    
    with col_table3:
        avg_comments = display_df['💬 COMENTARIOS'].mean() if '💬 COMENTARIOS' in display_df.columns else 0
        st.metric("📊 Comments promedio", f"{avg_comments:,.0f}")
    
    with col_table4:
        avg_perf = display_df['🚀 REND/DÍA'].mean() if '🚀 REND/DÍA' in display_df.columns else 0
        st.metric("📊 Rendimiento promedio", f"{avg_perf:.1f}")
    
    # AGREGAR ESTADÍSTICA DE SEGUIDORES SI EXISTE
    if '👥 SEGUIDORES TOTALES' in display_df.columns:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col_followers1, col_followers2, col_followers3, col_followers4 = st.columns(4)
        
        with col_followers1:
            total_seguidores = display_df['👥 SEGUIDORES TOTALES'].sum() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Total Seguidores", f"{total_seguidores:,}")
        
        with col_followers2:
            avg_seguidores = display_df['👥 SEGUIDORES TOTALES'].mean() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Promedio/Post", f"{avg_seguidores:,.0f}")
        
        with col_followers3:
            max_seguidores = display_df['👥 SEGUIDORES TOTALES'].max() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Máximo", f"{max_seguidores:,}")
        
        with col_followers4:
            min_seguidores = display_df['👥 SEGUIDORES TOTALES'].min() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Mínimo", f"{min_seguidores:,}")
    
else:
    st.info("No hay datos para mostrar en la tabla")

st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 3: ANÁLISIS DETALLADO EN DOS COLUMNAS
col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-family: Arial Black, sans-serif;">
                📊 PERFORMANCE ANALYTICS
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if not df.empty and 'rendimiento_por_dia' in df.columns:
        # Análisis de distribución por rendimiento
        q75 = df['rendimiento_por_dia'].quantile(0.75)
        q50 = df['rendimiento_por_dia'].quantile(0.50)
        q25 = df['rendimiento_por_dia'].quantile(0.25)
        
        high_perf = len(df[df['rendimiento_por_dia'] > q75])
        medium_high_perf = len(df[(df['rendimiento_por_dia'] > q50) & (df['rendimiento_por_dia'] <= q75)])
        medium_low_perf = len(df[(df['rendimiento_por_dia'] > q25) & (df['rendimiento_por_dia'] <= q50)])
        low_perf = len(df[df['rendimiento_por_dia'] <= q25])
        
        # Gráfico de pastel
        labels = ['🟢 Alto', '🟡 Medio-Alto', '🟠 Medio-Bajo', '🔴 Bajo']
        values = [high_perf, medium_high_perf, medium_low_perf, low_perf]
        colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            height=320,
            showlegend=False,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20),
            title_text="Distribución por Nivel de Rendimiento",
            title_font=dict(size=14)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Estadísticas detalladas
        high_perf_pct = (high_perf / total_posts * 100) if total_posts > 0 else 0
        medium_high_pct = (medium_high_perf / total_posts * 100) if total_posts > 0 else 0
        medium_low_pct = (medium_low_perf / total_posts * 100) if total_posts > 0 else 0
        low_perf_pct = (low_perf / total_posts * 100) if total_posts > 0 else 0
        
        st.markdown(f"""
        <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                    border-radius: 12px; border-left: 4px solid #3B82F6;">
            <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 15px; font-family: Arial Black, sans-serif;">📈 ANÁLISIS DE PERFORMANCE</h4>
            <div style="color: #4b5563; font-size: 13px; font-family: Arial, sans-serif;">
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟢 Alto rendimiento:</span>
                    <span style="font-weight: 700; color: #10b981;">{high_perf} posts ({high_perf_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟡 Medio-Alto:</span>
                    <span style="font-weight: 700; color: #f59e0b;">{medium_high_perf} posts ({medium_high_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟠 Medio-Bajo:</span>
                    <span style="font-weight: 700; color: #f97316;">{medium_low_perf} posts ({medium_low_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🔴 Bajo rendimiento:</span>
                    <span style="font-weight: 700; color: #ef4444;">{low_perf} posts ({low_perf_pct:.1f}%)</span>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                    <span style="display: inline-block; width: 160px;">📊 Rendimiento promedio:</span>
                    <span style="font-weight: 700; color: #3B82F6;">{df['rendimiento_por_dia'].mean():.1f} views/día</span>
                </div>
                <div style="margin-top: 6px;">
                    <span style="display: inline-block; width: 160px;">🚀 Mejor rendimiento:</span>
                    <span style="font-weight: 700; color: #8b5cf6;">{df['rendimiento_por_dia'].max():.1f} views/día</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("No hay datos para análisis de performance")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_analysis2:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-family: Arial Black, sans-serif;">
                📈 KEY METRICS - MÉTRICAS CLAVE
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Calcular métricas detalladas
        metrics_detailed = []
        
        # Métricas de visualizaciones
        if 'visualizaciones' in df.columns:
            metrics_detailed.append(('👁️ Avg. Views/Post', f"{df['visualizaciones'].mean():.0f}"))
            metrics_detailed.append(('👁️ Median Views', f"{df['visualizaciones'].median():.0f}"))
            metrics_detailed.append(('👁️ Std Dev Views', f"{df['visualizaciones'].std():.0f}"))
            metrics_detailed.append(('👁️ Min Views', f"{df['visualizaciones'].min():,}"))
            metrics_detailed.append(('👁️ Max Views', f"{df['visualizaciones'].max():,}"))
        
        # Métricas de engagement
        if 'me_gusta' in df.columns:
            metrics_detailed.append(('❤️ Avg. Likes/Post', f"{df['me_gusta'].mean():.1f}"))
            metrics_detailed.append(('❤️ Max Likes', f"{df['me_gusta'].max():,}"))
        
        if 'comentarios' in df.columns:
            metrics_detailed.append(('💬 Avg. Comments/Post', f"{df['comentarios'].mean():.1f}"))
            metrics_detailed.append(('💬 Max Comments', f"{df['comentarios'].max():,}"))
        
        # Métricas de seguidores si existen
        if 'Seguidores_Totales' in df.columns:
            metrics_detailed.append(('👥 Avg. Followers/Post', f"{df['Seguidores_Totales'].mean():.0f}"))
            metrics_detailed.append(('👥 Total Followers', f"{df['Seguidores_Totales'].sum():,}"))
        
        # Métricas de tiempo
        if 'dias_desde_publicacion' in df.columns:
            metrics_detailed.append(('📅 Avg. Content Age', f"{df['dias_desde_publicacion'].mean():.0f} días"))
            metrics_detailed.append(('📅 Newest Post', f"{df['dias_desde_publicacion'].min()} días"))
            metrics_detailed.append(('📅 Oldest Post', f"{df['dias_desde_publicacion'].max()} días"))
        
        # Métricas de rendimiento
        if 'rendimiento_por_dia' in df.columns:
            metrics_detailed.append(('🚀 Avg. Daily Perf.', f"{df['rendimiento_por_dia'].mean():.1f}"))
            metrics_detailed.append(('🚀 Median Daily Perf.', f"{df['rendimiento_por_dia'].median():.1f}"))
        
        # Engagement rate detallado
        metrics_detailed.append(('💬 Engagement Rate', f"{engagement_rate:.2f}%"))
        
        if total_views > 0 and total_likes > 0:
            like_to_view_ratio = (total_likes / total_views) * 100
            metrics_detailed.append(('👍 Like/View Ratio', f"{like_to_view_ratio:.2f}%"))
        
        if total_comments > 0 and total_likes > 0:
            comment_to_like_ratio = (total_comments / total_likes) * 100
            metrics_detailed.append(('💬 Comment/Like Ratio', f"{comment_to_like_ratio:.2f}%"))
        
        # Mostrar métricas en tabla mejorada
        for i, (metric, value) in enumerate(metrics_detailed):
            bg_color = "#ffffff" if i % 2 == 0 else "#f8fafc"
            icon = metric.split(' ')[0]
            metric_name = ' '.join(metric.split(' ')[1:])
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 12px 14px; background: {bg_color}; 
                        border-radius: 8px; margin: 3px 0; border: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 16px;">{icon}</span>
                    <span style="color: #4b5563; font-size: 13px; font-weight: 500; font-family: Arial, sans-serif;">{metric_name}</span>
                </div>
                <span style="font-weight: 700; color: #1f2937; font-size: 14px; font-family: Arial Black, sans-serif;">
                    {value}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis de engagement avanzado
        st.markdown("""
        <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                    border-radius: 12px; border-left: 4px solid #0ea5e9;">
            <h4 style="margin: 0 0 10px 0; color: #374151; font-size: 15px; font-family: Arial Black, sans-serif;">📊 ANÁLISIS DE ENGAGEMENT AVANZADO</h4>
            <div style="color: #4b5563; font-size: 13px; font-family: Arial, sans-serif;">
        """, unsafe_allow_html=True)
        
        engagement_html = ""
        
        if total_views > 0:
            like_rate = (total_likes / total_views * 100) if 'me_gusta' in df.columns else 0
            comment_rate = (total_comments / total_views * 100) if 'comentarios' in df.columns else 0
            
            engagement_html += f"""
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">👍 Tasa de Likes:</span>
                    <span style="font-weight: 700; color: #10b981;">{like_rate:.2f}%</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">💬 Tasa de Comentarios:</span>
                    <span style="font-weight: 700; color: #3B82F6;">{comment_rate:.2f}%</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">📊 Total Engagement:</span>
                    <span style="font-weight: 700; color: #8b5cf6;">{(like_rate + comment_rate):.2f}%</span>
                </div>
            """
        
        if total_likes > 0 and total_comments > 0:
            like_to_comment_ratio = total_likes / total_comments
            engagement_html += f"""
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                    <span style="display: inline-block; width: 160px;">⚖️ Ratio Likes/Comments:</span>
                    <span style="font-weight: 700; color: #EC4899;">{like_to_comment_ratio:.1f}</span>
                </div>
            """
        
        if engagement_html:
            st.markdown(engagement_html, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    else:
        st.info("No hay datos para métricas clave")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 12px; padding: 25px; 
            border-top: 1px solid #e5e7eb; margin-top: 30px;">
    <div style="display: flex; justify-content: center; gap: 25px; margin-bottom: 12px; flex-wrap: wrap; font-family: Arial, sans-serif;">
        <span>Social Media Dashboard PRO v3.3</span>
        <span>•</span>
        <span>Data from Backend API</span>
        <span>•</span>
        <span>{platform_name} Analytics</span>
        <span>•</span>
        <span>Updated in Real-time</span>
        <span>•</span>
        <span>Gráficas Avanzadas • Chat con IA</span>
    </div>
    <div style="font-size: 11px; color: #9ca3af; font-family: Arial, sans-serif;">
        © 2025 Social Media Analytics Platform • Connected to: <strong>{BACKEND_URL}</strong> • {current_time_full}
    </div>
</div>
""", unsafe_allow_html=True)
