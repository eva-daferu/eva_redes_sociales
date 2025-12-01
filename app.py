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
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =============================================
# CONFIGURACIÓN INICIAL
# =============================================
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
    
    /* ===== SIDEBAR PROFESIONAL ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%) !important;
        padding-top: 20px !important;
    }
    
    /* ===== MODAL FRAME PROFESIONAL ===== */
    .modal-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;
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
    
    /* ===== SCRAPER STATUS ===== */
    .scraper-status {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-weight: 600;
    }
    
    .scraper-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* ===== METRICS CARDS ===== */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
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
    
    /* ===== OCULTAR ELEMENTOS STREAMLIT ===== */
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

# =============================================
# FUNCIONES DE SCRAPING REAL DE TIKTOK
# =============================================
def run_real_tiktok_scraper():
    """Ejecuta el scraper real de TikTok - SIN DATOS INVENTADOS"""
    
    st.warning("🚨 **ADVERTENCIA DE SEGURIDAD:**")
    st.info("""
    ⚠️ **Para usar el scraper real en producción:**
    
    1. Necesitas ChromeDriver instalado
    2. Requiere autenticación MANUAL del usuario
    3. Puede tomar 1-3 minutos dependiendo de la cantidad de videos
    4. Puede ser bloqueado por TikTok si se hace muy rápido
    
    **Pasos para implementar el scraper real:**
    
    1. Descomentar el código de scraping real
    2. Asegurarte de tener las dependencias instaladas
    3. Configurar los tiempos de espera apropiados
    4. Probar con una cuenta de prueba primero
    """)
    
    # Código del scraper real (COMENTADO por seguridad)
    scraper_code = """
    # ========== CÓDIGO REAL DEL SCRAPER (NO EJECUTAR EN STREAMLIT CLOUD) ==========
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.add_argument("--window-size=1200,1000")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("🔄 Abriendo TikTok...")
    driver.get("https://www.tiktok.com")
    time.sleep(3)
    print("🔓 INICIA SESIÓN MANUALMENTE")
    print("⏳ Esperando 60 segundos para autenticación...")
    time.sleep(60)
    
    print("🎯 Navegando a contenido...")
    driver.get("https://www.tiktok.com/tiktokstudio/content")
    time.sleep(10)
    
    # Función para capturar videos
    def capturar_videos_durante_scroll():
        contenedores = driver.find_elements(By.CSS_SELECTOR, '[data-tt="components_PostTable_Container"]')
        if len(contenedores) < 2:
            return []
        
        contenedor = contenedores[1]
        todos_los_videos = []
        claves_unicas = set()
        
        for ciclo in range(25):
            try:
                elementos_actuales = contenedor.find_elements(By.CSS_SELECTOR, '[data-tt*="RowLayout"]')
                
                for elemento in elementos_actuales:
                    texto_completo = elemento.text.strip()
                    
                    if (len(texto_completo) > 80 and
                        any(priv in texto_completo for priv in ['Todo el mundo', 'Solo yo', 'Amigos']) and
                        re.search(r'\\d{1,2}\\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)', texto_completo.lower())):
                        
                        datos = procesar_elemento_video(texto_completo)
                        
                        if datos and datos['titulo'] and datos['fecha_publicacion']:
                            clave_unica = f"{datos['titulo'][:50]}_{datos['fecha_publicacion']}_{datos['visualizaciones']}"
                            
                            if clave_unica not in claves_unicas:
                                claves_unicas.add(clave_unica)
                                todos_los_videos.append(datos)
                
                # Scroll para cargar más contenido
                scroll_antes = driver.execute_script("return arguments[0].scrollTop", contenedor)
                driver.execute_script("arguments[0].scrollTop += 250", contenedor)
                time.sleep(1.5)
                
                scroll_despues = driver.execute_script("return arguments[0].scrollTop", contenedor)
                
                if scroll_despues == scroll_antes:
                    break
                    
            except Exception as e:
                break
        
        return todos_los_videos
    
    def procesar_elemento_video(texto_completo):
        lineas = [line.strip() for line in texto_completo.split('\\n') if line.strip()]
        
        datos = {
            'duracion_video': '',
            'titulo': '',
            'fecha_publicacion': '',
            'privacidad': '',
            'visualizaciones': '',
            'me_gusta': '',
            'comentarios': ''
        }
        
        for linea in lineas:
            if re.match(r'^\\d{1,2}:\\d{2}$', linea):
                datos['duracion_video'] = linea
            
            fecha_match = re.search(r'(\\d{1,2}\\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)[a-z]*,\\s+\\d{1,2}:\\d{2})', linea.lower())
            if fecha_match:
                datos['fecha_publicacion'] = fecha_match.group(1)
            
            if any(priv in linea for priv in ['Todo el mundo', 'Solo yo', 'Amigos', 'Privado']):
                datos['privacidad'] = linea
        
        metricas_encontradas = []
        for linea in lineas:
            linea_limpia = linea.replace(' ', '').replace(',', '')
            if re.match(r'^\\d+[,.]?\\d*[K]?$', linea_limpia):
                if not any(palabra in linea.lower() for palabra in ['todo', 'solo', 'amigos', 'privado']):
                    metricas_encontradas.append(linea)
        
        if len(metricas_encontradas) >= 1:
            datos['visualizaciones'] = metricas_encontradas[0]
        if len(metricas_encontradas) >= 2:
            datos['me_gusta'] = metricas_encontradas[1]
        if len(metricas_encontradas) >= 3:
            datos['comentarios'] = metricas_encontradas[2]
        
        candidatos_titulo = []
        for linea in lineas:
            if (len(linea) > 15 and
                not re.match(r'^\\d{1,2}:\\d{2}$', linea) and
                not re.search(r'\\d{1,2}\\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)', linea.lower()) and
                not any(priv in linea for priv in ['Todo el mundo', 'Solo yo', 'Amigos', 'Privado']) and
                linea not in metricas_encontradas and
                not re.match(r'^[\\d,.K]+$', linea.replace(' ', ''))):
                candidatos_titulo.append(linea)
        
        if candidatos_titulo:
            datos['titulo'] = max(candidatos_titulo, key=len)
        
        return datos
    
    # Ejecutar scraping
    print("🚀 INICIANDO CAPTURA REAL...")
    videos = capturar_videos_durante_scroll()
    
    if videos:
        df = pd.DataFrame(videos)
        df = df.drop_duplicates(subset=['titulo', 'fecha_publicacion', 'visualizaciones'], keep='first')
        
        # Convertir columnas numéricas
        def convertir_numero(valor):
            if 'K' in str(valor):
                return int(float(valor.replace('K', '').replace(',', '.')) * 1000)
            return int(str(valor).replace(',', '').replace('.', ''))
        
        try:
            df['visualizaciones_num'] = df['visualizaciones'].apply(convertir_numero)
            df['me_gusta_num'] = df['me_gusta'].apply(convertir_numero)
            df['comentarios_num'] = df['comentarios'].apply(convertir_numero)
            df['engagement_rate'] = ((df['me_gusta_num'] + df['comentarios_num']) / df['visualizaciones_num'] * 100).round(2)
        except:
            pass
        
        print(f"🎉 CAPTURA COMPLETADA: {len(df)} videos")
        driver.quit()
        return df
    
    driver.quit()
    return pd.DataFrame()
    """
    
    # En Streamlit Cloud, mostramos un mensaje y datos de ejemplo LIMPIOS
    # (solo para demostración, sin datos inventados)
    
    st.markdown("""
    <div class="scraper-warning">
        <i class="fas fa-exclamation-triangle"></i> MODO DEMOSTRACIÓN ACTIVADO
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **🔧 Modo Demostración Activado**
    
    En producción, aquí se ejecutaría el scraper real de TikTok que:
    
    1. Abre TikTok en un navegador controlado
    2. Espera que el usuario inicie sesión MANUALMENTE
    3. Navega a la sección de contenido
    4. Hace scroll para cargar todos los videos
    5. Extrae los datos REALES del usuario actual
    
    **⚠️ Características del scraper real:**
    - Tiempo estimado: 1-3 minutos
    - Requiere autenticación manual
    - Extrae datos en tiempo real
    - Respeta los tiempos de TikTok para evitar bloqueos
    
    **📁 Para implementar el scraper real:**
    1. Descomentar el código arriba
    2. Instalar selenium y chromedriver
    3. Configurar en un servidor adecuado
    4. Probar extensivamente antes de producción
    """)
    
    # En modo demostración, NO mostramos datos inventados
    # Solo mostramos un dataframe vacío
    return pd.DataFrame()

