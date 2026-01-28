import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import requests
from io import BytesIO
import json
import os
from openai import OpenAI

warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN - SOLUCIÓN HÍBRIDA
# ============================================
# Primero intentamos usar el backend, si falla usamos OpenAI directo
OPENAI_BACKEND_URL = "https://pahubisas.pythonanywhere.com/openai_response"
DATA_BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/followers"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/pauta_anuncio"
GRAFICA1_URL = "https://pahubisas.pythonanywhere.com/grafica1"
GRAFICA2_URL = "https://pahubisas.pythonanywhere.com/grafica2"

# Configuración de OpenAI (como respaldo)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ============================================
# FUNCIONES PARA CARGAR DATOS
# ============================================
def cargar_datos_backend():
    """Carga datos principales del backend"""
    try:
        r = requests.get(DATA_BACKEND_URL, timeout=20)
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
    """Carga datos de seguidores"""
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
    """Carga datos de pauta publicitaria"""
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
    """Descarga bytes de una URL"""
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content

def cargar_imagen_grafica1_bytes():
    """Carga imagen de gráfica 1"""
    try:
        content = _descargar_bytes(GRAFICA1_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 1: {str(e)}")
        return b""

def cargar_imagen_grafica2_bytes():
    """Carga imagen de gráfica 2"""
    try:
        content = _descargar_bytes(GRAFICA2_URL, timeout=30)
        return content
    except Exception as e:
        st.error(f"Error al cargar imagen de gráfica 2: {str(e)}")
        return b""

# Función para cargar datos con caché
@st.cache_data(ttl=300)
def cargar_datos():
    """Carga todos los datos necesarios"""
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

# ============================================
# FUNCIONES DE ASISTENTE IA - SOLUCIÓN HÍBRIDA
# ============================================
def preparar_contexto_ai(df_all, df_followers, df_pauta):
    """Prepara el contexto para el asistente IA"""
    total_posts = len(df_all)
    total_views = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0
    
    # Obtener seguidores
    total_followers = 0
    if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
        if not df_followers['Seguidores_Totales'].dropna().empty:
            total_followers = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])
    
    # Obtener datos de pauta
    coste_anuncio = df_pauta['coste_anuncio'].sum() if not df_pauta.empty and 'coste_anuncio' in df_pauta.columns else 0
    visualizaciones_videos = df_pauta['visualizaciones_videos'].sum() if not df_pauta.empty and 'visualizaciones_videos' in df_pauta.columns else 0
    nuevos_seguidores = df_pauta['nuevos_seguidores'].sum() if not df_pauta.empty and 'nuevos_seguidores' in df_pauta.columns else 0
    
    # Calcular métricas adicionales
    avg_views = total_views / total_posts if total_posts > 0 else 0
    costo_por_seguidor = coste_anuncio / nuevos_seguidores if nuevos_seguidores > 0 else 0
    costo_por_mil_views = (coste_anuncio / visualizaciones_videos * 1000) if visualizaciones_videos > 0 else 0
    
    # Filtrar por plataformas
    tiktok_posts = len(df_all[df_all['red'].str.contains('tiktok', case=False, na=False)]) if 'red' in df_all.columns else 0
    youtube_posts = len(df_all[df_all['red'].str.contains('youtub|youtobe', case=False, na=False)]) if 'red' in df_all.columns else 0
    
    contexto = f"""
    Eres DataBot, un asistente especializado en análisis de datos de redes sociales. 
    
    DATOS ACTUALES DEL DASHBOARD:
    
    📊 MÉTRICAS GENERALES:
    • Total de publicaciones: {total_posts:,}
    • Visualizaciones totales: {total_views:,}
    • Promedio de visualizaciones por post: {avg_views:,.0f}
    • Total de seguidores TikTok: {total_followers:,}
    
    💰 MÉTRICAS DE INVERSIÓN:
    • Inversión total en publicidad: ${coste_anuncio:,}
    • Visualizaciones de videos pagados: {visualizaciones_videos:,}
    • Nuevos seguidores de publicidad: {nuevos_seguidores:,}
    • Costo por nuevo seguidor: ${costo_por_seguidor:,.2f}
    • Costo por mil visualizaciones (CPM): ${costo_por_mil_views:,.2f}
    
    📈 PLATAFORMAS ANALIZADAS:
    • TikTok: {tiktok_posts} publicaciones
    • YouTube: {youtube_posts} publicaciones
    
    🔍 ANÁLISIS DISPONIBLE:
    Puedo ayudarte con:
    1. Análisis de tendencias y rendimiento
    2. ROI de campañas publicitarias
    3. Recomendaciones de contenido
    4. Comparativas entre plataformas
    5. Predicciones y proyecciones
    
    Responde de forma clara, concisa y profesional. Usa emojis relevantes y estructura la información.
    """
    
    return contexto

