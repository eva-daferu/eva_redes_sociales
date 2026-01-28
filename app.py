import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
import json

warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN DE ENDPOINTS
# ============================================
# ENDPOINTS DEL BACKEND EN PYTHONANYWHERE
BACKEND_BASE_URL = "https://pahubisas.pythonanywhere.com"
DATA_URL = f"{BACKEND_BASE_URL}/data"
FOLLOWERS_URL = f"{BACKEND_BASE_URL}/followers"
PAUTA_URL = f"{BACKEND_BASE_URL}/pauta_anuncio"
GRAFICA1_URL = f"{BACKEND_BASE_URL}/grafica1"
GRAFICA2_URL = f"{BACKEND_BASE_URL}/grafica2"
OPENAI_URL = f"{BACKEND_BASE_URL}/openai_response"  # Endpoint para IA

# ============================================
# FUNCIONES PARA CARGAR DATOS
# ============================================
@st.cache_data(ttl=300)
def cargar_datos_principales():
    """Carga datos principales del backend"""
    try:
        response = requests.get(DATA_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            df = pd.DataFrame(data["data"])
        else:
            df = pd.DataFrame(data)
        
        # Limpieza y transformación de datos
        if not df.empty:
            # Convertir fechas
            date_columns = ['fecha_publicacion', 'fecha', 'Fecha']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
            
            # Convertir columnas numéricas
            numeric_columns = ['visualizaciones', 'vistas', 'me_gusta', 'comentarios', 
                             'Seguidores_Totales', 'me_gusta_numero', 'comentarios_num']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Normalizar nombres de plataformas
            if 'red' in df.columns:
                df['red'] = df['red'].astype(str).str.lower().str.strip()
            elif 'platform' in df.columns:
                df['red'] = df['platform'].astype(str).str.lower().str.strip()
            else:
                df['red'] = 'desconocido'
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos principales: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def cargar_datos_seguidores():
    """Carga datos de seguidores"""
    try:
        response = requests.get(FOLLOWERS_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            df = pd.DataFrame(data["data"])
        else:
            df = pd.DataFrame(data)
        
        if not df.empty:
            # Convertir fechas
            if 'Fecha' in df.columns:
                df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
            
            # Convertir numéricas
            if 'Seguidores_Totales' in df.columns:
                df['Seguidores_Totales'] = pd.to_numeric(df['Seguidores_Totales'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos de seguidores: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def cargar_datos_pauta():
    """Carga datos de pauta publicitaria"""
    try:
        response = requests.get(PAUTA_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            df = pd.DataFrame(data["data"])
        else:
            df = pd.DataFrame(data)
        
        if not df.empty:
            # Normalizar nombres de columnas
            column_mapping = {
                'Costo': 'coste_anuncio',
                'Visualizaciones': 'visualizaciones_videos',
                'Seguidores': 'nuevos_seguidores',
                'fecha': 'fecha'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df[new_col] = df[old_col]
            
            # Convertir tipos de datos
            numeric_cols = ['coste_anuncio', 'visualizaciones_videos', 'nuevos_seguidores']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
        
        return df
    except Exception as e:
        return pd.DataFrame()

def cargar_imagen_grafica(url):
    """Carga imagen de gráfica desde URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"Error al cargar imagen: {str(e)}")
        return None

# ============================================
# FUNCIONES DE ASISTENTE IA - VERSIÓN ROBUSTA
# ============================================
def preparar_contexto_para_ia(df_all, df_followers, df_pauta):
    """
    Prepara un resumen completo de los datos para el contexto de IA
    """
    contexto = "CONTEXTO PARA ANÁLISIS DE REDES SOCIALES:\n\n"
    
    # 1. Resumen general
    contexto += "📊 RESUMEN GENERAL:\n"
    contexto += f"• Total de publicaciones: {len(df_all)}\n"
    
    if 'visualizaciones' in df_all.columns:
        total_views = df_all['visualizaciones'].sum()
        avg_views = total_views / len(df_all) if len(df_all) > 0 else 0
        contexto += f"• Visualizaciones totales: {total_views:,.0f}\n"
        contexto += f"• Promedio por publicación: {avg_views:,.0f}\n"
    
    # 2. Datos por plataforma
    contexto += "\n📱 DATOS POR PLATAFORMA:\n"
    if 'red' in df_all.columns:
        platforms = df_all['red'].value_counts()
        for platform, count in platforms.items():
            platform_data = df_all[df_all['red'] == platform]
            platform_views = platform_data['visualizaciones'].sum() if 'visualizaciones' in platform_data.columns else 0
            contexto += f"• {platform.upper()}: {count} publicaciones, {platform_views:,.0f} visualizaciones\n"
    
    # 3. Seguidores
    contexto += "\n👥 DATOS DE SEGUIDORES:\n"
    if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
        if not df_followers['Seguidores_Totales'].dropna().empty:
            latest_followers = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])
            contexto += f"• Seguidores actuales: {latest_followers:,}\n"
        
        # Crecimiento de seguidores si hay múltiples fechas
        if len(df_followers) > 1 and 'Fecha' in df_followers.columns:
            df_followers_sorted = df_followers.sort_values('Fecha')
            growth = df_followers_sorted['Seguidores_Totales'].iloc[-1] - df_followers_sorted['Seguidores_Totales'].iloc[0]
            contexto += f"• Crecimiento neto: {growth:+,}\n"
    
    # 4. Inversión publicitaria
    contexto += "\n💰 INVERSIÓN PUBLICITARIA:\n"
    if not df_pauta.empty:
        if 'coste_anuncio' in df_pauta.columns:
            total_investment = df_pauta['coste_anuncio'].sum()
            contexto += f"• Inversión total: ${total_investment:,.0f}\n"
        
        if 'visualizaciones_videos' in df_pauta.columns:
            paid_views = df_pauta['visualizaciones_videos'].sum()
            contexto += f"• Visualizaciones pagadas: {paid_views:,}\n"
            
            if total_investment > 0 and paid_views > 0:
                cpm = (total_investment / paid_views) * 1000
                contexto += f"• CPM (Costo por mil): ${cpm:,.2f}\n"
        
        if 'nuevos_seguidores' in df_pauta.columns:
            new_followers = df_pauta['nuevos_seguidores'].sum()
            contexto += f"• Nuevos seguidores de pauta: {new_followers:,}\n"
            
            if total_investment > 0 and new_followers > 0:
                cost_per_follower = total_investment / new_followers
                contexto += f"• Costo por seguidor: ${cost_per_follower:,.2f}\n"
    
    # 5. Top contenido
    contexto += "\n🏆 CONTENIDO DESTACADO:\n"
    if not df_all.empty and 'titulo' in df_all.columns and 'visualizaciones' in df_all.columns:
        top_content = df_all.nlargest(3, 'visualizaciones')[['titulo', 'visualizaciones', 'red']]
        for idx, row in top_content.iterrows():
            titulo = str(row['titulo'])[:50] + "..." if len(str(row['titulo'])) > 50 else str(row['titulo'])
            contexto += f"• {titulo}: {row['visualizaciones']:,} vistas ({row['red']})\n"
    
    # 6. Recomendaciones base
    contexto += "\n💡 INSTRUCCIONES PARA EL ASISTENTE:\n"
    contexto += """Eres un analista de redes sociales especializado. Basándote en los datos proporcionados:
    1. Analiza el rendimiento del contenido
    2. Evalúa el ROI de la inversión publicitaria
    3. Identifica tendencias y oportunidades
    4. Proporciona recomendaciones específicas y accionables
    5. Usa un tono profesional pero amigable
    6. Incluye métricas relevantes en tu análisis
    7. Responde directamente a la pregunta del usuario
    
    Formato de respuesta: Claro, estructurado y con emojis relevantes."""
    
    return contexto

def enviar_pregunta_a_backend(pregunta, contexto):
    """Envía la pregunta al backend de PythonAnywhere"""
    try:
        # Preparar el prompt completo
        prompt_completo = f"{contexto}\n\nPREGUNTA DEL USUARIO: {pregunta}\n\nRESPUESTA DEL ASISTENTE:"
        
        # Enviar al backend
        payload = {
            "input": prompt_completo,
            "model": "gpt-4.1-mini",
            "max_output_tokens": 500
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(OPENAI_URL, json=payload, headers=headers, timeout=60)
        
        # Manejar diferentes formatos de respuesta
        if response.status_code == 200:
            # Intentar como JSON
            try:
                data = response.json()
                # Buscar respuesta en diferentes estructuras
                if isinstance(data, dict):
                    if "data" in data and "output_text" in data["data"]:
                        return data["data"]["output_text"]
                    elif "output_text" in data:
                        return data["output_text"]
                    elif "response" in data:
                        return data["response"]
                    elif "text" in data:
                        return data["text"]
                    elif "message" in data:
                        return data["message"]
                    else:
                        # Devolver el primer valor de texto encontrado
                        for key, value in data.items():
                            if isinstance(value, str) and len(value) > 20:
                                return value
                # Si no es dict, devolver el texto
                return response.text
            except json.JSONDecodeError:
                # Si no es JSON, devolver texto plano
                text_response = response.text.strip()
                if text_response and text_response != "OpenAI response":
                    return text_response
                else:
                    return "El backend respondió pero no proporcionó una respuesta válida."
        else:
            return f"Error del backend: Código {response.status_code} - {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return "⏳ El servidor tardó demasiado en responder. Por favor, intenta nuevamente."
    except requests.exceptions.ConnectionError:
        return "🔌 Error de conexión con el servidor. Verifica tu conexión a internet."
    except Exception as e:
        return f"❌ Error inesperado: {str(e)}"

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ============================================
# CARGAR DATOS UNA VEZ
# ============================================
@st.cache_resource
def cargar_todos_los_datos():
    """Carga todos los datos necesarios"""
    with st.spinner("Cargando datos del servidor..."):
        df_all = cargar_datos_principales()
        df_followers = cargar_datos_seguidores()
        df_pauta = cargar_datos_pauta()
        
        # Preparar datos por plataforma
        youtobe_df = pd.DataFrame()
        tiktok_df = pd.DataFrame()
        
        if not df_all.empty and 'red' in df_all.columns:
            youtobe_df = df_all[df_all['red'].str.contains('youtub|youtobe', case=False, na=False)].copy()
            tiktok_df = df_all[df_all['red'].str.contains('tiktok', case=False, na=False)].copy()
        
        return df_all, youtobe_df, tiktok_df, df_followers, df_pauta

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_todos_los_datos()

# ============================================
# ESTILOS CSS
# ============================================
st.markdown("""
<style>
/* Estilos generales */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 16px;
    padding: 22px 26px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.35);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.dashboard-header h1 {
    margin: 0;
    font-size: 26px;
    font-weight: 800;
    line-height: 1.2;
    font-family: 'Arial Black', sans-serif;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.metric-card {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 14px;
    padding: 20px 16px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #bae6fd;
    text-align: center;
    transition: all 0.3s ease;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.metric-icon {
    font-size: 28px;
    margin-bottom: 10px;
    color: #0ea5e9;
}

.metric-value {
    font-size: 28px;
    font-weight: 900;
    color: #0369a1;
    margin: 5px 0;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.metric-label {
    font-size: 12px;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    line-height: 1.4;
}

/* Estilos para el chat */
.chat-container {
    background: white;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    height: 320px;
    overflow-y: auto;
    padding: 15px;
    margin-bottom: 15px;
}

.user-message {
    background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 14px 14px 4px 14px;
    max-width: 85%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 12px;
    line-height: 1.4;
}

.assistant-message {
    background: #f8fafc;
    color: #1f2937;
    padding: 10px 14px;
    border-radius: 14px 14px 14px 4px;
    max-width: 85%;
    margin-right: auto;
    margin-bottom: 10px;
    font-size: 12px;
    line-height: 1.4;
    border: 1px solid #e5e7eb;
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 10px 14px;
    background: #f8fafc;
    border-radius: 14px;
    width: fit-content;
    margin-right: auto;
}

.typing-dot {
    width: 6px;
    height: 6px;
    background: #8B5CF6;
    border-radius: 50%;
    animation: pulse 1.4s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - ASISTENTE IA
# ============================================
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="
            background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
            width: 52px; 
            height: 52px; 
            border-radius: 14px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin: 0 auto 12px auto; 
            font-size: 24px;
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
        ">
            🤖
        </div>
        <h3 style="color: white; margin: 0; font-size: 15px; font-weight: 800;">AI ANALYTICS PRO</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        test_response = requests.get(DATA_URL, timeout=5)
        if test_response.status_code == 200:
            st.success("✅ Backend conectado")
        else:
            st.error(f"⚠️ Backend error: {test_response.status_code}")
    except:
        st.error("⚠️ No se pudo conectar al backend")
    
    # Selector de plataforma
    st.markdown("---")
    st.subheader("📊 Panel de Análisis")
    
    platform_options = {
        "general": "🌐 Vista General",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok"
    }
    
    selected_platform = st.radio(
        "Selecciona plataforma:",
        options=list(platform_options.keys()),
        format_func=lambda x: platform_options[x],
        key="platform_selector"
    )
    
    # ASISTENTE IA
    st.markdown("---")
    st.subheader("🤖 Asistente IA")
    
    # Inicializar historial de chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 ¡Hola! Soy tu asistente de análisis de redes sociales. Puedo ayudarte a analizar métricas, tendencias, ROI de campañas y más. ¿En qué puedo ayudarte hoy?"}
        ]
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Mostrar historial de chat
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Mostrar indicador de escritura si está procesando
        if st.session_state.processing:
            st.markdown('''
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input de chat
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Escribe tu pregunta:",
            height=80,
            placeholder="Ej: ¿Cuál es el ROI de la campaña publicitaria?",
            key="chat_input"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_button = st.form_submit_button("Enviar", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("Limpiar", use_container_width=True, type="secondary")
    
    # Procesar mensaje
    if submit_button and user_input.strip():
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        st.session_state.processing = True
        
        # Preparar contexto con los datos actuales
        contexto = preparar_contexto_para_ia(df_all, df_followers, df_pauta)
        
        # Obtener respuesta del backend
        respuesta = enviar_pregunta_a_backend(user_input.strip(), contexto)
        
        # Agregar respuesta al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.session_state.processing = False
        st.rerun()
    
    # Limpiar chat
    if clear_button:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "👋 ¡Conversación reiniciada! ¿En qué puedo ayudarte ahora?"}
        ]
        st.rerun()

# ============================================
# CONTENIDO PRINCIPAL
# ============================================
st.markdown(f"""
<div class="dashboard-header">
    <h1>📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 0; opacity: 0.9; font-size: 13px;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================
# Calcular métricas
total_inversion = df_pauta['coste_anuncio'].sum() if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns else 0
total_visualizaciones_pagadas = df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0
nuevos_seguidores_pauta = df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0

# Seguidores actuales
seguidores_actuales = 0
if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
    if not df_followers['Seguidores_Totales'].dropna().empty:
        seguidores_actuales = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])

# Métricas de contenido
total_publicaciones = len(df_all)
total_visualizaciones = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0
promedio_visualizaciones = total_visualizaciones / total_publicaciones if total_publicaciones > 0 else 0

# Calcular ROI
costo_por_seguidor = total_inversion / nuevos_seguidores_pauta if nuevos_seguidores_pauta > 0 else 0
cpm = (total_inversion / total_visualizaciones_pagadas * 1000) if total_visualizaciones_pagadas > 0 else 0

# Mostrar métricas en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-value">${total_inversion:,.0f}</div>
        <div class="metric-label">INVERSIÓN TOTAL</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">👥</div>
        <div class="metric-value">{seguidores_actuales:,}</div>
        <div class="metric-label">SEGUIDORES ACTUALES</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-value">${costo_por_seguidor:,.1f}</div>
        <div class="metric-label">COSTO POR SEGUIDOR</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-value">{nuevos_seguidores_pauta:,}</div>
        <div class="metric-label">NUEVOS SEGUIDORES</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# GRÁFICAS Y TABLAS
# ============================================
st.markdown("---")

# Selector de visualización
viz_option = st.radio(
    "Selecciona visualización:",
    ["📈 Evolución de Seguidores", "💰 Análisis de Inversión", "📊 Heatmap de Performance"],
    horizontal=True,
    key="viz_selector"
)

if viz_option == "📈 Evolución de Seguidores":
    st.subheader("Evolución de Seguidores")
    
    if not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_followers['Fecha'],
            y=df_followers['Seguidores_Totales'],
            mode='lines+markers',
            name='Seguidores',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            xaxis_title="Fecha",
            yaxis_title="Seguidores Totales",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de seguidores disponibles")

elif viz_option == "💰 Análisis de Inversión":
    st.subheader("Análisis de Inversión")
    
    img_bytes = cargar_imagen_grafica(GRAFICA1_URL)
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.info("No hay gráfica de inversión disponible")

else:  # Heatmap de Performance
    st.subheader("Heatmap de Performance")
    
    img_bytes = cargar_imagen_grafica(GRAFICA2_URL)
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.info("No hay heatmap disponible")

# ============================================
# TABLA DE CONTENIDO
# ============================================
st.markdown("---")
st.subheader(f"📋 Contenido - {selected_platform.upper()}")

# Filtrar por plataforma seleccionada
if selected_platform == "youtube":
    display_df = youtobe_df.copy()
    platform_name = "YouTube"
elif selected_platform == "tiktok":
    display_df = tiktok_df.copy()
    platform_name = "TikTok"
else:
    display_df = df_all.copy()
    platform_name = "Todas las Plataformas"

if not display_df.empty:
    # Seleccionar columnas relevantes
    columns_to_show = []
    column_names = {}
    
    if 'titulo' in display_df.columns:
        columns_to_show.append('titulo')
        column_names['titulo'] = 'Título'
    
    if 'fecha_publicacion' in display_df.columns:
        columns_to_show.append('fecha_publicacion')
        column_names['fecha_publicacion'] = 'Fecha'
    
    if 'visualizaciones' in display_df.columns:
        columns_to_show.append('visualizaciones')
        column_names['visualizaciones'] = 'Vistas'
    
    if 'me_gusta' in display_df.columns:
        columns_to_show.append('me_gusta')
        column_names['me_gusta'] = 'Likes'
    
    if 'comentarios' in display_df.columns:
        columns_to_show.append('comentarios')
        column_names['comentarios'] = 'Comentarios'
    
    if columns_to_show:
        # Preparar DataFrame para mostrar
        df_to_display = display_df[columns_to_show].copy()
        
        # Formatear columnas
        if 'fecha_publicacion' in df_to_display.columns:
            df_to_display['fecha_publicacion'] = pd.to_datetime(df_to_display['fecha_publicacion']).dt.strftime('%d/%m/%Y')
        
        if 'titulo' in df_to_display.columns:
            df_to_display['titulo'] = df_to_display['titulo'].apply(
                lambda x: x[:50] + '...' if isinstance(x, str) and len(x) > 50 else x
            )
        
        # Renombrar columnas
        df_to_display = df_to_display.rename(columns=column_names)
        
        # Mostrar tabla
        st.dataframe(
            df_to_display,
            use_container_width=True,
            hide_index=True,
            height=300
        )
    else:
        st.info(f"No hay columnas disponibles para mostrar de {platform_name}")
else:
    st.info(f"No hay datos disponibles para {platform_name}")

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.caption(f"Social Media Dashboard PRO • Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
