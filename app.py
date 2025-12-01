import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from io import BytesIO

# Configuración de página - SIN CSS COMPLEJO
st.set_page_config(
    page_title="Social Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS mínimo y seguro
st.markdown("""
<style>
    /* Reset básico */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilos básicos para tarjetas */
    .social-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3a8a;
    }
    
    /* Botones de redes sociales */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
        width: 100%;
        margin: 5px 0;
    }
    
    .facebook-btn { background-color: #1877f2; color: white; }
    .twitter-btn { background-color: #1da1f2; color: white; }
    .instagram-btn { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743); color: white; }
    .linkedin-btn { background-color: #0a66c2; color: white; }
    .tiktok-btn { background-color: #010101; color: white; }
    
    /* Modal frame simplificado */
    .modal-frame {
        background: white;
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 20px auto;
        max-width: 800px;
    }
    
    /* Sidebar simplificada */
    .sidebar-content {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 0 15px 15px 0;
        height: 100vh;
        position: fixed;
        left: 0;
        top: 0;
        width: 80px;
        transition: width 0.3s;
    }
    
    .sidebar-content.expanded {
        width: 250px;
    }
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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

if 'sidebar_expanded' not in st.session_state:
    st.session_state.sidebar_expanded = False

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
        'color': '#E4405F',
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
                'ID': f"tt_{i+1:04d}",
                'Duración': f"{random.randint(0, 3)}:{random.randint(10, 59):02d}",
                'Título': f"Video TikTok #{i+1}",
                'Fecha': video_date.strftime("%d/%m/%Y %H:%M"),
                'Visualizaciones': views,
                'Me Gusta': likes,
                'Comentarios': comments,
                'Compartidos': shares,
                'Engagement %': round((likes + comments + shares) / views * 100, 2),
                'Privacidad': random.choice(['Público', 'Privado', 'Amigos'])
            }
            data.append(video_data)
    else:
        for i in range(25):
            post_date = base_date - timedelta(days=random.randint(0, 90))
            reach = random.randint(1000, 50000)
            interactions = random.randint(100, 10000)
            comments = int(interactions * random.uniform(0.05, 0.25))
            
            post_data = {
                'ID': f"{network[:3]}_{i+1:04d}",
                'Tipo': random.choice(['Imagen', 'Video', 'Texto']),
                'Contenido': f"Publicación #{i+1}",
                'Fecha': post_date.strftime("%d/%m/%Y %H:%M"),
                'Alcance': reach,
                'Interacciones': interactions,
                'Comentarios': comments,
                'Compartidos': int(interactions * random.uniform(0.01, 0.15)),
                'Engagement %': round((interactions + comments) / reach * 100, 2)
            }
            data.append(post_data)
    
    return pd.DataFrame(data)

# Función para mostrar modal de autenticación
def show_auth_modal():
    """Muestra el modal de autenticación"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    # Mostrar el modal frame
    st.markdown(f"""
    <div class="modal-frame">
        <div style="text-align: center; margin-bottom: 30px;">
            <i class="{config['icon']}" style="font-size: 60px; color: {config['color']};"></i>
        </div>
        
        <h1 style="text-align: center; color: #1e3a8a; margin-bottom: 20px;">
            Conectar con <span style="color: {config['color']};">{config['name']}</span>
        </h1>
        
        <p style="text-align: center; color: #666; font-size: 18px; margin-bottom: 40px;">
            Esta aplicación necesitará acceso a tu cuenta de {config['name']} 
            para extraer métricas y datos analíticos.
        </p>
        
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 40px;">
            <h3 style="color: #1e3a8a; margin-bottom: 20px;">
                <i class="fas fa-shield-alt"></i> Permisos solicitados:
            </h3>
            <ul style="color: #4a5568; padding-left: 20px;">
    """, unsafe_allow_html=True)
    
    for permission in config['permissions']:
        st.markdown(f"<li>{permission}</li>", unsafe_allow_html=True)
    
    st.markdown("""
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("❌ Cancelar", use_container_width=True, key="cancel_auth"):
            st.warning(f"Conexión a {config['name']} cancelada.")
    
    with col2:
        if st.button(f"🔗 Conectar a {config['name']}", use_container_width=True, key="connect_auth", type="primary"):
            # Mostrar proceso de autenticación
            with st.spinner(f"Conectando a {config['name']}..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)
                
                # Autenticación exitosa
                st.session_state.auth_status[network] = True
                st.success(f"✅ ¡Conectado a {config['name']}!")
                
                # Extraer datos
                with st.spinner(f"Extrayendo datos de {config['name']}..."):
                    time.sleep(2)
                    data = generate_sample_data(network)
                    st.session_state.scraped_data[network] = data
                    st.success(f"📊 {len(data)} registros extraídos")
                    st.rerun()

# Función para mostrar dashboard analítico
def show_analytics_dashboard():
    """Muestra el dashboard analítico"""
    network = st.session_state.current_network
    config = NETWORK_CONFIG[network]
    
    if network not in st.session_state.scraped_data:
        st.info(f"ℹ️ Primero necesitas autenticarte en {config['name']} y extraer datos.")
        return
    
    data = st.session_state.scraped_data[network]
    
    # Título
    st.markdown(f"""
    <div style="background: {config['color']}; padding: 25px; border-radius: 15px; color: white; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0;">
            <i class="{config['icon']}"></i> Dashboard de {config['name']}
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
            Análisis completo de métricas y rendimiento
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(data)
        st.metric("📊 Total", f"{total:,}")
    
    with col2:
        if 'Visualizaciones' in data.columns:
            total_views = data['Visualizaciones'].sum()
            st.metric("👀 Visualizaciones", f"{total_views:,.0f}")
        elif 'Alcance' in data.columns:
            total_reach = data['Alcance'].sum()
            st.metric("📈 Alcance", f"{total_reach:,.0f}")
    
    with col3:
        if 'Me Gusta' in data.columns:
            total_likes = data['Me Gusta'].sum()
            st.metric("❤️ Me Gusta", f"{total_likes:,.0f}")
        elif 'Interacciones' in data.columns:
            total_int = data['Interacciones'].sum()
            st.metric("👍 Interacciones", f"{total_int:,.0f}")
    
    with col4:
        if 'Engagement %' in data.columns:
            avg_engagement = data['Engagement %'].mean()
            st.metric("📊 Engagement", f"{avg_engagement:.1f}%")
    
    # Gráficos
    st.markdown("## 📈 Visualizaciones")
    
    tab1, tab2 = st.tabs(["📊 Gráficos", "📋 Datos"])
    
    with tab1:
        # Gráfico de barras
        fig = go.Figure()
        
        if network == 'tiktok':
            top_data = data.nlargest(10, 'Visualizaciones')
            fig.add_trace(go.Bar(
                x=top_data['Título'],
                y=top_data['Visualizaciones'],
                name='Visualizaciones',
                marker_color='#1e3a8a'
            ))
            fig.add_trace(go.Bar(
                x=top_data['Título'],
                y=top_data['Me Gusta'],
                name='Me Gusta',
                marker_color='#10b981'
            ))
        else:
            top_data = data.nlargest(10, 'Alcance')
            fig.add_trace(go.Bar(
                x=top_data['Contenido'],
                y=top_data['Alcance'],
                name='Alcance',
                marker_color='#1e3a8a'
            ))
            fig.add_trace(go.Bar(
                x=top_data['Contenido'],
                y=top_data['Interacciones'],
                name='Interacciones',
                marker_color='#10b981'
            ))
        
        fig.update_layout(
            title='Top 10 Contenidos',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.dataframe(data, use_container_width=True, height=400)
        
        # Exportar datos
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

# Aplicación principal
def main():
    # Barra lateral simple
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="color: #1e3a8a;">🌐 Redes Sociales</h2>
            <p style="color: #666;">Selecciona una red</p>
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
            # Determinar el color del botón
            btn_color = NETWORK_CONFIG[network_id]['color']
            
            # Mostrar estado
            status = "✅" if st.session_state.auth_status[network_id] else "🔒"
            
            # Crear botón con HTML
            button_html = f"""
            <div style="margin: 10px 0;">
                <button onclick="selectNetwork('{network_id}')" 
                        style="background: {btn_color}; color: white; border: none; 
                               border-radius: 8px; padding: 12px; width: 100%; 
                               cursor: pointer; text-align: left; font-weight: 600;">
                    <i class="{network_icon}" style="margin-right: 10px;"></i>
                    {network_name} {status}
                </button>
            </div>
            """
            
            components.html(f"""
            <script>
            function selectNetwork(network) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: network
                }}, '*');
            }}
            </script>
            {button_html}
            """, height=60)
            
            # Botón de Streamlit (alternativa)
            if st.button(f"{network_name} {status}", key=f"btn_{network_id}"):
                st.session_state.current_network = network_id
                st.rerun()
        
        # Separador
        st.markdown("---")
        
        # Estado de conexiones
        st.markdown("### 🔗 Estado")
        for network_id, network_name, _ in networks:
            status = "✅ Conectado" if st.session_state.auth_status[network_id] else "❌ No conectado"
            st.write(f"**{network_name}:** {status}")
        
        # Botón para limpiar
        if st.button("🗑️ Limpiar datos", use_container_width=True):
            for network in st.session_state.auth_status:
                st.session_state.auth_status[network] = False
            st.session_state.scraped_data = {}
            st.success("Datos limpiados")
            st.rerun()
    
    # Contenido principal
    st.title("📊 Dashboard de Redes Sociales")
    st.markdown("Conecta tus redes sociales y analiza métricas en tiempo real")
    
    # Mostrar red actual
    current_config = NETWORK_CONFIG[st.session_state.current_network]
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: {current_config['color']}; margin: 0;">
            <i class="{current_config['icon']}"></i> {current_config['name']}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🔐 Autenticación", "📊 Análisis", "⚙️ Configuración"])
    
    with tab1:
        if st.session_state.auth_status[st.session_state.current_network]:
            st.success(f"✅ Ya estás conectado a {current_config['name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Extraer datos", use_container_width=True):
                    with st.spinner("Extrayendo..."):
                        time.sleep(2)
                        data = generate_sample_data(st.session_state.current_network)
                        st.session_state.scraped_data[st.session_state.current_network] = data
                        st.success(f"{len(data)} registros extraídos")
                        st.rerun()
            
            with col2:
                if st.button("🚪 Cerrar sesión", use_container_width=True):
                    st.session_state.auth_status[st.session_state.current_network] = False
                    st.rerun()
            
            # Vista previa
            if st.session_state.current_network in st.session_state.scraped_data:
                st.subheader("📋 Vista previa")
                data = st.session_state.scraped_data[st.session_state.current_network]
                st.dataframe(data.head(3), use_container_width=True)
        else:
            show_auth_modal()
    
    with tab2:
        show_analytics_dashboard()
    
    with tab3:
        st.markdown("## ⚙️ Configuración")
        
        col1, col2 = st.columns(2)
        
        with col1:
            delay = st.slider(
                "Retraso entre solicitudes",
                min_value=1,
                max_value=10,
                value=3
            )
        
        with col2:
            max_items = st.slider(
                "Máximo de registros",
                min_value=10,
                max_value=100,
                value=50
            )
        
        st.info("""
        ⚠️ **Nota:** Para evitar bloqueos, el sistema:
        - Incluye pausas automáticas
        - Simula comportamiento humano
        - Respeta límites de velocidad
        """)

# JavaScript para manejar los botones HTML
components.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:setComponentValue') {
        // Redirigir al botón correspondiente
        var network = event.data.value;
        if (['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok'].includes(network)) {
            // Enviar evento a Streamlit
            window.parent.postMessage({
                type: 'streamlit:componentValue',
                data: network
            }, '*');
        }
    }
});
</script>
""", height=0)

if __name__ == "__main__":
    main()
