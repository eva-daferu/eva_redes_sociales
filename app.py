import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from io import BytesIO
import os
import sys
import requests

st.set_page_config(
    page_title="Social Dashboard - Panel Profesional",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp header {
        background-color: #2d3748 !important;
        height: 70px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
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
    st.session_state.current_network = 'tiktok'

if 'scraping_in_progress' not in st.session_state:
    st.session_state.scraping_in_progress = False

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'backend_data' not in st.session_state:
    st.session_state.backend_data = None

if 'backend_analytics' not in st.session_state:
    st.session_state.backend_analytics = {}

if 'last_backend_sync' not in st.session_state:
    st.session_state.last_backend_sync = None

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

BACKEND_URL = "https://pahubisas.pythonanywhere.com"

def load_tiktok_data_from_backend():
    try:
        st.session_state.scraping_in_progress = True
        response = requests.get(f"{BACKEND_URL}/data", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "success":
                data = result.get("data", [])
                analytics = result.get("analytics", {})
                df = pd.DataFrame(data)
                
                required_columns = ['duracion_video', 'titulo', 'fecha_publicacion', 
                                  'privacidad', 'visualizaciones', 'me_gusta', 'comentarios']
                
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    st.error(f"❌ Columnas faltantes: {missing_columns}")
                    return pd.DataFrame(), {}
                
                for col in ['visualizaciones', 'me_gusta', 'comentarios']:
                    if col in df.columns and df[col].dtype == 'object':
                        df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '')
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                if 'visualizaciones' in df.columns:
                    df['visualizaciones_num'] = df['visualizaciones'].fillna(0).astype(float)
                if 'me_gusta' in df.columns:
                    df['me_gusta_num'] = df['me_gusta'].fillna(0).astype(float)
                if 'comentarios' in df.columns:
                    df['comentarios_num'] = df['comentarios'].fillna(0).astype(float)
                
                if 'engagement_rate' not in df.columns:
                    mask = df['visualizaciones_num'] > 0
                    df['engagement_rate'] = 0.0
                    df.loc[mask, 'engagement_rate'] = ((df.loc[mask, 'me_gusta_num'] + df.loc[mask, 'comentarios_num']) / 
                                                      df.loc[mask, 'visualizaciones_num'] * 100).round(2)
                
                st.session_state.backend_data = df
                st.session_state.backend_analytics = analytics
                st.session_state.last_backend_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                return df, analytics
            else:
                st.error(f"❌ Error del backend: {result.get('message', 'Error desconocido')}")
                return pd.DataFrame(), {}
        else:
            st.error(f"❌ Error HTTP {response.status_code}")
            return pd.DataFrame(), {}
            
    except requests.exceptions.ConnectionError:
        st.error("❌ No se pudo conectar al servidor backend")
        return pd.DataFrame(), {}
    except requests.exceptions.Timeout:
        st.error("❌ Tiempo de espera agotado")
        return pd.DataFrame(), {}
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return pd.DataFrame(), {}
    finally:
        st.session_state.scraping_in_progress = False

def refresh_backend_data():
    try:
        response = requests.get(f"{BACKEND_URL}/refresh", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("status") == "success", result.get("message", "")
        else:
            return False, f"Error HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"Error al refrescar: {str(e)}"

def run_tiktok_scraper():
    try:
        df, analytics = load_tiktok_data_from_backend()
        
        if df.empty:
            st.error("❌ No se pudieron cargar datos del backend.")
            return pd.DataFrame()
        
        st.success(f"✅ Datos cargados: {len(df)} videos")
        return df
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

def create_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h2 style="color: white; margin: 0; font-weight: 700;">🌐 DASHBOARD</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 10px 0 0 0;">Panel Profesional</p>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            if st.button(
                f"{network_name} {status}",
                key=f"sidebar_{network_id}",
                use_container_width=True,
                type="primary" if st.session_state.current_network == network_id else "secondary"
            ):
                st.session_state.current_network = network_id
                st.rerun()
        
        st.markdown("---")
        
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
        
        if st.session_state.data_loaded and 'tiktok' in st.session_state.scraped_data:
            data = st.session_state.scraped_data['tiktok']
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: white; margin: 0 0 15px 0;">📊 Datos Cargados</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                    <strong>Videos:</strong> {len(data)}
                </p>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                    <strong>Vistas totales:</strong> {data['visualizaciones_num'].sum():,}
                </p>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                    <strong>Última actualización:</strong> {st.session_state.last_backend_sync or 'N/A'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.last_backend_sync:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: white; margin: 0 0 15px 0;">📊 Backend Status</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                    <strong>Última sincronización:</strong> {st.session_state.last_backend_sync}
                </p>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0; font-size: 14px;">
                    <strong>Estado:</strong> 🟢 Conectado
                </p>
            </div>
            """, unsafe_allow_html=True)

def show_auth_modal():
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    icon_color = config['color']
    if network == 'tiktok':
        icon_color = '#00f2ea'
    
    st.markdown("""
    <div class="modal-container">
        <div class="modal-frame">
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="network-icon-large">
        <i class="{config['icon']}" style="color: {icon_color}; font-size: 90px;"></i>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <h1 class="modal-title">Connect to <span class="social-network-name">{config['name']}</span>?</h1>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <p class="modal-subtitle">
        This will allow the dashboard to access your {config['name']} account data 
        to provide analytics, scheduling, and engagement metrics.
    </p>
    """, unsafe_allow_html=True)
    
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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("❌ Cancel", use_container_width=True, key="modal_cancel"):
                st.warning(f"Connection to {config['name']} cancelled")
        
        with button_col2:
            connect_key = f"modal_connect_{network}_{int(time.time())}"
            if st.button(f"🔗 Connect", use_container_width=True, key=connect_key, type="primary"):
                if network == 'tiktok':
                    st.session_state.scraping_in_progress = True
                    
                    with st.spinner("📂 Loading REAL data from Excel..."):
                        progress_bar = st.progress(0)
                        
                        df, analytics = load_tiktok_data_from_backend()
                        
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        if not df.empty:
                            st.session_state.auth_status[network] = True
                            st.session_state.scraped_data[network] = df
                            st.session_state.data_loaded = True
                            st.session_state.backend_analytics = analytics
                            st.session_state.last_backend_sync = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            st.success(f"✅ REAL data loaded: {len(df)} videos")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Could not load REAL data")
                            st.session_state.scraping_in_progress = False
                
                else:
                    with st.spinner(f"Authenticating with {config['name']}..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)
                        
                        st.session_state.auth_status[network] = True
                        st.success(f"✅ Connected to {config['name']}!")
                        time.sleep(1)
                        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_tiktok_dashboard():
    if 'tiktok' not in st.session_state.scraped_data:
        st.info("ℹ️ First authenticate with TikTok to view analytics")
        return
    
    data = st.session_state.scraped_data['tiktok']
    config = NETWORK_CONFIG['tiktok']
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {config['color']} 0%, #333333 100%); 
                padding: 30px; border-radius: 20px; color: white; margin-bottom: 40px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; display: flex; align-items: center; gap: 20px;">
            <i class="{config['icon']}" style="font-size: 50px; color: #00f2ea;"></i>
            TikTok Analytics Dashboard - DATOS REALES
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 18px;">
            Análisis de métricas REALES de tus videos de TikTok desde Excel
        </p>
        <p style="color: rgba(255,255,255,0.7); margin: 10px 0 0 0; font-size: 14px;">
            📅 Última actualización: {st.session_state.last_backend_sync or 'N/A'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    refresh_col1, refresh_col2, refresh_col3 = st.columns([1, 2, 1])
    with refresh_col2:
        if st.button("🔄 REFRESCAR DATOS REALES", use_container_width=True, type="primary"):
            with st.spinner("Refrescando datos REALES..."):
                success, message = refresh_backend_data()
                if success:
                    df, analytics = load_tiktok_data_from_backend()
                    if not df.empty:
                        st.session_state.scraped_data['tiktok'] = df
                        st.session_state.backend_analytics = analytics
                        st.success("✅ Datos REALES refrescados!")
                        st.rerun()
                    else:
                        st.error("❌ No se pudieron cargar los datos")
                else:
                    st.error(f"❌ {message}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_videos = len(data)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-video"></i></div>
            <div class="metric-value">{total_videos}</div>
            <div class="metric-label">Total Videos REALES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_views = int(data['visualizaciones_num'].sum())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-eye"></i></div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-label">Total Views REALES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_likes = int(data['me_gusta_num'].sum())
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-heart"></i></div>
            <div class="metric-value">{total_likes:,}</div>
            <div class="metric-label">Total Likes REALES</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_engagement = data['engagement_rate'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon"><i class="fas fa-chart-line"></i></div>
            <div class="metric-value">{avg_engagement:.1f}%</div>
            <div class="metric-label">Avg. Engagement REAL</div>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance", "📈 Trends", "🔍 Filters", "📋 Raw Data"])
    
    with tab1:
        st.subheader("🎯 Top Performing Videos REALES")
        
        top_col1, top_col2 = st.columns(2)
        with top_col1:
            top_n = st.slider("Number of top videos", 5, 20, 10, key="top_n_slider")
        
        with top_col2:
            metric_option = st.selectbox(
                "Rank by metric:",
                ['visualizaciones_num', 'me_gusta_num', 'comentarios_num', 'engagement_rate'],
                format_func=lambda x: {
                    'visualizaciones_num': 'Views',
                    'me_gusta_num': 'Likes',
                    'comentarios_num': 'Comments',
                    'engagement_rate': 'Engagement Rate'
                }[x],
                key="metric_select"
            )
        
        top_videos = data.nlargest(top_n, metric_option).copy()
        
        if metric_option == 'engagement_rate':
            chart_data = top_videos[['titulo', metric_option]]
            chart_data['titulo_short'] = chart_data['titulo'].str[:30] + '...'
            st.bar_chart(chart_data.set_index('titulo_short')[metric_option])
        else:
            chart_data = top_videos[['titulo', metric_option]]
            chart_data['titulo_short'] = chart_data['titulo'].str[:30] + '...'
            st.bar_chart(chart_data.set_index('titulo_short')[metric_option])
        
        st.subheader(f"📋 Top {top_n} Videos Details")
        display_cols = ['titulo', 'fecha_publicacion', 'visualizaciones', 
                       'me_gusta', 'comentarios', 'engagement_rate']
        st.dataframe(
            top_videos[display_cols],
            use_container_width=True,
            height=400,
            column_config={
                "titulo": "Title",
                "fecha_publicacion": "Date",
                "visualizaciones": st.column_config.NumberColumn("Views", format="%d"),
                "me_gusta": st.column_config.NumberColumn("Likes", format="%d"),
                "comentarios": st.column_config.NumberColumn("Comments", format="%d"),
                "engagement_rate": st.column_config.NumberColumn("Engagement %", format="%.2f")
            }
        )
    
    with tab2:
        st.subheader("📅 Performance Over Time")
        
        try:
            date_formats = ['%d %b, %H:%M', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d %b %Y']
            
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
                
                if len(data_with_dates['fecha_dt'].dt.date.unique()) > 1:
                    daily_data = data_with_dates.groupby(data_with_dates['fecha_dt'].dt.date).agg({
                        'visualizaciones_num': 'sum',
                        'me_gusta_num': 'sum',
                        'comentarios_num': 'sum',
                        'engagement_rate': 'mean'
                    }).reset_index()
                    
                    daily_data.columns = ['Fecha', 'Vistas', 'Likes', 'Comentarios', 'Engagement']
                    
                    metric_trend = st.selectbox(
                        "Select metric for trend:",
                        ['Vistas', 'Likes', 'Comentarios', 'Engagement'],
                        key="trend_metric"
                    )
                    
                    if metric_trend == 'Engagement':
                        st.line_chart(daily_data.set_index('Fecha')['Engagement'])
                    else:
                        st.line_chart(daily_data.set_index('Fecha')[metric_trend])
                    
                    if len(daily_data) > 1:
                        st.subheader("📈 Trend Analysis")
                        trend_col1, trend_col2, trend_col3 = st.columns(3)
                        
                        with trend_col1:
                            growth = ((daily_data[metric_trend].iloc[-1] - daily_data[metric_trend].iloc[0]) / 
                                     daily_data[metric_trend].iloc[0] * 100)
                            st.metric(f"Crecimiento {metric_trend}", f"{growth:.1f}%")
                        
                        with trend_col2:
                            avg_daily = daily_data[metric_trend].mean()
                            st.metric(f"Promedio diario {metric_trend}", f"{avg_daily:,.0f}")
                        
                        with trend_col3:
                            best_day = daily_data.loc[daily_data[metric_trend].idxmax(), 'Fecha']
                            st.metric(f"Mejor día {metric_trend}", str(best_day))
                else:
                    st.info("ℹ️ No hay suficientes fechas diferentes")
            else:
                st.warning("⚠️ No se pudieron parsear las fechas")
                
        except Exception as e:
            st.warning(f"⚠️ No se pudieron analizar tendencias")
    
    with tab3:
        st.subheader("🔍 Filter and Analyze")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            min_views = int(data['visualizaciones_num'].min())
            max_views = int(data['visualizaciones_num'].max())
            views_range = st.slider(
                "Views Range",
                min_views, max_views, (min_views, max_views),
                key="views_filter"
            )
        
        with filter_col2:
            min_likes = int(data['me_gusta_num'].min())
            max_likes = int(data['me_gusta_num'].max())
            likes_range = st.slider(
                "Likes Range",
                min_likes, max_likes, (min_likes, max_likes),
                key="likes_filter"
            )
        
        with filter_col3:
            privacy_options = data['privacidad'].unique()
            selected_privacy = st.multiselect(
                "Privacy Settings",
                privacy_options,
                default=privacy_options,
                key="privacy_filter"
            )
        
        filtered_data = data[
            (data['visualizaciones_num'] >= views_range[0]) &
            (data['visualizaciones_num'] <= views_range[1]) &
            (data['me_gusta_num'] >= likes_range[0]) &
            (data['me_gusta_num'] <= likes_range[1]) &
            (data['privacidad'].isin(selected_privacy))
        ]
        
        st.subheader(f"📊 Filtered Results: {len(filtered_data)} videos")
        
        if not filtered_data.empty:
            metric_f1, metric_f2, metric_f3 = st.columns(3)
            
            with metric_f1:
                avg_views_filtered = filtered_data['visualizaciones_num'].mean()
                st.metric("Avg Views (filtered)", f"{avg_views_filtered:,.0f}")
            
            with metric_f2:
                avg_engagement_filtered = filtered_data['engagement_rate'].mean()
                st.metric("Avg Engagement (filtered)", f"{avg_engagement_filtered:.1f}%")
            
            with metric_f3:
                total_comments_filtered = filtered_data['comentarios_num'].sum()
                st.metric("Total Comments (filtered)", f"{total_comments_filtered:,.0f}")
            
            st.subheader("📊 Distribution by Privacy")
            privacy_dist = filtered_data['privacidad'].value_counts()
            st.bar_chart(privacy_dist)
            
            st.subheader("⏱️ Average Video Duration")
            
            def duration_to_seconds(duration_str):
                try:
                    if pd.isna(duration_str):
                        return 0
                    parts = str(duration_str).split(':')
                    if len(parts) == 2:
                        minutes = int(parts[0])
                        seconds = int(parts[1])
                        return minutes * 60 + seconds
                    return 0
                except:
                    return 0
            
            filtered_data['duracion_segundos'] = filtered_data['duracion_video'].apply(duration_to_seconds)
            avg_duration = filtered_data['duracion_segundos'].mean()
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.metric("Average Duration", f"{avg_duration:.0f} seconds")
            
            with col_d2:
                st.metric("Average Duration", f"{avg_duration/60:.1f} minutes")
            
            st.subheader("📈 Engagement vs Views Analysis")
            
            scatter_data = filtered_data[['visualizaciones_num', 'engagement_rate', 'titulo']].copy()
            scatter_data['titulo_short'] = scatter_data['titulo'].str[:20] + '...'
            
            scatter_chart_data = scatter_data[['visualizaciones_num', 'engagement_rate']].copy()
            scatter_chart_data.columns = ['Views', 'Engagement Rate %']
            st.scatter_chart(scatter_chart_data)
            
        else:
            st.warning("⚠️ No hay videos que coincidan con los filtros")
    
    with tab4:
        st.subheader("📋 Complete TikTok Data REALES")
        
        view_col1, view_col2 = st.columns(2)
        
        with view_col1:
            show_all = st.checkbox("Show all columns", value=False)
        
        with view_col2:
            rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
        
        if show_all:
            display_cols = data.columns.tolist()
        else:
            display_cols = ['duracion_video', 'titulo', 'fecha_publicacion', 'privacidad', 
                           'visualizaciones', 'me_gusta', 'comentarios', 'engagement_rate']
        
        st.dataframe(
            data[display_cols],
            use_container_width=True,
            height=600,
            column_config={
                "duracion_video": "Duration",
                "titulo": "Title",
                "fecha_publicacion": "Date",
                "privacidad": "Privacy",
                "visualizaciones": st.column_config.NumberColumn("Views", format="%d"),
                "me_gusta": st.column_config.NumberColumn("Likes", format="%d"),
                "comentarios": st.column_config.NumberColumn("Comments", format="%d"),
                "engagement_rate": st.column_config.NumberColumn("Engagement %", format="%.2f")
            }
        )
        
        st.subheader("📊 Data Statistics")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            max_views = data['visualizaciones_num'].max()
            st.metric("Max Views", f"{max_views:,}")
        
        with stat_col2:
            min_views = data['visualizaciones_num'].min()
            st.metric("Min Views", f"{min_views:,}")
        
        with stat_col3:
            total_comments = data['comentarios_num'].sum()
            st.metric("Total Comments", f"{total_comments:,}")
        
        with stat_col4:
            std_engagement = data['engagement_rate'].std()
            st.metric("Std Dev Engagement", f"{std_engagement:.2f}%")
        
        st.subheader("💾 Export Data REALES")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            csv_data = data[display_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="tiktok_analytics_reales.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
        
        with export_col2:
            try:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    data[display_cols].to_excel(writer, index=False, sheet_name='TikTok Data REALES')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name="tiktok_analytics_reales.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error(f"No se pudo crear archivo Excel")

def main():
    create_sidebar()
    
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
                Professional dashboard for social media analytics - DATOS REALES
            </p>
            <p style="margin: 5px 0 0 0; color: #94a3b8; font-size: 14px;">
                Backend: {BACKEND_URL} | Última sincronización: {st.session_state.last_backend_sync or 'N/A'}
            </p>
        </div>
        <div style="background: {current_config['color']}; color: white; padding: 10px 25px; 
                    border-radius: 50px; font-weight: 600;">
            { '🟢 CONNECTED' if st.session_state.auth_status[st.session_state.current_network] else '🔴 DISCONNECTED' }
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    auth_tab, analytics_tab, settings_tab = st.tabs(["🔐 Authentication", "📊 Analytics", "⚙️ Settings"])
    
    with auth_tab:
        if st.session_state.auth_status[st.session_state.current_network]:
            st.success(f"✅ You are connected to {current_config['name']}")
            
            if st.session_state.current_network == 'tiktok':
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Reload Data REALES", use_container_width=True, type="primary"):
                        with st.spinner("Reloading TikTok REAL data..."):
                            data = run_tiktok_scraper()
                            if not data.empty:
                                st.session_state.scraped_data['tiktok'] = data
                                st.success(f"✅ Reloaded {len(data)} TikTok videos REALES!")
                                st.rerun()
                
                with col2:
                    if st.button("📊 View Dashboard", use_container_width=True):
                        st.info("Cambia a la pestaña 'Analytics' para ver el dashboard")
                
                with col3:
                    if st.button("🚪 Disconnect", use_container_width=True):
                        st.session_state.auth_status['tiktok'] = False
                        st.session_state.scraped_data.pop('tiktok', None)
                        st.session_state.data_loaded = False
                        st.rerun()
                
                if 'tiktok' in st.session_state.scraped_data:
                    data = st.session_state.scraped_data['tiktok']
                    
                    backend_status = "🟢 Conectado" if st.session_state.last_backend_sync else "🔴 Desconectado"
                    
                    st.info(f"""
                    **📊 Data Summary REALES:**
                    - **Videos Loaded:** {len(data)}
                    - **Total Views:** {data['visualizaciones_num'].sum():,}
                    - **Total Likes:** {data['me_gusta_num'].sum():,}
                    - **Average Engagement:** {data['engagement_rate'].mean():.1f}%
                    - **Backend Status:** {backend_status}
                    - **Last Updated:** {st.session_state.last_backend_sync or 'N/A'}
                    """)
                    
                    if st.button("🔄 REFRESCAR DESDE BACKEND", use_container_width=True):
                        with st.spinner("Refrescando desde backend..."):
                            success, message = refresh_backend_data()
                            if success:
                                df, analytics = load_tiktok_data_from_backend()
                                if not df.empty:
                                    st.session_state.scraped_data['tiktok'] = df
                                    st.session_state.backend_analytics = analytics
                                    st.success("✅ Datos REALES refrescados desde backend!")
                                    st.rerun()
                                else:
                                    st.error("❌ No se pudieron cargar los datos")
                            else:
                                st.error(f"❌ {message}")
            
            else:
                if st.button("🚪 Disconnect", use_container_width=True):
                    st.session_state.auth_status[st.session_state.current_network] = False
                    st.rerun()
        
        else:
            show_auth_modal()
    
    with analytics_tab:
        if st.session_state.auth_status[st.session_state.current_network]:
            if st.session_state.current_network == 'tiktok':
                show_tiktok_dashboard()
            else:
                st.info(f"📊 Analytics dashboard for {current_config['name']} coming soon!")
        else:
            st.warning(f"⚠️ Please authenticate with {current_config['name']} first to view analytics.")
    
    with settings_tab:
        st.markdown("## ⚙️ Configuration Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 Backend Settings")
            
            backend_status = "🟢 Conectado" if st.session_state.last_backend_sync else "🔴 Desconectado"
            st.metric("Backend Status", backend_status)
            
            if st.session_state.last_backend_sync:
                st.metric("Last Sync", st.session_state.last_backend_sync)
            
            if st.button("🔍 Test Backend Connection", use_container_width=True):
                try:
                    response = requests.get(f"{BACKEND_URL}/health", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ Backend connection successful!")
                    else:
                        st.error(f"❌ Backend responded with status: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Cannot connect to backend: {str(e)}")
            
            if st.button("🔄 Force Backend Refresh", use_container_width=True):
                with st.spinner("Forcing backend refresh..."):
                    success, message = refresh_backend_data()
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        
        with col2:
            st.markdown("### 💾 Data Management")
            
            if st.button("💾 Backup Data to JSON", use_container_width=True):
                backup_data = {
                    'auth_status': st.session_state.auth_status,
                    'scraped_data': {}
                }
                
                for network, data in st.session_state.scraped_data.items():
                    if isinstance(data, pd.DataFrame):
                        backup_data['scraped_data'][network] = data.to_dict('records')
                
                st.download_button(
                    label="📥 Download Backup",
                    data=json.dumps(backup_data, indent=2),
                    file_name="social_dashboard_backup.json",
                    mime="application/json"
                )
            
            if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
                for network in st.session_state.auth_status:
                    st.session_state.auth_status[network] = False
                st.session_state.scraped_data = {}
                st.session_state.data_loaded = False
                st.session_state.backend_data = None
                st.session_state.backend_analytics = {}
                st.session_state.last_backend_sync = None
                st.success("All data cleared successfully!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 System Information")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            connected_count = sum(st.session_state.auth_status.values())
            st.metric("Connected Networks", f"{connected_count}/5")
        
        with info_col2:
            total_records = sum([len(data) for data in st.session_state.scraped_data.values() 
                               if isinstance(data, pd.DataFrame)])
            st.metric("Total Records", f"{total_records}")
        
        with info_col3:
            st.metric("App Version", "2.0.0")
        
        st.markdown("---")
        st.markdown("### 🔗 Backend Information")
        st.code(f"URL: {BACKEND_URL}")
        st.code(f"Status: {'🟢 Online' if st.session_state.last_backend_sync else '🔴 Offline'}")
        st.code(f"Last Sync: {st.session_state.last_backend_sync or 'Never'}")

if __name__ == "__main__":
    main()
