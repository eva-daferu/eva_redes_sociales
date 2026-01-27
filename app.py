import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
import openai

warnings.filterwarnings('ignore')

# Configuración de OpenAI
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

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
METRICAS1_URL = "https://pahubisas.pythonanywhere.com/metricas_grafica1"
METRICAS2_URL = "https://pahubisas.pythonanywhere.com/metricas_grafica2"

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

.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 22px 18px;
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

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #1f2937;
    margin: 12px 0 5px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.metric-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.data-table-container {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

.chat-container {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    border: 1px solid #e5e7eb;
    height: 500px;
    overflow-y: auto;
}

.chat-message {
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 80%;
}

.user-message {
    background: #3B82F6;
    color: white;
    margin-left: auto;
}

.assistant-message {
    background: #f1f5f9;
    color: #1f2937;
}

.grafica-selector {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.selector-btn {
    padding: 10px 20px;
    border-radius: 8px;
    background: #f1f5f9;
    border: 2px solid #e5e7eb;
    color: #64748b;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.selector-btn.active {
    background: #3B82F6;
    color: white;
    border-color: #3B82F6;
}

.selector-btn:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar para el chat
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 55px; height: 55px; border-radius: 14px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 12px auto; font-size: 26px;">
            🤖
        </div>
        <h2 style="color: #1f2937; margin-bottom: 4px; font-size: 20px;">Asistente de Datos</h2>
        <p style="color: #6b7280; font-size: 12px; margin: 0;">Consulta sobre los datos estadísticos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar historial de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input de chat
    user_input = st.chat_input("Haz una pregunta sobre los datos...")
    
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Preparar contexto con los datos
        contexto = """
        Datos disponibles del dashboard:
        
        1. Datos principales de contenido:
        - Total de publicaciones: {total_posts}
        - Visualizaciones totales: {total_views}
        - Total de seguidores: {total_followers}
        
        2. Métricas de pauta publicitaria:
        - Coste total de anuncios: ${coste_anuncio:,}
        - Visualizaciones de videos: {visualizaciones_videos:,}
        - Nuevos seguidores: {nuevos_seguidores:,}
        
        3. Fuentes de datos:
        - Contenidos de TikTok: {tiktok_posts} publicaciones
        - Contenidos de YouTube: {youtube_posts} publicaciones
        - Datos de seguidores disponibles desde: {fecha_inicio_seguidores} hasta {fecha_fin_seguidores}
        """.format(
            total_posts=len(df_all),
            total_views=df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0,
            total_followers=df_followers['Seguidores_Totales'].iloc[-1] if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns else 0,
            coste_anuncio=df_pauta['coste_anuncio'].sum() if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns else 0,
            visualizaciones_videos=df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0,
            nuevos_seguidores=df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0,
            tiktok_posts=len(tiktok_df),
            youtube_posts=len(youtobe_df),
            fecha_inicio_seguidores=df_followers['Fecha'].min().strftime('%Y-%m-%d') if not df_followers.empty and 'Fecha' in df_followers.columns else 'N/D',
            fecha_fin_seguidores=df_followers['Fecha'].max().strftime('%Y-%m-%d') if not df_followers.empty and 'Fecha' in df_followers.columns else 'N/D'
        )
        
        # Llamar a OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente especializado en análisis de datos de redes sociales. Tienes acceso a datos estadísticos de TikTok, YouTube y métricas de pauta publicitaria. Responde de manera clara y concisa."},
                    {"role": "system", "content": contexto},
                    *st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=500
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
<div style="background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
            border-radius: 18px;
            padding: 25px 30px;
            color: white;
            margin-bottom: 20px;">
    <h1 style="margin: 0; font-size: 32px; font-weight: 800;">📊 SOCIAL MEDIA DASHBOARD</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px;">
        Analytics en Tiempo Real • Monitoreo de Performance
    </p>
    <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8;">
        Actualizado: {current_time}
    </div>
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
    
    st.markdown("### 📊 MÉTRICAS DE PAUTA PUBLICITARIA")
    col_pauta1, col_pauta2, col_pauta3 = st.columns(3)
    
    with col_pauta1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">COSTE ANUNCIO</div>
            <div class="metric-value">${format_number(coste_anuncio_sum)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">VISUALIZACIONES VIDEOS</div>
            <div class="metric-value">{format_number(visualizaciones_videos_sum)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">NUEVOS SEGUIDORES</div>
            <div class="metric-value">{format_number(nuevos_seguidores_sum)}</div>
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
    </div>
    """, unsafe_allow_html=True)

with col_gen2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL CONTENIDOS</div>
        <div class="metric-value">{total_contenidos:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_gen3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">VISUALIZACIONES TOTALES</div>
        <div class="metric-value">{total_visualizaciones:,}</div>
    </div>
    """, unsafe_allow_html=True)

# Selector de gráficas
st.markdown("### 📈 GRÁFICA DE EVOLUCIÓN")

# Inicializar estado para gráfica seleccionada
if "grafica_seleccionada" not in st.session_state:
    st.session_state.grafica_seleccionada = "grafica1"

# Selector visual
col1, col2 = st.columns(2)
with col1:
    if st.button("📈 Gráfica 1 - Inversión vs Seguidores", 
                 key="btn_grafica1",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "grafica1" else "secondary"):
        st.session_state.grafica_seleccionada = "grafica1"
        st.rerun()

with col2:
    if st.button("📊 Gráfica 2 - Heatmap CPS", 
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
else:
    st.markdown("#### 📊 Gráfica 2: Heatmap CPS")
    img_bytes = cargar_imagen_grafica2_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 2")

# Gráfica de Evolución de Seguidores y Pauta
if not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
    st.markdown("### 📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA")
    
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
            marker=dict(size=8, color='#000000'),
            line=dict(color='#000000', width=3),
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores Totales: %{y:,}<extra></extra>'
        ))
        
        # Costo de Pauta (barras)
        fig.add_trace(go.Bar(
            x=df_merged['Fecha'],
            y=df_merged['coste_anuncio'],
            name='💰 Costo Pauta',
            marker=dict(color='#ef4444', opacity=0.7),
            hovertemplate='Costo Pauta: $%{y:,}<extra></extra>',
            yaxis='y2'
        ))
        
        # Configurar layout
        fig.update_layout(
            height=450,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(title="Fecha", gridcolor='#f1f5f9', tickformat='%d/%m/%Y'),
            yaxis=dict(title="Seguidores", gridcolor='#f1f5f9'),
            yaxis2=dict(
                title="Costo ($)",
                overlaying='y',
                side='right',
                gridcolor='rgba(241, 245, 249, 0.5)',
                showgrid=False
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            latest_followers = df_merged['Seguidores_Totales'].iloc[-1] if len(df_merged) > 0 else 0
            st.metric("👥 Últimos seguidores", f"{latest_followers:,}")
        
        with col_stat2:
            total_costo = df_merged['coste_anuncio'].sum()
            st.metric("💰 Costo total pauta", f"${total_costo:,}")
        
        with col_stat3:
            if 'nuevos_seguidores' in df_merged.columns:
                total_nuevos = df_merged['nuevos_seguidores'].sum()
                st.metric("👥 Seguidores nuevos pauta", f"{total_nuevos:,}")
            else:
                st.metric("👥 Seguidores nuevos pauta", "N/D")
                
    except Exception as e:
        st.warning(f"Error al generar gráfica: {str(e)}")

# Tabla de contenido
st.markdown("### 📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA")

if not df_all.empty:
    display_df = df_all.copy()
    
    # Seleccionar columnas relevantes
    column_order = []
    if 'titulo' in display_df.columns:
        column_order.append('titulo')
        display_df['titulo'] = display_df['titulo'].fillna('Sin título')
    
    if 'fecha_publicacion' in display_df.columns:
        column_order.append('fecha_publicacion')
        display_df['fecha_publicacion'] = display_df['fecha_publicacion'].dt.strftime('%d/%m/%Y %H:%M')
    
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
        'titulo': '📝 TÍTULO',
        'fecha_publicacion': '📅 FECHA',
        'red': '🌐 PLATAFORMA',
        'visualizaciones': '👁️ VISUALIZACIONES',
        'me_gusta': '❤️ LIKES',
        'comentarios': '💬 COMENTARIOS',
        'Seguidores_Totales': '👥 SEGUIDORES'
    }
    
    display_df = display_df.rename(columns={k: v for k, v in rename_dict.items() if k in display_df.columns})
    
    # Mostrar tabla
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Estadísticas de la tabla
    col_tab1, col_tab2, col_tab3 = st.columns(3)
    
    with col_tab1:
        avg_views = display_df['👁️ VISUALIZACIONES'].mean() if '👁️ VISUALIZACIONES' in display_df.columns else 0
        st.metric("📊 Views promedio", f"{avg_views:,.0f}")
    
    with col_tab2:
        avg_likes = display_df['❤️ LIKES'].mean() if '❤️ LIKES' in display_df.columns else 0
        st.metric("📊 Likes promedio", f"{avg_likes:,.0f}")
    
    with col_tab3:
        avg_comments = display_df['💬 COMENTARIOS'].mean() if '💬 COMENTARIOS' in display_df.columns else 0
        st.metric("📊 Comments promedio", f"{avg_comments:,.0f}")

# Footer
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 12px; padding: 25px; 
            border-top: 1px solid #e5e7eb; margin-top: 30px;">
    <div style="display: flex; justify-content: center; gap: 25px; margin-bottom: 12px; flex-wrap: wrap;">
        <span>Social Media Dashboard v1.0</span>
        <span>•</span>
        <span>Data from Backend API</span>
        <span>•</span>
        <span>Updated: {current_time_full}</span>
    </div>
</div>
""", unsafe_allow_html=True)
