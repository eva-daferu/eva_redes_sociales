import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from io import BytesIO
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="Social Dashboard - Panel Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CSS EXACTO DEL DISEÑO ORIGINAL MEJORADO
# =============================================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* ===== TOP BAR ===== */
    .stApp header {
        background-color: #2d3748 !important;
        height: 70px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* ===== SIDEBAR PROFESIONAL ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%) !important;
        padding-top: 70px !important;
        min-width: 90px !important;
        max-width: 250px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 30px !important;
        background: transparent !important;
    }
    
    /* Botones de redes sociales en sidebar */
    .network-sidebar-btn {
        width: 100%;
        height: 60px;
        border-radius: 12px;
        border: none;
        margin: 5px 0 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        color: white;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        padding: 0 20px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .network-sidebar-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .network-sidebar-btn.active {
        background: rgba(255, 255, 255, 0.25);
        border-left: 4px solid;
        padding-left: 16px;
    }
    
    .network-icon {
        font-size: 20px;
        margin-right: 15px;
        min-width: 24px;
        text-align: center;
    }
    
    .network-name {
        font-weight: 600;
        flex-grow: 1;
    }
    
    .network-status {
        font-size: 12px;
        opacity: 0.8;
    }
    
    /* ===== MODAL FRAME PROFESIONAL ===== */
    .modal-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        padding: 20px;
    }
    
    .modal-frame {
        max-width: 800px;
        width: 100%;
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        padding: 60px;
        text-align: center;
        margin: 0 auto;
        border: 1px solid rgba(229, 231, 235, 0.5);
    }
    
    .modal-title {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 25px;
        line-height: 1.2;
        letter-spacing: -0.5px;
    }
    
    .modal-subtitle {
        font-size: 20px;
        line-height: 1.8;
        color: #4a5568;
        margin-bottom: 50px;
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .social-network-name {
        color: #1e3a8a;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .permissions-list {
        text-align: left;
        background-color: #f8fafc;
        padding: 35px;
        border-radius: 15px;
        margin-bottom: 50px;
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .permissions-list h3 {
        margin-bottom: 25px;
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .permissions-list ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .permissions-list li {
        padding: 15px 0;
        display: flex;
        align-items: center;
        font-size: 17px;
        color: #4a5568;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .permissions-list li:last-child {
        border-bottom: none;
    }
    
    .permissions-list i {
        color: #1e3a8a;
        margin-right: 15px;
        font-size: 20px;
        min-width: 24px;
    }
    
    .button-group {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 50px;
        flex-wrap: wrap;
    }
    
    .modal-btn {
        padding: 20px 45px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        min-width: 200px;
        letter-spacing: 0.3px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    
    .btn-cancel {
        background-color: #f1f5f9;
        color: #475569;
        border: 2px solid #e2e8f0;
    }
    
    .btn-cancel:hover {
        background-color: #e2e8f0;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .btn-connect {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.3);
        border: none;
    }
    
    .btn-connect:hover {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(30, 58, 138, 0.4);
    }
    
    .network-icon-large {
        font-size: 90px;
        margin-bottom: 40px;
        display: flex;
        justify-content: center;
    }
    
    /* ===== DASHBOARD HEADER ===== */
    .dashboard-header {
        background: linear-gradient(135deg, var(--network-color) 0%, #333333 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    /* ===== METRICS CARDS ===== */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-top: 5px solid;
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* ===== HEATMAP STYLES ===== */
    .heatmap-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin: 20px 0;
        border: 1px solid #e2e8f0;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .modal-frame {
            padding: 40px 25px;
            margin: 20px;
        }
        
        .modal-title {
            font-size: 32px;
        }
        
        .modal-subtitle {
            font-size: 18px;
        }
        
        .button-group {
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }
        
        .modal-btn {
            width: 100%;
            max-width: 300px;
        }
        
        .network-icon-large {
            font-size: 70px;
        }
    }
    
    /* ===== OCULTAR ELEMENTOS STREAMLIT ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Botones de Streamlit mejorados */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# ESTADO DE LA SESIÓN
# =============================================
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = {
        'tiktok': False,
        'youtube': False,
        'facebook': False,
        'twitter': False,
        'instagram': False,
        'linkedin': False
    }

if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {}

if 'current_network' not in st.session_state:
    st.session_state.current_network = 'tiktok'

if 'scraping_in_progress' not in st.session_state:
    st.session_state.scraping_in_progress = False

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# =============================================
# CONFIGURACIÓN DE REDES SOCIALES
# =============================================
NETWORK_CONFIG = {
    'tiktok': {
        'name': 'TikTok',
        'color': '#010101',
        'icon': 'fab fa-tiktok',
        'icon_color': '#00f2ea',
        'auth_url': 'https://www.tiktok.com/login',
        'permissions': [
            'Acceso a videos y métricas',
            'Lectura de analíticas de contenido',
            'Gestión de comentarios',
            'Análisis de tendencias y hashtags'
        ],
        'data_source': r"C:\Users\diana\OneDrive\Documentos\WasaFlete\Eva\descargas\base_tiktok.xlsx"
    },
    'youtube': {
        'name': 'YouTube',
        'color': '#FF0000',
        'icon': 'fab fa-youtube',
        'icon_color': '#FF0000',
        'auth_url': 'https://www.youtube.com/login',
        'permissions': [
            'Acceso a videos y estadísticas',
            'Lectura de métricas de visualizaciones',
            'Gestión de comentarios',
            'Análisis de rendimiento de contenido'
        ],
        'data_source': r"C:\Users\diana\OneDrive\Documentos\WasaFlete\Eva\descargas\base_youtobe.xlsx"
    },
    'facebook': {
        'name': 'Facebook',
        'color': '#1877f2',
        'icon': 'fab fa-facebook-f',
        'icon_color': '#1877f2',
        'auth_url': 'https://www.facebook.com/login',
        'permissions': [
            'Acceso a información básica del perfil',
            'Lectura de publicaciones y métricas',
            'Gestión de páginas conectadas',
            'Análisis de audiencia y alcance'
        ],
        'data_source': None
    },
    'twitter': {
        'name': 'Twitter',
        'color': '#1da1f2',
        'icon': 'fab fa-twitter',
        'icon_color': '#1da1f2',
        'auth_url': 'https://twitter.com/i/flow/login',
        'permissions': [
            'Acceso a tweets y métricas',
            'Lectura de seguidores y seguidos',
            'Análisis de engagement',
            'Datos históricos de actividad'
        ],
        'data_source': None
    },
    'instagram': {
        'name': 'Instagram',
        'color': '#E4405F',
        'icon': 'fab fa-instagram',
        'icon_color': '#E4405F',
        'auth_url': 'https://www.instagram.com/accounts/login/',
        'permissions': [
            'Acceso a publicaciones y stories',
            'Lectura de insights y métricas',
            'Gestión de comentarios',
            'Análisis de hashtags y menciones'
        ],
        'data_source': None
    },
    'linkedin': {
        'name': 'LinkedIn',
        'color': '#0a66c2',
        'icon': 'fab fa-linkedin-in',
        'icon_color': '#0a66c2',
        'auth_url': 'https://www.linkedin.com/login',
        'permissions': [
            'Acceso a perfil profesional',
            'Lectura de publicaciones y artículos',
            'Análisis de conexiones',
            'Métricas de engagement profesional'
        ],
        'data_source': None
    }
}

# =============================================
# FUNCIONES PARA CARGAR DATOS
# =============================================
def load_data_from_excel(file_path):
    """Carga datos desde archivo Excel"""
    
    try:
        if not os.path.exists(file_path):
            return pd.DataFrame(), f"❌ Archivo no encontrado: {file_path}"
        
        # Cargar datos desde Excel
        df = pd.read_excel(file_path)
        
        # Verificar columnas necesarias
        required_columns = ['duracion_video', 'titulo', 'fecha_publicacion', 
                          'privacidad', 'visualizaciones', 'me_gusta', 'comentarios']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return pd.DataFrame(), f"❌ Columnas faltantes: {missing_columns}"
        
        # Limpiar y preparar datos
        for col in ['visualizaciones', 'me_gusta', 'comentarios']:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Crear columnas numéricas
        df['visualizaciones_num'] = df['visualizaciones'].fillna(0).astype(float)
        df['me_gusta_num'] = df['me_gusta'].fillna(0).astype(float)
        df['comentarios_num'] = df['comentarios'].fillna(0).astype(float)
        
        # Calcular engagement rate
        mask = df['visualizaciones_num'] > 0
        df['engagement_rate'] = 0.0
        df.loc[mask, 'engagement_rate'] = ((df.loc[mask, 'me_gusta_num'] + df.loc[mask, 'comentarios_num']) / 
                                          df.loc[mask, 'visualizaciones_num'] * 100).round(2)
        
        # Convertir duración a segundos
        def duration_to_seconds(duration_str):
            try:
                if pd.isna(duration_str):
                    return 0
                parts = str(duration_str).split(':')
                if len(parts) == 3:  # HH:MM:SS
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])
                    return hours * 3600 + minutes * 60 + seconds
                elif len(parts) == 2:  # MM:SS
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    return minutes * 60 + seconds
                else:  # Solo segundos
                    return int(duration_str)
            except:
                return 0
        
        df['duracion_segundos'] = df['duracion_video'].apply(duration_to_seconds)
        
        return df, f"✅ Datos cargados exitosamente: {len(df)} videos"
        
    except Exception as e:
        return pd.DataFrame(), f"❌ Error al cargar datos: {str(e)}"

def run_data_loader(network):
    """Función para cargar datos de la red especificada"""
    
    st.session_state.scraping_in_progress = True
    
    try:
        config = NETWORK_CONFIG[network]
        file_path = config['data_source']
        
        if not file_path:
            return pd.DataFrame(), "❌ No hay fuente de datos configurada para esta red"
        
        df, message = load_data_from_excel(file_path)
        
        if df.empty:
            return pd.DataFrame(), message
        
        return df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error: {str(e)}"
    finally:
        st.session_state.scraping_in_progress = False
        st.session_state.data_loaded = True

# =============================================
# COMPONENTES DE INTERFAZ
# =============================================
def create_sidebar():
    """Crea la sidebar profesional"""
    with st.sidebar:
        # Logo y título
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h2 style="color: white; margin: 0; font-weight: 700;">🌐 DASHBOARD</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 10px 0 0 0;">Panel Profesional</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones de redes sociales
        networks = [
            ('tiktok', 'TikTok', 'fab fa-tiktok'),
            ('youtube', 'YouTube', 'fab fa-youtube'),
            ('facebook', 'Facebook', 'fab fa-facebook-f'),
            ('twitter', 'Twitter', 'fab fa-twitter'),
            ('instagram', 'Instagram', 'fab fa-instagram'),
            ('linkedin', 'LinkedIn', 'fab fa-linkedin-in')
        ]
        
        for network_id, network_name, network_icon in networks:
            config = NETWORK_CONFIG[network_id]
            status = "✅" if st.session_state.auth_status[network_id] else "🔒"
            is_active = st.session_state.current_network == network_id
            active_class = "active" if is_active else ""
            
            # Determinar color del borde izquierdo
            border_color = config['color']
            
            # Botón de selección
            button_html = f"""
            <button class="network-sidebar-btn {active_class}" onclick="setNetwork('{network_id}')" 
                    style="border-left-color: {border_color} !important;">
                <div class="network-icon">
                    <i class="{network_icon}" style="color: {config['icon_color']};"></i>
                </div>
                <div class="network-name">{network_name}</div>
                <div class="network-status">{status}</div>
            </button>
            """
            
            st.markdown(button_html, unsafe_allow_html=True)
        
        # JavaScript para cambiar red
        st.markdown("""
        <script>
        function setNetwork(network) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: network
            }, '*');
        }
        </script>
        """, unsafe_allow_html=True)
        
        # Separador
        st.markdown("---")
        
        # Estado de conexiones
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: white; margin: 0 0 15px 0;">🔗 Estado Conexiones</h4>
        """, unsafe_allow_html=True)
        
        for network_id, network_name, _ in networks:
            if network_id in ['tiktok', 'youtube']:  # Solo mostrar redes con datos
                status = "🟢 Conectado" if st.session_state.auth_status[network_id] else "🔴 No conectado"
                color = "#10b981" if st.session_state.auth_status[network_id] else "#ef4444"
                st.markdown(f"""
                <p style="color: {color}; margin: 8px 0; font-size: 14px;">
                    <strong>{network_name}:</strong> {status}
                </p>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Información de datos
        current_network = st.session_state.current_network
        if st.session_state.data_loaded and current_network in st.session_state.scraped_data:
            data = st.session_state.scraped_data[current_network]
            if isinstance(data, pd.DataFrame) and not data.empty:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
                    <h4 style="color: white; margin: 0 0 15px 0;">📊 Datos Cargados</h4>
                    <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                        <strong>Videos:</strong> {len(data)}
                    </p>
                    <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                        <strong>Vistas totales:</strong> {data['visualizaciones_num'].sum():,}
                    </p>
                </div>
                """, unsafe_allow_html=True)

def show_auth_modal():
    """Muestra el modal de autenticación profesional"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    st.markdown("""
    <div class="modal-container">
        <div class="modal-frame">
    """, unsafe_allow_html=True)
    
    # Icono grande
    st.markdown(f"""
    <div class="network-icon-large">
        <i class="{config['icon']}" style="color: {config['icon_color']}; font-size: 90px;"></i>
    </div>
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown(f"""
    <h1 class="modal-title">Conectar con <span class="social-network-name">{config['name']}</span>?</h1>
    """, unsafe_allow_html=True)
    
    # Subtítulo
    st.markdown(f"""
    <p class="modal-subtitle">
        Esto permitirá al dashboard acceder a los datos de tu cuenta de {config['name']} 
        para proporcionar análisis, métricas de engagement y visualizaciones detalladas.
    </p>
    """, unsafe_allow_html=True)
    
    # Permisos
    st.markdown("""
    <div class="permissions-list">
        <h3><i class="fas fa-shield-alt"></i> Permisos solicitados:</h3>
        <ul>
    """, unsafe_allow_html=True)
    
    for permission in config['permissions']:
        st.markdown(f'<li><i class="fas fa-check-circle"></i> {permission}</li>', unsafe_allow_html=True)
    
    st.markdown("""
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("❌ Cancelar", use_container_width=True, key="modal_cancel"):
                st.warning(f"Conexión con {config['name']} cancelada")
        
        with button_col2:
            if st.button(f"🔗 Conectar", use_container_width=True, key="modal_connect", type="primary"):
                if network in ['tiktok', 'youtube']:
                    with st.spinner(f"📂 Cargando datos de {config['name']}..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        
                        # Cargar datos desde archivo
                        data, message = run_data_loader(network)
                        
                        if not data.empty:
                            st.session_state.auth_status[network] = True
                            st.session_state.scraped_data[network] = data
                            st.success(message)
                        else:
                            st.error(message)
                        
                        st.rerun()
                else:
                    # Para otras redes, simular autenticación
                    with st.spinner(f"Autenticando con {config['name']}..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)
                        
                        st.session_state.auth_status[network] = True
                        st.success(f"✅ ¡Conectado exitosamente a {config['name']}!")
                        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def create_heatmap(data, metric_column, title):
    """Crea un heatmap de calor por contenido"""
    
    # Preparar datos para el heatmap
    heatmap_data = data.copy()
    
    # Agrupar por contenido (usando títulos truncados)
    heatmap_data['titulo_short'] = heatmap_data['titulo'].str[:40] + '...'
    
    # Ordenar por la métrica seleccionada
    heatmap_data = heatmap_data.sort_values(metric_column, ascending=False).head(20)
    
    # Crear valores normalizados para el heatmap
    values = heatmap_data[metric_column].values
    normalized_values = (values - values.min()) / (values.max() - values.min() + 1e-8)
    
    # Crear figura
    fig = go.Figure(data=go.Heatmap(
        z=[normalized_values],
        x=heatmap_data['titulo_short'].tolist(),
        y=[''],
        colorscale='RdYlGn_r',  # Rojo para alto, verde para bajo
        showscale=True,
        hoverongaps=False,
        hovertemplate='<b>%{x}</b><br>' + metric_column + ': %{customdata}<extra></extra>',
        customdata=[[f"{val:,.0f}" if metric_column != 'engagement_rate' else f"{val:.1f}%" 
                    for val in values]]
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color='#0f172a')
        ),
        xaxis=dict(
            title='Contenido',
            tickangle=45,
            tickfont=dict(size=10)
        ),
        yaxis=dict(visible=False),
        height=400,
        margin=dict(l=20, r=20, t=60, b=150),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

def show_tiktok_dashboard():
    """Dashboard específico para TikTok con datos reales"""
    if 'tiktok' not in st.session_state.scraped_data:
        st.info("ℹ️ Primero autentica con TikTok para ver los análisis")
        return
    
    data = st.session_state.scraped_data['tiktok']
    config = NETWORK_CONFIG['tiktok']
    
    # Header del dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {config['color']} 0%, #333333 100%); 
                padding: 30px; border-radius: 20px; color: white; margin-bottom: 40px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; display: flex; align-items: center; gap: 20px;">
            <i class="{config['icon']}" style="font-size: 50px; color: #00f2ea;"></i>
            TikTok Analytics Dashboard
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 18px;">
            Análisis de métricas y rendimiento de tus videos de TikTok
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_videos = len(data)
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: {config['color']};">
            <div class="metric-icon"><i class="fas fa-video" style="color: {config['color']};"></i></div>
            <div class="metric-value">{total_videos}</div>
            <div class="metric-label">Total Videos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_views = int(data['visualizaciones_num'].sum())
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: {config['color']};">
            <div class="metric-icon"><i class="fas fa-eye" style="color: {config['color']};"></i></div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-label">Total Views</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_likes = int(data['me_gusta_num'].sum())
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: {config['color']};">
            <div class="metric-icon"><i class="fas fa-heart" style="color: {config['color']};"></i></div>
            <div class="metric-value">{total_likes:,}</div>
            <div class="metric-label">Total Likes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_engagement = data['engagement_rate'].mean()
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: {config['color']};">
            <div class="metric-icon"><i class="fas fa-chart-line" style="color: {config['color']};"></i></div>
            <div class="metric-value">{avg_engagement:.1f}%</div>
            <div class="metric-label">Avg. Engagement</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs de análisis
    tab1, tab2, tab3 = st.tabs(["📈 Gráficas Multilineales", "🔥 Heatmap por Contenido", "📋 Datos Completos"])
    
    with tab1:
        st.subheader("📈 Gráficas Multilineales de Rendimiento")
        
        # Intentar parsear fechas
        try:
            date_formats = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
            data_with_dates = data.copy()
            date_parsed = False
            
            for fmt in date_formats:
                try:
                    data_with_dates['fecha_dt'] = pd.to_datetime(data_with_dates['fecha_publicacion'], format=fmt, errors='coerce')
                    if data_with_dates['fecha_dt'].notna().sum() > 0:
                        date_parsed = True
                        break
                except:
                    continue
            
            if date_parsed and 'fecha_dt' in data_with_dates.columns:
                data_with_dates = data_with_dates.sort_values('fecha_dt')
                
                # Agrupar por fecha
                if len(data_with_dates['fecha_dt'].dt.date.unique()) > 1:
                    daily_data = data_with_dates.groupby(data_with_dates['fecha_dt'].dt.date).agg({
                        'visualizaciones_num': 'sum',
                        'me_gusta_num': 'sum',
                        'comentarios_num': 'sum',
                        'engagement_rate': 'mean'
                    }).reset_index()
                    
                    daily_data.columns = ['Fecha', 'Vistas',