def obtener_respuesta_ia_backend(prompt):
    """Intenta obtener respuesta del backend"""
    try:
        payload = {
            "input": prompt,
            "model": "gpt-4.1-mini",
            "max_output_tokens": 500
        }
        
        headers = {"Content-Type": "application/json"}
        r = requests.post(OPENAI_BACKEND_URL, json=payload, headers=headers, timeout=30)
        
        if r.status_code == 200:
            try:
                data = r.json()
                # Intentar diferentes formatos de respuesta
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
                
                # Si es texto plano
                text_response = r.text.strip()
                if text_response and text_response != "OpenAI response":
                    return text_response
                
            except:
                # Si no es JSON, devolver texto
                text_response = r.text.strip()
                if text_response and text_response != "OpenAI response":
                    return text_response
        
        return None  # Falló
    except:
        return None  # Falló

def obtener_respuesta_ia_openai_directo(prompt):
    """Usa OpenAI directamente como respaldo"""
    try:
        if not OPENAI_API_KEY:
            return "❌ **Error:** No se configuró la API Key de OpenAI. Configura la variable de entorno OPENAI_API_KEY."
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres DataBot, un asistente especializado en análisis de datos de redes sociales. Responde de forma clara, concisa y profesional. Usa emojis relevantes y estructura la información."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ **Error al usar OpenAI directamente:** {str(e)}"

def openai_chat_híbrido(prompt):
    """Solución híbrida: primero intenta backend, luego OpenAI directo"""
    # Primero intenta con el backend
    respuesta_backend = obtener_respuesta_ia_backend(prompt)
    
    if respuesta_backend:
        return respuesta_backend
    
    # Si el backend falla o devuelve "OpenAI response", usa OpenAI directo
    st.sidebar.info("⚠️ Usando OpenAI directamente (backend no disponible)")
    return obtener_respuesta_ia_openai_directo(prompt)

def procesar_respuesta_ia(df_all, df_followers, df_pauta):
    """Procesa la respuesta del asistente IA"""
    if "processing_chat" not in st.session_state:
        st.session_state.processing_chat = False
    
    if st.session_state.get("process_chat_request", False) and not st.session_state.processing_chat:
        st.session_state.processing_chat = True
        
        try:
            # Obtener último mensaje del usuario
            if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
                ultimo_mensaje = st.session_state.messages[-1]["content"]
                
                # Preparar contexto
                contexto = preparar_contexto_ai(df_all, df_followers, df_pauta)
                
                # Construir el prompt completo
                # Incluir solo los últimos 3 intercambios para no sobrecargar
                conversacion_reciente = ""
                for i, msg in enumerate(st.session_state.messages[-6:]):
                    role = "Usuario" if msg["role"] == "user" else "DataBot"
                    conversacion_reciente += f"{role}: {msg['content']}\n"
                
                # Si es el primer mensaje después del saludo, no incluir conversación anterior
                if len(st.session_state.messages) <= 2:
                    prompt_completo = f"{contexto}\n\nUsuario: {ultimo_mensaje}\nDataBot: "
                else:
                    prompt_completo = f"{contexto}\n\n{conversacion_reciente}DataBot: "
                
                # Usar solución híbrida
                respuesta = openai_chat_híbrido(prompt_completo)
                
                # Agregar respuesta del asistente
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
        
        except Exception as e:
            respuesta = f"❌ **Error al procesar tu consulta:**\n\n`{str(e)}`\n\nPor favor, intenta nuevamente."
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
        
        finally:
            # Resetear estados
            st.session_state.process_chat_request = False
            st.session_state.processing_chat = False

# ============================================
# FUNCIONES DE INTERFAZ
# ============================================
def format_number(num):
    """Formatea números para mostrar"""
    try:
        num = float(num)
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return f"{int(num):,}"
    except:
        return "0"

def create_metric_card(icon, value, label, is_light=False):
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

