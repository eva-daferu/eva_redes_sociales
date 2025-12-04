import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# CONEXIÓN A BACKEND REAL (NO TOCAR)
#############################################
BACKEND_URL = "http://pahubisas.pythonanywhere.com/data"

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
                   "me_gusta", "comentarios_num"]
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

        # Asegurar que 'red' esté en minúsculas y limpia
        if "red" in df.columns:
            df["red"] = df["red"].astype(str).str.lower().str.strip()

        # Tipo fijo si no existe
        if "tipo" not in df.columns:
            df["tipo"] = "general"

        return df

    except Exception as e:
        st.error(f"Error al conectar con el backend: {str(e)}")
        return pd.DataFrame()

#############################################
# FIN CONEXIÓN BACKEND REAL
#############################################

# Función para cargar datos con caché
@st.cache_data(ttl=300)  # 5 minutos de caché
def cargar_datos():
    """Carga datos desde el backend y separa por plataforma"""
    df = cargar_datos_backend()
    
    if df.empty:
        # Datos de respaldo si falla el backend
        st.warning("Usando datos de respaldo. El backend no está disponible.")
        
        # Datos de ejemplo (simplificados para respaldo)
        youtobe_data = pd.DataFrame({
            'titulo': ['Amazonía al borde', 'El costo oculto de botar comida'],
            'fecha_publicacion': ['01/10/2025', '23/09/2025'],
            'visualizaciones': [18, 22],
            'me_gusta': [0, 0],
            'comentarios': [0, 0],
            'red': ['youtobe', 'youtobe']  # CORREGIDO: 'youtobe' en lugar de 'youtube'
        })
        
        tiktok_data = pd.DataFrame({
            'titulo': ['Especie única en Colombia', 'Una peli que te volará la mente'],
            'fecha_publicacion': ['03/12/2025', '28/11/2025'],
            'visualizaciones': [127, 5669],
            'me_gusta': [19, 211],
            'comentarios': [2, 5],
            'red': ['tiktok', 'tiktok']
        })
        
        youtobe_data['fecha_publicacion'] = pd.to_datetime(youtobe_data['fecha_publicacion'], dayfirst=True)
        tiktok_data['fecha_publicacion'] = pd.to_datetime(tiktok_data['fecha_publicacion'], dayfirst=True)
        
    else:
        # DEBUG: Mostrar valores únicos en 'red'
        if "red" in df.columns:
            unique_reds = df["red"].unique()
            st.sidebar.info(f"Valores en 'red': {list(unique_reds)[:10]}")
        
        # CORREGIDO: Separar por plataforma usando valores exactos
        # Para YouTube buscar 'youtobe' (con 'o' en lugar de 'u')
        youtobe_mask = (df['red'] == 'youtobe') | (df['red'] == 'youtube')  # Ambos casos
        youtobe_data = df[youtobe_mask].copy()
        
        # Para TikTok buscar 'tiktok'
        tiktok_mask = df['red'] == 'tiktok'
        tiktok_data = df[tiktok_mask].copy()
        
        # Si no hay datos específicos, mostrar mensaje
        if youtobe_data.empty:
            st.sidebar.warning("No se encontraron datos para YouTube/Youtobe")
        if tiktok_data.empty:
            st.sidebar.warning("No se encontraron datos para TikTok")
        
        # Mostrar conteos en sidebar
        st.sidebar.success(f"YouTube: {len(youtobe_data)} posts | TikTok: {len(tiktok_data)} posts")
    
    # Calcular métricas comunes para ambos datasets
    for df_data in [youtobe_data, tiktok_data]:
        if not df_data.empty and 'fecha_publicacion' in df_data.columns:
            hoy = pd.Timestamp.now()
            df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
            df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
            df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
    
    return youtobe_data, tiktok_data

