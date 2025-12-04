import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import json

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
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"

def cargar_datos_backend():
    try:
        st.info("Conectando al backend...")
        r = requests.get(BACKEND_URL, timeout=30)
        r.raise_for_status()
        data = r.json()
        
        # Debug: mostrar estructura de datos
        st.sidebar.write(f"Datos recibidos: {len(data.get('data', []))} registros")
        
        # Data principal
        df = pd.DataFrame(data.get("data", []))
        
        if df.empty:
            st.warning("El backend devolvió un DataFrame vacío")
            return df
        
        # Debug: mostrar columnas disponibles
        st.sidebar.write(f"Columnas disponibles: {list(df.columns)}")
        
        # Normalización básica
        if "fecha_publicacion" in df.columns:
            df["fecha_publicacion"] = pd.to_datetime(
                df["fecha_publicacion"],
                dayfirst=True,
                errors="coerce"
            )
        
        # Convertir números
        num_cols = ["vistas", "comentarios", "me_gusta_numero", "visualizaciones", 
                   "me_gusta", "comentarios_num", "visualizaciones_num"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Asegurar columnas estándar
        if "visualizaciones" not in df.columns:
            if "vistas" in df.columns:
                df["visualizaciones"] = df["vistas"]
            elif "visualizaciones_num" in df.columns:
                df["visualizaciones"] = df["visualizaciones_num"]
            else:
                df["visualizaciones"] = 0
        
        if "me_gusta" not in df.columns and "me_gusta_numero" in df.columns:
            df["me_gusta"] = df["me_gusta_numero"]
        elif "me_gusta" not in df.columns:
            df["me_gusta"] = 0
        
        if "comentarios" not in df.columns:
            if "comentarios_num" in df.columns:
                df["comentarios"] = df["comentarios_num"]
            else:
                df["comentarios"] = 0
        
        # Asegurar columna 'red' existe y está en minúsculas
        if "red" not in df.columns:
            df["red"] = "desconocido"
        else:
            # Convertir a minúsculas y limpiar espacios
            df["red"] = df["red"].astype(str).str.lower().str.strip()
        
        # Asegurar columna 'titulo'
        if "titulo" not in df.columns:
            df["titulo"] = "Sin título"
        
        # Filtros calculados
        if "fecha_publicacion" in df.columns:
            hoy = pd.Timestamp.now()
            df["dias"] = (hoy - df["fecha_publicacion"]).dt.days.fillna(0).astype(int)
            df["dias_desde_publicacion"] = df["dias"].apply(lambda x: max(x, 1))
            df["rendimiento_por_dia"] = df["visualizaciones"] / df["dias_desde_publicacion"]
            df["semana"] = df["fecha_publicacion"].dt.isocalendar().week.fillna(0).astype(int)
            df["meses"] = df["fecha_publicacion"].dt.month.fillna(0).astype(int)
        
        # Debug: mostrar valores únicos de 'red'
        unique_reds = df["red"].unique()[:10]  # Mostrar primeros 10
        st.sidebar.write(f"Valores únicos en 'red': {list(unique_reds)}")
        
        # Contar por plataforma
        platform_counts = df["red"].value_counts()
        st.sidebar.write("Conteo por plataforma:")
        for platform, count in platform_counts.items():
            st.sidebar.write(f"  {platform}: {count}")
        
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
        
        # Datos de ejemplo
        youtobe_data = pd.DataFrame({
            'titulo': ['Amazonía al borde', 'El costo oculto de botar comida'],
            'fecha_publicacion': ['01/10/2025', '23/09/2025'],
            'visualizaciones': [18, 22],
            'me_gusta': [0, 0],
            'comentarios': [0, 0],
            'red': ['youtobe', 'youtobe']
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
        
        # Calcular métricas
        for df_data in [youtobe_data, tiktok_data]:
            hoy = pd.Timestamp.now()
            df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
            df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
            df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
        
        return youtobe_data, tiktok_data
    
    else:
        # DEBUG: Mostrar información del DataFrame
        st.sidebar.write(f"Total registros: {len(df)}")
        st.sidebar.write(f"Columnas: {list(df.columns)}")
        
        # Filtrar datos por plataforma usando comparación exacta
        # Buscar 'youtobe' (con esta ortografía específica)
        youtobe_mask = df['red'] == 'youtobe'
        youtobe_data = df[youtobe_mask].copy()
        
        # Buscar 'tiktok' (con esta ortografía específica)
        tiktok_mask = df['red'] == 'tiktok'
        tiktok_data = df[tiktok_mask].copy()
        
        # DEBUG: Mostrar conteos
        st.sidebar.write(f"Registros 'youtobe': {len(youtobe_data)}")
        st.sidebar.write(f"Registros 'tiktok': {len(tiktok_data)}")
        
        # Si no hay datos para youtobe, buscar variantes
        if len(youtobe_data) == 0:
            # Buscar otras posibles variantes de YouTube
            youtube_variants = ['youtube', 'yt', 'youtub', 'youtob']
            for variant in youtube_variants:
                variant_mask = df['red'].str.contains(variant, case=False, na=False)
                variant_data = df[variant_mask]
                if len(variant_data) > 0:
                    st.sidebar.write(f"Encontrado con variante '{variant}': {len(variant_data)} registros")
                    youtobe_data = variant_data.copy()
                    break
        
        # Si no hay datos para tiktok, buscar variantes
        if len(tiktok_data) == 0:
            tiktok_variants = ['tiktok', 'tt', 'tik tok']
            for variant in tiktok_variants:
                variant_mask = df['red'].str.contains(variant, case=False, na=False)
                variant_data = df[variant_mask]
                if len(variant_data) > 0:
                    st.sidebar.write(f"Encontrado con variante '{variant}': {len(variant_data)} registros")
                    tiktok_data = variant_data.copy()
                    break
        
        # Calcular métricas para cada dataset
        for df_data in [youtobe_data, tiktok_data]:
            if not df_data.empty:
                if 'fecha_publicacion' in df_data.columns:
                    hoy = pd.Timestamp.now()
                    df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
                    df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
                    df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
        
        return youtobe_data, tiktok_data

# Estilos CSS mejorados
st.markdown("""
<style>
/* Main container */
.main { padding: 0; }

/* Sidebar styling - AZUL PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
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
    padding: 25px 20px;
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
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.metric-value {
    font-size: 36px;
    font-weight: 800;
    color: #1f2937;
    margin: 15px 0 5px 0;
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
    font-size: 13px;
    display: flex;
    align-items: center;
    margin-top: 8px;
    font-weight: 500;
}

.trend-up { color: #10b981; }
.trend-down { color: #ef4444; }

/* Header principal */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 20px;
    padding: 35px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 15px 35px rgba(59, 130, 246, 0.25);
    position: relative;
    overflow: hidden;
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
    padding: 12px 20px;
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
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 20px 0;
    border: 1px solid #e5e7eb;
}

.data-table-container {
    background: white;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 20px 0;
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
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    margin-top: 25px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Status containers */
.status-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
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
    padding: 14px 16px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
}

.dataframe td {
    padding: 12px 16px;
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
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
}

/* Loader */
.loader {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3B82F6;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Backend status */
.backend-status {
    padding: 10px 15px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 13px;
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
    .metric-value { font-size: 28px; }
    .dashboard-header { padding: 25px; }
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
youtobe_df, tiktok_df = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 60px; height: 60px; border-radius: 16px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 15px auto; font-size: 28px;">
            📊
        </div>
        <h2 style="color: white; margin-bottom: 5px; font-size: 22px;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 13px; margin: 0;">Social Media Analytics v3.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div class="backend-status backend-connected">✅ Backend Conectado</div>', unsafe_allow_html=True)
            # Mostrar información del backend
            data = backend_test.json()
            st.sidebar.write(f"Total registros: {len(data.get('data', []))}")
        else:
            st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Error: {backend_test.status_code}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Offline: {str(e)[:50]}...</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
    # Botones de plataformas con estado de selección
    platforms = {
        "facebook": ("📘 Facebook", "#1877F2"),
        "twitter": ("🐦 Twitter", "#1DA1F2"),
        "instagram": ("📷 Instagram", "#E4405F"),
        "linkedin": ("💼 LinkedIn", "#0A66C2"),
        "youtube": ("▶️ YouTube", "#FF0000"),
        "tiktok": ("🎵 TikTok", "#000000")
    }
    
    # Inicializar estado si no existe
    if "selected_platform" not in st.session_state:
        st.session_state["selected_platform"] = "youtube"
    
    selected_platform = st.session_state["selected_platform"]
    
    # Mostrar botones
    for platform_key, (platform_name, platform_color) in platforms.items():
        # Determinar si este botón está seleccionado
        is_selected = (selected_platform == platform_key)
        
        # Crear botón con estilo condicional
        if st.button(platform_name, 
                    key=f"{platform_key}_btn", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
            st.rerun()
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">📈 Status Conexiones</p>', unsafe_allow_html=True)
    
    # Estado de conexiones basado en datos reales
    connection_status = []
    
    # Verificar YouTube
    if not youtobe_df.empty:
        youtube_status = ("YouTube", "connected", len(youtobe_df))
    else:
        youtube_status = ("YouTube", "disconnected", 0)
    
    # Verificar TikTok
    if not tiktok_df.empty:
        tiktok_status = ("TikTok", "connected", len(tiktok_df))
    else:
        tiktok_status = ("TikTok", "disconnected", 0)
    
    connection_status = [
        ("Facebook", "disconnected", 0),
        ("Twitter", "disconnected", 0),
        ("Instagram", "disconnected", 0),
        ("LinkedIn", "disconnected", 0),
        youtube_status,
        tiktok_status
    ]
    
    for platform, status, count in connection_status:
        if status == "connected":
            icon = "🟢"
            status_class = "status-connected"
            status_text = f"{count} posts"
        elif status == "warning":
            icon = "🟡"
            status_class = "status-warning"
            status_text = "Parcial"
        else:
            icon = "🔴"
            status_class = "status-disconnected"
            status_text = "No datos"
        
        st.markdown(f"""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">{platform}</span>
                <span class="{status_class}">{icon} {status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal
st.markdown("""
<div class="dashboard-header">
    <h1 style="margin: 0; font-size: 38px; font-weight: 800;">📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px; font-weight: 400;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
    <div style="position: absolute; bottom: 20px; right: 30px; font-size: 14px; opacity: 0.8;">
        Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
</div>
""".format(datetime=datetime), unsafe_allow_html=True)

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

# Verificar si hay datos para la plataforma seleccionada
if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    st.info(f"""
    **Posibles soluciones:**
    1. Verifica que el backend esté devolviendo datos
    2. Asegúrate que la columna 'red' contenga el valor '{selected_platform}'
    3. Revisa la consola de PythonAnywhere para errores
    4. Verifica la conexión a {BACKEND_URL}
    """)
    
    # Mostrar información de debug
    with st.expander("🔍 Información de Debug"):
        st.write("**Plataforma seleccionada:**", selected_platform)
        st.write("**DataFrame de YouTube:**", f"{len(youtobe_df)} registros")
        st.write("**DataFrame de TikTok:**", f"{len(tiktok_df)} registros")
        st.write("**Columnas disponibles en youtobe_df:**", list(youtobe_df.columns) if not youtobe_df.empty else "Vacío")
        st.write("**Columnas disponibles en tiktok_df:**", list(tiktok_df.columns) if not tiktok_df.empty else "Vacío")
        
        if not youtobe_df.empty and 'red' in youtobe_df.columns:
            st.write("**Valores únicos en youtobe_df['red']:**", list(youtobe_df['red'].unique()))
        if not tiktok_df.empty and 'red' in tiktok_df.columns:
            st.write("**Valores únicos en tiktok_df['red']:**", list(tiktok_df['red'].unique()))
    
    st.stop()

# Mostrar información de la plataforma seleccionada
st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 30px;">
    <div style="font-size: 32px; margin-right: 15px; color: {platform_color};">{platform_icon}</div>
    <div>
        <h2 style="margin: 0; color: {platform_color}; font-size: 28px;">{platform_name} ANALYTICS</h2>
        <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 14px;">
            {len(df)} contenidos analizados • Última actualización: {datetime.now().strftime('%H:%M')}
            {f" • Valores en 'red': {list(df['red'].unique()[:3])}" if 'red' in df.columns and len(df['red'].unique()) > 0 else ""}
        </p>
    </div>
    <div style="margin-left: auto; display: flex; gap: 10px; align-items: center;">
        <div style="background: {platform_color}15; color: {platform_color}; padding: 8px 20px; border-radius: 20px; font-size: 14px; font-weight: 600;">
            {len(df)} {platform_name} Posts
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_videos = len(df)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL CONTENIDOS</div>
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
        <div class="metric-label">VISUALIZACIONES TOTALES</div>
        <div class="metric-value">{total_views:,}</div>
        <div class="metric-trend trend-up">
            <span>👁️ Alcance Total</span>
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
        <div class="metric-label">RENDIMIENTO DIARIO</div>
        <div class="metric-value">{avg_daily_perf:.1f}</div>
        <div class="metric-trend trend-up">
            <span>🚀 Views/Día</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if 'visualizaciones' in df.columns and total_views > 0:
        total_engagement = (df['me_gusta'].sum() if 'me_gusta' in df.columns else 0) + \
                          (df['comentarios'].sum() if 'comentarios' in df.columns else 0)
        engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0
    else:
        engagement_rate = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TASA DE ENGAGEMENT</div>
        <div class="metric-value">{engagement_rate:.2f}%</div>
        <div class="metric-trend trend-up">
            <span>💬 Interacción</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Gráfica de performance
st.markdown("""
<div class="performance-chart">
    <h3 style="margin-top: 0; margin-bottom: 25px; color: #1f2937; font-size: 20px;">
        📈 PERFORMANCE OVER TIME
    </h3>
""", unsafe_allow_html=True)

try:
    if not df.empty and 'fecha_publicacion' in df.columns and 'visualizaciones' in df.columns:
        df_sorted = df.sort_values('fecha_publicacion')
        
        # Crear subplots simplificados para mejor rendimiento
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                'Evolución de Visualizaciones',
                'Distribución de Engagement'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'bar'}]
            ]
        )
        
        # 1. Evolución de visualizaciones
        fig.add_trace(
            go.Scatter(
                x=df_sorted['fecha_publicacion'],
                y=df_sorted['visualizaciones'],
                mode='lines+markers',
                name='Visualizaciones',
                line=dict(color=platform_color, width=3),
                marker=dict(size=6),
                hovertemplate='<b>%{x|%d/%m}</b><br>Views: %{y:,}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Métricas de engagement
        engagement_data = []
        engagement_labels = []
        
        if 'me_gusta' in df.columns:
            engagement_data.append(df['me_gusta'].sum())
            engagement_labels.append('Likes')
        
        if 'comentarios' in df.columns:
            engagement_data.append(df['comentarios'].sum())
            engagement_labels.append('Comments')
        
        if engagement_data:
            fig.add_trace(
                go.Bar(
                    x=engagement_labels,
                    y=engagement_data,
                    marker_color=[platform_color, '#8b5cf6'],
                    name='Engagement',
                    hovertemplate='<b>%{x}</b><br>Total: %{y:,}<extra></extra>'
                ),
                row=1, col=2
            )
        
        # Actualizar layout
        fig.update_layout(
            height=400,
            showlegend=False,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Visualizaciones", row=1, col=1)
        fig.update_xaxes(title_text="Métrica", row=1, col=2)
        fig.update_yaxes(title_text="Cantidad", row=1, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos suficientes para generar gráficas")
        
except Exception as e:
    st.error(f"Error al generar gráficas: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

st.markdown("</div>", unsafe_allow_html=True)

# Tabla de contenidos
st.markdown("""
<div class="data-table-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <h3 style="margin: 0; color: #1f2937; font-size: 20px;">📊 CONTENT PERFORMANCE DATA</h3>
        <div style="color: #6b7280; font-size: 13px;">
            Mostrando top 10 por visualizaciones
        </div>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # Preparar datos para la tabla
    display_columns = {}
    
    if 'titulo' in df.columns:
        display_columns['Título'] = df['titulo'].str[:60] + '...'
    
    if 'fecha_publicacion' in df.columns:
        display_columns['Fecha'] = df['fecha_publicacion'].dt.strftime('%d/%m/%Y')
    
    if 'visualizaciones' in df.columns:
        display_columns['Views'] = df['visualizaciones']
    
    if 'me_gusta' in df.columns:
        display_columns['Likes'] = df['me_gusta']
    
    if 'comentarios' in df.columns:
        display_columns['Comentarios'] = df['comentarios']
    
    if 'rendimiento_por_dia' in df.columns:
        display_columns['Rend/Día'] = df['rendimiento_por_dia']
    
    if 'red' in df.columns:
        display_columns['Plataforma'] = df['red']
    
    # Crear DataFrame para mostrar
    display_df = pd.DataFrame(display_columns)
    
    # Ordenar por Views y tomar top 10
    if 'Views' in display_df.columns:
        display_df = display_df.sort_values('Views', ascending=False).head(10)
    
    # Mostrar tabla
    if not display_df.empty:
        # Formatear números para visualización
        formatted_df = display_df.copy()
        
        if 'Views' in formatted_df.columns:
            formatted_df['Views'] = formatted_df['Views'].apply(lambda x: f"{int(x):,}")
        
        if 'Rend/Día' in formatted_df.columns:
            formatted_df['Rend/Día'] = formatted_df['Rend/Día'].apply(lambda x: f"{float(x):.1f}")
        
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Top performing content
        if not df.empty and 'titulo' in df.columns and 'visualizaciones' in df.columns:
            top_idx = df['visualizaciones'].idxmax()
            top_video = df.loc[top_idx]
            
            st.markdown(f"""
            <div style="margin-top: 25px; padding: 20px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                        border-radius: 12px; border-left: 4px solid {platform_color};">
                <div style="display: flex; align-items: flex-start; gap: 15px;">
                    <div style="font-size: 24px; color: {platform_color};">🏆</div>
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 10px 0; color: #374151;">Top Performing Content:</h4>
                        <p style="margin: 0 0 8px 0; color: #4b5563; font-size: 15px;">
                            <strong>{str(top_video.get('titulo', 'Sin título'))[:100]}{'...' if len(str(top_video.get('titulo', ''))) > 100 else ''}</strong>
                        </p>
                        <div style="display: flex; gap: 20px; margin-top: 10px;">
                            <span style="color: #6b7280; font-size: 13px;">
                                <strong>📈 {top_video.get('visualizaciones', 0):,}</strong> Views
                            </span>
                            <span style="color: #6b7280; font-size: 13px;">
                                <strong>👍 {top_video.get('me_gusta', 0):,}</strong> Likes
                            </span>
                            <span style="color: #6b7280; font-size: 13px;">
                                <strong>💬 {top_video.get('comentarios', 0):,}</strong> Comments
                            </span>
                            <span style="color: #6b7280; font-size: 13px;">
                                <strong>🚀 {top_video.get('rendimiento_por_dia', 0):.1f}</strong> Perf/Día
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay datos para mostrar en la tabla")
else:
    st.info("No hay datos disponibles")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 13px; padding: 30px; 
            border-top: 1px solid #e5e7eb; margin-top: 40px;">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;">
        <span>Social Media Dashboard PRO v3.0</span>
        <span>•</span>
        <span>Backend: {BACKEND_URL}</span>
        <span>•</span>
        <span>{platform_name} Analytics</span>
    </div>
    <div style="font-size: 12px; color: #9ca3af;">
        Datos en tiempo real • Conectado al backend • {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    </div>
</div>
""", unsafe_allow_html=True)
