# app.py - STREAMLIT FRONTEND PARA PYTHONANYWHERE
import streamlit as st
import requests
import pandas as pd
import json
from io import BytesIO
import time

# Configuración
st.set_page_config(
    page_title="TikTok Dashboard - PythonAnywhere",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de tu API en PythonAnywhere (CAMBIAR ESTO)
PYTHONANYWHERE_API = "https://tudominio.pythonanywhere.com"  # Ejemplo: https://tiktokscraper.pythonanywhere.com

# Estado
if 'tiktok_data' not in st.session_state:
    st.session_state.tiktok_data = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'cookies_json' not in st.session_state:
    st.session_state.cookies_json = ""

# =============================================
# FUNCIONES DE API
# =============================================
def test_api_connection():
    """Prueba la conexión a la API"""
    try:
        response = requests.get(f"{PYTHONANYWHERE_API}/health", timeout=10)
        return response.status_code == 200
    except:
        return False

def scrape_tiktok_api(cookies_json):
    """Llama a la API para hacer scraping"""
    try:
        cookies = json.loads(cookies_json)
        response = requests.post(
            f"{PYTHONANYWHERE_API}/scrape",
            json={"cookies": cookies},
            timeout=300  # 5 minutos timeout
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "error": str(e)}

# =============================================
# INTERFAZ STREAMLIT
# =============================================
def create_sidebar():
    with st.sidebar:
        # Header
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 30px 0;">
            <h2 style="color: white; margin: 0;">🎬 TIKTOK</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 5px 0;">PythonAnywhere API</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Estado de conexión
        if test_api_connection():
            st.success("✅ API Conectada")
        else:
            st.error("❌ API No disponible")
            st.info(f"API URL: {PYTHONANYWHERE_API}")
        
        st.markdown("---")
        
        # Configuración de API
        st.subheader("🔧 Configuración")
        
        api_url = st.text_input(
            "URL de la API",
            value=PYTHONANYWHERE_API,
            help="URL de tu API en PythonAnywhere"
        )
        
        if api_url != PYTHONANYWHERE_API:
            st.session_state.api_key = api_url
            st.rerun()
        
        st.markdown("---")
        
        # Instrucciones para obtener cookies
        with st.expander("🔐 Cómo obtener cookies"):
            st.markdown("""
            **Para obtener cookies de TikTok:**
            
            1. Abre TikTok en Chrome/Firefox
            2. Inicia sesión en tu cuenta
            3. Presiona `F12` para abrir DevTools
            4. Ve a la pestaña **Application/Storage**
            5. Busca **Cookies** → **https://tiktok.com**
            6. Copia todas las cookies como JSON
            
            **Ejemplo de formato:**
            ```json
            [
              {
                "name": "sessionid",
                "value": "abc123...",
                "domain": ".tiktok.com"
              },
              {
                "name": "tt_webid",
                "value": "xyz789...",
                "domain": ".tiktok.com"
              }
            ]
            ```
            """)
        
        # Área para cookies
        st.subheader("🍪 Cookies de TikTok")
        cookies_input = st.text_area(
            "Pega las cookies JSON aquí:",
            height=150,
            value=st.session_state.cookies_json,
            help="Cookies de sesión de TikTok"
        )
        
        if cookies_input:
            st.session_state.cookies_json = cookies_input
        
        st.markdown("---")
        
        # Botón de scraping
        if st.button("🚀 Ejecutar Scraper", use_container_width=True, type="primary"):
            if not st.session_state.cookies_json:
                st.error("Primero pega las cookies de TikTok")
            else:
                st.session_state.scraping_in_progress = True
                st.rerun()

def show_dashboard():
    # Header principal
    st.markdown("""
    <div style="padding: 30px 0 20px 0; border-bottom: 1px solid #e2e8f0;">
        <h1 style="margin: 0; color: #0f172a;">🎬 TikTok Analytics Dashboard</h1>
        <p style="color: #64748b; margin: 10px 0 0 0;">
            Backend: PythonAnywhere • Scraping Real • Datos en Tiempo Real
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Si está en progreso de scraping
    if 'scraping_in_progress' in st.session_state and st.session_state.scraping_in_progress:
        with st.spinner("🚀 Ejecutando scraper real (2-3 minutos)..."):
            result = scrape_tiktok_api(st.session_state.cookies_json)
            
            if result.get("status") == "success":
                st.session_state.tiktok_data = result.get("data", [])
                st.success(f"✅ {result.get('count', 0)} videos obtenidos")
                st.session_state.scraping_in_progress = False
                st.rerun()
            else:
                st.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
                st.session_state.scraping_in_progress = False
    
    # Mostrar datos
    if st.session_state.tiktok_data:
        data = st.session_state.tiktok_data
        df = pd.DataFrame(data)
        
        # Métricas
        st.subheader("📊 Métricas Obtenidas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Videos", len(df))
        
        # Calcular métricas si existen
        if 'visualizaciones_num' in df.columns:
            with col2:
                total_views = df['visualizaciones_num'].sum()
                st.metric("Visualizaciones", f"{total_views:,}")
        
        if 'me_gusta_num' in df.columns:
            with col3:
                total_likes = df['me_gusta_num'].sum()
                st.metric("Me Gusta", f"{total_likes:,}")
        
        if 'engagement_rate' in df.columns:
            with col4:
                avg_engagement = df['engagement_rate'].mean()
                st.metric("Engagement", f"{avg_engagement:.1f}%")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📋 Datos", "📈 Análisis", "💾 Exportar"])
        
        with tab1:
            st.dataframe(df, use_container_width=True, height=400)
        
        with tab2:
            if len(df) > 0:
                # Análisis básico
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'privacidad' in df.columns:
                        st.subheader("Configuración de Privacidad")
                        privacy_counts = df['privacidad'].value_counts()
                        st.bar_chart(privacy_counts)
                
                with col2:
                    if 'visualizaciones_num' in df.columns:
                        st.subheader("Top Videos por Visualizaciones")
                        top_videos = df.nlargest(5, 'visualizaciones_num')
                        st.write(top_videos[['titulo', 'visualizaciones']])
        
        with tab3:
            st.subheader("Exportar Datos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 CSV",
                    data=csv,
                    file_name="tiktok_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='TikTok Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Excel",
                    data=excel_data,
                    file_name="tiktok_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col3:
                if st.button("🗑️ Limpiar Datos", use_container_width=True):
                    st.session_state.tiktok_data = None
                    st.rerun()
    
    else:
        # Pantalla de bienvenida
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 15px; margin: 40px 0;">
            <div style="font-size: 80px; margin-bottom: 20px;">🎯</div>
            <h2>Scraping Real de TikTok</h2>
            <p style="font-size: 18px; color: #4b5563; max-width: 800px; margin: 0 auto;">
                Conecta tu cuenta de TikTok mediante cookies y obtén datos reales de tus videos.
                El scraping se ejecuta en PythonAnywhere con Selenium real.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Características
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h4>🚀 Real</h4>
                <p>Scraping con Selenium real, no simulado</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h4>🔒 Seguro</h4>
                <p>Cookies no se almacenan, solo se usan para sesión</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h4>⚡ Rápido</h4>
                <p>Backend en PythonAnywhere 24/7</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    # CSS
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    create_sidebar()
    
    # Dashboard
    show_dashboard()

if __name__ == "__main__":
    main()