# Estilos CSS mejorados - Agregando efectos visuales
st.markdown("""
<style>
/* Main container */
.main { padding: 0; }

/* Sidebar styling - AZUL PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.2);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Social media buttons - MEJORADO con efecto de selección */
.stButton > button {
    display: flex;
    align-items: center;
    padding: 14px 20px;
    margin: 8px 0;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
    text-align: left;
    justify-content: flex-start;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateX(8px) scale(1.02);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.stButton > button[kind="primary"] {
    background: rgba(59, 130, 246, 0.25) !important;
    border-color: #3B82F6 !important;
    color: #60a5fa !important;
    box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3), 0 4px 12px rgba(59, 130, 246, 0.2);
}

.stButton > button[kind="primary"]::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 4px;
    background: #3B82F6;
    border-radius: 2px;
}

/* Efecto de pulso para botón activo */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
    70% { box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

.stButton > button[kind="primary"] {
    animation: pulse 2s infinite;
}

/* Metrics cards - MEJORADAS con efectos */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 18px;
    padding: 28px 22px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
    height: 5px;
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
    border-radius: 18px 18px 0 0;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    border-color: #d1d5db;
}

.metric-card:hover::before {
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
}

.metric-value {
    font-size: 40px;
    font-weight: 800;
    color: #1f2937;
    margin: 18px 0 8px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.metric-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-trend {
    font-size: 14px;
    display: flex;
    align-items: center;
    margin-top: 10px;
    font-weight: 500;
    gap: 6px;
}

.trend-up { 
    color: #10b981;
    text-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}
.trend-down { 
    color: #ef4444;
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
}

/* Header principal con efectos */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 22px;
    padding: 40px;
    color: white;
    margin-bottom: 35px;
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
    position: relative;
    overflow: hidden;
    animation: headerFloat 6s ease-in-out infinite;
}

@keyframes headerFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.1;
    animation: backgroundMove 20s linear infinite;
}

@keyframes backgroundMove {
    0% { transform: translateX(0) translateY(0); }
    100% { transform: translateX(-20px) translateY(-20px); }
}

.dashboard-header::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Tabs mejorados con efectos */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    padding: 8px;
    border-radius: 14px;
    border: 1px solid #cbd5e1;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 14px 24px;
    background: transparent;
    color: #64748b;
    font-weight: 500;
    transition: all 0.3s;
    border: 1px solid transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.7);
    color: #475569;
    border-color: #cbd5e1;
}

.stTabs [aria-selected="true"] {
    background: white;
    color: #3B82F6;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    font-weight: 600;
    border-color: #3B82F6;
    transform: scale(1.05);
}

/* Chart containers con efectos */
.performance-chart {
    background: white;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.1);
    margin: 25px 0;
    border: 1px solid #e5e7eb;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.performance-chart:hover {
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15);
    border-color: #d1d5db;
}

.performance-chart::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899);
    border-radius: 20px 20px 0 0;
}

.data-table-container {
    background: white;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.1);
    margin: 25px 0;
    border: 1px solid #e5e7eb;
    transition: all 0.3s;
}

.data-table-container:hover {
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15);
    border-color: #d1d5db;
}

/* Platform-specific colors con efectos */
.youtube-color { 
    color: #FF0000;
    text-shadow: 0 0 15px rgba(255, 0, 0, 0.2);
}
.tiktok-color { 
    color: #000000;
    text-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}
.facebook-color { 
    color: #1877F2;
    text-shadow: 0 0 15px rgba(24, 119, 242, 0.2);
}
.twitter-color { 
    color: #1DA1F2;
    text-shadow: 0 0 15px rgba(29, 161, 242, 0.2);
}
.instagram-color { 
    color: #E4405F;
    text-shadow: 0 0 15px rgba(228, 64, 95, 0.2);
}
.linkedin-color { 
    color: #0A66C2;
    text-shadow: 0 0 15px rgba(10, 102, 194, 0.2);
}

/* Status indicators con efectos */
.status-connected {
    color: #10b981;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}

.status-disconnected {
    color: #ef4444;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
}

.status-warning {
    color: #f59e0b;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
}

/* Sidebar titles con efectos */
.sidebar-title {
    color: #cbd5e1 !important;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 15px;
    margin-top: 30px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    position: relative;
    padding-left: 15px;
}

.sidebar-title::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 16px;
    background: #3B82F6;
    border-radius: 2px;
}

/* Status containers con efectos */
.status-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s;
    backdrop-filter: blur(10px);
}

.status-container:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Custom table con efectos */
.dataframe {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
}

.dataframe th {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    padding: 16px 20px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
    backdrop-filter: blur(10px);
}

.dataframe td {
    padding: 14px 20px;
    border-bottom: 1px solid #e5e7eb;
    color: #4b5563;
    transition: all 0.2s;
}

.dataframe tr:hover {
    background: linear-gradient(90deg, #f9fafb 0%, #f3f4f6 100%);
    transform: scale(1.01);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.dataframe tr:last-child td {
    border-bottom: none;
}

/* Badges con efectos */
.platform-badge {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 24px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
    transition: all 0.3s;
    cursor: pointer;
}

.platform-badge:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Loader con efectos */
.loader {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3B82F6;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

@keyframes spin {
    0% { transform: rotate(0deg); box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
    50% { box-shadow: 0 0 30px rgba(59, 130, 246, 0.6); }
    100% { transform: rotate(360deg); box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
}

/* Backend status con efectos */
.backend-status {
    padding: 12px 18px;
    border-radius: 12px;
    margin: 18px 0;
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
    border: 1px solid transparent;
}

.backend-status:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.backend-connected {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
    color: #10b981;
    border-color: rgba(16, 185, 129, 0.3);
    animation: pulseGreen 2s infinite;
}

@keyframes pulseGreen {
    0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
}

.backend-disconnected {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
    color: #ef4444;
    border-color: rgba(239, 68, 68, 0.3);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .metric-value { font-size: 32px; }
    .dashboard-header { padding: 30px; }
    .metric-card { padding: 20px 15px; }
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
youtobe_df, tiktok_df = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 35px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 70px; height: 70px; border-radius: 18px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 20px auto; font-size: 32px;
                    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
                    animation: logoFloat 3s ease-in-out infinite;">
            📊
        </div>
        <style>
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-5px) rotate(2deg); }
        }
        </style>
        <h2 style="color: white; margin-bottom: 5px; font-size: 24px; font-weight: 700;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 14px; margin: 0; font-weight: 400;">Social Media Analytics v3.1</p>
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
    
    st.markdown('<p class="sidebar-title">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
    # Botones de plataformas
    platforms = {
        "facebook": ("📘 Facebook", "#1877F2"),
        "twitter": ("🐦 Twitter", "#1DA1F2"),
        "instagram": ("📷 Instagram", "#E4405F"),
        "linkedin": ("💼 LinkedIn", "#0A66C2"),
        "youtube": ("▶️ YouTube", "#FF0000"),
        "tiktok": ("🎵 TikTok", "#000000")
    }
    
    selected_platform = st.session_state.get("selected_platform", "youtube")
    
    # Mostrar estado de datos en tiempo real
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8; font-size: 13px;">YouTube:</span>
            <span style="color: #10b981; font-weight: 600;">{len(youtobe_df)} posts</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8; font-size: 13px;">TikTok:</span>
            <span style="color: #10b981; font-weight: 600;">{len(tiktok_df)} posts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for platform_key, (platform_name, platform_color) in platforms.items():
        button_type = "primary" if selected_platform == platform_key else "secondary"
        
        if st.button(platform_name, key=f"{platform_key}_btn", use_container_width=True, type=button_type):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
            st.rerun()
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">📈 Status Conexiones</p>', unsafe_allow_html=True)
    
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
                <span style="color: #e2e8f0; font-size: 14px;">{platform}</span>
                <span class="{status_class}" style="font-size: 13px;">{icon} {status.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal
st.markdown(f"""
<div class="dashboard-header">
    <h1 style="margin: 0; font-size: 42px; font-weight: 900; letter-spacing: -0.5px;">📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 12px 0 0 0; opacity: 0.95; font-size: 17px; font-weight: 400; max-width: 800px;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
    <div style="position: absolute; bottom: 25px; right: 35px; font-size: 14px; opacity: 0.9; background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; backdrop-filter: blur(10px);">
        ⏰ Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
</div>
""", unsafe_allow_html=True)

# Determinar datos según plataforma seleccionada
platform_config = {
    "youtube": ("YouTube", "#FF0000", "▶️", youtobe_df),
    "tiktok": ("TikTok", "#000000", "🎵", tiktok_df),
    "facebook": ("Facebook", "#1877F2", "📘", youtobe_df),
    "twitter": ("Twitter", "#1DA1F2", "🐦", youtobe_df),
    "instagram": ("Instagram", "#E4405F", "📷", youtobe_df),
    "linkedin": ("LinkedIn", "#0A66C2", "💼", youtobe_df)
}

platform_name, platform_color, platform_icon, df = platform_config.get(
    selected_platform, 
    ("YouTube", "#FF0000", "▶️", youtobe_df)
)

# Verificar si hay datos
if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    
    # Mostrar información de debug
    with st.expander("🔍 Información de Depuración", expanded=False):
        st.write(f"**Plataforma seleccionada:** {selected_platform}")
        st.write(f"**Total registros YouTube/Youtobe:** {len(youtobe_df)}")
        st.write(f"**Total registros TikTok:** {len(tiktok_df)}")
        
        if not youtobe_df.empty:
            st.write("**Primeras filas YouTube:**")
            st.dataframe(youtobe_df.head())
            
        if not tiktok_df.empty:
            st.write("**Primeras filas TikTok:**")
            st.dataframe(tiktok_df.head())
    
    st.info("Conectando al backend para cargar datos en tiempo real...")
    st.stop()

st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 35px; padding: 20px; background: rgba({platform_color.replace('#', '')}, 0.05); border-radius: 18px; border-left: 6px solid {platform_color};">
    <div style="font-size: 42px; margin-right: 20px; color: {platform_color}; animation: iconBounce 2s infinite;">
        {platform_icon}
    </div>
    <div style="flex: 1;">
        <h2 style="margin: 0; color: {platform_color}; font-size: 32px; font-weight: 800;">{platform_name} ANALYTICS</h2>
        <p style="margin: 8px 0 0 0; color: #6b7280; font-size: 15px; display: flex; align-items: center; gap: 10px;">
            <span>📊 {len(df)} contenidos analizados</span>
            <span>•</span>
            <span>🕐 Última actualización: {datetime.now().strftime('%H:%M:%S')}</span>
        </p>
    </div>
    <div style="margin-left: auto; display: flex; gap: 15px; align-items: center;">
        <div style="background: {platform_color}20; color: {platform_color}; padding: 10px 24px; border-radius: 24px; font-size: 15px; font-weight: 700; border: 2px solid {platform_color}40;">
            {len(df)} {platform_name} Posts
        </div>
    </div>
</div>

<style>
@keyframes iconBounce {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-5px) scale(1.1); }
}
</style>
""", unsafe_allow_html=True)

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_videos = len(df)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="display: flex; align-items: center; gap: 8px;">
            <span>📁</span> TOTAL CONTENIDOS
        </div>
        <div class="metric-value">{total_videos}</div>
        <div class="metric-trend trend-up">
            <span>📈 Contenido Activo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_views = df['visualizaciones'].sum() if 'visualizaciones' in df.columns else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="display: flex; align-items: center; gap: 8px;">
            <span>👁️</span> VISUALIZACIONES TOTALES
        </div>
        <div class="metric-value">{total_views:,}</div>
        <div class="metric-trend trend-up">
            <span>🎯 Alcance Total</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if 'rendimiento_por_dia' in df.columns:
        avg_daily_perf = df['rendimiento_por_dia'].mean()
    else:
        avg_daily_perf = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="display: flex; align-items: center; gap: 8px;">
            <span>🚀</span> RENDIMIENTO DIARIO
        </div>
        <div class="metric-value">{avg_daily_perf:.1f}</div>
        <div class="metric-trend trend-up">
            <span>📊 Views/Día Promedio</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if 'visualizaciones' in df.columns and total_views > 0:
        total_engagement = (df['me_gusta'].sum() if 'me_gusta' in df.columns else 0) + \
                          (df['comentarios'].sum() if 'comentarios' in df.columns else 0)
        engagement_rate = (total_engagement / total_views * 100)
    else:
        engagement_rate = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="display: flex; align-items: center; gap: 8px;">
            <span>💬</span> TASA DE ENGAGEMENT
        </div>
        <div class="metric-value">{engagement_rate:.2f}%</div>
        <div class="metric-trend trend-up">
            <span>❤️ Interacción del Público</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Gráfica de performance
