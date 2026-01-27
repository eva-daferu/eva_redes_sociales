import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
from openai import OpenAI
from streamlit.components.v1 import html

warnings.filterwarnings('ignore')

# Configuración de OpenAI
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# ENDPOINTS
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
        df = pd.DataFrame(data.get("data", []))
        
        if "fecha_publicacion" in df.columns:
            df["fecha_publicacion"] = pd.to_datetime(
                df["fecha_publicacion"],
                dayfirst=True,
                errors="coerce"
            )

        num_cols = ["vistas", "comentarios", "me_gusta_numero", "visualizaciones", 
                   "me_gusta", "comentarios_num", "Seguidores_Totales"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "visualizaciones" not in df.columns and "vistas" in df.columns:
            df["visualizaciones"] = df["vistas"]
        
        if "me_gusta" not in df.columns and "me_gusta_numero" in df.columns:
            df["me_gusta"] = df["me_gusta_numero"]
        
        if "comentarios" not in df.columns and "comentarios_num" in df.columns:
            df["comentarios"] = df["comentarios_num"]

        if "red" not in df.columns and "platform" in df.columns:
            df["red"] = df["platform"]
        elif "red" not in df.columns:
            df["red"] = "desconocido"

        return df
    except Exception as e:
        st.error(f"Error al conectar con el backend: {str(e)}")
        return pd.DataFrame()

def cargar_datos_seguidores():
    try:
        r = requests.get(FOLLOWERS_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        df_followers = pd.DataFrame(data.get("data", []))
        
        if "Fecha" in df_followers.columns:
            df_followers["Fecha"] = pd.to_datetime(
                df_followers["Fecha"],
                dayfirst=True,
                errors="coerce"
            )
        
        if "Seguidores_Totales" in df_followers.columns:
            df_followers["Seguidores_Totales"] = pd.to_numeric(df_followers["Seguidores_Totales"], errors="coerce")
        
        return df_followers
    except Exception as e:
        st.error(f"Error al conectar con el backend de seguidores: {str(e)}")
        return pd.DataFrame()

def cargar_datos_pauta():
    try:
        r = requests.get(PAUTA_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        df_pauta = pd.DataFrame(data.get("data", []))
        
        if not df_pauta.empty:
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores'] = df_pauta['Seguidores']
            
            if "coste_anuncio" in df_pauta.columns:
                df_pauta["coste_anuncio"] = pd.to_numeric(df_pauta["coste_anuncio"], errors="coerce").fillna(0).astype(int)
            
            for col in ["visualizaciones_videos", "nuevos_seguidores"]:
                if col in df_pauta.columns:
                    df_pauta[col] = pd.to_numeric(df_pauta[col], errors="coerce").fillna(0).astype(int)
            
            if "fecha" in df_pauta.columns:
                df_pauta["fecha"] = pd.to_datetime(df_pauta["fecha"], errors='coerce', dayfirst=True)
        
        return df_pauta
    except Exception as e:
        return pd.DataFrame()

def _descargar_bytes(url, timeout=30):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content

def cargar_imagen_grafica1_bytes():
    try:
        content = _descargar_bytes(GRAFICA1_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 1: {str(e)}")
        return b""

def cargar_imagen_grafica2_bytes():
    try:
        content = _descargar_bytes(GRAFICA2_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 2: {str(e)}")
        return b""

# Función para cargar datos con caché
@st.cache_data(ttl=300)
def cargar_datos():
    df = cargar_datos_backend()
    df_followers = cargar_datos_seguidores()
    df_pauta = cargar_datos_pauta()
    
    if df.empty:
        st.warning("Usando datos de respaldo.")
        
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
        
        df_followers = pd.DataFrame({
            'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Seguidores_Totales': range(400, 430)
        })
        
        df_pauta = pd.DataFrame({
            'coste_anuncio': [641140],
            'visualizaciones_videos': [180500],
            'nuevos_seguidores': [4170],
            'fecha': ['2025-10-19']
        })
        
    else:
        if 'red' in df.columns:
            df['red'] = df['red'].astype(str).str.lower().str.strip()
        
        youtobe_data = df[df['red'] == 'youtobe'].copy()
        if youtobe_data.empty:
            youtobe_data = df[df['red'] == 'youtube'].copy()
        
        tiktok_data = df[df['red'] == 'tiktok'].copy()
    
    return df, youtobe_data, tiktok_data, df_followers, df_pauta

# Estilos CSS mejorados
st.markdown("""
<style>
/* Eliminar espacio superior */
.main { 
    padding: 0 !important;
    padding-top: 0 !important;
}
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0 !important;
}

/* Sidebar styling - AZUL PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.8rem;
}

/* Botones de plataformas */
.stButton > button {
    display: flex;
    align-items: center;
    padding: 8px 15px;
    margin: 3px 0;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    font-size: 13px;
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
    transform: translateX(3px);
}

.stButton > button[kind="primary"] {
    background: rgba(59, 130, 246, 0.2);
    border-color: #3B82F6;
    color: #3B82F6;
}

/* Métricas en una sola franja horizontal - DISEÑO MEJORADO */
.metrics-horizontal {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
    width: 100%;
    overflow-x: auto;
    padding-bottom: 5px;
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 #f1f5f9;
}

.metrics-horizontal::-webkit-scrollbar {
    height: 6px;
}

.metrics-horizontal::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.metrics-horizontal::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

.metric-horizontal-item {
    flex: 1 0 auto;
    min-width: 160px;
    max-width: 200px;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 12px;
    padding: 15px 12px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    text-align: center;
    backdrop-filter: blur(10px);
}

.metric-horizontal-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #3B82F6 100%);
    background-size: 200% 100%;
    animation: shimmer 3s infinite linear;
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.metric-horizontal-item:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 25px rgba(59, 130, 246, 0.15);
    border-color: #3B82F6;
}

.metric-horizontal-value {
    font-size: 22px;
    font-weight: 900;
    color: #1f2937;
    margin: 8px 0 4px 0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    letter-spacing: -0.5px;
}

.metric-horizontal-label {
    font-size: 11px;
    color: #6b7280;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    line-height: 1.3;
}

.metric-horizontal-icon {
    font-size: 20px;
    margin-bottom: 8px;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1));
}

/* Tarjetas de pauta publicitaria en horizontal - DISEÑO MEJORADO */
.pauta-horizontal-item {
    flex: 1 0 auto;
    min-width: 160px;
    max-width: 200px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 12px;
    padding: 15px 12px;
    box-shadow: 0 6px 15px rgba(14, 165, 233, 0.12);
    border: 1px solid #bae6fd;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    text-align: center;
    backdrop-filter: blur(10px);
}

.pauta-horizontal-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0ea5e9 0%, #3B82F6 50%, #0ea5e9 100%);
    background-size: 200% 100%;
    animation: shimmer 3s infinite linear;
}

.pauta-horizontal-item:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 25px rgba(14, 165, 233, 0.2);
    border-color: #0ea5e9;
}

.pauta-horizontal-value {
    font-size: 22px;
    font-weight: 900;
    color: #0369a1;
    margin: 8px 0 4px 0;
    text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    letter-spacing: -0.5px;
}

.pauta-horizontal-label {
    font-size: 11px;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    line-height: 1.3;
}

.pauta-horizontal-icon {
    font-size: 20px;
    margin-bottom: 8px;
    color: #0ea5e9;
    filter: drop-shadow(0 2px 3px rgba(14, 165, 233, 0.3));
}

/* Header principal */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 12px;
    padding: 18px 22px;
    color: white;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.25);
    position: relative;
    overflow: hidden;
    border: 1px solid #3B82F6;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 800;
    line-height: 1.2;
    font-family: 'Arial Black', sans-serif;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 20px 20px;
    opacity: 0.1;
}

/* Selector de gráficas - DISEÑO MEJORADO CON FONDO Y EFECTOS */
.grafica-selector-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 12px;
    padding: 10px;
    margin: 12px 0 15px 0;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.grafica-selector-title {
    font-size: 14px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 10px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.grafica-selector-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
}

/* Botones de selección de gráficas - DISEÑO MEJORADO */
.grafica-selector-btn {
    flex: 1;
    max-width: 220px;
    padding: 16px 15px;
    border-radius: 12px;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e5e7eb;
    color: #64748b;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-align: center;
    font-size: 13px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
}

.grafica-selector-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: 0.5s;
}

.grafica-selector-btn:hover {
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    border-color: #cbd5e1;
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
}

.grafica-selector-btn:hover::before {
    left: 100%;
}

.grafica-selector-btn.active {
    background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    color: white;
    border-color: #3B82F6;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
    transform: translateY(-3px);
}

.grafica-selector-btn.active:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 15px 30px rgba(59, 130, 246, 0.5);
}

.grafica-btn-icon {
    font-size: 24px;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1));
}

.grafica-selector-btn.active .grafica-btn-icon {
    filter: drop-shadow(0 2px 3px rgba(255,255,255,0.3));
}

.grafica-btn-text {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* Contenedores */
.performance-chart {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
}

.data-table-container {
    background: white;
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
}

/* Sidebar titles */
.sidebar-title {
    color: #cbd5e1 !important;
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 6px;
    margin-top: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Status containers */
.status-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 5px 8px;
    border-radius: 6px;
    margin-bottom: 3px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s;
    font-size: 10px;
}

/* Chat container */
.chat-container {
    max-height: 220px;
    overflow-y: auto;
    margin-top: 8px;
}

.chat-message {
    padding: 7px 9px;
    border-radius: 7px;
    margin-bottom: 5px;
    font-size: 11px;
    max-width: 90%;
}

.user-message {
    background: #3B82F6;
    color: white;
    margin-left: auto;
}

.assistant-message {
    background: #f1f5f9;
    color: #1f2937;
    border: 1px solid #e5e7eb;
}

/* Tabla compacta */
.dataframe {
    font-size: 11px !important;
}

.dataframe th {
    padding: 8px 10px !important;
    font-size: 11px !important;
    background: #f8fafc;
}

.dataframe td {
    padding: 6px 10px !important;
    font-size: 11px !important;
}

/* Responsive */
@media (max-width: 768px) {
    .metric-horizontal-value, .pauta-horizontal-value { font-size: 18px; }
    .metric-horizontal-label, .pauta-horizontal-label { font-size: 10px; }
    .dashboard-header { padding: 15px; }
    .dashboard-header h1 { font-size: 20px; }
    .metric-horizontal-item, .pauta-horizontal-item {
        min-width: 140px;
    }
    .grafica-selector-buttons {
        flex-wrap: wrap;
    }
    .grafica-selector-btn {
        min-width: calc(50% - 4px);
        padding: 14px 10px;
    }
    .grafica-btn-icon { font-size: 20px; }
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px; padding: 0 8px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 40px; height: 40px; border-radius: 8px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 6px auto; font-size: 20px;">
            📊
        </div>
        <h3 style="color: white; margin-bottom: 2px; font-size: 13px; font-weight: 700;">DASHBOARD PRO</h3>
        <p style="color: #94a3b8; font-size: 9px; margin: 0;">Social Media Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div class="status-container" style="background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2);">✅ Backend Conectado</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-container" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">⚠️ Backend Error</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="status-container" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.2);">⚠️ Backend Offline</div>', unsafe_allow_html=True)
    
    # Botones de plataformas
    st.markdown('<p class="sidebar-title">🔗 PANEL PROFESIONAL</p>', unsafe_allow_html=True)
    
    platforms = {
        "general": "🌐 GENERAL",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok"
    }
    
    selected_platform = st.session_state.get("selected_platform", "general")
    
    for platform_key, platform_name in platforms.items():
        if st.button(platform_name, key=f"{platform_key}_btn", use_container_width=True):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
            st.rerun()
    
    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    
    # Asistente de Chat
    st.markdown('<p class="sidebar-title">🤖 ASISTENTE DE DATOS</p>', unsafe_allow_html=True)
    
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Contenedor del chat
    with st.container(height=200):
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input de chat
    user_input = st.chat_input("Pregunta sobre los datos...", key="chat_input")
    
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Preparar contexto con datos actuales
        total_posts = len(df_all)
        total_views = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0
        
        # Obtener correctamente los seguidores
        total_followers = 0
        if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
            # Obtener el último valor no nulo
            if not df_followers['Seguidores_Totales'].dropna().empty:
                total_followers = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])
        
        coste_anuncio = df_pauta['coste_anuncio'].sum() if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns else 0
        visualizaciones_videos = df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0
        nuevos_seguidores = df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0
        
        contexto = f"""
        Eres un asistente especializado en análisis de datos de redes sociales. 
        
        Datos actuales del dashboard:
        - Total de publicaciones: {total_posts}
        - Visualizaciones totales: {total_views:,}
        - Total de seguidores TikTok: {total_followers:,}
        - Inversión en publicidad: ${coste_anuncio:,}
        - Visualizaciones de videos pagados: {visualizaciones_videos:,}
        - Nuevos seguidores de publicidad: {nuevos_seguidores:,}
        
        Puedes responder preguntas sobre estas métricas, tendencias, eficiencia de publicidad, y análisis de datos.
        """
        
        # Llamar a OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": contexto},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            assistant_response = response.choices[0].message.content
            
            # Agregar respuesta del asistente
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Rerun para mostrar la respuesta
            st.rerun()
            
        except Exception as e:
            st.error(f"Error al conectar con OpenAI: {str(e)}")

# Contenido principal - HEADER MEJORADO
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div class="dashboard-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1 style="font-family: 'Arial Black', sans-serif; margin-bottom: 4px; letter-spacing: 0.5px;">📊 SOCIAL MEDIA DASHBOARD PRO</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 12px; font-weight: 400;">
                Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
            </p>
        </div>
        <div style="font-size: 11px; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 15px; font-weight: 500;">
            {current_time}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Métricas en UNA SOLA FRANJA HORIZONTAL - SOLUCIÓN DEFINITIVA
def format_number(num):
    try:
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return f"{int(num):,}"
    except:
        return "0"

# Calcular métricas
# Métricas de pauta publicitaria
if not df_pauta.empty:
    coste_anuncio_sum = df_pauta['coste_anuncio'].sum() if 'coste_anuncio' in df_pauta.columns else 0
    visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum() if 'visualizaciones_videos' in df_pauta.columns else 0
    nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum() if 'nuevos_seguidores' in df_pauta.columns else 0
else:
    coste_anuncio_sum = 0
    visualizaciones_videos_sum = 0
    nuevos_seguidores_sum = 0

# Métricas generales
total_seguidores = 0
if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
    if not df_followers['Seguidores_Totales'].dropna().empty:
        total_seguidores = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])

total_contenidos = len(df_all)
total_visualizaciones = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0

# Usar st.columns para crear una fila horizontal
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    html(f"""
    <div class="pauta-horizontal-item">
        <div class="pauta-horizontal-icon">💰</div>
        <div class="pauta-horizontal-label">COSTE ANUNCIO</div>
        <div class="pauta-horizontal-value">${format_number(coste_anuncio_sum)}</div>
    </div>
    """, height=120)

with col2:
    html(f"""
    <div class="pauta-horizontal-item">
        <div class="pauta-horizontal-icon">👁️</div>
        <div class="pauta-horizontal-label">VISUALIZACIONES VIDEOS</div>
        <div class="pauta-horizontal-value">{format_number(visualizaciones_videos_sum)}</div>
    </div>
    """, height=120)

with col3:
    html(f"""
    <div class="pauta-horizontal-item">
        <div class="pauta-horizontal-icon">📈</div>
        <div class="pauta-horizontal-label">NUEVOS SEGUIDORES</div>
        <div class="pauta-horizontal-value">{format_number(nuevos_seguidores_sum)}</div>
    </div>
    """, height=120)

with col4:
    html(f"""
    <div class="metric-horizontal-item">
        <div class="metric-horizontal-icon">👥</div>
        <div class="metric-horizontal-label">TOTAL SEGUIDORES</div>
        <div class="metric-horizontal-value">{format_number(total_seguidores)}</div>
    </div>
    """, height=120)

with col5:
    html(f"""
    <div class="metric-horizontal-item">
        <div class="metric-horizontal-icon">📊</div>
        <div class="metric-horizontal-label">TOTAL CONTENIDOS</div>
        <div class="metric-horizontal-value">{format_number(total_contenidos)}</div>
    </div>
    """, height=120)

with col6:
    html(f"""
    <div class="metric-horizontal-item">
        <div class="metric-horizontal-icon">👁️</div>
        <div class="metric-horizontal-label">VISUALIZACIONES TOTALES</div>
        <div class="metric-horizontal-value">{format_number(total_visualizaciones)}</div>
    </div>
    """, height=120)

# Selector de gráficas - DISEÑO MEJORADO CON BOTONES EN HORIZONTAL
st.markdown('<div class="grafica-selector-container">', unsafe_allow_html=True)
st.markdown('<div class="grafica-selector-title">📈 SELECCIONA EL TIPO DE GRÁFICA</div>', unsafe_allow_html=True)

# Inicializar estado para gráfica seleccionada
if "grafica_seleccionada" not in st.session_state:
    st.session_state.grafica_seleccionada = "evolucion"

# Selector visual mejorado con HTML/CSS personalizado
st.markdown('<div class="grafica-selector-buttons">', unsafe_allow_html=True)

# Crear botones con HTML/CSS personalizado para mejor control visual
col1, col2, col3 = st.columns(3)

with col1:
    btn1_active = st.session_state.grafica_seleccionada == "evolucion"
    if st.button("**📈** **Evolución**", 
                 key="btn_evolucion",
                 use_container_width=True,
                 type="primary" if btn1_active else "secondary"):
        st.session_state.grafica_seleccionada = "evolucion"
        st.rerun()

with col2:
    btn2_active = st.session_state.grafica_seleccionada == "grafica1"
    if st.button("**💰** **Inversión vs Seguidores**", 
                 key="btn_grafica1",
                 use_container_width=True,
                 type="primary" if btn2_active else "secondary"):
        st.session_state.grafica_seleccionada = "grafica1"
        st.rerun()

with col3:
    btn3_active = st.session_state.grafica_seleccionada == "grafica2"
    if st.button("**📊** **Heatmap CPS**", 
                 key="btn_grafica2",
                 use_container_width=True,
                 type="primary" if btn3_active else "secondary"):
        st.session_state.grafica_seleccionada = "grafica2"
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# Mostrar gráfica seleccionada
if st.session_state.grafica_seleccionada == "grafica1":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 Gráfica 1: Inversión vs Seguidores")
    img_bytes = cargar_imagen_grafica1_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 1")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.grafica_seleccionada == "grafica2":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📊 Gráfica 2: Heatmap CPS")
    img_bytes = cargar_imagen_grafica2_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 2")
    st.markdown('</div>', unsafe_allow_html=True)

else:  # Gráfica de evolución
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA")
    
    if not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
        try:
            # Preparar datos de pauta si existen (MÉTODO ORIGINAL)
            if not df_pauta.empty:
                if 'Costo' in df_pauta.columns:
                    df_pauta['coste_anuncio'] = df_pauta['Costo']
                if 'Visualizaciones' in df_pauta.columns:
                    df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
                if 'Seguidores' in df_pauta.columns:
                    df_pauta['nuevos_seguidores_pauta'] = df_pauta['Seguidores']
                
                df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
                
                df_pauta_agg = df_pauta.groupby('fecha').agg({
                    'coste_anuncio': 'sum',
                    'visualizaciones_videos': 'sum',
                    'nuevos_seguidores_pauta': 'sum'
                }).reset_index()
                
                # Fusionar por fecha - USAR OUTER JOIN
                df_merged = pd.merge(df_followers, df_pauta_agg, left_on='Fecha', right_on='fecha', how='outer')
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
            
            # Crear gráfica de 4 líneas (MÉTODO ORIGINAL)
            fig_followers = go.Figure()
            
            # 1. Seguidores Totales (línea principal)
            fig_followers.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['Seguidores_Totales'],
                mode='lines+markers',
                name='👥 Seguidores Totales',
                marker=dict(
                    size=6,
                    color='#000000',
                    symbol='circle',
                    line=dict(width=1, color='white')
                ),
                line=dict(color='#000000', width=2),
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
                        size=5,
                        color='#10b981',
                        symbol='diamond'
                    ),
                    line=dict(color='#10b981', width=1.5, dash='dot'),
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
                        opacity=0.6
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
                        size=5,
                        color='#3B82F6',
                        symbol='triangle-up'
                    ),
                    line=dict(color='#3B82F6', width=1.5, dash='dash'),
                    hovertemplate='Visualizaciones Pauta: %{y:,}<extra></extra>',
                    yaxis='y2'
                ))
            
            # Configurar layout con eje secundario (MÉTODO ORIGINAL)
            fig_followers.update_layout(
                height=350,
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=40, r=40, t=20, b=40),
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
                        
        except Exception as e:
            st.warning(f"Error al generar gráfica combinada: {str(e)}")
    else:
        st.warning("No hay datos de seguidores disponibles")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tabla de contenido - COMPACTA
st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
st.markdown("##### 📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA")

if not df_all.empty:
    # Filtrar por plataforma seleccionada
    if selected_platform == "tiktok":
        display_df = tiktok_df.copy()
    elif selected_platform == "youtube":
        display_df = youtobe_df.copy()
    else:
        display_df = df_all.copy()
    
    # Seleccionar columnas relevantes
    column_order = []
    if 'titulo' in display_df.columns:
        column_order.append('titulo')
        display_df['titulo'] = display_df['titulo'].fillna('Sin título').str.slice(0, 35) + '...'
    
    if 'fecha_publicacion' in display_df.columns:
        column_order.append('fecha_publicacion')
        display_df['fecha_publicacion'] = display_df['fecha_publicacion'].dt.strftime('%d/%m')
    
    if 'red' in display_df.columns:
        column_order.append('red')
    
    if 'visualizaciones' in display_df.columns:
        column_order.append('visualizaciones')
    
    if 'me_gusta' in display_df.columns:
        column_order.append('me_gusta')
    
    if 'comentarios' in display_df.columns:
        column_order.append('comentarios')
    
    if 'Seguidores_Totales' in display_df.columns:
        column_order.append('Seguidores_Totales')
    
    column_order = [col for col in column_order if col in display_df.columns]
    display_df = display_df[column_order]
    
    # Renombrar columnas
    rename_dict = {
        'titulo': 'Título',
        'fecha_publicacion': 'Fecha',
        'red': 'Plataforma',
        'visualizaciones': 'Views',
        'me_gusta': 'Likes',
        'comentarios': 'Comentarios',
        'Seguidores_Totales': 'Seguidores'
    }
    
    display_df = display_df.rename(columns={k: v for k, v in rename_dict.items() if k in display_df.columns})
    
    # Mostrar tabla compacta
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=250
    )
    
st.markdown('</div>', unsafe_allow_html=True)

# Footer minimalista
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 9px; padding: 8px 0; margin-top: 12px; border-top: 1px solid #e5e7eb;">
    Social Media Dashboard PRO v3.2 • Analytics en Tiempo Real • {current_time_full}
</div>
""", unsafe_allow_html=True)