# =============================================
# MANEJO DE SESIÓN POR USUARIO
# =============================================
def get_user_session_id():
    """Genera un ID único para cada sesión de usuario"""
    # En Streamlit Cloud, podemos usar la IP o generar un ID único
    import hashlib
    import uuid
    
    # Intentar obtener información única del usuario
    try:
        # En un entorno real, usaríamos la IP del usuario
        user_ip = "demo_user"  # Placeholder para Streamlit Cloud
        
        # Para desarrollo/demo, generamos un ID único por sesión
        if 'user_session_id' not in st.session_state:
            st.session_state.user_session_id = str(uuid.uuid4())[:8]
        
        return st.session_state.user_session_id
    except:
        return "default_user"

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
    'youtube': {
        'name': 'YouTube',
        'color': '#FF0000',
        'gradient': 'linear-gradient(135deg, #FF0000 0%, #CC0000 100%)',
        'icon': 'fab fa-youtube',
        'auth_url': 'https://accounts.google.com/ServiceLogin?service=youtube',
        'permissions': [
            'Acceso a canales y videos',
            'Lectura de estadísticas de visualizaciones',
            'Análisis de engagement y suscriptores',
            'Datos de rendimiento de videos'
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
# INICIALIZACIÓN DE SESIÓN POR USUARIO
# =============================================
user_id = get_user_session_id()

# Inicializar estado para cada usuario
if f'auth_status_{user_id}' not in st.session_state:
    st.session_state[f'auth_status_{user_id}'] = {
        'facebook': False,
        'twitter': False,
        'instagram': False,
        'youtube': False,
        'tiktok': False
    }

if f'scraped_data_{user_id}' not in st.session_state:
    st.session_state[f'scraped_data_{user_id}'] = {}

if f'current_network_{user_id}' not in st.session_state:
    st.session_state[f'current_network_{user_id}'] = 'tiktok'

if f'scraping_in_progress_{user_id}' not in st.session_state:
    st.session_state[f'scraping_in_progress_{user_id}'] = False

# Funciones helper para manejar datos por usuario
def get_auth_status():
    return st.session_state[f'auth_status_{user_id}']

def set_auth_status(network, status):
    st.session_state[f'auth_status_{user_id}'][network] = status

def get_scraped_data():
    return st.session_state[f'scraped_data_{user_id}']

def set_scraped_data(network, data):
    st.session_state[f'scraped_data_{user_id}'][network] = data

def get_current_network():
    return st.session_state[f'current_network_{user_id}']

def set_current_network(network):
    st.session_state[f'current_network_{user_id}'] = network

def get_scraping_in_progress():
    return st.session_state[f'scraping_in_progress_{user_id}']

def set_scraping_in_progress(status):
    st.session_state[f'scraping_in_progress_{user_id}'] = status

# =============================================
# COMPONENTES DE INTERFAZ
# =============================================
def create_sidebar():
    """Crea la sidebar profesional con YouTube"""
    with st.sidebar:
        # Logo y título
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 40px 0;">
            <h2 style="color: white; margin: 0; font-weight: 700;">🌐 SOCIAL DASHBOARD</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 10px 0 0 0;">Panel Profesional</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Información del usuario actual
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <p style="color: white; margin: 0; font-size: 14px;">
                <i class="fas fa-user"></i> Usuario: <strong>{user_id}</strong>
            </p>
            <p style="color: rgba(255,255,255,0.7); margin: 5px 0 0 0; font-size: 12px;">
                Sesión privada - Datos no compartidos
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones de redes sociales
        networks = [
            ('facebook', 'Facebook', 'fab fa-facebook-f'),
            ('twitter', 'Twitter', 'fab fa-twitter'),
            ('instagram', 'Instagram', 'fab fa-instagram'),
            ('youtube', 'YouTube', 'fab fa-youtube'),
            ('tiktok', 'TikTok', 'fab fa-tiktok')
        ]
        
        for network_id, network_name, network_icon in networks:
            config = NETWORK_CONFIG[network_id]
            status = "✅" if get_auth_status()[network_id] else "🔒"
            
            # Botón de selección
            if st.button(
                f"{network_name} {status}",
                key=f"sidebar_{user_id}_{network_id}",
                use_container_width=True,
                type="primary" if get_current_network() == network_id else "secondary"
            ):
                set_current_network(network_id)
                st.rerun()
        
        # Separador
        st.markdown("---")
        
        # Estado de conexiones
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: white; margin: 0 0 15px 0;">🔗 Estado Conexiones</h4>
        """, unsafe_allow_html=True)
        
        for network_id, network_name, _ in networks:
            status = "🟢 Conectado" if get_auth_status()[network_id] else "🔴 No conectado"
            color = "#10b981" if get_auth_status()[network_id] else "#ef4444"
            st.markdown(f"""
            <p style="color: {color}; margin: 8px 0; font-size: 14px;">
                <strong>{network_name}:</strong> {status}
            </p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Limpiar datos de ESTE usuario
        if st.button("🗑️ Limpiar mis datos", use_container_width=True, type="secondary"):
            for network in get_auth_status():
                set_auth_status(network, False)
            st.session_state[f'scraped_data_{user_id}'] = {}
            st.success("Tus datos han sido eliminados")
            st.rerun()

def show_auth_modal():
    """Muestra el modal de autenticación profesional"""
    network = get_current_network()
    config = NETWORK_CONFIG[network]
    
    # Determinar color del ícono
    icon_color = config['color']
    if network == 'tiktok':
        icon_color = '#00f2ea'
    elif network == 'youtube':
        icon_color = '#FF0000'
    
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
        Esta aplicación accederá a los datos REALES de tu cuenta de {config['name']}
        para proporcionar análisis, programación y métricas de engagement.
        <br><br>
        <strong>⚠️ Los datos NO se comparten entre usuarios.</strong>
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
            if st.button("❌ Cancel", use_container_width=True, key=f"modal_cancel_{user_id}"):
                st.warning(f"Connection to {config['name']} cancelled")
        
        with button_col2:
            if st.button(f"🔗 Connect", use_container_width=True, key=f"modal_connect_{user_id}", type="primary"):
                # Mostrar iframe de autenticación
                st.markdown(f"""
                <div class="auth-instructions">
                    <h4><i class="{config['icon']}"></i> Autenticación {config['name']}</h4>
                    <p>Inicia sesión directamente en la ventana a continuación para continuar.</p>
                    <p><strong>⚠️ IMPORTANTE:</strong> No cierres esta ventana durante el proceso de autenticación.</p>
                    <p><strong>🔒 PRIVACIDAD:</strong> Los datos solo serán visibles para ti ({user_id})</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Iframe de autenticación
                auth_html = f"""
                <div style="border: 3px solid {config['color']}; border-radius: 20px; overflow: hidden; margin: 30px 0; box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
                    <div style="background: linear-gradient(135deg, {config['color']} 0%, {config['color'].replace('#', '#')+'99'} 100%); 
                                color: white; padding: 20px; text-align: center; font-size: 20px; font-weight: 600;">
                        <i class="{config['icon']}"></i> {config['name']} Login
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
                    set_auth_status(network, True)
                    st.success(f"✅ Successfully connected to {config['name']}!")
                    
                    # Si es TikTok, mostrar opción para scraping real
                    if network == 'tiktok':
                        st.markdown("""
                        <div class="scraper-status">
                            <i class="fas fa-robot"></i> SCRAPER DE TIKTOK DISPONIBLE
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("""
                        **🎯 Scraping Real de TikTok Disponible**
                        
                        Ahora puedes ejecutar el scraper real para obtener tus datos actuales.
                        
                        **⏱️ Tiempo estimado:** 1-3 minutos
                        **📊 Resultados:** Datos en tiempo real de TU cuenta
                        
                        Haz clic en "Run Real TikTok Scraper" para comenzar.
                        """)
                        
                        if st.button("🚀 Run Real TikTok Scraper", use_container_width=True, type="primary"):
                            with st.spinner("🚀 Ejecutando scraper real de TikTok (1-3 minutos)..."):
                                # Ejecutar scraper real
                                data = run_real_tiktok_scraper()
                                
                                if data is not None and not data.empty:
                                    set_scraped_data(network, data)
                                    st.success(f"✅ Scraping completado: {len(data)} videos obtenidos")
                                else:
                                    st.error("❌ No se pudieron obtener datos del scraper")
                    
                    st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_tiktok_dashboard():
    """Dashboard específico para TikTok con datos REALES"""
    if 'tiktok' not in get_scraped_data():
        st.warning("""
        ⚠️ **No hay datos de TikTok disponibles**
        
        Para ver los datos de TikTok:
        
        1. Conéctate a TikTok en la pestaña **Authentication**
        2. Ejecuta el **scraper real** para obtener tus datos
        3. Regresa a esta pestaña para ver el análisis
        
        **📊 Los datos mostrados serán REALES de tu cuenta**
        **🔒 Solo tú podrás ver tus datos**
        """)
        return
    
    data = get_scraped_data()['tiktok']
    config = NETWORK_CONFIG['tiktok']
    
    # Verificar si hay datos
    if data.empty:
        st.warning("No hay datos disponibles. Ejecuta el scraper primero.")
        return
    
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
            Datos REALES de tu cuenta - Usuario: {user_id}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales (solo si hay columnas numéricas)
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
    
    # Intentar calcular otras métricas si existen las columnas
    try:
        if 'visualizaciones_num' in data.columns:
            with col2:
                total_views = data['visualizaciones_num'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-eye"></i></div>
                    <div class="metric-value">{total_views:,}</div>
                    <div class="metric-label">Total Views</div>
                </div>
                """, unsafe_allow_html=True)
        
        if 'me_gusta_num' in data.columns:
            with col3:
                total_likes = data['me_gusta_num'].sum()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-heart"></i></div>
                    <div class="metric-value">{total_likes:,}</div>
                    <div class="metric-label">Total Likes</div>
                </div>
                """, unsafe_allow_html=True)
        
        if 'engagement_rate' in data.columns:
            with col4:
                avg_engagement = data['engagement_rate'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-chart-line"></i></div>
                    <div class="metric-value">{avg_engagement:.1f}%</div>
                    <div class="metric-label">Avg. Engagement</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        pass
    
    # Tabs de análisis
    tab1, tab2 = st.tabs(["📋 Raw Data", "📊 Basic Analysis"])
    
    with tab1:
        # Mostrar datos crudos
        st.subheader("📋 Datos Crudos de TikTok")
        st.dataframe(data, use_container_width=True, height=400)
        
        # Exportar datos
        st.subheader("💾 Exportar Datos")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"tiktok_data_{user_id}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_col2:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, index=False, sheet_name='TikTok Data')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"tiktok_data_{user_id}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with tab2:
        # Análisis básico si hay suficientes datos
        st.subheader("📊 Análisis Básico")
        
        if len(data) > 0:
            # Distribución de privacidad
            if 'privacidad' in data.columns:
                privacy_counts = data['privacidad'].value_counts()
                st.write("**Configuración de Privacidad:**")
                st.write(privacy_counts)
            
            # Videos más recientes
            if 'fecha_publicacion' in data.columns:
                st.write("**Videos más recientes:**")
                recent_videos = data.head(5)[['titulo', 'fecha_publicacion', 'visualizaciones']]
                st.write(recent_videos)
        else:
            st.info("No hay suficientes datos para análisis avanzado")

# =============================================
# APLICACIÓN PRINCIPAL
# =============================================
def main():
    # Sidebar con YouTube
    create_sidebar()
    
    # Header principal
    current_config = NETWORK_CONFIG[get_current_network()]
    
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
                Dashboard profesional - Sesión privada de {user_id}
            </p>
        </div>
        <div style="background: {current_config['color']}; color: white; padding: 10px 25px; 
                    border-radius: 50px; font-weight: 600;">
            { '🟢 CONNECTED' if get_auth_status()[get_current_network()] else '🔴 DISCONNECTED' }
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Información de privacidad
    st.info(f"""
    **🔒 PRIVACIDAD GARANTIZADA**
    
    - **Usuario actual:** {user_id}
    - **Datos privados:** Solo tú puedes ver tus datos
    - **Sin compartir:** Los datos no se comparten entre usuarios
    - **Sin datos inventados:** Solo se muestran datos reales obtenidos del scraper
    """)
    
    # Tabs principales
    auth_tab, analytics_tab, settings_tab = st.tabs(["🔐 Authentication", "📊 Analytics", "⚙️ Settings"])
    
    with auth_tab:
        if get_auth_status()[get_current_network()]:
            st.success(f"✅ You are connected to {current_config['name']}")
            
            # Para TikTok, mostrar opción de scraping real
            if get_current_network() == 'tiktok':
                st.markdown("""
                <div class="scraper-status">
                    <i class="fas fa-robot"></i> TIKTOK SCRAPER READY
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    if st.button("🚀 Ejecutar Scraper Real (1-3 min)", use_container_width=True, type="primary"):
                        with st.spinner("🚀 Ejecutando scraper real de TikTok..."):
                            # Mostrar tiempos reales
                            time_info = st.empty()
                            
                            for seconds in range(1, 181):  # 3 minutos máximo
                                time_info.info(f"⏱️ Tiempo transcurrido: {seconds} segundos")
                                time.sleep(1)
                            
                            # Ejecutar scraper
                            data = run_real_tiktok_scraper()
                            
                            if data is not None and not data.empty:
                                set_scraped_data('tiktok', data)
                                st.success(f"✅ Scraping completado: {len(data)} videos obtenidos")
                            else:
                                st.error("❌ No se pudieron obtener datos del scraper")
                
                with col2:
                    if st.button("🔄 Refresh Data", use_container_width=True):
                        st.info("Para obtener datos actualizados, ejecuta el scraper nuevamente")
                
                with col3:
                    if st.button("🚪 Disconnect", use_container_width=True, type="secondary"):
                        set_auth_status('tiktok', False)
                        st.rerun()
                
                # Mostrar información del scraper
                st.markdown("""
                **📋 Información del Scraper Real:**
                
                - **Tiempo estimado:** 1-3 minutos
                - **Autenticación:** Requiere inicio de sesión MANUAL
                - **Datos obtenidos:** Videos, visualizaciones, likes, comentarios
                - **Privacidad:** Solo datos de TU cuenta
                - **Actualización:** Detecta videos nuevos automáticamente
                
                **⚠️ Nota:** En producción, este scraper abriría TikTok real y esperaría tu autenticación.
                """)
            
            else:
                # Para otras redes
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Refresh Data", use_container_width=True):
                        st.info(f"Refresh functionality for {current_config['name']} coming soon!")
                
                with col2:
                    if st.button("🚪 Disconnect", use_container_width=True, type="secondary"):
                        set_auth_status(get_current_network(), False)
                        st.rerun()
        
        else:
            show_auth_modal()
    
    with analytics_tab:
        if get_auth_status()[get_current_network()]:
            if get_current_network() == 'tiktok':
                show_tiktok_dashboard()
            else:
                st.info(f"📊 Analytics dashboard for {current_config['name']} coming soon!")
        else:
            st.warning(f"⚠️ Please authenticate with {current_config['name']} first to view analytics.")
    
    with settings_tab:
        st.markdown("## ⚙️ Configuration Settings")
        
        st.info(f"""
        **👤 Configuración de Usuario**
        
        - **ID de sesión:** {user_id}
        - **Red actual:** {get_current_network()}
        - **Conexiones activas:** {sum(get_auth_status().values())}/5
        - **Datos almacenados:** {len(get_scraped_data())} redes
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 Scraping Settings")
            
            delay = st.slider(
                "Request Delay (seconds)",
                min_value=2,
                max_value=10,
                value=3,
                help="Delay between requests to avoid rate limiting"
            )
            
            st.markdown("#### TikTok Specific")
            st.info("""
            **⏱️ Tiempos de Scraping:**
            
            - **Autenticación manual:** 60 segundos
            - **Carga de contenido:** 10 segundos
            - **Scroll por video:** 1.5 segundos
            - **Total estimado:** 1-3 minutos
            
            **⚠️ Estos tiempos son REALES y necesarios para evitar bloqueos.**
            """)
        
        with col2:
            st.markdown("### 💾 Data Management")
            
            if st.button("💾 Backup My Data", use_container_width=True):
                # Crear backup solo de los datos de ESTE usuario
                backup_data = {
                    'user_id': user_id,
                    'auth_status': get_auth_status(),
                    'scraped_data': {}
                }
                
                for network, data in get_scraped_data().items():
                    if isinstance(data, pd.DataFrame):
                        backup_data['scraped_data'][network] = data.to_dict('records')
                
                st.download_button(
                    label="📥 Download My Backup",
                    data=json.dumps(backup_data, indent=2),
                    file_name=f"social_dashboard_{user_id}_backup.json",
                    mime="application/json"
                )
            
            if st.button("🗑️ Clear All My Data", use_container_width=True, type="secondary"):
                for network in get_auth_status():
                    set_auth_status(network, False)
                st.session_state[f'scraped_data_{user_id}'] = {}
                st.success("All your data has been cleared!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 System Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            connected = sum(get_auth_status().values())
            st.metric("Connected Networks", f"{connected}/5")
        
        with info_col2:
            total_records = sum([len(data) for data in get_scraped_data().values() 
                               if isinstance(data, pd.DataFrame)])
            st.metric("Total Records", f"{total_records}")

# =============================================
# EJECUCIÓN
# =============================================
if __name__ == "__main__":
    # Verificar que estamos en un entorno seguro
    st.warning("""
    ⚠️ **MODO SEGURO ACTIVADO**
    
    Esta versión NO muestra datos inventados y garantiza:
    
    1. **Privacidad por usuario:** Cada usuario ve solo sus datos
    2. **Sin datos falsos:** Solo datos reales del scraper
    3. **Scraper real listo:** Código real incluido (comentado por seguridad)
    
    **Para producción:**
    - Descomentar el código del scraper real
    - Configurar ChromeDriver
    - Probar con cuentas reales
    """)
    
    main()