# ============================================
# ESTILOS CSS MEJORADOS
# ============================================
st.markdown("""
<style>
/* Animaciones */
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
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
    animation: fadeIn 0.5s ease-out;
}

.metric-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
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

/* ASISTENTE IA - ESTILOS MEJORADOS */
.ai-header {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.ai-header h3 {
    color: white;
    margin: 0;
    font-size: 14px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.chat-container {
    background: white;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    height: 320px;
    overflow-y: auto;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
}

.chat-message {
    margin-bottom: 12px;
    animation: fadeIn 0.3s ease-out;
}

.user-message {
    background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    color: white;
    padding: 10px 14px;
    border-radius: 14px 14px 4px 14px;
    max-width: 85%;
    margin-left: auto;
    font-size: 12px;
    line-height: 1.4;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.assistant-message {
    background: #f8fafc;
    color: #1f2937;
    padding: 10px 14px;
    border-radius: 14px 14px 14px 4px;
    max-width: 85%;
    margin-right: auto;
    font-size: 12px;
    line-height: 1.4;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.assistant-message strong {
    color: #7c3aed;
}

.chat-input-container {
    display: flex;
    gap: 10px;
    align-items: center;
}

.chat-input {
    flex: 1;
    padding: 10px 14px;
    border-radius: 10px;
    border: 2px solid #e5e7eb;
    font-size: 12px;
    transition: all 0.3s ease;
}

.chat-input:focus {
    outline: none;
    border-color: #8B5CF6;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.send-button {
    background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.send-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.clear-chat-btn {
    background: transparent;
    color: #94a3b8;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
    width: 100%;
}

.clear-chat-btn:hover {
    background: #f1f5f9;
    color: #64748b;
}

/* Indicador de escritura */
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

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

/* Estilo para mensajes de error */
.error-message {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    color: #dc2626;
    padding: 10px 14px;
    border-radius: 14px 14px 14px 4px;
    max-width: 85%;
    margin-right: auto;
    font-size: 12px;
    line-height: 1.4;
    border: 1px solid #fecaca;
    box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
}

/* Estilo para mensajes informativos */
.info-message {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    color: #0369a1;
    padding: 10px 14px;
    border-radius: 14px 14px 14px 4px;
    max-width: 85%;
    margin-right: auto;
    font-size: 12px;
    line-height: 1.4;
    border: 1px solid #bae6fd;
    box-shadow: 0 2px 8px rgba(3, 105, 161, 0.1);
}
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ============================================
# CARGAR DATOS
# ============================================
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# ============================================
# SIDEBAR MEJORADO
# ============================================
with st.sidebar:
    # Logo y título
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 0 10px;">
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
            animation: pulse 2s infinite;
        ">
            🤖
        </div>
        <h3 style="color: white; margin-bottom: 4px; font-size: 15px; font-weight: 800;">AI ANALYTICS PRO</h3>
        <p style="color: #94a3b8; font-size: 11px; margin: 0;">Powered by GPT-4</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del sistema
    try:
        backend_test = requests.get(DATA_BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(16, 185, 129, 0.2); font-size: 11px; display: flex; align-items: center; gap: 8px;"><span style="font-size: 14px;">✅</span> <strong>Backend Conectado</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(239, 68, 68, 0.2); font-size: 11px; display: flex; align-items: center; gap: 8px;"><span style="font-size: 14px;">⚠️</span> <strong>Backend Error</strong></div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(239, 68, 68, 0.2); font-size: 11px; display: flex; align-items: center; gap: 8px;"><span style="font-size: 14px;">⚠️</span> <strong>Backend Offline</strong></div>', unsafe_allow_html=True)
    
    # Estado de OpenAI
    if OPENAI_API_KEY:
        st.markdown('<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(16, 185, 129, 0.2); font-size: 11px; display: flex; align-items: center; gap: 8px;"><span style="font-size: 14px;">🔑</span> <strong>OpenAI API Key Disponible</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: rgba(245, 158, 11, 0.1); color: #f59e0b; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid rgba(245, 158, 11, 0.2); font-size: 11px; display: flex; align-items: center; gap: 8px;"><span style="font-size: 14px;">⚠️</span> <strong>Sin OpenAI API Key</strong></div>', unsafe_allow_html=True)
    
    # Selector de plataformas
    st.markdown('<div style="background: rgba(139, 92, 246, 0.1); padding: 12px; border-radius: 12px; margin: 15px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #8B5CF6; font-size: 12px; font-weight: 700; margin-bottom: 10px; letter-spacing: 0.8px; text-transform: uppercase; display: flex; align-items: center; gap: 6px;"><span style="font-size: 16px;">📱</span> PANEL PROFESIONAL</p>', unsafe_allow_html=True)
    
    platforms = {
        "general": "🌐 VISIÓN GENERAL",
        "youtube": "▶️ YOUTUBE ANALYTICS",
        "tiktok": "🎵 TIKTOK INSIGHTS"
    }
    
    selected_platform = st.session_state.get("selected_platform", "general")
    
    for platform_key, platform_name in platforms.items():
        if st.button(platform_name, 
                    key=f"{platform_key}_btn",
                    use_container_width=True,
                    type="primary" if selected_platform == platform_key else "secondary"):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # ASISTENTE IA MEJORADO
    # ============================================
    st.markdown('<div class="ai-header">', unsafe_allow_html=True)
    st.markdown('<h3><span>🤖</span> ASISTENTE IA DE DATOS</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 ¡Hola! Soy **DataBot**, tu asistente de análisis de redes sociales. Puedo ayudarte a analizar métricas, tendencias, ROI de campañas y más. ¿En qué puedo ayudarte hoy?"
            }
        ]
    
    # Inicializar estados del chat
    if "process_chat_request" not in st.session_state:
        st.session_state.process_chat_request = False
    
    # Contenedor del chat
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            # Formatear respuesta del asistente
            content = message["content"]
            content = content.replace('\n', '<br>')
            # Determinar tipo de mensaje
            if content.startswith("❌") or content.startswith("⚠️") or content.startswith("⏰") or content.startswith("🔌"):
                st.markdown(f'<div class="chat-message"><div class="error-message">{content}</div></div>', unsafe_allow_html=True)
            elif content.startswith("👋") or content.startswith("📊") or content.startswith("💰"):
                st.markdown(f'<div class="chat-message"><div class="assistant-message">{content}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message"><div class="info-message">{content}</div></div>', unsafe_allow_html=True)
    
    # Mostrar indicador de escritura si está procesando
    if st.session_state.get("processing_chat", False):
        st.markdown('''
        <div class="chat-message">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input de chat
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Escribe tu pregunta...",
                key="chat_input_form",
                label_visibility="collapsed",
                placeholder="Ej: ¿Cuál es el ROI de la campaña?"
            )
        with col2:
            submit_button = st.form_submit_button("➤", use_container_width=True, type="primary")
    
    # Procesar mensaje cuando se envía el formulario
    if submit_button and user_input.strip():
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        # Marcar para procesar
        st.session_state.process_chat_request = True
        # Forzar actualización
        st.rerun()
    
    # Botón para limpiar chat
    if st.button("🗑️ Limpiar Conversación", use_container_width=True, type="secondary"):
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 ¡Conversación reiniciada! ¿En qué puedo ayudarte ahora?"
            }
        ]
        st.session_state.process_chat_request = False
        st.session_state.processing_chat = False

# ============================================
# PROCESAR RESPUESTA IA (fuera del sidebar)
# ============================================
procesar_respuesta_ia(df_all, df_followers, df_pauta)

# ============================================
# CONTENIDO PRINCIPAL
# ============================================
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

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================
# Calcular métricas
if not df_pauta.empty:
    coste_anuncio_sum = df_pauta['coste_anuncio'].sum() if 'coste_anuncio' in df_pauta.columns else 0
    visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum() if 'visualizaciones_videos' in df_pauta.columns else 0
    nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum() if 'nuevos_seguidores' in df_pauta.columns else 0
else:
    coste_anuncio_sum = 0
    visualizaciones_videos_sum = 0
    nuevos_seguidores_sum = 0

# Obtener seguidores
total_seguidores = 0
if not df_followers.empty and 'Seguidores_Totales' in df_followers.columns:
    if not df_followers['Seguidores_Totales'].dropna().empty:
        total_seguidores = int(df_followers['Seguidores_Totales'].dropna().iloc[-1])

total_contenidos = len(df_all)
total_visualizaciones = df_all['visualizaciones'].sum() if 'visualizaciones' in df_all.columns else 0

# Calcular métricas adicionales
costo_por_seguidor = coste_anuncio_sum / nuevos_seguidores_sum if nuevos_seguidores_sum > 0 else 0
engagement_rate = ((df_all['me_gusta'].sum() if 'me_gusta' in df_all.columns else 0) + 
                   (df_all['comentarios'].sum() if 'comentarios' in df_all.columns else 0)) / total_seguidores * 100 if total_seguidores > 0 else 0

# Crear métricas
col1, col2, col3 = st.columns(3)

with col1:
    # Tarjeta 1: Inversión
    html = create_metric_card(
        icon="💰", 
        value=f"${format_number(coste_anuncio_sum)}", 
        label="INVERSIÓN TOTAL",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)
    
    # Tarjeta 2: Seguidores Totales
    html = create_metric_card(
        icon="👥", 
        value=format_number(total_seguidores), 
        label="SEGUIDORES TOTALES",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)

with col2:
    # Tarjeta 3: Visualizaciones
    html = create_metric_card(
        icon="👁️", 
        value=format_number(visualizaciones_videos_sum), 
        label="VISUALIZACIONES PAGADAS",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)
    
    # Tarjeta 4: Nuevos Seguidores
    html = create_metric_card(
        icon="📈", 
        value=format_number(nuevos_seguidores_sum), 
        label="NUEVOS SEGUIDORES",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)

with col3:
    # Tarjeta 5: ROI
    html = create_metric_card(
        icon="📊", 
        value=f"${costo_por_seguidor:,.1f}", 
        label="COSTO POR SEGUIDOR",
        is_light=False
    )
    st.markdown(html, unsafe_allow_html=True)
    
    # Tarjeta 6: Engagement
    html = create_metric_card(
        icon="💬", 
        value=f"{engagement_rate:.1f}%", 
        label="ENGAGEMENT RATE",
        is_light=True
    )
    st.markdown(html, unsafe_allow_html=True)

# Agregar espacio
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ============================================
# SELECTOR DE GRÁFICAS
# ============================================
st.markdown('<div class="grafica-selector-container">', unsafe_allow_html=True)
st.markdown('<div class="grafica-selector-title">📈 SELECCIONA EL TIPO DE ANÁLISIS</div>', unsafe_allow_html=True)

# Inicializar estado para gráfica seleccionada
if "grafica_seleccionada" not in st.session_state:
    st.session_state.grafica_seleccionada = "evolucion"

# Selector visual
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("**📈** **Evolución Seguidores**", 
                 key="btn_evolucion",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "evolucion" else "secondary"):
        st.session_state.grafica_seleccionada = "evolucion"

with col2:
    if st.button("**💰** **Inversión vs ROI**", 
                 key="btn_grafica1",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "grafica1" else "secondary"):
        st.session_state.grafica_seleccionada = "grafica1"

with col3:
    if st.button("**📊** **Heatmap Performance**", 
                 key="btn_grafica2",
                 use_container_width=True,
                 type="primary" if st.session_state.grafica_seleccionada == "grafica2" else "secondary"):
        st.session_state.grafica_seleccionada = "grafica2"

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# GRÁFICAS
# ============================================
if st.session_state.grafica_seleccionada == "grafica1":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 Análisis: Inversión vs ROI")
    img_bytes = cargar_imagen_grafica1_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar la gráfica de inversión")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.grafica_seleccionada == "grafica2":
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📊 Heatmap de Performance")
    img_bytes = cargar_imagen_grafica2_bytes()
    if img_bytes:
        st.image(img_bytes, use_container_width=True)
    else:
        st.warning("No se pudo cargar el heatmap")
    st.markdown('</div>', unsafe_allow_html=True)

else:  # Gráfica de evolución
    st.markdown('<div class="performance-chart">', unsafe_allow_html=True)
    st.markdown("##### 📈 EVOLUCIÓN DE SEGUIDORES Y MÉTRICAS")
    
    if not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
        try:
            # Preparar datos
            df_merged = df_followers.copy()
            
            # Agregar datos de pauta si existen
            if not df_pauta.empty:
                if 'fecha' in df_pauta.columns:
                    df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
                    df_pauta_agg = df_pauta.groupby('fecha').agg({
                        'coste_anuncio': 'sum',
                        'visualizaciones_videos': 'sum',
                        'nuevos_seguidores': 'sum'
                    }).reset_index()
                    
                    # Fusionar datos
                    df_merged = pd.merge(df_followers, df_pauta_agg, left_on='Fecha', right_on='fecha', how='left')
                    df_merged = df_merged.sort_values('Fecha')
                    
                    # Rellenar valores nulos
                    df_merged['coste_anuncio'] = df_merged['coste_anuncio'].fillna(0)
                    df_merged['visualizaciones_videos'] = df_merged['visualizaciones_videos'].fillna(0)
                    df_merged['nuevos_seguidores'] = df_merged['nuevos_seguidores'].fillna(0)
                else:
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
                line=dict(color='#000000', width=3),
                marker=dict(size=8, color='#000000'),
                hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores: %{y:,}<extra></extra>'
            ))
            
            # Nuevos Seguidores (barras)
            if 'nuevos_seguidores' in df_merged.columns:
                fig.add_trace(go.Bar(
                    x=df_merged['Fecha'],
                    y=df_merged['nuevos_seguidores'],
                    name='📈 Nuevos Seguidores',
                    marker_color='#10b981',
                    opacity=0.6,
                    hovertemplate='Nuevos Seguidores: %{y:,}<extra></extra>',
                    yaxis='y2'
                ))
            
            # Costo de Pauta (línea de área)
            if 'coste_anuncio' in df_merged.columns:
                fig.add_trace(go.Scatter(
                    x=df_merged['Fecha'],
                    y=df_merged['coste_anuncio'],
                    mode='lines',
                    name='💰 Inversión',
                    line=dict(color='#ef4444', width=2, dash='dot'),
                    fill='tozeroy',
                    fillcolor='rgba(239, 68, 68, 0.1)',
                    hovertemplate='Inversión: $%{y:,}<extra></extra>',
                    yaxis='y3'
                ))
            
            # Configurar layout
            fig.update_layout(
                height=400,
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white',
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
                    tickformat='%d/%m'
                ),
                yaxis=dict(
                    title="Seguidores Totales",
                    gridcolor='#f1f5f9',
                    title_font=dict(color='#000000')
                ),
                yaxis2=dict(
                    title="Nuevos Seguidores",
                    overlaying='y',
                    side='right',
                    gridcolor='rgba(241, 245, 249, 0.5)',
                    title_font=dict(color='#10b981')
                ),
                yaxis3=dict(
                    title="Inversión ($)",
                    overlaying='y',
                    side='right',
                    position=0.95,
                    gridcolor='rgba(241, 245, 249, 0.3)',
                    title_font=dict(color='#ef4444')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error al generar la gráfica: {str(e)}")
    else:
        st.warning("No hay datos de seguidores disponibles para mostrar")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TABLA DE CONTENIDO
# ============================================
st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
st.markdown(f"##### 📊 CONTENIDO - {selected_platform.upper()}")

if not df_all.empty:
    # Filtrar por plataforma seleccionada
    if selected_platform == "tiktok":
        display_df = tiktok_df.copy()
        platform_name = "TikTok"
    elif selected_platform == "youtube":
        display_df = youtobe_df.copy()
        platform_name = "YouTube"
    else:
        display_df = df_all.copy()
        platform_name = "Todas las Plataformas"
    
    # Mostrar resumen
    st.markdown(f"**{platform_name}** - {len(display_df)} publicaciones analizadas")
    
    # Seleccionar y formatear columnas
    if not display_df.empty:
        column_mapping = {
            'titulo': 'Título',
            'fecha_publicacion': 'Fecha',
            'red': 'Plataforma',
            'visualizaciones': 'Views',
            'me_gusta': 'Likes',
            'comentarios': 'Comentarios',
            'Seguidores_Totales': 'Seguidores'
        }
        
        # Crear DataFrame para mostrar
        display_cols = []
        for col in ['titulo', 'fecha_publicacion', 'visualizaciones', 'me_gusta', 'comentarios']:
            if col in display_df.columns:
                display_cols.append(col)
        
        if display_cols:
            df_to_show = display_df[display_cols].copy()
            
            # Formatear fecha
            if 'fecha_publicacion' in df_to_show.columns:
                df_to_show['fecha_publicacion'] = pd.to_datetime(df_to_show['fecha_publicacion']).dt.strftime('%d/%m')
            
            # Formatear título
            if 'titulo' in df_to_show.columns:
                df_to_show['titulo'] = df_to_show['titulo'].fillna('Sin título').apply(
                    lambda x: x[:40] + '...' if len(str(x)) > 40 else x
                )
            
            # Renombrar columnas
            df_to_show = df_to_show.rename(columns={k: v for k, v in column_mapping.items() if k in df_to_show.columns})
            
            # Mostrar tabla
            st.dataframe(
                df_to_show,
                use_container_width=True,
                hide_index=True,
                height=280
            )
        else:
            st.warning("No hay columnas disponibles para mostrar")
    else:
        st.info(f"No hay datos disponibles para {platform_name}")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 10px; padding: 12px 0; margin-top: 20px; border-top: 1px solid #e5e7eb;">
    Social Media Dashboard PRO v4.0 • Powered by OpenAI • {current_time_full}
</div>
""", unsafe_allow_html=True)
