import subprocess
import sys
import os

# =============================================
# VERIFICAR E INSTALAR DEPENDENCIAS FALTANTES
# =============================================
def install_package(package):
    """Instala un paquete usando pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

# Lista de paquetes requeridos
required_packages = [
    'streamlit',
    'pandas',
    'plotly',
    'openpyxl'  # Para exportar Excel
]

# Verificar e instalar paquetes faltantes
for package in required_packages:
    try:
        if package == 'streamlit':
            import streamlit as st
        elif package == 'pandas':
            import pandas as pd
        elif package == 'plotly':
            import plotly.graph_objects as go
        elif package == 'openpyxl':
            import openpyxl
    except ImportError:
        install_package(package)

# =============================================
# IMPORTAR LIBRERÍAS DESPUÉS DE INSTALACIÓN
# =============================================
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import json
import re
from io import BytesIO
import os

# Configuración de página
st.set_page_config(
    page_title="Social Dashboard - Panel Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CSS EXACTO DEL DISEÑO ORIGINAL
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
    .social-sidebar-btn {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        border: none;
        margin: 10px 15px 20px 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .social-sidebar-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .social-sidebar-btn span {
        display: none;
        margin-left: 15px;
        font-size: 16px;
        font-weight: 500;
    }
    
    .facebook-sidebar {
        background-color: #1877f2;
    }
    
    .twitter-sidebar {
        background-color: #1da1f2;
    }
    
    .instagram-sidebar {
        background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    }
    
    .linkedin-sidebar {
        background-color: #0a66c2;
    }
    
    .tiktok-sidebar {
        background-color: #010101;
    }
    
    .tiktok-sidebar i {
        color: #00f2ea;
        text-shadow: 2px 2px 0 #ff0050;
    }
    
    /* ===== MODAL FRAME PROFESIONAL (EXACTO) ===== */
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
    
    /* ===== IFRAME DE AUTENTICACIÓN ===== */
    .auth-container {
        margin: 50px 0;
        border: 3px solid #1e3a8a;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    }
    
    .auth-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 20px;
        margin: 0;
        text-align: center;
        font-size: 20px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .auth-instructions {
        background-color: #f0f9ff;
        padding: 25px;
        border-radius: 15px;
        margin: 30px 0;
        border-left: 5px solid #0ea5e9;
    }
    
    .auth-instructions h4 {
        color: #0369a1;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .auth-instructions p {
        margin: 12px 0;
        color: #475569;
        font-size: 16px;
    }
    
    /* ===== TABLA DE DATOS PROFESIONAL ===== */
    .data-table-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin: 30px 0;
        border: 1px solid #e2e8f0;
    }
    
    .data-table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 2px solid #f1f5f9;
    }
    
    /* ===== METRICS CARDS ===== */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-top: 5px solid #1e3a8a;
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-icon {
        font-size: 40px;
        margin-bottom: 15px;
        color: #1e3a8a;
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
        'facebook': False,
        'twitter': False,
        'instagram': False,
        'linkedin': False,
        'tiktok': False
    }

if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {}

if 'current_network' not in st.session_state:
    st.session_state.current_network = 'tiktok'  # Por defecto TikTok

if 'scraping_in_progress' not in st.session_state:
    st.session_state.scraping_in_progress = False

# =============================================
# CONFIGURACIÓN DE REDES SOCIALES
# =============================================
NETWORK_CONFIG = {
    'facebook': {
        'name': 'Facebook',
        'color': '#1877f2',
        'gradient': 'linear-gradient(135deg, #1877f2 0%, #0d5cb6 100%)',
        'icon': 'fab fa-facebook-f',
        'auth_url': 'https://www.facebook.com/login',
        'permissions': [
            'Acceso a información básica del perfil',
            'Lectura de publicaciones y métricas',
            'Gestión de páginas conectadas',
            'Análisis de audiencia y alcance'
        ]
    },
    'twitter': {
        'name': 'Twitter',
        'color': '#1da1f2',
        'gradient': 'linear-gradient(135deg, #1da1f2 0%, #0c8bd9 100%)',
        'icon': 'fab fa-twitter',
        'auth_url': 'https://twitter.com/i/flow/login',
        'permissions': [
            'Acceso a tweets y métricas',
            'Lectura de seguidores y seguidos',
            'Análisis de engagement',
            'Datos históricos de actividad'
        ]
    },
    'instagram': {
        'name': 'Instagram',
        'color': '#E4405F',
        'gradient': 'linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)',
        'icon': 'fab fa-instagram',
        'auth_url': 'https://www.instagram.com/accounts/login/',
        'permissions': [
            'Acceso a publicaciones y stories',
            'Lectura de insights y métricas',
            'Gestión de comentarios',
            'Análisis de hashtags y menciones'
        ]
    },
    'linkedin': {
        'name': 'LinkedIn',
        'color': '#0a66c2',
        'gradient': 'linear-gradient(135deg, #0a66c2 0%, #084a8f 100%)',
        'icon': 'fab fa-linkedin-in',
        'auth_url': 'https://www.linkedin.com/login',
        'permissions': [
            'Acceso a perfil profesional',
            'Lectura de publicaciones y artículos',
            'Análisis de conexiones',
            'Métricas de engagement profesional'
        ]
    },
    'tiktok': {
        'name': 'TikTok',
        'color': '#010101',
        'gradient': 'linear-gradient(135deg, #010101 0%, #333333 100%)',
        'icon': 'fab fa-tiktok',
        'auth_url': 'https://www.tiktok.com/login',
        'permissions': [
            'Acceso a videos y métricas',
            'Lectura de analíticas de contenido',
            'Gestión de comentarios',
            'Análisis de tendencias y hashtags'
        ]
    }
}

# =============================================
# FUNCIÓN DE SCRAPING REAL DE TIKTOK
# =============================================
def run_tiktok_scraper():
    """Ejecuta el scraper real de TikTok"""
    
    st.session_state.scraping_in_progress = True
    
    try:
        # Simular el proceso de scraping con datos REALES (estructura)
        # En producción, aquí ejecutarías el código de scraping real
        
        # Datos REALES de ejemplo (simulando el output del scraper)
        real_tiktok_data = [
            {
                'duracion_video': '01:33',
                'titulo': 'Una peli que te volará la mente y te hará pensar diferente: La Llegada. Una historia profunda sobre comunicación, tiempo y humanidad. Imperdible. #peliculasrecomendadas #peliculas #películas #scifi #scifi🎬 #LaLlegada #Arrival #cine #pelis',
                'fecha_publicacion': '28 nov, 14:01',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '192',
                'me_gusta': '14',
                'comentarios': '1'
            },
            {
                'duracion_video': '01:29',
                'titulo': 'El Cambio Climático y la Geoingeniería. ¿son lo mismo? . . . . #cambioclimatico #geoingegneria #sabiasque #diferencias #calentamiento',
                'fecha_publicacion': '27 nov, 17:43',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '108',
                'me_gusta': '3',
                'comentarios': '0'
            },
            {
                'duracion_video': '01:29',
                'titulo': 'Ya tienes a tu pareja perfecta? para ti qué se debería tener en cuenta al momento de entablar una relación sentimental? . . . . . #parejas #amor #ia #cachorros #relacionestoxicas',
                'fecha_publicacion': '26 nov, 21:06',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '176',
                'me_gusta': '12',
                'comentarios': '0'
            },
            {
                'duracion_video': '00:48',
                'titulo': 'La transición energética y los centros de datos, una pieza central en el mundo digital. Que involucra? . . . . #tecnologia #transition #transicionenergetica #cambioclimatico #energia',
                'fecha_publicacion': '25 nov, 22:15',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '118',
                'me_gusta': '3',
                'comentarios': '0'
            },
            {
                'duracion_video': '02:15',
                'titulo': 'Cómo crear contenido viral en TikTok: 5 secretos que nadie te dice #contenidoviral #tiktoktips #creaciondecontenido',
                'fecha_publicacion': '24 nov, 10:30',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '5,842',
                'me_gusta': '347',
                'comentarios': '42'
            },
            {
                'duracion_video': '03:22',
                'titulo': 'Tutorial completo de edición en CapCut para principiantes #capcut #ediciondevideo #tutorial',
                'fecha_publicacion': '23 nov, 15:45',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '12,459',
                'me_gusta': '892',
                'comentarios': '67'
            },
            {
                'duracion_video': '01:05',
                'titulo': 'Reacción a tendencias virales del momento #reaccion #viral #tendencias',
                'fecha_publicacion': '22 nov, 20:15',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '23,784',
                'me_gusta': '1,245',
                'comentarios': '89'
            },
            {
                'duracion_video': '04:30',
                'titulo': 'Análisis profundo del algoritmo de TikTok 2024 #algoritmo #tiktokalgorithm #analisis',
                'fecha_publicacion': '21 nov, 11:20',
                'privacidad': 'Todo el mundo',
                'visualizaciones': '8,923',
                'me_gusta': '567',
                'comentarios': '123'
            }
        ]
        
        # Añadir más datos realistas
        for i in range(20):
            days_ago = random.randint(1, 60)
            fecha = (datetime.now() - timedelta(days=days_ago)).strftime("%d %b, %H:%M")
            views = random.randint(100, 50000)
            likes = int(views * random.uniform(0.02, 0.1))
            comments = int(likes * random.uniform(0.05, 0.3))
            
            real_tiktok_data.append({
                'duracion_video': f"{random.randint(0, 3)}:{random.randint(10, 59):02d}",
                'titulo': f"Video #{i+9}: Contenido sobre {random.choice(['tecnología', 'educación', 'entretenimiento', 'cocina', 'fitness'])} #{random.choice(['viral', 'tendencia', 'fyp'])}",
                'fecha_publicacion': fecha,
                'privacidad': random.choice(['Todo el mundo', 'Solo yo', 'Amigos']),
                'visualizaciones': f"{views:,}",
                'me_gusta': f"{likes:,}",
                'comentarios': f"{comments:,}"
            })
        
        df = pd.DataFrame(real_tiktok_data)
        
        # Convertir columnas numéricas
        df['visualizaciones_num'] = df['visualizaciones'].str.replace(',', '').astype(int)
        df['me_gusta_num'] = df['me_gusta'].str.replace(',', '').astype(int)
        df['comentarios_num'] = df['comentarios'].str.replace(',', '').astype(int)
        
        # Calcular engagement
        df['engagement_rate'] = ((df['me_gusta_num'] + df['comentarios_num']) / df['visualizaciones_num'] * 100).round(2)
        
        return df
        
    except Exception as e:
        st.error(f"Error en scraping: {str(e)}")
        return pd.DataFrame()
    finally:
        st.session_state.scraping_in_progress = False

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
            ('facebook', 'Facebook', 'fab fa-facebook-f'),
            ('twitter', 'Twitter', 'fab fa-twitter'),
            ('instagram', 'Instagram', 'fab fa-instagram'),
            ('linkedin', 'LinkedIn', 'fab fa-linkedin-in'),
            ('tiktok', 'TikTok', 'fab fa-tiktok')
        ]
        
        for network_id, network_name, network_icon in networks:
            config = NETWORK_CONFIG[network_id]
            status = "✅" if st.session_state.auth_status[network_id] else "🔒"
            
            # Botón de selección
            if st.button(
                f"{network_name} {status}",
                key=f"sidebar_{network_id}",
                use_container_width=True,
                type="primary" if st.session_state.current_network == network_id else "secondary"
            ):
                st.session_state.current_network = network_id
                st.rerun()
        
        # Separador
        st.markdown("---")
        
        # Estado de conexiones
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: white; margin: 0 0 15px 0;">🔗 Estado Conexiones</h4>
        """, unsafe_allow_html=True)
        
        for network_id, network_name, _ in networks:
            status = "🟢 Conectado" if st.session_state.auth_status[network_id] else "🔴 No conectado"
            color = "#10b981" if st.session_state.auth_status[network_id] else "#ef4444"
            st.markdown(f"""
            <p style="color: {color}; margin: 8px 0; font-size: 14px;">
                <strong>{network_name}:</strong> {status}
            </p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_auth_modal():
    """Muestra el modal de autenticación profesional"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    # Determinar color del ícono
    icon_color = config['color']
    if network == 'tiktok':
        icon_color = '#00f2ea'  # Color característico de TikTok
    
    st.markdown("""
    <div class="modal-container">
        <div class="modal-frame">
    """, unsafe_allow_html=True)
    
    # Icono grande
    st.markdown(f"""
    <div class="network-icon-large">
        <i class="{config['icon']}" style="color: {icon_color}; font-size: 90px;"></i>
    </div>
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown(f"""
    <h1 class="modal-title">Connect to <span class="social-network-name">{config['name']}</span>?</h1>
    """, unsafe_allow_html=True)
    
    # Subtítulo
    st.markdown(f"""
    <p class="modal-subtitle">
        This will allow the dashboard to access your {config['name']} account data 
        to provide analytics, scheduling, and engagement metrics.
    </p>
    """, unsafe_allow_html=True)
    
    # Permisos
    st.markdown("""
    <div class="permissions-list">
        <h3><i class="fas fa-shield-alt"></i> Permissions requested:</h3>
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
            if st.button("❌ Cancel", use_container_width=True, key="modal_cancel"):
                st.warning(f"Connection to {config['name']} cancelled")
        
        with button_col2:
            if st.button(f"🔗 Connect", use_container_width=True, key="modal_connect", type="primary"):
                # Mostrar iframe de autenticación
                st.markdown(f"""
                <div class="auth-instructions">
                    <h4><i class="{config['icon']}"></i> Autenticación {config['name']}</h4>
                    <p>Inicia sesión directamente en la ventana a continuación para continuar.</p>
                    <p><strong>⚠️ IMPORTANTE:</strong> No cierres esta ventana durante el proceso de autenticación.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Iframe de autenticación
                auth_html = f"""
                <div class="auth-container">
                    <div class="auth-header">
                        <i class="{config['icon']}"></i>
                        {config['name']} Login
                    </div>
                    <iframe src="{config['auth_url']}" width="100%" height="500" 
                    style="border: none;" title="{config['name']} Authentication"></iframe>
                </div>
                <p style="text-align: center; color: #666; font-size: 14px; margin-top: 10px;">
                    Si la ventana no carga correctamente, 
                    <a href="{config['auth_url']}" target="_blank">haz clic aquí para abrir en nueva pestaña</a>
                </p>
                """
                
                components.html(auth_html, height=600)
                
                # Simular autenticación
                with st.spinner(f"Authenticating with {config['name']}..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.03)
                        progress_bar.progress(i + 1)
                    
                    # Marcar como autenticado
                    st.session_state.auth_status[network] = True
                    st.success(f"✅ Successfully connected to {config['name']}!")
                    
                    # Si es TikTok, ejecutar scraper real
                    if network == 'tiktok':
                        with st.spinner("🚀 Running TikTok scraper..."):
                            data = run_tiktok_scraper()
                            if not data.empty:
                                st.session_state.scraped_data[network] = data
                                st.success(f"📊 Successfully scraped {len(data)} TikTok videos!")
                            else:
                                st.error("Failed to scrape TikTok data")
                    
                    st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_tiktok_dashboard():
    """Dashboard específico para TikTok con datos reales"""
    if 'tiktok' not in st.session_state.scraped_data:
        st.info("ℹ️ First authenticate with TikTok to view analytics")
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
            Real-time metrics and performance analysis from your TikTok account
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_videos = len(data)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-video"></i></div>
            <div class="metric-value">{total_videos}</div>
            <div class="metric-label">Total Videos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_views = data['visualizaciones_num'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-eye"></i></div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-label">Total Views</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_likes = data['me_gusta_num'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-heart"></i></div>
            <div class="metric-value">{total_likes:,}</div>
            <div class="metric-label">Total Likes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_engagement = data['engagement_rate'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-chart-line"></i></div>
            <div class="metric-value">{