st.markdown("""
<div class="performance-chart">
    <h3 style="margin-top: 0; margin-bottom: 25px; color: #1f2937; font-size: 22px; display: flex; align-items: center; gap: 10px;">
        <span style="background: linear-gradient(90deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📈</span> 
        PERFORMANCE OVER TIME
    </h3>
""", unsafe_allow_html=True)

try:
    # Preparar datos para la gráfica
    if 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
        df_sorted = df.sort_values('fecha_publicacion')
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '📊 Evolución de Visualizaciones',
                '🎯 Distribución por Rendimiento',
                '💬 Métricas de Engagement',
                '📅 Tendencia Semanal'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'pie'}],
                [{'type': 'bar'}, {'type': 'scatter'}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Evolución de visualizaciones
        fig.add_trace(
            go.Scatter(
                x=df_sorted['fecha_publicacion'],
                y=df_sorted['visualizaciones'],
                mode='lines+markers',
                name='Visualizaciones',
                line=dict(color=platform_color, width=4, shape='spline'),
                marker=dict(size=8, color=platform_color, line=dict(width=2, color='white')),
                hovertemplate='<b>📅 %{x|%d/%m}</b><br>👁️ Views: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor=f'{platform_color}20'
            ),
            row=1, col=1
        )
        
        # 2. Distribución por rendimiento
        if 'rendimiento_por_dia' in df.columns:
            categories = pd.qcut(df['rendimiento_por_dia'], q=4, 
                                labels=['🔴 Bajo', '🟡 Medio-Bajo', '🔵 Medio-Alto', '🟢 Alto'])
            category_counts = categories.value_counts()
            
            fig.add_trace(
                go.Pie(
                    labels=category_counts.index,
                    values=category_counts.values,
                    hole=0.5,
                    marker=dict(colors=['#ef4444', '#f59e0b', '#3B82F6', '#10b981']),
                    name='Rendimiento',
                    hovertemplate='<b>%{label}</b><br>📊 %{value} posts<br>📈 %{percent}<extra></extra>',
                    textinfo='label+percent',
                    textposition='outside'
                ),
                row=1, col=2
            )
        
        # 3. Métricas de engagement
        engagement_data = []
        engagement_labels = []
        
        if 'me_gusta' in df.columns:
            engagement_data.append(df['me_gusta'].sum())
            engagement_labels.append('👍 Likes')
        
        if 'comentarios' in df.columns:
            engagement_data.append(df['comentarios'].sum())
            engagement_labels.append('💬 Comments')
        
        if engagement_data:
            fig.add_trace(
                go.Bar(
                    x=engagement_labels,
                    y=engagement_data,
                    marker_color=[platform_color, '#8b5cf6'],
                    name='Engagement',
                    hovertemplate='<b>%{x}</b><br>📊 Total: %{y:,}<extra></extra>',
                    text=engagement_data,
                    textposition='auto',
                    texttemplate='%{y:,}'
                ),
                row=2, col=1
            )
        
        # 4. Tendencia semanal
        if 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
            df['semana'] = df['fecha_publicacion'].dt.isocalendar().week
            weekly_views = df.groupby('semana')['visualizaciones'].sum().reset_index()
            
            fig.add_trace(
                go.Scatter(
                    x=weekly_views['semana'],
                    y=weekly_views['visualizaciones'],
                    mode='lines+markers',
                    name='Views Semanales',
                    line=dict(color='#10b981', width=3, shape='spline'),
                    marker=dict(size=10, color='#10b981', symbol='diamond'),
                    hovertemplate='<b>📅 Semana %{x}</b><br>👁️ Views: %{y:,}<extra></extra>',
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.2)'
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
            title_font=dict(size=16, family='Arial', color='#1f2937'),
            font=dict(size=13, family='Arial'),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial"
            )
        )
        
        # Actualizar ejes
        fig.update_xaxes(
            title_text="📅 Fecha", 
            row=1, col=1,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        fig.update_yaxes(
            title_text="👁️ Visualizaciones", 
            row=1, col=1,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        
        fig.update_xaxes(
            title_text="📊 Métrica", 
            row=2, col=1,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        fig.update_yaxes(
            title_text="📈 Cantidad", 
            row=2, col=1,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        
        fig.update_xaxes(
            title_text="📅 Semana", 
            row=2, col=2,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        fig.update_yaxes(
            title_text="👁️ Visualizaciones", 
            row=2, col=2,
            gridcolor='#f3f4f6',
            showline=True,
            linecolor='#e5e7eb'
        )
        
        # Añadir título general
        fig.update_layout(
            title={
                'text': f"📊 {platform_name} Analytics Dashboard",
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, color=platform_color)
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
except Exception as e:
    st.warning(f"⚠️ Error al generar gráficas: {str(e)}")
    st.info("Mostrando vista simplificada...")

st.markdown("</div>", unsafe_allow_html=True)

# Tabla de contenidos
st.markdown("""
<div class="data-table-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div>
            <h3 style="margin: 0; color: #1f2937; font-size: 22px; display: flex; align-items: center; gap: 10px;">
                <span style="background: linear-gradient(90deg, #10b981, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📊</span> 
                CONTENT PERFORMANCE DATA
            </h3>
            <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 14px;">
                Top 10 contenidos por visualizaciones
            </p>
        </div>
        <div style="color: #6b7280; font-size: 13px; background: #f8fafc; padding: 8px 16px; border-radius: 20px; border: 1px solid #e5e7eb;">
            Ordenado por 👁️ Views
        </div>
    </div>
""", unsafe_allow_html=True)

if selected_platform in ["youtube", "tiktok"] and not df.empty:
    # Seleccionar top 10 videos
    top_videos = df.nlargest(10, 'visualizaciones').copy()
    
    # Preparar columnas para mostrar
    display_columns = {}
    
    if 'titulo' in top_videos.columns:
        display_columns['📝 Título'] = top_videos['titulo'].str[:50] + '...'
    
    if 'fecha_publicacion' in top_videos.columns:
        display_columns['📅 Fecha'] = top_videos['fecha_publicacion'].dt.strftime('%d/%m/%Y')
    
    if 'visualizaciones' in top_videos.columns:
        display_columns['👁️ Views'] = top_videos['visualizaciones']
    
    if 'me_gusta' in top_videos.columns:
        display_columns['👍 Likes'] = top_videos['me_gusta']
    
    if 'comentarios' in top_videos.columns:
        display_columns['💬 Comments'] = top_videos['comentarios']
    
    if 'rendimiento_por_dia' in top_videos.columns:
        display_columns['🚀 Rend/Día'] = top_videos['rendimiento_por_dia']
    
    if 'dias_desde_publicacion' in top_videos.columns:
        display_columns['📅 Días'] = top_videos['dias_desde_publicacion']
    
    # Crear DataFrame para mostrar
    display_df = pd.DataFrame(display_columns)
    
    # Formatear números
    if '👁️ Views' in display_df.columns:
        display_df['👁️ Views'] = display_df['👁️ Views'].apply(lambda x: f"{int(x):,}")
    
    if '🚀 Rend/Día' in display_df.columns:
        display_df['🚀 Rend/Día'] = display_df['🚀 Rend/Día'].apply(lambda x: f"{float(x):.1f}")
    
    # Mostrar tabla con estilos
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "👁️ Views": st.column_config.NumberColumn(format="%d"),
            "👍 Likes": st.column_config.NumberColumn(format="%d"),
            "💬 Comments": st.column_config.NumberColumn(format="%d"),
            "🚀 Rend/Día": st.column_config.NumberColumn(format="%.1f")
        }
    )
    
    # Top performing video
    if not top_videos.empty:
        top_video = top_videos.iloc[0]
        
        # Calcular porcentaje de engagement
        engagement_pct = 0
        if 'visualizaciones' in top_video and top_video['visualizaciones'] > 0:
            total_interactions = (top_video.get('me_gusta', 0) + top_video.get('comentarios', 0))
            engagement_pct = (total_interactions / top_video['visualizaciones']) * 100
        
        st.markdown(f"""
        <div style="margin-top: 25px; padding: 25px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                    border-radius: 16px; border-left: 6px solid {platform_color};
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);">
            <div style="display: flex; align-items: flex-start; gap: 20px;">
                <div style="font-size: 32px; color: {platform_color}; animation: trophySpin 3s ease-in-out infinite;">
                    🏆
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 18px; display: flex; align-items: center; gap: 8px;">
                        <span>🌟</span> Top Performing Content:
                    </h4>
                    <p style="margin: 0 0 10px 0; color: #4b5563; font-size: 16px; line-height: 1.5;">
                        <strong>{str(top_video.get('titulo', 'Sin título'))[:120]}{'...' if len(str(top_video.get('titulo', ''))) > 120 else ''}</strong>
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px;">
                        <div style="background: white; padding: 12px; border-radius: 10px; border: 1px solid #e5e7eb; text-align: center;">
                            <div style="color: #6b7280; font-size: 12px; margin-bottom: 4px;">👁️ Views</div>
                            <div style="color: #1f2937; font-size: 18px; font-weight: 700;">{top_video.get('visualizaciones', 0):,}</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 10px; border: 1px solid #e5e7eb; text-align: center;">
                            <div style="color: #6b7280; font-size: 12px; margin-bottom: 4px;">👍 Likes</div>
                            <div style="color: #1f2937; font-size: 18px; font-weight: 700;">{top_video.get('me_gusta', 0):,}</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 10px; border: 1px solid #e5e7eb; text-align: center;">
                            <div style="color: #6b7280; font-size: 12px; margin-bottom: 4px;">💬 Comments</div>
                            <div style="color: #1f2937; font-size: 18px; font-weight: 700;">{top_video.get('comentarios', 0):,}</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 10px; border: 1px solid #e5e7eb; text-align: center;">
                            <div style="color: #6b7280; font-size: 12px; margin-bottom: 4px;">🚀 Perf/Día</div>
                            <div style="color: #1f2937; font-size: 18px; font-weight: 700;">{top_video.get('rendimiento_por_dia', 0):.1f}</div>
                        </div>
                    </div>
                    <div style="margin-top: 15px; padding: 10px 15px; background: linear-gradient(90deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1)); border-radius: 10px; border-left: 4px solid #10b981;">
                        <div style="color: #374151; font-size: 13px; display: flex; justify-content: space-between;">
                            <span>📊 Engagement Rate:</span>
                            <span style="font-weight: 700; color: #10b981;">{engagement_pct:.2f}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes trophySpin {
            0% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(5deg) scale(1.1); }
            100% { transform: rotate(0deg) scale(1); }
        }
        </style>
        """, unsafe_allow_html=True)

else:
    st.info(f"🔒 {platform_name} analytics require platform connection or no data available")

st.markdown("</div>", unsafe_allow_html=True)

# Análisis avanzado
col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <h3 style="margin-top: 0; margin-bottom: 20px; color: #1f2937; font-size: 20px; display: flex; align-items: center; gap: 8px;">
            <span style="background: linear-gradient(90deg, #EC4899, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📊</span>
            PERFORMANCE ANALYTICS
        </h3>
    """, unsafe_allow_html=True)
    
    if selected_platform in ["youtube", "tiktok"] and not df.empty and 'rendimiento_por_dia' in df.columns:
        # Categorizar performance
        q75 = df['rendimiento_por_dia'].quantile(0.75)
        q25 = df['rendimiento_por_dia'].quantile(0.25)
        
        high_perf = len(df[df['rendimiento_por_dia'] > q75])
        medium_perf = len(df[(df['rendimiento_por_dia'] >= q25) & (df['rendimiento_por_dia'] <= q75)])
        low_perf = len(df[df['rendimiento_por_dia'] < q25])
        
        # Gráfico de barras para performance
        perf_data = pd.DataFrame({
            'Categoría': ['🟢 Alto Rendimiento', '🔵 Rendimiento Medio', '🔴 Bajo Rendimiento'],
            'Cantidad': [high_perf, medium_perf, low_perf],
            'Color': ['#10b981', '#3B82F6', '#6b7280']
        })
        
        fig_perf = go.Figure(data=[
            go.Bar(
                x=perf_data['Categoría'],
                y=perf_data['Cantidad'],
                marker_color=perf_data['Color'],
                text=perf_data['Cantidad'],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>📊 Posts: %{y}<extra></extra>',
                marker=dict(
                    line=dict(width=2, color='white')
                )
            )
        ])
        
        fig_perf.update_layout(
            height=350,
            showlegend=False,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title="🎯 Categoría de Rendimiento",
            yaxis_title="📊 Número de Posts",
            xaxis=dict(
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb'
            ),
            yaxis=dict(
                gridcolor='#f3f4f6',
                showline=True,
                linecolor='#e5e7eb'
            )
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
        
        # Insights
        total_posts = len(df)
        high_perf_pct = (high_perf / total_posts * 100) if total_posts > 0 else 0
        
        st.markdown(f"""
        <div style="margin-top: 20px; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                    border-radius: 12px; border-left: 4px solid #8B5CF6; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
            <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 16px; display: flex; align-items: center; gap: 8px;">
                <span>📈</span> Insights de Performance:
            </h4>
            <div style="color: #4b5563; font-size: 14px; line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>🟢 Alto rendimiento:</span>
                    <span style="font-weight: 700; color: #10b981;">{high_perf_pct:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>📊 Rendimiento promedio:</span>
                    <span style="font-weight: 700; color: #3B82F6;">{df['rendimiento_por_dia'].mean():.1f} views/día</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>🚀 Mejor post:</span>
                    <span style="font-weight: 700; color: #EC4899;">{df['rendimiento_por_dia'].max():.1f} views/día</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>🔴 Posts con bajo rendimiento:</span>
                    <span style="font-weight: 700; color: #ef4444;">{low_perf}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("📊 Performance data requires platform connection")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_analysis2:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <h3 style="margin-top: 0; margin-bottom: 20px; color: #1f2937; font-size: 20px; display: flex; align-items: center; gap: 8px;">
            <span style="background: linear-gradient(90deg, #F59E0B, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📈</span>
            KEY METRICS
        </h3>
    """, unsafe_allow_html=True)
    
    if selected_platform in ["youtube", "tiktok"] and not df.empty:
        # Calcular métricas clave
        metrics = []
        metric_icons = ['📊', '🚀', '📈', '👍', '📊', '💬', '📊', '🚀', '📅', '📅', '💬']
        
        if 'visualizaciones' in df.columns:
            metrics.append(('📊 Avg. Views/Post', f"{df['visualizaciones'].mean():.0f}"))
            metrics.append(('🚀 Max Views', f"{df['visualizaciones'].max():,}"))
            metrics.append(('📈 Total Views', f"{df['visualizaciones'].sum():,}"))
        
        if 'me_gusta' in df.columns:
            metrics.append(('👍 Avg. Likes/Post', f"{df['me_gusta'].mean():.1f}"))
            metrics.append(('📊 Total Likes', f"{df['me_gusta'].sum():,}"))
        
        if 'comentarios' in df.columns:
            metrics.append(('💬 Avg. Comments/Post', f"{df['comentarios'].mean():.1f}"))
            metrics.append(('📊 Total Comments', f"{df['comentarios'].sum():,}"))
        
        if 'rendimiento_por_dia' in df.columns:
            metrics.append(('🚀 Avg. Daily Perf.', f"{df['rendimiento_por_dia'].mean():.1f}"))
            metrics.append(('📈 Max Daily Perf.', f"{df['rendimiento_por_dia'].max():.1f}"))
        
        if 'dias_desde_publicacion' in df.columns:
            metrics.append(('📅 Avg. Content Age', f"{df['dias_desde_publicacion'].mean():.0f} días"))
            metrics.append(('📅 Oldest Post', f"{df['dias_desde_publicacion'].max()} días"))
        
        metrics.append(('💬 Engagement Rate', f"{engagement_rate:.2f}%"))
        
        # Mostrar métricas en una tabla estilizada
        for i, (metric, value) in enumerate(metrics):
            bg_color = "#ffffff" if i % 2 == 0 else "#f8fafc"
            icon_color = platform_color if i % 3 == 0 else "#6b7280" if i % 3 == 1 else "#10b981"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 16px 18px; background: {bg_color}; 
                        border-radius: 10px; margin: 6px 0; transition: all 0.3s;
                        border: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 18px; color: {icon_color};">{metric.split(' ')[0]}</span>
                    <span style="color: #4b5563; font-size: 14px; font-weight: 500;">{metric.split(' ', 1)[1]}</span>
                </div>
                <span style="font-weight: 700; color: #1f2937; font-size: 16px; background: linear-gradient(90deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {value}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Resumen de engagement
        if 'visualizaciones' in df.columns and total_views > 0:
            like_rate = (df['me_gusta'].sum() / total_views * 100) if 'me_gusta' in df.columns else 0
            comment_rate = (df['comentarios'].sum() / total_views * 100) if 'comentarios' in df.columns else 0
            
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 20px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                        border-radius: 12px; border-left: 4px solid #0ea5e9; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">
                <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 16px; display: flex; align-items: center; gap: 8px;">
                    <span>💬</span> Engagement Analysis:
                </h4>
                <div style="color: #4b5563; font-size: 14px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>👍 Tasa de Likes:</span>
                        <span style="font-weight: 700; color: #10b981;">{like_rate:.2f}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>💬 Tasa de Comentarios:</span>
                        <span style="font-weight: 700; color: #3B82F6;">{comment_rate:.2f}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>📊 Total Engagement:</span>
                        <span style="font-weight: 700; color: #8B5CF6;">{(like_rate + comment_rate):.2f}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>⚖️ Ratio Likes/Comments:</span>
                        <span style="font-weight: 700; color: #EC4899;">{(df['me_gusta'].sum()/max(df['comentarios'].sum(), 1)):.1f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("📈 Connect to view platform metrics")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer mejorado
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 13px; padding: 35px; 
            border-top: 1px solid #e5e7eb; margin-top: 40px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 0 0 20px 20px;">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; flex-wrap: wrap;">
        <span style="display: flex; align-items: center; gap: 6px;">📊 Social Media Dashboard PRO v3.1</span>
        <span style="color: #cbd5e1;">•</span>
        <span style="display: flex; align-items: center; gap: 6px;">🔗 Backend: {BACKEND_URL}</span>
        <span style="color: #cbd5e1;">•</span>
        <span style="display: flex; align-items: center; gap: 6px;">🎯 {platform_name} Analytics</span>
        <span style="color: #cbd5e1;">•</span>
        <span style="display: flex; align-items: center; gap: 6px;">⚡ Updated in Real-time</span>
    </div>
    <div style="font-size: 12px; color: #9ca3af; margin-top: 10px; display: flex; justify-content: center; align-items: center; gap: 15px;">
        <span>© 2025 Social Media Analytics Platform</span>
        <span style="width: 4px; height: 4px; background: #cbd5e1; border-radius: 50%;"></span>
        <span>📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span>
        <span style="width: 4px; height: 4px; background: #cbd5e1; border-radius: 50%;"></span>
        <span style="color: {platform_color}; font-weight: 600;">{platform_name}: {len(df)} posts</span>
    </div>
</div>
""", unsafe_allow_html=True)
