import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
from openai import OpenAI

warnings.filterwarnings('ignore')

# Configuración de OpenAI
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard",
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

# Estilos CSS simplificados
st.markdown("""
<style>
.main { 
    padding: 0;
    padding-top: 0.5rem !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

.sidebar-title {
    color: #cbd5e1 !important;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
    margin-top: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    height: 100%;
    position: relative;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #1f2937;
    margin: 8px 0 3px 0;
}

.metric-label {
    font-size: 11px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* Selector de gráficas */
.grafica-selector {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
}

.selector-btn {
    padding: 8px 16px;
    border-radius: 6px;
    background: #f8fafc;
    border: 2px solid #e5e7eb;
    color: #64748b;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 13px;
}

.selector-btn.active {
    background: #3B82F6;
    color: white;
    border-color: #3B82F6;
}

.selector-btn:hover {
    background: #f1f5f9;
}

/* Chat styles */
.chat-message {
    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 13px;
}

.user-message {
    background: #3B82F6;
    color: white;
    margin-left: 20px;
}

.assistant-message {
    background: #f1f5f9;
    color: #1f2937;
    margin-right: 20px;
}

.chat-container {
    max-height: 300px;
    overflow-y: auto;
    margin-top: 10px;
}

/* Table styling */
.dataframe {
    font-size: 12px;
}

.dataframe th {
    font-size: 11px;
    padding: 8px 10px;
}

.dataframe td {
    padding: 6px 10px;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 45px; height: 45px; border-radius: 10px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 10px auto; font-size: 22px;">
            📊
        </div>
        <h3 style="color: white; margin-bottom: 3px; font-size: 16px;">Social Media</h3>
        <p style="color: #94a3b8; font-size: 11px; margin: 0;">Dashboard Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 6px 10px; border-radius: 6px; font-size: 11px; margin-bottom: 15px;">✅ Backend Conectado</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 6px 10px; border-radius: 6px; font-size: 11px; margin-bottom: 15px;">⚠️ Backend Error</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 6px 10px; border-radius: 6px; font-size: 11px; margin-bottom: 15px;">⚠️ Backend Offline</div>', unsafe_allow_html=True)
    
    # Botones de plataformas
    st.markdown('<p class="sidebar-title">🔗 Plataformas</p>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Asistente de Chat
    st.markdown('<p class="sidebar-title">🤖 Asistente de Datos</p>', unsafe_allow_html=True)
    
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Contenedor del chat
    chat_container = st.container(height=300)
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input de chat
    user_input = st.chat_input("Pregunta sobre los datos...")
    
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Preparar contexto con datos actuales
        total_posts = len(df_all)
        total_views = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0
        total_followers = df_followers['Seguidores_Totales'].iloc[-1] if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns else 0
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
        - Datos disponibles desde: {df_followers['Fecha'].min().strftime('%Y-%m-%d') if not df_followers.empty and 'Fecha' in df_followers.columns else 'N/D'}
        
        Puedes responder preguntas sobre estas métricas, tendencias, eficiencia de publicidad, y análisis de datos.
        """
        
        # Llamar a OpenAI con la nueva API
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

# Contenido principal
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div style="padding: 15px 0;">
    <h1 style="margin: 0; font-size: 24px; color: #1f2937; font-weight: 700;">📊 SOCIAL MEDIA DASHBOARD</h1>
    <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 13px;">
        Analytics en Tiempo Real • Monitoreo de Performance • {current_time}
    </p>
</div>
""", unsafe_allow_html=True)

# Métricas de pauta publicitaria
if not df_pauta.empty:
    coste_anuncio_sum = df_pauta['coste_anuncio'].sum() if 'coste_anuncio' in df_pauta.columns else 0
    visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum() if 'visualizaciones_videos' in df_pauta.columns else 0
    nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum() if 'nuevos_seguidores' in df_pauta.columns else 0
    
    def format_number(num):
        try:
            return f"{int(num):,}".replace(",", ".")
        except:
            return "0"
    
    st.markdown("### 📊 MÉTRICAS DE PAUTA")
    col_pauta1, col_pauta2, col_pauta3 = st.columns(3)
    
    with col_pauta1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">COSTE ANUNCIO</div>
            <div class="metric-value">${format_number(coste_anuncio_sum)}</div>
            <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Total invertido</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">VISUALIZACIONES VIDEOS</div>
            <div class="metric-value">{format_number(visualizaciones_videos_sum)}</div>
            <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Reproducciones totales</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">NUEVOS SEGUIDORES</div>
            <div class="metric-value">{format_number(nuevos_seguidores_sum)}</div>
            <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Audiencia ganada</div>
        </div>
        """, unsafe_allow_html=True)

# Métricas generales
total_seguidores = 0
if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
    total_seguidores = int(df_followers['Seguidores_Totales'].iloc[-1] if len(df_followers) > 0 else 0)

total_contenidos = len(df_all)
total_visualizaciones = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0

st.markdown("### 📈 MÉTRICAS GENERALES")
col_gen1, col_gen2, col_gen3 = st.columns(3)

with col_gen1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL SEGUIDORES</div>
        <div class="metric-value">{total_seguidores:,}</div>
        <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Seguidores TikTok</div>
    </div>
    """, unsafe_allow_html=True)

with col_gen2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL CONTENIDOS</div>
        <div class="metric-value">{total_contenidos:,}</div>
        <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Publicaciones totales</div>
    </div>
    """, unsafe_allow_html=True)

