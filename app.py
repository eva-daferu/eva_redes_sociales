import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
from openai import OpenAI
import json

warnings.filterwarnings('ignore')

# Configuración de OpenAI
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
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
    """Carga datos de seguidores con mejor manejo de errores"""
    try:
        r = requests.get(FOLLOWERS_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Debug: Mostrar estructura de datos
        st.sidebar.info(f"Estructura datos seguidores: {list(data.keys()) if isinstance(data, dict) else 'No es dict'}")
        
        df_followers = pd.DataFrame(data.get("data", []))
        
        if df_followers.empty:
            # Intentar diferente estructura
            if isinstance(data, list):
                df_followers = pd.DataFrame(data)
            elif isinstance(data, dict) and "followers" in data:
                df_followers = pd.DataFrame(data["followers"])
        
        # Depuración
        if not df_followers.empty:
            st.sidebar.success(f"Datos seguidores cargados: {len(df_followers)} filas")
            st.sidebar.info(f"Columnas: {list(df_followers.columns)}")
            st.sidebar.info(f"Primeras filas:\n{df_followers.head().to_string()}")
        
        # Manejar diferentes nombres de columnas
        column_mapping = {
            'Seguidores_Totales': ['Seguidores_Totales', 'seguidores_totales', 'total_followers', 'followers_total', 'Followers'],
            'Fecha': ['Fecha', 'fecha', 'date', 'Date', 'fecha_registro']
        }
        
        # Renombrar columnas si es necesario
        for standard_name, possible_names in column_mapping.items():
            for possible_name in possible_names:
                if possible_name in df_followers.columns and standard_name not in df_followers.columns:
                    df_followers[standard_name] = df_followers[possible_name]
                    break
        
        if "Fecha" in df_followers.columns:
            df_followers["Fecha"] = pd.to_datetime(
                df_followers["Fecha"],
                dayfirst=True,
                errors="coerce"
            )
        
        if "Seguidores_Totales" in df_followers.columns:
            # Convertir a numérico y manejar valores no numéricos
            df_followers["Seguidores_Totales"] = pd.to_numeric(
                df_followers["Seguidores_Totales"], 
                errors='coerce'
            )
            # Remover filas con valores NaN
            df_followers = df_followers.dropna(subset=['Seguidores_Totales'])
        
        return df_followers
    except Exception as e:
        st.sidebar.error(f"Error cargando seguidores: {str(e)}")
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
                # Convertir a numérico y limpiar
                df_pauta["coste_anuncio"] = pd.to_numeric(df_pauta["coste_anuncio"], errors="coerce")
                # Reemplazar NaN por 0
                df_pauta["coste_anuncio"] = df_pauta["coste_anuncio"].fillna(0)
            
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
        st.warning("Usando datos de respaldo para contenido principal.")
        
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
        
        # Datos de prueba solo si no hay datos reales
        if df_followers.empty:
            df_followers = pd.DataFrame({
                'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
                'Seguidores_Totales': range(400, 430)
            })
            st.sidebar.warning("Usando datos de prueba para seguidores")
        
        if df_pauta.empty:
            df_pauta = pd.DataFrame({
                'coste_anuncio': [641140],
                'visualizaciones_videos': [180500],
                'nuevos_seguidores': [4170],
                'fecha': ['2025-10-19']
            })
            st.sidebar.warning("Usando datos de prueba para pauta")
        
    else:
        if 'red' in df.columns:
            df['red'] = df['red'].astype(str).str.lower().str.strip()
        
        youtobe_data = df[df['red'] == 'youtobe'].copy()
        if youtobe_data.empty:
            youtobe_data = df[df['red'] == 'youtube'].copy()
        
        tiktok_data = df[df['red'] == 'tiktok'].copy()
    
    return df, youtobe_data, tiktok_data, df_followers, df_pauta

# Estilos CSS
st.markdown("""
<style>
/* Animación shimmer */
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Header principal */
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

/* Contenedores */
.performance-chart {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
    border: 1px solid #e5e7eb;
}

.data-table-container {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
    border: 1px solid #e5e7eb;
}

/* Selector de gráficas */
.grafica-selector-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 16px;
    padding: 15px;
    margin: 15px 0 18px 0;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.grafica-selector-title {
    font-size: 15px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 12px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.grafica-selector-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.grafica-selector-btn {
    flex: 1;
    max-width: 240px;
    padding: 18px 16px;
    border-radius: 14px;
    background: white;
    border: 2px solid #e5e7eb;
    color: #64748b;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    font-size: 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.grafica-selector-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

.grafica-selector-btn.active {
    background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    color: white;
    border-color: #3B82F6;
    box-shadow: 0 12px 30px rgba(59, 130, 246, 0.5);
}

/* Estilos para las métricas */
.metric-container {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 14px;
    padding: 20px 16px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #bae6fd;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.metric-shimmer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0ea5e9 0%, #3B82F6 50%, #0ea5e9 100%);
    background-size: 200% 100%;
    animation: shimmer 3s infinite linear;
    border-radius: 14px 14px 0 0;
}

.metric-icon {
    font-size: 24px;
    margin-bottom: 10px;
    color: #0ea5e9;
}

.metric-value {
    font-size: 20px;
    font-weight: 900;
    color: #0369a1;
    margin: 5px 0;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    word-wrap: break-word;
    max-width: 100%;
}

.metric-label {
    font-size: 12px;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    line-height: 1.4;
}

.metric-container-light {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
}

.metric-shimmer-light {
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #3B82F6 100%);
}

.metric-icon-light {
    color: #1f2937;
}

.metric-value-light {
    color: #1f2937;
}

.metric-label-light {
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 0 10px;">
        <div style="
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            width: 48px; 
            height: 48px; 
            border-radius: 12px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin: 0 auto 10px auto; 
            font-size: 22px;
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
        ">
            📊
        </div>
        <h3 style="color: white; margin-bottom: 4px; font-size: 14px; font-weight: 800;">DASHBOARD PRO</h3>
        <p style="color: #94a3b8; font-size: 10px; margin: 0;">Social Media Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 8px 10px; border-radius: 8px; margin-bottom: 4px; border: 1px solid rgba(16, 185, 129, 0.2); font-size: 10px;">✅ <strong>Backend Conectado</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 8px 10px; border-radius: 8px; margin-bottom: 4px; border: 1px solid rgba(239, 68, 68, 0.2); font-size: 10px;">⚠️ <strong>Backend Error</strong></div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 8px 10px; border-radius: 8px; margin-bottom: 4px; border: 1px solid rgba(239, 68, 68, 0.2); font-size: 10px;">⚠️ <strong>Backend Offline</strong></div>', unsafe_allow_html=True)
    
    # Botones de plataformas
    st.markdown('<p style="color: #cbd5e1; font-size: 11px; font-weight: 600; margin-bottom: 8px; margin-top: 15px; letter-spacing: 0.8px; text-transform: uppercase;">🔗 PANEL PROFESIONAL</p>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    
    # Asistente de Chat
    st.markdown('<p style="color: #cbd5e1; font-size: 11px; font-weight: 600; margin-bottom: 8px; margin-top: 15px; letter-spacing: 0.8px; text-transform: uppercase;">🤖 ASISTENTE DE DATOS</p>', unsafe_allow_html=True)
    
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Contenedor del chat
    with st.container(height=220):
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div style="background: #3B82F6; color: white; padding: 8px 10px; border-radius: 9px; margin-bottom: 6px; font-size: 11px; max-width: 90%; margin-left: auto;">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background: #f1f5f9; color: #1f2937; padding: 8px 10px; border-radius: 9px; margin-bottom: 6px; font-size: 11px; max-width: 90%; border: 1px solid #e5e7eb;">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input de chat
    user_input = st.chat_input("Pregunta sobre los datos...", key="chat_input")
    
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Preparar contexto con datos actuales
        total_posts = len(df_all)
        total_views = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0
        
        # Obtener correctamente los seguidores
        total_followers = 0
        if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
            if not df_followers['Seguidores_Totales'].dropna().empty:
                # Ordenar por fecha para obtener el más reciente
                if 'Fecha' in df_followers.columns:
                    df_followers_sorted = df_followers.sort_values('Fecha')
                    total_followers = int(df_followers_sorted['Seguidores_Totales'].iloc[-1])
                else:
                    total_followers = int(df_followers['Seguidores_Totales'].iloc[-1])
        
        # Calcular coste con IVA
        coste_base = df_pauta['coste_anuncio'].sum() if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns else 0
        coste_anuncio = coste_base * 1.19  # Añadir 19% IVA
        
        visualizaciones_videos = df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0
        nuevos_seguidores = df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0
        
        contexto = f"""
        Eres un asistente especializado en análisis de datos de redes sociales. 
        
        Datos actuales del dashboard:
        - Total de publicaciones: {total_posts}
        - Visualizaciones totales: {total_views:,}
        - Total de seguidores TikTok: {total_followers:,}
        - Inversión en publicidad (con IVA 19%): ${coste_anuncio:,.0f}
        - Visualizaciones de videos pagados: {visualizaciones_videos:,}
        - Nuevos seguidores de publicidad: {nuevos_seguidores:,}
        
        Puedes responder preguntas sobre estas métricas, tendencias, eficiencia de publicidad, y análisis de datos.
        """
        
        # Llamar a OpenAI
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

# Contenido principal - HEADER
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div class="dashboard-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h1>📊 SOCIAL MEDIA DASHBOARD PRO</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 13px; font-weight: 500;">
                Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
            </p>
        </div>
        <div style="font-size: 12px; opacity: 0.9; background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 20px; font-weight: 600;">
            ⏱️ {current_time}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# MÉTRICAS - VERSIÓN SIMPLIFICADA USANDO FUNCIONES HELPER
def format_number(num, full_format=False):
    try:
        num = float(num)
        if full_format:
            # Formato completo con separadores de miles
            return f"{num:,.0f}".replace(",", ".")
        elif num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return f"{int(num):,}"
    except:
        return "0"

def create_metric_card(icon, value, label, is_light=False, full_format=False):
    """Crea una tarjeta de métrica con HTML"""
    if is_light:
        return f"""
        <div class="metric-container metric-container-light">
            <div class="metric-shimmer metric-shimmer-light"></div>
            <div class="metric-icon metric-icon-light">{icon}</div>
            <div class="metric-value metric-value-light">{value}</div>
            <div class="metric-label metric-label-light">{label}</div>
        </div>
        """
    else:
        return f"""
        <div class="metric-container">
            <div class="metric-shimmer"></div>
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """

# Calcular métricas REALES
# 1. Coste de anuncio CON IVA (19%)
if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns:
    coste_base = df_pauta['coste_anuncio'].sum()
    coste_anuncio_sum = coste_base * 1.19  # Agregar 19% IVA
else:
    coste_anuncio_sum = 0

visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0
nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0

# 2. Total seguidores - MEJORADO
total_seguidores = 0
seguidores_info = ""

if not df_followers.empty:
    # Depuración en sidebar
    st.sidebar.info(f"Filas seguidores: {len(df_followers)}")
    
    # Verificar columnas disponibles
    available_columns = list(df_followers.columns)
    st.sidebar.info(f"Columnas disponibles: {available_columns}")
    
    # Buscar columna de seguidores
    seguidores_columns = [col for col in available_columns if 'seguidor' in col.lower() or 'follower' in col.lower()]
    
    if seguidores_columns:
        seguidores_col = seguidores_columns[0]
        st.sidebar.success(f"Columna seguidores encontrada: {seguidores_col}")
        
        # Convertir a numérico
        df_followers[seguidores_col] = pd.to_numeric(df_followers[seguidores_col], errors='coerce')
        
        # Ordenar por fecha si existe
        fecha_columns = [col for col in available_columns if 'fecha' in col.lower() or 'date' in col.lower()]
        if fecha_columns:
            fecha_col = fecha_columns[0]
            df_followers[fecha_col] = pd.to_datetime(df_followers[fecha_col], errors='coerce')
            df_followers = df_followers.sort_values(fecha_col)
            total_seguidores = int(df_followers[seguidores_col].dropna().iloc[-1])
        else:
            total_seguidores = int(df_followers[seguidores_col].dropna().iloc[-1])
        
        seguidores_info = f"Último valor: {total_seguadores:,}"
    else:
        st.sidebar.warning("No se encontró columna de seguidores")
        seguidores_info = "Columna no encontrada"

# También buscar en df_all para datos de TikTok
if total_seguidores == 0 and not tiktok_df.empty:
    if 'Seguidores_Totales' in tiktok_df.columns:
        tiktok_df['Seguidores_Totales'] = pd.to_numeric(tiktok_df['Seguidores_Totales'], errors='coerce')
        if not tiktok_df['Seguidores_Totales'].dropna().empty:
            total_seguidores = int(tiktok_df['Seguidores_Totales'].max())
            seguidores_info = "De datos TikTok"

total_contenidos = len(df_all)
total_visualizaciones = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0

# Crear columnas para las métricas
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Métrica 1: Coste Anuncio CON IVA (formato completo)
with col1:
    html = create_metric_card(
        icon="💰", 
        value=f"${format_number(coste_anuncio_sum, full_format=True)}", 
        label="COSTE ANUNCIO (+IVA 19%)",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)

# Métrica 2: Visualizaciones Videos
with col2:
    html = create_metric_card(
        icon="👁️", 
        value=format_number(visualizaciones_videos_sum), 
        label="VISUALIZACIONES VIDEOS",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)

# Métrica 3: Nuevos Seguidores
with col3:
    html = create_metric_card(
        icon="📈", 
        value=format_number(nuevos_seguidores_sum), 
        label="NUEVOS SEGUIDORES",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)

# Métrica 4: Total Seguidores (REALES) - CORREGIDO
with col4:
    html = create_metric_card(
        icon="👥", 
        value=format_number(total_seguidores), 
        label="TOTAL SEGUIDORES TIKTOK",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)
    
    # Mostrar información adicional
    if seguidores_info:
        st.caption(f"ℹ️ {seguidores_info}")

# Métrica 5: Total Contenidos
with col5:
    html = create_metric_card(
        icon="📊", 
        value=format_number(total_contenidos), 
        label="TOTAL CONTENIDOS",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)

# Métrica 6: Visualizaciones Totales
with col6:
    html = create_metric_card(
        icon="👁️", 
        value=format_number(total_visualizaciones), 
        label="VISUALIZACIONES TOTALES",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)

# Agregar espacio
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Selector de gráficas
st.markdown('<div class="grafica-selector-container">', unsafe_allow_html=True)
st.markdown('<div class="grafica-selector-title">📈 SELECCIONA EL TIPO DE GRÁFICA</div>', unsafe_allow_html=True)

# Inicializar estado para gráfica seleccionada
if "grafica_seleccionada" not in st.session_state:
    st.session_state.grafica_seleccionada = "evolucion"

# Selector visual
st.markdown('<div class="grafica-selector-buttons">', unsafe_allow_html=True)

# Crear botones
col1, col2, col3 = st.columns(3)

with col1:
    btn1_active = st.session_state.grafica_seleccionada == "evolucion"
    if st.button("**📈** **Evolución**", 
                 key="btn_evolucion",
                 use_container_width=True,
                 type="primary" if btn1_active else "secondary"):
        st.session_state.grafica_seleccionada = "evolucion"
        st.rerun()

with col2:
    btn2_active = st.session_state.grafica_seleccionada == "grafica1"
    if st.button("**💰** **Inversión vs Seguidores**", 
                 key="btn_grafica1",
                 use_container_width=True,
                 type="primary" if btn2_active else "secondary"):
        st.session_state.grafica_seleccionada = "grafica1"
        st.rerun()

with col3:
    btn3_active = st.session_state.grafica_seleccionada == "grafica2"
    if st.button("**📊** **Heatmap CPS**", 
                 key="btn_grafica2",
                 use_container_width=True,
                 type="primary" if btn3_active else "secondary"):
        st.session_state.grafica_seleccionada = "grafica2"
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# Mostrar gráfica seleccionada
if st.session_state.grafica_seleccionada == "grafica1":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 Gráfica 1: Inversión vs Seguidores")
    img_bytes = cargar_imagen_grafica1_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 1")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.grafica_seleccionada == "grafica2":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📊 Gráfica 2: Heatmap CPS")
    img_bytes = cargar_imagen_grafica2_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la Gráfica 2")
    st.markdown('</div>', unsafe_allow_html=True)

else:  # Gráfica de evolución
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA")
    
    if not df_followers.empty:
        try:
            # Buscar columnas de fecha y seguidores
            fecha_cols = [col for col in df_followers.columns if 'fecha' in col.lower() or 'date' in col.lower()]
            seguidor_cols = [col for col in df_followers.columns if 'seguidor' in col.lower() or 'follower' in col.lower()]
            
            if fecha_cols and seguidor_cols:
                fecha_col = fecha_cols[0]
                seguidor_col = seguidor_cols[0]
                
                # Convertir tipos
                df_followers[fecha_col] = pd.to_datetime(df_followers[fecha_col], errors='coerce')
                df_followers[seguidor_col] = pd.to_numeric(df_followers[seguidor_col], errors='coerce')
                
                # Ordenar por fecha
                df_followers = df_followers.sort_values(fecha_col)
                
                # Preparar datos de pauta
                if not df_pauta.empty:
                    # Calcular coste con IVA para la gráfica
                    if 'Costo' in df_pauta.columns:
                        df_pauta['coste_anuncio'] = df_pauta['Costo'] * 1.19  # Con IVA
                    if 'Visualizaciones' in df_pauta.columns:
                        df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
                    if 'Seguidores' in df_pauta.columns:
                        df_pauta['nuevos_seguidores_pauta'] = df_pauta['Seguidores']
                    
                    df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
                    
                    df_pauta_agg = df_pauta.groupby('fecha').agg({
                        'coste_anuncio': 'sum',
                        'visualizaciones_videos': 'sum',
                        'nuevos_seguidores_pauta': 'sum'
                    }).reset_index()
                    
                    # Fusionar por fecha
                    df_merged = pd.merge(df_followers, df_pauta_agg, left_on=fecha_col, right_on='fecha', how='outer')
                    df_merged = df_merged.sort_values(fecha_col)
                    
                    # Rellenar valores faltantes
                    if seguidor_col in df_merged.columns:
                        df_merged[seguidor_col] = df_merged[seguidor_col].fillna(method='ffill').fillna(0)
                    
                    if 'coste_anuncio' in df_merged.columns:
                        df_merged['coste_anuncio'] = df_merged['coste_anuncio'].fillna(0)
                    
                    if 'visualizaciones_videos' in df_merged.columns:
                        df_merged['visualizaciones_videos'] = df_merged['visualizaciones_videos'].fillna(0)
                    
                    if 'nuevos_seguidores_pauta' in df_merged.columns:
                        df_merged['nuevos_seguidores_pauta'] = df_merged['nuevos_seguidores_pauta'].fillna(0)
                else:
                    df_merged = df_followers.copy()
                    df_merged['coste_anuncio'] = 0
                    df_merged['visualizaciones_videos'] = 0
                    df_merged['nuevos_seguidores_pauta'] = 0
                
                # Crear gráfica
                fig_followers = go.Figure()
                
                # 1. Seguidores Totales
                fig_followers.add_trace(go.Scatter(
                    x=df_merged[fecha_col],
                    y=df_merged[seguidor_col],
                    mode='lines+markers',
                    name='👥 Seguidores Totales',
                    marker=dict(size=6, color='#000000'),
                    line=dict(color='#000000', width=2),
                    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores: %{y:,}<extra></extra>'
                ))
                
                # 2. Costo de Pauta CON IVA
                if 'coste_anuncio' in df_merged.columns:
                    fig_followers.add_trace(go.Bar(
                        x=df_merged[fecha_col],
                        y=df_merged['coste_anuncio'],
                        name='💰 Costo Pauta (+IVA)',
                        marker=dict(color='#ef4444', opacity=0.6),
                        hovertemplate='Costo Pauta: $%{y:,.0f}<extra></extra>',
                        yaxis='y2'
                    ))
                
                fig_followers.update_layout(
                    height=350,
                    template='plotly_white',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=40, r=40, t=20, b=40),
                    hovermode='x unified',
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
                        showgrid=True,
                        tickformat='%d/%m/%Y'
                    ),
                    yaxis=dict(
                        title="Seguidores",
                        gridcolor='#f1f5f9',
                        showgrid=True,
                        title_font=dict(color='#000000')
                    ),
                    yaxis2=dict(
                        title="Costo ($)",
                        overlaying='y',
                        side='right',
                        showgrid=False,
                        title_font=dict(color='#ef4444')
                    )
                )
                
                st.plotly_chart(fig_followers, use_container_width=True)
            else:
                st.warning("No se encontraron columnas de fecha o seguidores en los datos")
                
        except Exception as e:
            st.error(f"Error al generar gráfica: {str(e)}")
    else:
        st.warning("No hay datos de seguidores disponibles")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tabla de contenido
st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
st.markdown("##### 📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA")

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
        display_df['titulo'] = display_df['titulo'].fillna('Sin título').str.slice(0, 35) + '...'
    
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
    
    # Mostrar tabla compacta
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=250
    )
    
st.markdown('</div>', unsafe_allow_html=True)

# Footer
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 10px; padding: 12px 0; margin-top: 15px; border-top: 1px solid #e5e7eb;">
    Social Media Dashboard PRO v3.4 • Analytics en Tiempo Real • {current_time_full}
</div>
""", unsafe_allow_html=True)
