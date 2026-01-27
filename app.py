import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import numpy as np
from io import BytesIO

warnings.filterwarnings('ignore')

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
DATOS1_URL = "https://pahubisas.pythonanywhere.com/datos1"
DATOS2_URL = "https://pahubisas.pythonanywhere.com/datos2"


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
# NUEVAS FUNCIONES PARA GRÁFICAS AVANZADAS - CORREGIDAS
#############################################

def _download_bytes(url, timeout=60):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content


def cargar_imagen_grafica1_bytes():
    try:
        return _download_bytes(GRAFICA1_URL, timeout=30)
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 1: {str(e)}")
        return b""


def cargar_imagen_grafica2_bytes():
    try:
        return _download_bytes(GRAFICA2_URL, timeout=30)
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 2: {str(e)}")
        return b""


def cargar_excel_metricas_grafica1_bytes():
    try:
        return _download_bytes(DATOS1_URL, timeout=60)
    except Exception as e:
        st.error(f"Error al cargar Excel de métricas (gráfica 1): {str(e)}")
        return b""


def cargar_excel_metricas_grafica2_bytes():
    try:
        return _download_bytes(DATOS2_URL, timeout=60)
    except Exception as e:
        st.error(f"Error al cargar Excel de métricas (gráfica 2): {str(e)}")
        return b""


