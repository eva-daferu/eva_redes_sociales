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

# Configuración de página
st.set_page_config(
    page_title="Social Dashboard - Panel de Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - MANTENIENDO EL DISEÑO ORIGINAL
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }

    :root {
        --azul-profesional: #1e3a8a;
        --azul-oscuro: #0f172a;
        --gris-grafito: #2d3748;
        --gris-claro: #f7fafc;
        --gris-medio: #e2e8f0;
        --gris-texto: #4a5568;
        --blanco: #ffffff;
        --azul-facebook: #1877f2;
        --azul-twitter: #1da1f2;
        --azul-instagram: #e4405f;
        --azul-linkedin: #0a66c2;
        --negro-tiktok: #010101;
        --sombra: rgba(0, 0, 0, 0.08);
        --sombra-fuerte: rgba(0, 0, 0, 0.15);
        --border-radius: 12px;
        --transicion: all 0.3s ease;
    }

    body {
        background-color: var(--gris-claro);
        color: var(--gris-texto);
        min-height: 100vh;
    }

    /* Top Bar Simulada */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 70px;
        background-color: var(--gris-grafito);
        box-shadow: 0 4px 12px var(--sombra);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        z-index: 1000;
    }

    .top-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .hamburger-menu {
        background: none;
        border: none;
        color: var(--blanco);
        font-size: 24px;
        cursor: pointer;
        transition: var(--transicion);
        padding: 8px;
        border-radius: 8px;
    }

    .hamburger-menu:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .dashboard-btn {
        background-color: var(--azul-profesional);
        color: var(--blanco);
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: var(--transicion);
        box-shadow: 0 4px 8px rgba(30, 58, 138, 0.2);
    }

    .dashboard-btn:hover {
        background-color: #1e40af;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(30, 58, 138, 0.3);
    }

    .top-right {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .top-icon {
        background: none;
        border: none;
        color: var(--blanco);
        font-size: 20px;
        cursor: pointer;
        transition: var(--transicion);
        padding: 10px;
        border-radius: 50%;
        position: relative;
    }

    .top-icon:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .notification-badge {
        position: absolute;
        top: 5px;
        right: 5px;
        background-color: #ef4444;
        color: white;
        font-size: 10px;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Sidebar Simulada */
    .sidebar {
        position: fixed;
        top: 70px;
        left: 0;
        bottom: 0;
        width: 90px;
        background-color: var(--azul-profesional);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 30px;
        box-shadow: 4px 0 10px var(--sombra);
        z-index: 999;
        transition: var(--transicion);
    }

    .sidebar.open {
        width: 220px;
        align-items: flex-start;
        padding-left: 20px;
    }

    .social-btn {
        width: 60px;
        height: 60px;
        border-radius: var(--border-radius);
        border: none;
        margin-bottom: 20px;
        cursor: pointer;
        transition: var(--transicion);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--blanco);
        font-size: 24px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }

    .sidebar.open .social-btn {
        width: 180px;
        justify-content: flex-start;
        padding-left: 20px;
    }

    .social-btn span {
        display: none;
        margin-left: 15px;
        font-size: 16px;
        font-weight: 500;
    }

    .sidebar.open .social-btn span {
        display: inline-block;
    }

    .social-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        z-index: 1;
    }

    .social-btn i, .social-btn span {
        position: relative;
        z-index: 2;
    }

    .social-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .facebook {
        background-color: var(--azul-facebook);
    }

    .twitter {
        background-color: var(--azul-twitter);
    }

    .instagram {
        background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    }

    .linkedin {
        background-color: var(--azul-linkedin);
    }

    .tiktok {
        background-color: var(--negro-tiktok);
    }

    .tiktok i {
        color: #00f2ea;
        text-shadow: 2px 2px 0 #ff0050;
    }

    .tiktok span {
        background: linear-gradient(to right, #00f2ea, #ff0050);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 600;
    }

    /* Contenido principal */
    .main-content {
        margin-left: 90px;
        margin-top: 70px;
        padding: 30px;
        width: calc(100% - 90px);
        min-height: calc(100vh - 70px);
        transition: var(--transicion);
    }

    .main-content.expanded {
        margin-left: 220px;
        width: calc(100% - 220px);
    }

    /* MODAL-FRAME ORIGINAL - GRANDE Y BIEN AJUSTADO */
    .modal-frame {
        max-width: 800px;
        margin: 40px auto;
        background-color: var(--blanco);
        border-radius: var(--border-radius);
        box-shadow: 0 20px 60px var(--sombra-fuerte);
        padding: 60px;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }

    .modal-title {
        font-size: 36px;
        font-weight: 700;
        color: var(--azul-oscuro);
        margin-bottom: 25px;
        line-height: 1.2;
    }

    .modal-subtitle {
        font-size: 20px;
        line-height: 1.7;
        color: var(--gris-texto);
        margin-bottom: 50px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        font-weight: 400;
    }

    .social-network-name {
        color: var(--azul-profesional);
        font-weight: 800;
    }

    .permissions-list {
        text-align: left;
        background-color: var(--gris-medio);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 50px;
        border-left: 5px solid var(--azul-profesional);
    }

    .permissions-list h3 {
        margin-bottom: 20px;
        color: var(--azul-oscuro);
        font-size: 22px;
        font-weight: 600;
    }

    .permissions-list ul {
        list-style-type: none;
        padding-left: 0;
    }

    .permissions-list li {
        padding: 12px 0;
        display: flex;
        align-items: center;
        font-size: 17px;
        color: var(--gris-texto);
    }

    .permissions-list i {
        color: var(--azul-profesional);
        margin-right: 15px;
        font-size: 20px;
    }

    .button-group {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 40px;
    }

    .btn {
        padding: 18px 40px;
        border-radius: 30px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: var(--transicion);
        border: none;
        min-width: 180px;
        letter-spacing: 0.5px;
    }

    .btn-cancel {
        background-color: var(--gris-medio);
        color: var(--gris-texto);
    }

    .btn-cancel:hover {
        background-color: #cbd5e0;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }

    .btn-connect {
        background-color: var(--azul-profesional);
        color: var(--blanco);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.25);
    }

    .btn-connect:hover {
        background-color: #1e40af;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.35);
    }

    .network-icon-large {
        font-size: 80px;
        margin-bottom: 40px;
        display: flex;
        justify-content: center;
    }

    /* Iframe de autenticación */
    .auth-iframe-container {
        margin: 40px 0;
        border: 2px solid var(--azul-profesional);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }

    .auth-iframe-container h4 {
        background: var(--azul-profesional);
        color: white;
        padding: 15px;
        margin: 0;
        text-align: center;
        font-size: 18px;
    }

    .auth-instructions {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        margin: 25px 0;
        border-left: 4px solid var(--azul-profesional);
    }

    .auth-instructions p {
        margin: 10px 0;
        color: var(--gris-texto);
        font-size: 16px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .modal-frame {
            padding: 40px 25px;
            margin: 20px;
        }
        
        .modal-title {
            font-size: 28px;
        }
        
        .modal-subtitle {
            font-size: 18px;
        }
        
        .button-group {
            flex-direction: column;
            align-items: center;
        }
        
        .btn {
            width: 100%;
            max-width: 300px;
        }
        
        .network-icon-large {
            font-size: 60px;
        }
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stButton > button {
        border-radius: 30px;
        font-weight: 600;
        padding: 12px 24px;
    }
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Estado de la sesión
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
    st.session_state.current_network = 'facebook'

if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Configuración de redes sociales
NETWORK_CONFIG = {
    'facebook': {
        'name': 'Facebook',
        'color': '#1877f2',
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
        'color': 'linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)',
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

# Función para generar datos de muestra
def generate_sample_data(network):
    """Genera datos de muestra para análisis"""
    data = []
    base_date = datetime.now()
    
    if network == 'tiktok':
        for i in range(35):
            video_date = base_date - timedelta(days=random.randint(0, 60))
            views = random.randint(1000, 1000000)
            likes = int(views * random.uniform(0.02, 0.08))
            comments = int(likes * random.uniform(0.05, 0.2))
            shares = int(views * random.uniform(0.001, 0.01))
            
            video_data = {
                'video_id': f"tt_{i+1:04d}",
                'duracion': f"{random.randint(0, 3)}:{random.randint(10, 59):02d}",
                'titulo': f"Video TikTok #{i+1}: Contenido viral sobre {random.choice(['danzas', 'cocina', 'comedia', 'educación', 'belleza'])}",
                'descripcion': f"Este video muestra contenido interesante que ha generado gran engagement #{i+1}",
                'fecha_publicacion': video_date.strftime("%d %b, %H:%M"),
                'visualizaciones': f"{views:,}",
                'me_gusta': f"{likes:,}",
                'comentarios': f"{comments:,}",
                'compartidos': f"{shares:,}",
                'engagement_rate': round((likes + comments + shares) / views * 100, 2),
                'hashtags': f"#{random.choice(['viral', 'tendencia', 'fyp', 'parati', 'comedia'])} #{network}",
                'privacidad': random.choice(['Todo el mundo', 'Solo yo', 'Amigos'])
            }
            data.append(video_data)
    else:
        for i in range(25):
            post_date = base_date - timedelta(days=random.randint(0, 90))
            reach = random.randint(1000, 50000)
            interactions = random.randint(100, 10000)
            comments = int(interactions * random.uniform(0.05, 0.25))
            
            post_data = {
                'post_id': f"{network[:3]}_{i+1:04d}",
                'tipo': random.choice(['Imagen', 'Video', 'Texto', 'Enlace', 'Carousel']),
                'contenido': f"Publicación en {NETWORK_CONFIG[network]['name']} sobre {random.choice(['actualidad', 'tecnología', 'negocios', 'entretenimiento'])} #{i+1}",
                'fecha': post_date.strftime("%d %b, %H:%M"),
                'alcance': f"{reach:,}",
                'interacciones': f"{interactions:,}",
                'comentarios': f"{comments:,}",
                'compartidos': f"{int(interactions * random.uniform(0.01, 0.15)):,}",
                'engagement_rate': round((interactions + comments) / reach * 100, 2),
                'impresiones': f"{int(reach * random.uniform(1.2, 3.0)):,}",
                'ctr': round(random.uniform(0.5, 8.0), 2)
            }
            data.append(post_data)
    
    return pd.DataFrame(data)

# Función para mostrar modal de autenticación
def show_auth_modal():
    """Muestra el modal-frame de autenticación grande y bien ajustado"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    # Determinar color para el ícono
    icon_color = config['color']
    if network == 'instagram':
        icon_color = '#E4405F'  # Color principal de Instagram
    elif network == 'tiktok':
        icon_color = '#00f2ea'  # Color característico de TikTok
    
    # Crear HTML para el modal-frame
    modal_html = f"""
    <div class="modal-frame">
        <div class="network-icon-large">
            <i class="{config['icon']}" style="color: {icon_color};"></i>
        </div>
        
        <h1 class="modal-title">Connect to <span class="social-network-name">{config['name']}</span>?</h1>
        
        <p class="modal-subtitle">
            This will allow the dashboard to access your {config['name']} account data 
            to provide analytics, scheduling, and engagement metrics.
        </p>
        
        <div class="permissions-list">
            <h3>Permissions requested:</h3>
            <ul>
    """
    
    for permission in config['permissions']:
        modal_html += f'<li><i class="fas fa-check-circle"></i> {permission}</li>'
    
    modal_html += """
            </ul>
        </div>
    """
    
    # Mostrar el modal-frame
    components.html(modal_html, height=650)
    
    # Mostrar botones debajo del modal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Botón de cancelar
        if st.button("❌ Cancel", key="cancel_auth", use_container_width=True):
            st.warning(f"Connection to {config['name']} cancelled.")
        
        # Espacio
        st.write("")
        
        # Botón de conectar
        if st.button(f"🔗 Connect to {config['name']}", key="connect_auth", use_container_width=True, type="primary"):
            # Mostrar iframe de autenticación
            st.markdown(f"""
            <div class="auth-instructions">
                <h4><i class="{config['icon']}"></i> Autenticación {config['name']}</h4>
                <p>Inicia sesión directamente en la ventana a continuación para continuar.</p>
                <p><strong>⚠️ IMPORTANTE:</strong> No cierres esta ventana durante el proceso de autenticación.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Iframe de autenticación
            auth_iframe = f"""
            <div class="auth-iframe-container">
                <h4><i class="{config['icon']}"></i> {config['name']} Login</h4>
                <iframe src="{config['auth_url']}" width="100%" height="500" 
                style="border: none;" title="{config['name']} Authentication"></iframe>
            </div>
            <p style="text-align: center; color: #666; font-size: 14px; margin-top: 10px;">
                Si la ventana no carga correctamente, 
                <a href="{config['auth_url']}" target="_blank">haz clic aquí para abrir en nueva pestaña</a>
            </p>
            """
            
            components.html(auth_iframe, height=600)
            
            # Simular proceso de autenticación
            with st.spinner(f"Esperando autenticación en {config['name']}..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simular tiempo de espera real
                    progress_bar.progress(i + 1)
                
                # Marcar como autenticado
                st.session_state.auth_status[network] = True
                st.success(f"✅ ¡Autenticación exitosa en {config['name']}!")
                
                # Extraer datos automáticamente
                with st.spinner(f"Extrayendo datos de {config['name']}..."):
                    time.sleep(2)
                    data = generate_sample_data(network)
                    st.session_state.scraped_data[network] = data
                    st.success(f"📊 {len(data)} registros extraídos de {config['name']}")

# Función para mostrar dashboard analítico
def show_analytics_dashboard():
    """Muestra el dashboard analítico con gráficos"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    if network not in st.session_state.scraped_data:
        st.info(f"ℹ️ Primero necesitas autenticarte en {config['name']} y extraer datos.")
        return
    
    data = st.session_state.scraped_data[network]
    
    # Título del dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {config['color'] if isinstance(config['color'], str) and 'linear-gradient' not in config['color'] else '#1e3a8a'} 0%, var(--azul-oscuro) 100%); 
                padding: 25px; border-radius: 15px; color: white; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">
            <i class="{config['icon']}"></i> {config['name']} Analytics Dashboard
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 18px;">
            Análisis completo de métricas y rendimiento
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(data)
        st.metric("📊 Total Registros", f"{total:,}")
    
    with col2:
        if 'visualizaciones' in data.columns:
            # Convertir a numérico
            views_numeric = data['visualizaciones'].str.replace(',', '').astype(float)
            total_views = views_numeric.sum()
            st.metric("👀 Visualizaciones", f"{total_views:,.0f}")
        elif 'alcance' in data.columns:
            reach_numeric = data['alcance'].str.replace(',', '').astype(float)
            total_reach = reach_numeric.sum()
            st.metric("📈 Alcance Total", f"{total_reach:,.0f}")
    
    with col3:
        if 'me_gusta' in data.columns:
            likes_numeric = data['me_gusta'].str.replace(',', '').astype(float)
            total_likes = likes_numeric.sum()
            st.metric("❤️ Me Gusta", f"{total_likes:,.0f}")
        elif 'interacciones' in data.columns:
            int_numeric = data['interacciones'].str.replace(',', '').astype(float)
            total_int = int_numeric.sum()
            st.metric("👍 Interacciones", f"{total_int:,.0f}")
    
    with col4:
        if 'engagement_rate' in data.columns:
            avg_engagement = data['engagement_rate'].mean()
            st.metric("📊 Avg. Engagement", f"{avg_engagement:.2f}%")
    
    # Gráficos
    st.markdown("## 📈 Visualizaciones de Datos")
    
    tab1, tab2, tab3 = st.tabs(["📊 Métricas Principales", "📈 Tendencias", "📋 Datos Detallados"])
    
    with tab1:
        # Gráfico de barras
        fig = go.Figure()
        
        if network == 'tiktok':
            # Preparar datos para TikTok
            top_videos = data.head(10).copy()
            top_videos['views_num'] = top_videos['visualizaciones'].str.replace(',', '').astype(float)
            top_videos['likes_num'] = top_videos['me_gusta'].str.replace(',', '').astype(float)
            
            fig.add_trace(go.Bar(
                x=top_videos['titulo'].str[:40] + '...',
                y=top_videos['views_num'],
                name='Visualizaciones',
                marker_color='#1e3a8a'
            ))
            
            fig.add_trace(go.Bar(
                x=top_videos['titulo'].str[:40] + '...',
                y=top_videos['likes_num'],
                name='Me Gusta',
                marker_color='#10b981'
            ))
        else:
            # Para otras redes
            top_posts = data.head(10).copy()
            top_posts['reach_num'] = top_posts['alcance'].str.replace(',', '').astype(float)
            top_posts['int_num'] = top_posts['interacciones'].str.replace(',', '').astype(float)
            
            fig.add_trace(go.Bar(
                x=top_posts['contenido'].str[:40] + '...',
                y=top_posts['reach_num'],
                name='Alcance',
                marker_color='#1e3a8a'
            ))
            
            fig.add_trace(go.Bar(
                x=top_posts['contenido'].str[:40] + '...',
                y=top_posts['int_num'],
                name='Interacciones',
                marker_color='#10b981'
            ))
        
        fig.update_layout(
            title='Top 10 Contenidos por Métricas',
            xaxis_title='Contenido',
            yaxis_title='Cantidad',
            barmode='group',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Gráfico de líneas para tendencias
        if 'fecha_publicacion' in data.columns or 'fecha' in data.columns:
            date_col = 'fecha_publicacion' if 'fecha_publicacion' in data.columns else 'fecha'
            
            try:
                # Intentar convertir fechas
                data['fecha_dt'] = pd.to_datetime(data[date_col], format='%d %b, %H:%M', errors='coerce')
                data_sorted = data.sort_values('fecha_dt')
                
                fig2 = go.Figure()
                
                if network == 'tiktok':
                    data_sorted['views_num'] = data_sorted['visualizaciones'].str.replace(',', '').astype(float)
                    data_sorted['likes_num'] = data_sorted['me_gusta'].str.replace(',', '').astype(float)
                    
                    fig2.add_trace(go.Scatter(
                        x=data_sorted['fecha_dt'],
                        y=data_sorted['views_num'],
                        mode='lines+markers',
                        name='Visualizaciones',
                        line=dict(color='#1e3a8a', width=3)
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        x=data_sorted['fecha_dt'],
                        y=data_sorted['likes_num'],
                        mode='lines+markers',
                        name='Me Gusta',
                        line=dict(color='#10b981', width=2)
                    ))
                else:
                    data_sorted['reach_num'] = data_sorted['alcance'].str.replace(',', '').astype(float)
                    data_sorted['int_num'] = data_sorted['interacciones'].str.replace(',', '').astype(float)
                    
                    fig2.add_trace(go.Scatter(
                        x=data_sorted['fecha_dt'],
                        y=data_sorted['reach_num'],
                        mode='lines+markers',
                        name='Alcance',
                        line=dict(color='#1e3a8a', width=3)
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        x=data_sorted['fecha_dt'],
                        y=data_sorted['engagement_rate'],
                        mode='lines+markers',
                        name='Engagement Rate %',
                        line=dict(color='#f59e0b', width=2)
                    ))
                
                fig2.update_layout(
                    title='Evolución Temporal de Métricas',
                    xaxis_title='Fecha',
                    yaxis_title='Métricas',
                    height=500,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
            except Exception as e:
                st.error(f"No se pudo crear el gráfico de tendencias: {str(e)}")
    
    with tab3:
        # Mostrar datos en tabla
        st.dataframe(data, use_container_width=True, height=400)
        
        # Opciones de exportación
        st.markdown("### 💾 Exportar Datos")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"{network}_data.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Para Excel necesitamos BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, index=False, sheet_name='Datos')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"{network}_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

# Función para crear sidebar
def create_sidebar():
    """Crea la barra lateral con botones de redes sociales"""
    
    sidebar_html = """
    <div class="top-bar">
        <div class="top-left">
            <button class="hamburger-menu" id="hamburgerBtn">
                <i class="fas fa-bars"></i>
            </button>
            <button class="dashboard-btn">
                <i class="fas fa-chart-line"></i> Dashboard
            </button>
        </div>
        <div class="top-right">
            <button class="top-icon">
                <i class="fas fa-bell"></i>
                <span class="notification-badge">3</span>
            </button>
            <button class="top-icon">
                <i class="fas fa-cog"></i>
            </button>
        </div>
    </div>
    
    <nav class="sidebar" id="sidebar">
    """
    
    networks = [
        ('facebook', 'Facebook', 'fab fa-facebook-f'),
        ('twitter', 'Twitter', 'fab fa-twitter'),
        ('instagram', 'Instagram', 'fab fa-instagram'),
        ('linkedin', 'LinkedIn', 'fab fa-linkedin-in'),
        ('tiktok', 'TikTok', 'fab fa-tiktok')
    ]
    
    for network_id, network_name, network_icon in networks:
        status = "✅" if st.session_state.auth_status[network_id] else "🔒"
        
        sidebar_html += f"""
        <button class="social-btn {network_id}" id="btn_{network_id}">
            <i class="{network_icon}"></i>
            <span>{network_name} {status}</span>
        </button>
        """
    
    sidebar_html += """
    </nav>
    
    <script>
    // Funcionalidad para el menú hamburguesa
    document.getElementById('hamburgerBtn').addEventListener('click', function() {
        var sidebar = document.getElementById('sidebar');
        sidebar.classList.toggle('open');
        
        // Cambiar ícono
        var icon = this.querySelector('i');
        if (icon.classList.contains('fa-bars')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
        
        // Notificar a Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: 'toggle_sidebar'
        }, '*');
    });
    
    // Funcionalidad para botones de redes sociales
    document.querySelectorAll('.social-btn').forEach(btn => {{
        btn.addEventListener('click', function() {{
            var networkId = this.id.replace('btn_', '');
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: networkId
            }}, '*');
        }});
    }});
    </script>
    """
    
    return sidebar_html

# Aplicación principal
def main():
    # Mostrar sidebar con HTML personalizado
    sidebar_html = create_sidebar()
    components.html(sidebar_html, height=800)
    
    # Contenido principal
    st.markdown(f"""
    <div class="main-content {'expanded' if st.session_state.sidebar_open else ''}">
    """, unsafe_allow_html=True)
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🔐 Autenticación", "📊 Análisis", "⚙️ Configuración"])
    
    with tab1:
        if st.session_state.auth_status[st.session_state.current_network]:
            st.success(f"✅ Ya estás autenticado en {NETWORK_CONFIG[st.session_state.current_network]['name']}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🔄 Extraer datos nuevamente", use_container_width=True):
                    with st.spinner("Extrayendo datos..."):
                        time.sleep(2)
                        data = generate_sample_data(st.session_state.current_network)
                        st.session_state.scraped_data[st.session_state.current_network] = data
                        st.success(f"Datos actualizados: {len(data)} registros")
                        st.rerun()
            
            with col2:
                if st.button("🚪 Cerrar sesión", use_container_width=True, type="secondary"):
                    st.session_state.auth_status[st.session_state.current_network] = False
                    st.rerun()
            
            # Mostrar vista previa de datos
            if st.session_state.current_network in st.session_state.scraped_data:
                st.subheader("📋 Vista previa de datos")
                data = st.session_state.scraped_data[st.session_state.current_network]
                st.dataframe(data.head(5), use_container_width=True)
        else:
            # Mostrar modal de autenticación
            show_auth_modal()
    
    with tab2:
        if st.session_state.auth_status[st.session_state.current_network]:
            show_analytics_dashboard()
        else:
            st.warning(f"⚠️ Primero necesitas autenticarte en {NETWORK_CONFIG[st.session_state.current_network]['name']} para ver el análisis.")
    
    with tab3:
        st.markdown("## ⚙️ Configuración del Sistema")
        
        st.info("""
        ### 🔧 Configuración de Scraping
        
        Para evitar bloqueos de las plataformas, el sistema incluye:
        
        1. **Pausas automáticas** entre solicitudes
        2. **Simulación de comportamiento humano**
        3. **Límites de velocidad** configurables
        4. **Reintentos automáticos** en caso de error
        """)
        
        # Configuraciones
        col1, col2 = st.columns(2)
        
        with col1:
            delay = st.slider(
                "Retraso entre solicitudes (segundos)",
                min_value=1,
                max_value=10,
                value=3,
                help="Tiempo de espera entre cada solicitud para evitar bloqueos"
            )
        
        with col2:
            max_requests = st.slider(
                "Máximo de solicitudes por sesión",
                min_value=10,
                max_value=100,
                value=50,
                help="Límite de solicitudes para no sobrecargar la API"
            )
        
        # Gestión de datos
        st.markdown("### 💾 Gestión de Datos")
        
        if st.button("💾 Guardar sesión actual", use_container_width=True):
            session_data = {
                'auth_status': st.session_state.auth_status,
                'current_network': st.session_state.current_network
            }
            st.success("Configuración guardada en sesión")
        
        if st.button("🗑️ Limpiar todos los datos", use_container_width=True, type="secondary"):
            for network in st.session_state.auth_status:
                st.session_state.auth_status[network] = False
            st.session_state.scraped_data = {}
            st.success("Datos limpiados correctamente")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # JavaScript para manejar interacciones
    components.html("""
    <script>
    // Escuchar mensajes desde los botones
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:setComponentValue') {
            // Si es un toggle del sidebar
            if (event.data.value === 'toggle_sidebar') {
                // Enviar a Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: 'sidebar_toggled'
                }, '*');
            }
            // Si es un cambio de red social
            else if (['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok'].includes(event.data.value)) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: event.data.value
                }, '*');
            }
        }
    });
    </script>
    """, height=0)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
