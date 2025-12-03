import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from io import BytesIO
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
    
    /* Estilos para gráficos */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin: 20px 0;
        border: 1px solid #e2e8f0;
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
        'data_source': r"base_tiktok.xlsx"
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
        'data_source': r"base_youtobe.xlsx"
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
            # Intentar con ruta relativa en Streamlit Cloud
            file_path = file_path.split('/')[-1]  # Solo el nombre del archivo
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
# FUNCIONES PARA GRÁFICOS
# =============================================
def create_multiline_chart(daily_data, metric_trend, config):
    """Crea gráfico multilineal con matplotlib"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Configurar estilo
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Crear gráfico
    if metric_trend == 'Engagement':
        ax.plot(daily_data['Fecha'], daily_data['Engagement'], 
                marker='o', linewidth=3, markersize=8, color=config['color'])
        ax.set_ylabel('Engagement Rate (%)')
    else:
        metric_data = daily_data[metric_trend]
        ax.plot(daily_data['Fecha'], metric_data, 
                marker='o', linewidth=3, markersize=8, color=config['color'])
        ax.set_ylabel(metric_trend)
    
    # Personalizar gráfico
    ax.set_xlabel('Fecha')
    ax.set_title(f'Tendencia de {metric_trend} a lo largo del tiempo', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    # Mejorar formato de fechas
    fig.autofmt_xdate()
    
    # Añadir área sombreada bajo la línea
    if metric_trend == 'Engagement':
        ax.fill_between(daily_data['Fecha'], daily_data['Engagement'], alpha=0.2, color=config['color'])
    else:
        metric_data = daily_data[metric_trend]
        ax.fill_between(daily_data['Fecha'], metric_data, alpha=0.2, color=config['color'])
    
    plt.tight_layout()
    return fig

def create_heatmap_chart(data, metric_column, title, config):
    """Crea heatmap de calor por contenido con matplotlib"""
    
    # Preparar datos
    heatmap_data = data.copy()
    heatmap_data['titulo_short'] = heatmap_data['titulo'].str[:40] + '...'
    heatmap_data = heatmap_data.sort_values(metric_column, ascending=False).head(15)
    
    # Crear valores normalizados
    values = heatmap_data[metric_column].values
    normalized_values = (values - values.min()) / (values.max() - values.min() + 1e-8)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Crear heatmap con colormap
    cmap = plt.cm.RdYlGn_r  # Rojo (alto) a Verde (bajo)
    colors = cmap(normalized_values)
    
    # Crear barras horizontales
    bars = ax.barh(range(len(heatmap_data)), normalized_values, color=colors)
    
    # Añadir etiquetas de valores
    for i, (bar, val) in enumerate(zip(bars, values)):
        if metric_column == 'engagement_rate':
            value_text = f"{val:.1f}%"
        else:
            value_text = f"{val:,.0f}"
        
        # Posicionar texto dentro o fuera de la barra
        if normalized_values[i] > 0.5:
            ax.text(bar.get_width() - 0.02, bar.get_y() + bar.get_height()/2, 
                   value_text, va='center', ha='right', color='white', fontweight='bold')
        else:
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                   value_text, va='center', ha='left', color='black', fontweight='bold')
    
    # Configurar eje Y
    ax.set_yticks(range(len(heatmap_data)))
    ax.set_yticklabels(heatmap_data['titulo_short'])
    
    # Configurar eje X
    ax.set_xlim(0, 1.1)
    ax.set_xlabel('Rendimiento Normalizado (0 = mínimo, 1 = máximo)')
    
    # Título
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Añadir leyenda de colores
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d73027', label='Alto rendimiento'),
        Patch(facecolor='#fee08b', label='Rendimiento medio'),
        Patch(facecolor='#1a9850', label='Bajo rendimiento')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return fig

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
            <div class="network-sidebar-btn {active_class}" 
                 style="border-left-color: {border_color} !important; cursor: pointer;"
                 onclick="parent.window.location.href='?network={network_id}'">
                <div class="network-icon">
                    <i class="{network_icon}" style="color: {config['icon_color']};"></i>
                </div>
                <div class="network-name">{network_name}</div>
                <div class="network-status">{status}</div>
            </div>
            """
            
            st.markdown(button_html, unsafe_allow_html=True)
        
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

