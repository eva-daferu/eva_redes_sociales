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
# ENDPOINTS (DATOS + GRÁFICAS)
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/followers"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/pauta_anuncio"

# Gráfica 1
GRAFICA1_IMG_URL = "https://pahubisas.pythonanywhere.com/grafica1"
METRICAS1_URL = "https://pahubisas.pythonanywhere.com/metricas_grafica1"

# Gráfica 2
GRAFICA2_IMG_URL = "https://pahubisas.pythonanywhere.com/grafica2"
METRICAS2_URL = "https://pahubisas.pythonanywhere.com/metricas_grafica2"


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
# FUNCIONES PARA GRÁFICAS (ARCHIVOS)
#############################################

def _descargar_bytes(url, timeout=30):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content, r.headers.get("Content-Type", "")


def cargar_imagen_grafica1_bytes():
    """Descarga la imagen PNG de la Gráfica 1"""
    try:
        content, _ = _descargar_bytes(GRAFICA1_IMG_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 1: {str(e)}")
        return b""


def cargar_excel_metricas_grafica1_bytes():
    """Descarga el Excel XLSX de métricas de la Gráfica 1"""
    try:
        content, _ = _descargar_bytes(METRICAS1_URL, timeout=60)
        return content
    except Exception as e:
        st.error(f"Error al cargar Excel de métricas (gráfica 1): {str(e)}")
        return b""


def cargar_imagen_grafica2_bytes():
    """Descarga la imagen PNG de la Gráfica 2"""
    try:
        content, _ = _descargar_bytes(GRAFICA2_IMG_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 2: {str(e)}")
        return b""


def cargar_excel_metricas_grafica2_bytes():
    """Descarga el Excel XLSX de métricas de la Gráfica 2"""
    try:
        content, _ = _descargar_bytes(METRICAS2_URL, timeout=60)
        return content
    except Exception as e:
        st.error(f"Error al cargar Excel de métricas (gráfica 2): {str(e)}")
        return b""


def leer_excel_primer_sheet(excel_bytes):
    """Lee SOLO la primera hoja del Excel (la más relevante por defecto)."""
    if not excel_bytes:
        return pd.DataFrame()
    try:
        xls = pd.ExcelFile(BytesIO(excel_bytes))
        if not xls.sheet_names:
            return pd.DataFrame()
        return xls.parse(xls.sheet_names[0])
    except Exception:
        return pd.DataFrame()


#############################################
# FIN NUEVAS FUNCIONES CORREGIDAS
#############################################

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
.status-indicator {
    display: inline-flex;
    align-items: center;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.status-active {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-warning {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Tablas mejoradas */
.dataframe {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

/* Gráficas Avanzadas (contenedor) */
.grafica-container {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.10);
    border: 1px solid #e5e7eb;
    margin: 16px 0 24px 0;
}

.grafica-title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.grafica-subtitle {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    margin-bottom: 16px;
}

.grafica-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
}

.grafica-tab {
    padding: 10px 14px;
    border-radius: 12px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    font-weight: 700;
    color: #334155;
}

.grafica-tab:hover {
    background: #e2e8f0;
}

.grafica-tab.active {
    background: rgba(59,130,246,0.15);
    border-color: rgba(59,130,246,0.35);
    color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# ================================================================
# SIDEBAR: Selección de plataforma y opciones
# ================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="color: white; margin: 0;">📊 Dashboard PRO</h2>
        <p style="color: #94a3b8; margin: 5px 0 0 0;">Social Media Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Selección de plataforma
    st.markdown("### 🎯 Seleccionar Plataforma")

    if "selected_platform" not in st.session_state:
        st.session_state.selected_platform = "general"

    platforms = [
        ("general", "Vista General", "📊"),
        ("tiktok", "TikTok", "🎵"),
        ("youtobe", "YouTube", "▶️"),
        ("instagram", "Instagram", "📷"),
        ("facebook", "Facebook", "📘")
    ]

    for platform_id, platform_name, icon in platforms:
        if st.button(
            f"{icon} {platform_name}",
            key=f"btn_{platform_id}",
            use_container_width=True,
            type="primary" if st.session_state.selected_platform == platform_id else "secondary"
        ):
            st.session_state.selected_platform = platform_id

    st.markdown("---")

    # Filtro de tiempo
    st.markdown("### 📅 Filtro de Tiempo")

    time_options = ["Todo el período", "Últimos 7 días", "Últimos 30 días", "Últimos 90 días"]
    if "tiempo_filtro" not in st.session_state:
        st.session_state.tiempo_filtro = "Todo el período"

    st.session_state.tiempo_filtro = st.selectbox(
        "Seleccionar período:",
        time_options,
        index=time_options.index(st.session_state.tiempo_filtro)
    )

    st.markdown("---")

    # Acciones rápidas
    st.markdown("### ⚡ Acciones Rápidas")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with col_btn2:
        if st.button("📊 Exportar", use_container_width=True):
            st.session_state.show_export = True

    st.markdown("---")

    # Gráficas Avanzadas
    st.markdown("### 📈 Gráficas Avanzadas")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        if st.button("📈 Gráfica 1", key="grafica1_btn", use_container_width=True,
                     type="primary" if st.session_state.get("show_grafica1", False) else "secondary"):
            st.session_state["show_grafica1"] = not st.session_state.get("show_grafica1", False)
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False

    with col_g2:
        if st.button("📊 Gráfica 2", key="grafica2_btn", use_container_width=True,
                     type="primary" if st.session_state.get("show_grafica2", False) else "secondary"):
            st.session_state["show_grafica2"] = not st.session_state.get("show_grafica2", False)
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False

    if st.session_state.get("show_grafica1", False) or st.session_state.get("show_grafica2", False):
        if st.button("❌ Cerrar Gráficas", use_container_width=True):
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False


# ================================================================
# MAIN: Header y contenido principal
# ================================================================
selected_platform = st.session_state.selected_platform

# Header principal
st.markdown(f"""
<div class="dashboard-header">
    <h1>📊 Social Media Dashboard PRO</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 16px;">
        Análisis avanzado de rendimiento • Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </p>
</div>
""", unsafe_allow_html=True)

# Seleccionar dataset según plataforma
if selected_platform == "general":
    df = df_all.copy()
    platform_name = "Vista General"
    platform_color = "#3B82F6"
    platform_icon = "📊"
elif selected_platform == "tiktok":
    df = tiktok_df.copy()
    platform_name = "TikTok"
    platform_color = "#000000"
    platform_icon = "🎵"
elif selected_platform == "youtobe":
    df = youtobe_df.copy()
    platform_name = "YouTube"
    platform_color = "#FF0000"
    platform_icon = "▶️"
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
            Análisis de eficiencia por nivel de inversión • CPS (Costo por Seguidor) • Punto óptimo
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando imagen y métricas..."):
        img_bytes = cargar_imagen_grafica1_bytes()
        if img_bytes:
            st.image(img_bytes, caption="Inversion vs Seguidores", use_container_width=True)
            st.markdown(f"[Abrir imagen en navegador]({GRAFICA1_IMG_URL})")
        else:
            st.warning("No se pudo cargar la imagen.")

        excel_bytes = cargar_excel_metricas_grafica1_bytes()
        if excel_bytes:
            st.download_button(
                label="⬇️ Descargar Excel: metricas_grafica1.xlsx",
                data=excel_bytes,
                file_name="metricas_grafica1.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown(f"[Abrir Excel en navegador]({METRICAS1_URL})")
        else:
            st.warning("No se pudo cargar el Excel.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Gráfica 2: Heatmap CPS
elif st.session_state.get("show_grafica2", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📊 GRÁFICA 2: HEATMAP CPS (COSTO POR SEGUIDOR)</div>
        <div class="grafica-subtitle">
            Análisis por día de semana y semana ISO • CPS bajo = mejor eficiencia • Etiquetas siempre visibles
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando imagen y métricas..."):
        img_bytes = cargar_imagen_grafica2_bytes()
        if img_bytes:
            st.image(img_bytes, caption="grafica2", use_container_width=True)
            st.markdown(f"[Abrir imagen en navegador]({GRAFICA2_IMG_URL})")
        else:
            st.warning("No se pudo cargar la imagen.")

        excel_bytes = cargar_excel_metricas_grafica2_bytes()
        df_metricas = leer_excel_primer_sheet(excel_bytes)

        if not df_metricas.empty:
            st.dataframe(df_metricas, use_container_width=True)
        else:
            st.warning("No hay datos para mostrar.")

        if excel_bytes:
            st.download_button(
                label="⬇️ Descargar Excel: metricas_seguidores_vs_inversion.xlsx",
                data=excel_bytes,
                file_name="metricas_seguidores_vs_inversion.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown(f"[Abrir Excel en navegador]({METRICAS2_URL})")
        else:
            st.warning("No se pudo cargar el Excel.")

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
    <div style="padding: 8px 0;">
        <h2 style="margin: 0; color: #1f2937;">{platform_name} Analytics</h2>
        <p style="margin: 3px 0 0 0; color: #6b7280; font-weight: 500;">
            Período: {st.session_state.tiempo_filtro} • Actualizado: {current_time_short}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_header3:
    status_class = "status-active" if not df.empty else "status-warning"
    status_text = "✅ Datos Activos" if not df.empty else "⚠️ Sin Datos"
    st.markdown(f"""
    <div style="text-align: right; padding: 10px 0;">
        <span class="status-indicator {status_class}">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# MÉTRICAS PRINCIPALES
# ================================================================
col1, col2, col3, col4, col5 = st.columns(5)

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return f"{num:,.0f}"

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Posts</div>
        <div class="metric-value">{total_posts}</div>
        <div class="metric-trend trend-up">📈 Contenido publicado</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Visualizaciones</div>
        <div class="metric-value">{format_number(total_views)}</div>
        <div class="metric-trend trend-up">👁️ Total acumulado</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Me gusta</div>
        <div class="metric-value">{format_number(total_likes)}</div>
        <div class="metric-trend trend-up">❤️ Engagement</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Comentarios</div>
        <div class="metric-value">{format_number(total_comments)}</div>
        <div class="metric-trend trend-up">💬 Interacciones</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Seguidores</div>
        <div class="metric-value">{format_number(total_followers)}</div>
        <div class="metric-trend trend-up">👥 Comunidad</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================================================================
# TABS PRINCIPALES DEL DASHBOARD
# ================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Rendimiento", "📈 Análisis Temporal", "🎯 Contenido Top", "💰 Pauta Publicitaria"])

# ================================================================
# TAB 1: RENDIMIENTO GENERAL
# ================================================================
with tab1:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("📊 Visualizaciones por Contenido")

        if 'titulo' in df.columns and 'visualizaciones' in df.columns:
            df_sorted = df.sort_values('visualizaciones', ascending=False).head(15)

            fig_bar = px.bar(
                df_sorted,
                x='visualizaciones',
                y='titulo',
                orientation='h',
                title="Top 15 Contenidos por Visualizaciones",
                labels={'visualizaciones': 'Visualizaciones', 'titulo': 'Contenido'}
            )

            fig_bar.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )

            st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.subheader("🎯 Distribución Engagement")

        engagement_data = {
            'Tipo': ['Me gusta', 'Comentarios'],
            'Cantidad': [total_likes, total_comments]
        }

        fig_pie = px.pie(
            pd.DataFrame(engagement_data),
            values='Cantidad',
            names='Tipo',
            title="Engagement Total"
        )

        fig_pie.update_layout(height=500)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Tabla de datos
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.subheader("📋 Datos Detallados")

    # Seleccionar columnas relevantes
    cols_to_show = []
    for col in ['titulo', 'fecha_publicacion', 'visualizaciones', 'me_gusta', 'comentarios', 'rendimiento_por_dia']:
        if col in df.columns:
            cols_to_show.append(col)

    if cols_to_show:
        df_display = df[cols_to_show].copy()

        # Formatear fecha
        if 'fecha_publicacion' in df_display.columns:
            df_display['fecha_publicacion'] = df_display['fecha_publicacion'].dt.strftime('%d/%m/%Y')

        st.dataframe(df_display, use_container_width=True, height=400)

    st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# TAB 2: ANÁLISIS TEMPORAL
# ================================================================
with tab2:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)

    st.subheader("📈 Evolución Temporal")

    if 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
        df_time = df.groupby('fecha_publicacion').agg({
            'visualizaciones': 'sum',
            'me_gusta': 'sum' if 'me_gusta' in df.columns else 'count',
            'comentarios': 'sum' if 'comentarios' in df.columns else 'count'
        }).reset_index()

        fig_line = go.Figure()

        fig_line.add_trace(go.Scatter(
            x=df_time['fecha_publicacion'],
            y=df_time['visualizaciones'],
            mode='lines+markers',
            name='Visualizaciones'
        ))

        if 'me_gusta' in df_time.columns:
            fig_line.add_trace(go.Scatter(
                x=df_time['fecha_publicacion'],
                y=df_time['me_gusta'],
                mode='lines+markers',
                name='Me gusta',
                yaxis='y2'
            ))

        fig_line.update_layout(
            title="Evolución de Métricas en el Tiempo",
            xaxis_title="Fecha",
            yaxis_title="Visualizaciones",
            yaxis2=dict(
                title="Me gusta",
                overlaying='y',
                side='right'
            ),
            height=500
        )

        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Seguidores temporal
    if not df_followers.empty and selected_platform in ["general", "tiktok"]:
        st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
        st.subheader("👥 Evolución de Seguidores")

        if 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
            fig_followers = px.line(
                df_followers,
                x='Fecha',
                y='Seguidores_Totales',
                title="Crecimiento de Seguidores",
                markers=True
            )

            fig_followers.update_layout(height=400)
            st.plotly_chart(fig_followers, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# TAB 3: CONTENIDO TOP
# ================================================================
with tab3:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)

    st.subheader("🏆 Top Contenidos")

    col_top1, col_top2 = st.columns(2)

    with col_top1:
        st.markdown("#### 👁️ Más Vistos")
        if 'visualizaciones' in df.columns:
            top_views = df.nlargest(10, 'visualizaciones')[['titulo', 'visualizaciones']]
            st.dataframe(top_views, use_container_width=True)

    with col_top2:
        st.markdown("#### ❤️ Más Engagement")
        if 'me_gusta' in df.columns:
            df['engagement_total'] = df['me_gusta'] + df['comentarios']
            top_engagement = df.nlargest(10, 'engagement_total')[['titulo', 'engagement_total', 'me_gusta', 'comentarios']]
            st.dataframe(top_engagement, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# TAB 4: PAUTA PUBLICITARIA
# ================================================================
with tab4:
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.subheader("💰 Resumen Pauta Publicitaria")

    if not df_pauta.empty:
        # Calcular métricas de pauta
        total_inversion = df_pauta['coste_anuncio'].sum() if 'coste_anuncio' in df_pauta.columns else 0
        total_visualizaciones_ads = df_pauta['visualizaciones_videos'].sum() if 'visualizaciones_videos' in df_pauta.columns else 0
        total_nuevos_seguidores = df_pauta['nuevos_seguidores'].sum() if 'nuevos_seguidores' in df_pauta.columns else 0

        col_p1, col_p2, col_p3 = st.columns(3)

        with col_p1:
            st.markdown(f"""
            <div class="pauta-card">
                <div class="pauta-label">Inversión Total</div>
                <div class="pauta-value">${total_inversion:,.0f}</div>
                <div class="pauta-period">COP</div>
            </div>
            """, unsafe_allow_html=True)

        with col_p2:
            st.markdown(f"""
            <div class="pauta-card">
                <div class="pauta-label">Visualizaciones Ads</div>
                <div class="pauta-value">{format_number(total_visualizaciones_ads)}</div>
                <div class="pauta-period">Total</div>
            </div>
            """, unsafe_allow_html=True)

        with col_p3:
            st.markdown(f"""
            <div class="pauta-card">
                <div class="pauta-label">Nuevos Seguidores</div>
                <div class="pauta-value">{format_number(total_nuevos_seguidores)}</div>
                <div class="pauta-period">Generados</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabla de pauta
        st.markdown("#### 📋 Detalle de Campañas")
        st.dataframe(df_pauta, use_container_width=True)

    else:
        st.warning("No hay datos de pauta publicitaria disponibles.")

    st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# EXPORTACIÓN (SI ESTÁ ACTIVADA)
# ================================================================
if st.session_state.get("show_export", False):
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.subheader("📤 Exportar Datos")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.markdown("#### 📊 Exportar Datos Principales")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name=f"datos_{selected_platform}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_exp2:
        st.markdown("#### 📈 Exportar Reporte Completo")
        st.info("Funcionalidad en desarrollo...")

    if st.button("❌ Cerrar Exportación"):
        st.session_state.show_export = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