with col_gen3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">VISUALIZACIONES TOTALES</div>
        <div class="metric-value">{total_visualizaciones:,}</div>
        <div style="font-size: 10px; color: #9ca3af; margin-top: 5px;">Alcance total</div>
    </div>
    """, unsafe_allow_html=True)

# Selector de gráficas
st.markdown("### 📈 GRÁFICAS DE ANÁLISIS")

# Inicializar estado para gráfica seleccionada
if "grafica_seleccionada" not in st.session_state:
    st.session_state.grafica_seleccionada = "evolucion"

# Selector visual
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈 Evolución", 
                 key="btn_evolucion",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "evolucion" else "secondary"):
        st.session_state.grafica_seleccionada = "evolucion"
        st.rerun()

with col2:
    if st.button("💰 Inversión vs Seguidores", 
                 key="btn_grafica1",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "grafica1" else "secondary"):
        st.session_state.grafica_seleccionada = "grafica1"
        st.rerun()

with col3:
    if st.button("📊 Heatmap CPS", 
                 key="btn_grafica2",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "grafica2" else "secondary"):
        st.session_state.grafica_seleccionada = "grafica2"
        st.rerun()

# Mostrar gráfica seleccionada
if st.session_state.grafica_seleccionada == "grafica1":
    st.markdown("#### 📈 Gráfica 1: Inversión vs Seguidores")
    img_bytes = cargar_imagen_grafica1_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 1")

elif st.session_state.grafica_seleccionada == "grafica2":
    st.markdown("#### 📊 Gráfica 2: Heatmap CPS")
    img_bytes = cargar_imagen_grafica2_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 2")

else:  # Gráfica de evolución
    st.markdown("#### 📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA")
    
    if not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
        try:
            # Preparar datos combinados
            if not df_pauta.empty:
                df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
                df_pauta_agg = df_pauta.groupby('fecha').agg({
                    'coste_anuncio': 'sum',
                    'visualizaciones_videos': 'sum',
                    'nuevos_seguidores': 'sum'
                }).reset_index()
                
                df_merged = pd.merge(df_followers, df_pauta_agg, left_on='Fecha', right_on='fecha', how='outer')
                df_merged = df_merged.sort_values('Fecha')
                
                for col in ['Seguidores_Totales', 'coste_anuncio', 'visualizaciones_videos', 'nuevos_seguidores']:
                    if col in df_merged.columns:
                        df_merged[col] = df_merged[col].fillna(method='ffill').fillna(0)
            else:
                df_merged = df_followers.copy()
                df_merged['coste_anuncio'] = 0
                df_merged['visualizaciones_videos'] = 0
                df_merged['nuevos_seguidores'] = 0
            
            # Crear gráfica
            fig = go.Figure()
            
            # Seguidores Totales
            fig.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['Seguidores_Totales'],
                mode='lines+markers',
                name='👥 Seguidores Totales',
                marker=dict(size=6, color='#000000'),
                line=dict(color='#000000', width=2),
                hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores: %{y:,}<extra></extra>'
            ))
            
            # Costo de Pauta (barras)
            if 'coste_anuncio' in df_merged.columns and df_merged['coste_anuncio'].sum() > 0:
                fig.add_trace(go.Bar(
                    x=df_merged['Fecha'],
                    y=df_merged['coste_anuncio'],
                    name='💰 Costo Pauta',
                    marker=dict(color='#ef4444', opacity=0.6),
                    hovertemplate='Costo Pauta: $%{y:,}<extra></extra>',
                    yaxis='y2'
                ))
            
            # Configurar layout
            fig.update_layout(
                height=350,
                template='plotly_white',
                hovermode='x unified',
                showlegend=True,
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
                    tickformat='%d/%m/%Y',
                    title_font=dict(size=12)
                ),
                yaxis=dict(
                    title="Seguidores",
                    gridcolor='#f1f5f9',
                    title_font=dict(size=12)
                ),
                yaxis2=dict(
                    title="Costo ($)",
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    title_font=dict(size=12, color='#ef4444')
                ) if 'coste_anuncio' in df_merged.columns and df_merged['coste_anuncio'].sum() > 0 else None,
                margin=dict(l=40, r=40, t=20, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas resumidas
            if len(df_merged) > 0:
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    latest_followers = df_merged['Seguidores_Totales'].iloc[-1]
                    st.metric("👥 Seguidores actuales", f"{latest_followers:,}")
                
                with col_stat2:
                    if 'coste_anuncio' in df_merged.columns:
                        total_costo = df_merged['coste_anuncio'].sum()
                        st.metric("💰 Inversión total", f"${total_costo:,}")
                    else:
                        st.metric("💰 Inversión total", "N/D")
                
                with col_stat3:
                    if 'nuevos_seguidores' in df_merged.columns:
                        total_nuevos = df_merged['nuevos_seguidores'].sum()
                        st.metric("📈 Seguidores nuevos", f"{total_nuevos:,}")
                    else:
                        st.metric("📈 Seguidores nuevos", "N/D")
                        
        except Exception as e:
            st.warning(f"Error al generar gráfica: {str(e)}")
    else:
        st.warning("No hay datos de seguidores disponibles")

# Tabla de contenido
st.markdown("### 📊 TABLA DE CONTENIDOS")

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
        display_df['titulo'] = display_df['titulo'].fillna('Sin título').str.slice(0, 50) + '...'
    
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
    
    # Mostrar tabla con estilo minimalista
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    # Contador de registros
    st.caption(f"Mostrando {len(display_df)} registros • Plataforma: {selected_platform.title()}")

# Footer minimalista
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 11px; padding: 15px 0; margin-top: 20px; border-top: 1px solid #e5e7eb;">
    Social Media Dashboard v1.0 • Data from Backend API • Actualizado en tiempo real
</div>
""", unsafe_allow_html=True)