def show_social_dashboard(network):
    """Dashboard específico para cada red social"""
    if network not in st.session_state.scraped_data:
        st.info("ℹ️ Primero autentica con esta red para ver los análisis")
        return
    
    data = st.session_state.scraped_data[network]
    config = NETWORK_CONFIG[network]
    
    # Header del dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {config['color']} 0%, #333333 100%); 
                padding: 30px; border-radius: 20px; color: white; margin-bottom: 40px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; display: flex; align-items: center; gap: 20px;">
            <i class="{config['icon']}" style="font-size: 50px; color: {config['icon_color']};"></i>
            {config['name']} Analytics Dashboard
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 18px;">
            Análisis de métricas y rendimiento de tus videos en {config['name']}
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
    if network == 'tiktok':
        tab1, tab2, tab3 = st.tabs(["📈 Gráficas Multilineales", "🔥 Heatmap por Contenido", "📋 Datos Completos"])
    else:
        tab1, tab2 = st.tabs(["📈 Gráficas Multilineales", "📋 Datos Completos"])
    
    with tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
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
                    
                    daily_data.columns = ['Fecha', 'Vistas', 'Likes', 'Comentarios', 'Engagement']
                    
                    # Selección de métrica para gráfico
                    metric_trend = st.selectbox(
                        "Selecciona métrica para la tendencia:",
                        ['Vistas', 'Likes', 'Comentarios', 'Engagement'],
                        key=f"trend_metric_{network}"
                    )
                    
                    # Crear gráfico multilineal
                    fig = create_multiline_chart(daily_data, metric_trend, config)
                    st.pyplot(fig)
                    
                    # Estadísticas de tendencia
                    if len(daily_data) > 1:
                        st.subheader("📈 Análisis de Tendencia")
                        trend_col1, trend_col2, trend_col3 = st.columns(3)
                        
                        with trend_col1:
                            if metric_trend == 'Engagement':
                                growth = ((daily_data[metric_trend].iloc[-1] - daily_data[metric_trend].iloc[0]) / 
                                         daily_data[metric_trend].iloc[0] * 100) if daily_data[metric_trend].iloc[0] != 0 else 0
                                st.metric(f"Crecimiento {metric_trend}", f"{growth:.1f}%")
                            else:
                                growth = ((daily_data[metric_trend].iloc[-1] - daily_data[metric_trend].iloc[0]) / 
                                         daily_data[metric_trend].iloc[0] * 100) if daily_data[metric_trend].iloc[0] != 0 else 0
                                st.metric(f"Crecimiento {metric_trend}", f"{growth:.1f}%")
                        
                        with trend_col2:
                            if metric_trend == 'Engagement':
                                avg_daily = daily_data[metric_trend].mean()
                                st.metric(f"Promedio diario {metric_trend}", f"{avg_daily:.1f}%")
                            else:
                                avg_daily = daily_data[metric_trend].mean()
                                st.metric(f"Promedio diario {metric_trend}", f"{avg_daily:,.0f}")
                        
                        with trend_col3:
                            best_day = daily_data.loc[daily_data[metric_trend].idxmax(), 'Fecha']
                            st.metric(f"Mejor día {metric_trend}", str(best_day))
                else:
                    st.info("ℹ️ No hay suficientes fechas diferentes para mostrar tendencias temporales")
            else:
                st.warning("⚠️ No se pudieron parsear las fechas correctamente")
                
        except Exception as e:
            st.warning(f"⚠️ No se pudieron analizar tendencias temporales: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if network == 'tiktok':
        with tab2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🔥 Heatmap de Calor por Contenido")
            
            # Seleccionar métrica para heatmap
            heatmap_metric = st.selectbox(
                "Selecciona métrica para el heatmap:",
                ['visualizaciones_num', 'me_gusta_num', 'comentarios_num', 'engagement_rate'],
                format_func=lambda x: {
                    'visualizaciones_num': 'Vistas',
                    'me_gusta_num': 'Likes',
                    'comentarios_num': 'Comentarios',
                    'engagement_rate': 'Engagement Rate'
                }[x],
                key=f"heatmap_metric_{network}"
            )
            
            # Crear heatmap
            heatmap_title = f"Heatmap de Calor por {['Vistas', 'Likes', 'Comentarios', 'Engagement Rate'][['visualizaciones_num', 'me_gusta_num', 'comentarios_num', 'engagement_rate'].index(heatmap_metric)]}"
            fig = create_heatmap_chart(data, heatmap_metric, heatmap_title, config)
            st.pyplot(fig)
            
            # Explicación del heatmap
            st.info("""
            **📊 Interpretación del Heatmap:**
            - **Rojo intenso:** Contenido con mayor rendimiento
            - **Amarillo:** Contenido con rendimiento intermedio
            - **Verde intenso:** Contenido con menor rendimiento
            
            Los colores muestran el rendimiento relativo de cada video en la métrica seleccionada.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab de datos completos
    if network == 'tiktok':
        with tab3:
            show_data_table(data, config)
    else:
        with tab2:
            show_data_table(data, config)

def show_data_table(data, config):
    """Muestra la tabla completa de datos"""
    st.subheader("📋 Datos Completos")
    
    # Opciones de visualización
    view_col1, view_col2 = st.columns(2)
    
    with view_col1:
        show_all = st.checkbox("Mostrar todas las columnas", value=False, key=f"show_all_{config['name']}")
    
    with view_col2:
        rows_per_page = st.selectbox("Filas por página", [10, 25, 50, 100], index=1, key=f"rows_per_page_{config['name']}")
    
    # Seleccionar columnas para mostrar
    if show_all:
        display_cols = data.columns.tolist()
    else:
        display_cols = ['duracion_video', 'titulo', 'fecha_publicacion', 'privacidad', 
                       'visualizaciones', 'me_gusta', 'comentarios', 'engagement_rate']
    
    # Mostrar datos
    st.dataframe(
        data[display_cols],
        use_container_width=True,
        height=400,
        column_config={
            "duracion_video": "Duración",
            "titulo": "Título",
            "fecha_publicacion": "Fecha",
            "privacidad": "Privacidad",
            "visualizaciones": st.column_config.NumberColumn("Vistas", format="%d"),
            "me_gusta": st.column_config.NumberColumn("Likes", format="%d"),
            "comentarios": st.column_config.NumberColumn("Comentarios", format="%d"),
            "engagement_rate": st.column_config.NumberColumn("Engagement %", format="%.2f")
        }
    )
    
    # Estadísticas adicionales
    st.subheader("📊 Estadísticas de Datos")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        max_views = data['visualizaciones_num'].max()
        st.metric("Máx Vistas", f"{max_views:,}")
    
    with stat_col2:
        min_views = data['visualizaciones_num'].min()
        st.metric("Mín Vistas", f"{min_views:,}")
    
    with stat_col3:
        total_comments = data['comentarios_num'].sum()
        st.metric("Total Comentarios", f"{total_comments:,}")
    
    with stat_col4:
        std_engagement = data['engagement_rate'].std()
        st.metric("Desv. Estándar Engagement", f"{std_engagement:.2f}%")
    
    # Exportar datos
    st.subheader("💾 Exportar Datos")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        # Exportar a CSV
        csv_data = data[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv_data,
            file_name=f"{config['name'].lower()}_analytics.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with export_col2:
        # Exportar a Excel
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data[display_cols].to_excel(writer, index=False, sheet_name=f'{config["name"]} Data')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"{config['name'].lower()}_analytics.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
        except Exception as e:
            st.error(f"No se pudo crear archivo Excel: {str(e)}")

# =============================================
# APLICACIÓN PRINCIPAL
# =============================================
def main():
    # Manejar parámetros de URL para cambiar red
    query_params = st.query_params
    if 'network' in query_params:
        network = query_params['network']
        if network in NETWORK_CONFIG:
            st.session_state.current_network = network
    
    # Sidebar
    create_sidebar()
    
    # Header principal
    current_config = NETWORK_CONFIG[st.session_state.current_network]
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                margin-bottom: 30px; padding: 20px; background: white; 
                border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
        <div>
            <h1 style="margin: 0; color: #0f172a;">
                <i class="{current_config['icon']}" style="color: {current_config['color']}; margin-right: 15px;"></i>
                {current_config['name']} Analytics
            </h1>
            <p style="margin: 10px 0 0 0; color: #64748b;">
                Panel profesional para análisis de redes sociales
            </p>
        </div>
        <div style="background: {current_config['color']}; color: white; padding: 10px 25px; 
                    border-radius: 50px; font-weight: 600;">
            {'🟢 CONECTADO' if st.session_state.auth_status[st.session_state.current_network] else '🔴 DESCONECTADO'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs principales
    auth_tab, analytics_tab, settings_tab = st.tabs(["🔐 Autenticación", "📊 Análisis", "⚙️ Configuración"])
    
    with auth_tab:
        if st.session_state.auth_status[st.session_state.current_network]:
            st.success(f"✅ Estás conectado a {current_config['name']}")
            
            # Para redes con datos (TikTok y YouTube)
            if st.session_state.current_network in ['tiktok', 'youtube']:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Recargar Datos", use_container_width=True, type="primary"):
                        with st.spinner(f"Recargando datos de {current_config['name']}..."):
                            data, message = run_data_loader(st.session_state.current_network)
                            if not data.empty:
                                st.session_state.scraped_data[st.session_state.current_network] = data
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                
                with col2:
                    if st.button("📊 Ver Dashboard", use_container_width=True):
                        st.info("Cambia a la pestaña 'Análisis' para ver el dashboard")
                
                with col3:
                    if st.button("🚪 Desconectar", use_container_width=True):
                        st.session_state.auth_status[st.session_state.current_network] = False
                        st.rerun()
                
                # Mostrar resumen de datos
                if st.session_state.current_network in st.session_state.scraped_data:
                    data = st.session_state.scraped_data[st.session_state.current_network]
                    
                    # Información del archivo fuente
                    file_path = current_config['data_source']
                    file_exists = os.path.exists(file_path)
                    
                    st.info(f"""
                    **📊 Resumen de Datos:**
                    - **Videos Cargados:** {len(data)}
                    - **Vistas Totales:** {data['visualizaciones_num'].sum():,}
                    - **Likes Totales:** {data['me_gusta_num'].sum():,}
                    - **Engagement Promedio:** {data['engagement_rate'].mean():.1f}%
                    - **Fuente de Datos:** {'✅ Archivo encontrado' if file_exists else '❌ Archivo no encontrado'}
                    - **Última Actualización:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
                    """)
            
            else:
                if st.button("🚪 Desconectar", use_container_width=True):
                    st.session_state.auth_status[st.session_state.current_network] = False
                    st.rerun()
        
        else:
            show_auth_modal()
    
    with analytics_tab:
        if st.session_state.auth_status[st.session_state.current_network]:
            if st.session_state.current_network in ['tiktok', 'youtube']:
                show_social_dashboard(st.session_state.current_network)
            else:
                st.info(f"📊 Dashboard de análisis para {current_config['name']} próximamente!")
        else:
            st.warning(f"⚠️ Por favor autentícate con {current_config['name']} primero para ver los análisis.")
    
    with settings_tab:
        st.markdown("## ⚙️ Configuración")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 Configuración de Datos")
            
            # Ruta del archivo
            if st.session_state.current_network in ['tiktok', 'youtube']:
                config = NETWORK_CONFIG[st.session_state.current_network]
                file_path = config['data_source']
                file_exists = os.path.exists(file_path)
                
                st.metric("Estado del Archivo", "✅ Encontrado" if file_exists else "❌ No Encontrado")
                
                if file_exists:
                    try:
                        file_size = os.path.getsize(file_path) / 1024 / 1024  # MB
                        st.metric("Tamaño del Archivo", f"{file_size:.2f} MB")
                    except:
                        st.metric("Tamaño del Archivo", "Desconocido")
                
                if st.button("📂 Verificar Archivo", use_container_width=True):
                    if file_exists:
                        st.success(f"✅ Archivo encontrado en: {file_path}")
                        try:
                            # Intentar cargar el archivo para verificar
                            test_df = pd.read_excel(file_path, nrows=5)
                            st.success(f"✅ Archivo legible. Columnas: {', '.join(test_df.columns)}")
                            st.success(f"✅ Datos de muestra cargados: {len(test_df)} filas")
                        except Exception as e:
                            st.error(f"❌ Error leyendo archivo: {str(e)}")
                    else:
                        st.error(f"❌ Archivo no encontrado en: {file_path}")
        
        with col2:
            st.markdown("### 💾 Gestión de Datos")
            
            if st.button("💾 Respaldar Datos a JSON", use_container_width=True):
                # Crear backup de datos
                backup_data = {
                    'auth_status': st.session_state.auth_status,
                    'scraped_data': {},
                    'timestamp': datetime.now().isoformat()
                }
                
                for network, data in st.session_state.scraped_data.items():
                    if isinstance(data, pd.DataFrame):
                        backup_data['scraped_data'][network] = data.to_dict('records')
                
                st.download_button(
                    label="📥 Descargar Respaldo",
                    data=json.dumps(backup_data, indent=2, ensure_ascii=False),
                    file_name="social_dashboard_backup.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            if st.button("🗑️ Limpiar Todos los Datos", use_container_width=True, type="secondary"):
                for network in st.session_state.auth_status:
                    st.session_state.auth_status[network] = False
                st.session_state.scraped_data = {}
                st.session_state.data_loaded = False
                st.success("¡Todos los datos han sido limpiados exitosamente!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Información del Sistema")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            connected_count = sum(st.session_state.auth_status.values())
            st.metric("Redes Conectadas", f"{connected_count}/6")
        
        with info_col2:
            total_records = sum([len(data) for data in st.session_state.scraped_data.values() 
                               if isinstance(data, pd.DataFrame)])
            st.metric("Registros Totales", f"{total_records}")
        
        with info_col3:
            st.metric("Versión de la App", "1.1.0")

# =============================================
# EJECUCIÓN
# =============================================
if __name__ == "__main__":
    main()