def leer_excel_primer_sheet(excel_bytes):
    if not excel_bytes:
        return pd.DataFrame()
    try:
        xls = pd.ExcelFile(BytesIO(excel_bytes))
        if not xls.sheet_names:
            return pd.DataFrame()
        return xls.parse(xls.sheet_names[0])
    except Exception:
        return pd.DataFrame()


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
.status-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 10px 12px;
    margin: 6px 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.status-connected { color: #10b981; font-weight: 600; }
.status-warning { color: #f59e0b; font-weight: 600; }
.status-disconnected { color: #ef4444; font-weight: 600; }

.sidebar-title {
    color: #e2e8f0;
    font-size: 14px;
    font-weight: 800;
    margin: 12px 0 8px 0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.backend-status {
    padding: 8px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
    margin: 10px 0;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.10);
}

.backend-connected {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
}

.backend-disconnected {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
}

/* Gráficas avanzadas */
.grafica-container {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    margin-top: 15px;
}

.grafica-title {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 6px;
    font-family: 'Arial Black', sans-serif;
}

.grafica-subtitle {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 18px;
    font-weight: 600;
}

.footer-container {
    padding: 18px;
    background: #0f172a;
    border-radius: 14px;
    color: #e2e8f0;
    margin-top: 18px;
    border: 1px solid #334155;
    font-size: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar principal
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size: 28px; font-weight: 900; color: #e2e8f0; font-family: 'Arial Black', sans-serif;">
            DASHBOARD PRO
        </div>
        <div style="font-size: 12px; opacity: 0.85; color: #cbd5e1; margin-top: 6px; font-family: Arial, sans-serif;">
            Social Analytics • Powered by PythonAnywhere
        </div>
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

    with col_graf2:
        if st.button("📊 Gráfica 2", key="grafica2_btn", use_container_width=True,
                     help="Gráfica 2 + métricas Excel"):
            st.session_state["show_grafica2"] = not st.session_state.get("show_grafica2", False)
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False

    # Botón para ocultar gráficas
    if st.session_state.get("show_grafica1", False) or st.session_state.get("show_grafica2", False):
        if st.button("⬅️ Volver a Dashboard", key="back_dashboard", use_container_width=True):
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
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

# ================================================================
# SECCIÓN: GRÁFICAS AVANZADAS (si están activadas)
# ================================================================

# Gráfica 1: Inversión vs Seguidores
if st.session_state.get("show_grafica1", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📈 GRÁFICA 1: INVERSIÓN VS SEGUIDORES</div>
        <div class="grafica-subtitle">
            Imagen + Excel de métricas (1 hoja) • Descarga directa desde el backend
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando imagen y métricas (gráfica 1)..."):
        img_bytes = cargar_imagen_grafica1_bytes()
        if img_bytes:
            st.image(img_bytes, caption="Inversion vs Seguidores", use_container_width=True)
            st.markdown(f"[Abrir imagen en navegador]({GRAFICA1_URL})")
        else:
            st.warning("No se pudo cargar la imagen.")

        xlsx_bytes = cargar_excel_metricas_grafica1_bytes()
        df_metricas = leer_excel_primer_sheet(xlsx_bytes)
        if not df_metricas.empty:
            st.dataframe(df_metricas, use_container_width=True)
        else:
            if xlsx_bytes:
                st.info("Excel descargado, pero no se pudo leer la hoja.")
            else:
                st.warning("No se pudo cargar el Excel.")

        if xlsx_bytes:
            st.download_button(
                label="⬇️ Descargar Excel: metricas_seguidores_vs_inversion.xlsx",
                data=xlsx_bytes,
                file_name="metricas_seguidores_vs_inversion.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown(f"[Abrir Excel en navegador]({DATOS1_URL})")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Gráfica 2: Heatmap CPS
elif st.session_state.get("show_grafica2", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📊 GRÁFICA 2</div>
        <div class="grafica-subtitle">
            Imagen + Excel de métricas (1 hoja) • Descarga directa desde el backend
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando imagen y métricas (gráfica 2)..."):
        img_bytes = cargar_imagen_grafica2_bytes()
        if img_bytes:
            st.image(img_bytes, caption="Grafica 2", use_container_width=True)
            st.markdown(f"[Abrir imagen en navegador]({GRAFICA2_URL})")
        else:
            st.warning("No se pudo cargar la imagen.")

        xlsx_bytes = cargar_excel_metricas_grafica2_bytes()
        df_metricas = leer_excel_primer_sheet(xlsx_bytes)
        if not df_metricas.empty:
            st.dataframe(df_metricas, use_container_width=True)
        else:
            if xlsx_bytes:
                st.info("Excel descargado, pero no se pudo leer la hoja.")
            else:
                st.warning("No se pudo cargar el Excel.")

        if xlsx_bytes:
            st.download_button(
                label="⬇️ Descargar Excel: metricas_grafica2.xlsx",
                data=xlsx_bytes,
                file_name="metricas_grafica2.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown(f"[Abrir Excel en navegador]({DATOS2_URL})")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================================================================
# DASHBOARD NORMAL (si no se están mostrando gráficas avanzadas)
# ================================================================

# Calcular métricas clave
total_posts = len(df)
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

current_time_short = datetime.now().strftime('%H:%M')

# Información de la plataforma
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    st.markdown(f'<div style="font-size: 38px; text-align: center; color: {platform_color};">{platform_icon}</div>', unsafe_allow_html=True)

with col_header2:
    st.markdown(f"""
    <div style="text-align: left; padding-top: 6px;">
        <div style="font-size: 22px; font-weight: 900; color: #0f172a; font-family: 'Arial Black', sans-serif;">
            {platform_name} Analytics
        </div>
        <div style="font-size: 12px; color: #64748b; font-weight: 600; font-family: Arial, sans-serif;">
            Resumen de rendimiento y métricas clave
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_header3:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 8px;">
        <div style="font-size: 12px; color: #64748b; font-weight: 700; font-family: Arial, sans-serif;">
            {current_time_short}
        </div>
        <div style="font-size: 11px; color: #94a3b8; font-weight: 600; font-family: Arial, sans-serif;">
            Hora local
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Métricas principales
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Publicaciones</div>
        <div class="metric-value">{total_posts:,}</div>
        <div class="metric-trend trend-up">📌 Total</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Visualizaciones</div>
        <div class="metric-value">{int(total_views):,}</div>
        <div class="metric-trend trend-up">👁️ Total</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Me gusta</div>
        <div class="metric-value">{int(total_likes):,}</div>
        <div class="metric-trend trend-up">❤️ Total</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Comentarios</div>
        <div class="metric-value">{int(total_comments):,}</div>
        <div class="metric-trend trend-up">💬 Total</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Engagement</div>
        <div class="metric-value">{engagement_rate:.1f}%</div>
        <div class="metric-trend trend-up">📈 Promedio</div>
    </div>
    """, unsafe_allow_html=True)

# Sección de pauta publicitaria (solo GENERAL)
if selected_platform == "general" and not df_pauta.empty:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 18px; font-weight: 900; color: #0f172a; font-family: 'Arial Black', sans-serif; margin-bottom: 6px;">
        📣 Pauta Publicitaria (Resumen)
    </div>
    """, unsafe_allow_html=True)

    # Tomar último registro si hay varios
    row = df_pauta.iloc[-1].to_dict() if len(df_pauta) > 0 else {}
    coste = int(row.get("coste_anuncio", 0)) if row.get("coste_anuncio", 0) is not None else 0
    vis = int(row.get("visualizaciones_videos", 0)) if row.get("visualizaciones_videos", 0) is not None else 0
    seg = int(row.get("nuevos_seguidores", 0)) if row.get("nuevos_seguidores", 0) is not None else 0
    fecha = row.get("fecha", "")
    fecha_txt = ""
    try:
        if pd.notna(fecha):
            fecha_txt = pd.to_datetime(fecha).strftime("%d/%m/%Y")
    except Exception:
        fecha_txt = str(fecha)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">Inversión</div>
            <div class="pauta-value">${coste:,}</div>
            <div class="pauta-period">{fecha_txt}</div>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">Visualizaciones</div>
            <div class="pauta-value">{vis:,}</div>
            <div class="pauta-period">{fecha_txt}</div>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">Seguidores</div>
            <div class="pauta-value">{seg:,}</div>
            <div class="pauta-period">{fecha_txt}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📊 Rendimiento", "📈 Tendencias", "🗂️ Datos"])

# TAB 1: Rendimiento
with tab1:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)

    if 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
        # Top 10 posts por visualizaciones
        df_top = df.dropna(subset=['fecha_publicacion', 'visualizaciones']).sort_values('visualizaciones', ascending=False).head(10)

        fig = px.bar(
            df_top,
            x='visualizaciones',
            y='titulo' if 'titulo' in df_top.columns else df_top.index.astype(str),
            orientation='h',
            title="Top 10 Publicaciones por Visualizaciones",
        )
        fig.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=60, b=10),
            yaxis_title="",
            xaxis_title="Visualizaciones",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay columnas suficientes para graficar rendimiento.")

    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Tendencias
with tab2:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)

    try:
        # Evolución de visualizaciones por fecha (si existe)
        if 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
            df_ts = df.dropna(subset=['fecha_publicacion']).copy()
            df_ts['fecha_publicacion'] = pd.to_datetime(df_ts['fecha_publicacion'], errors='coerce')
            df_ts = df_ts.dropna(subset=['fecha_publicacion'])
            df_daily = df_ts.groupby(df_ts['fecha_publicacion'].dt.date)['visualizaciones'].sum().reset_index()
            df_daily.columns = ['fecha', 'visualizaciones']

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_daily['fecha'],
                y=df_daily['visualizaciones'],
                mode='lines+markers',
                name='Visualizaciones'
            ))
            fig.update_layout(
                title="Tendencia diaria de visualizaciones",
                height=420,
                margin=dict(l=10, r=10, t=60, b=10),
                xaxis_title="Fecha",
                yaxis_title="Visualizaciones"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes para generar tendencias.")
    except Exception as e:
        st.warning(f"Error al generar gráfica de tendencias: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Datos
with tab3:
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 16px; font-weight: 900; color: #0f172a; font-family: 'Arial Black', sans-serif; margin-bottom: 10px;">
        🗂️ Datos crudos (filtrados por plataforma)
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True, height=460)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div class="footer-container">
    © 2025 Social Media Analytics Platform • Connected to: <strong>{BACKEND_URL}</strong> • {current_time_full}
</div>
""", unsafe_allow_html=True)
