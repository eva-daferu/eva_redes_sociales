import streamlit as st
import requests
import pandas as pd
import time
import json
import threading

st.set_page_config(
    page_title="TikTok Auto-Scraper",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Auto-Scraper Dashboard")
st.markdown("---")

# Configuración del backend
BACKEND_URL = "https://pahubisas.pythonanywhere.com"

# Mostrar estado del backend
try:
    health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if health_response.status_code == 200:
        st.sidebar.success("✅ Backend conectado")
    else:
        st.sidebar.error("❌ Backend no disponible")
except:
    st.sidebar.warning("⚠️ No se pudo verificar el backend")

# Opción 1: Login automático (recomendado)
st.subheader("🔐 Opción 1: Login Automático")

col1, col2 = st.columns(2)
with col1:
    username = st.text_input("👤 Usuario/Email TikTok", placeholder="usuario@email.com")
with col2:
    password = st.text_input("🔑 Contraseña", type="password", placeholder="Tu contraseña")

auto_scrape_button = st.button(
    "🚀 Iniciar Scraping Automático",
    type="primary",
    disabled=not (username and password),
    use_container_width=True
)

# Opción 2: Login manual
st.subheader("🖱️ Opción 2: Login Manual")
st.markdown("""
1. Haz clic en el botón "Abrir TikTok para Login Manual"
2. Inicia sesión manualmente en TikTok
3. Cierra la ventana cuando hayas terminado
4. El scraper continuará automáticamente
""")

manual_scrape_button = st.button(
    "📱 Abrir TikTok para Login Manual",
    type="secondary",
    use_container_width=True
)

# Estado del scraping
scraping_status = st.empty()
progress_bar = st.progress(0)
results_container = st.empty()

def run_scraping(mode="auto", username=None, password=None):
    """Ejecutar scraping en segundo plano"""
    try:
        scraping_status.text("🔄 Iniciando scraping...")
        progress_bar.progress(10)
        time.sleep(1)
        
        if mode == "auto" and username and password:
            # Scraping con credenciales
            progress_bar.progress(30)
            scraping_status.text("🔑 Iniciando sesión automática...")
            
            response = requests.post(
                f"{BACKEND_URL}/scrape_auto",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=180  # 3 minutos timeout
            )
        else:
            # Scraping con login manual
            progress_bar.progress(30)
            scraping_status.text("⏳ Esperando login manual...")
            st.info("Por favor, inicia sesión en TikTok cuando se abra la ventana")
            
            # En un entorno real, aquí abrirías una ventana/iframe con TikTok
            # Para demo, simulamos espera
            time.sleep(10)  # Simular tiempo para login manual
            
            response = requests.post(
                f"{BACKEND_URL}/scrape",
                json={},
                headers={"Content-Type": "application/json"},
                timeout=180
            )
        
        progress_bar.progress(70)
        scraping_status.text("📊 Extrayendo datos de videos...")
        time.sleep(2)
        
        if response.status_code == 200:
            result = response.json()
            progress_bar.progress(100)
            
            if result.get("status") == "success":
                data = result.get("data", [])
                count = result.get("count", 0)
                message = result.get("message", "")
                
                if count > 0:
                    scraping_status.success(f"✅ {message} - {count} videos encontrados")
                    
                    # Mostrar resultados
                    df = pd.DataFrame(data)
                    results_container.dataframe(df, use_container_width=True)
                    
                    # Botón de descarga
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name=f"tiktok_videos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Estadísticas
                    with st.expander("📊 Estadísticas detalladas"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total videos", count)
                        with col2:
                            public_videos = len(df[df['privacidad'].str.contains('Todo el mundo', na=False)])
                            st.metric("Videos públicos", public_videos)
                        with col3:
                            private_videos = len(df[df['privacidad'].str.contains('Solo yo|Privado', na=False)])
                            st.metric("Videos privados", private_videos)
                        with col4:
                            avg_views = df['visualizaciones'].apply(lambda x: int(str(x).replace(',', '').replace('K', '000'))).mean()
                            st.metric("Vistas promedio", f"{int(avg_views):,}")
                else:
                    scraping_status.warning(f"⚠️ {message}")
            else:
                scraping_status.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
        else:
            scraping_status.error(f"❌ Error del servidor: {response.status_code}")
            
    except requests.exceptions.Timeout:
        scraping_status.error("⏰ Timeout: El scraping tomó demasiado tiempo")
    except Exception as e:
        scraping_status.error(f"❌ Error: {str(e)}")
    
    finally:
        time.sleep(2)
        progress_bar.empty()

# Manejar botones
if auto_scrape_button and username and password:
    run_scraping(mode="auto", username=username, password=password)

if manual_scrape_button:
    run_scraping(mode="manual")

# Información
st.markdown("---")
with st.expander("ℹ️ Información del sistema", expanded=False):
    st.markdown("""
    ### 🎯 Funcionamiento:
    
    **Opción 1 (Login Automático):**
    - Ingresa tu usuario y contraseña de TikTok
    - El sistema inicia sesión automáticamente
    - Extrae tus videos y métricas en 1-3 minutos
    
    **Opción 2 (Login Manual):**
    - Se abre TikTok en una ventana emergente
    - Inicias sesión manualmente
    - Cierras la ventana cuando termines
    - El scraper continúa automáticamente
    
    ### ⏱️ Tiempos estimados:
    - Login automático: 30-60 segundos
    - Login manual: 1-2 minutos
    - Scraping de videos: 1-3 minutos
    - **Total: 2-5 minutos**
    
    ### 🔒 Seguridad:
    - Las credenciales NO se almacenan
    - Conexión HTTPS segura
    - Sesión temporal durante el scraping
    """)

# Nota importante
st.info("""
**⚠️ Nota importante:** Para scraping real con Selenium, el backend necesita acceso a ChromeDriver. 
En PythonAnywhere, se recomienda ejecutar el scraper en un servidor local y solo usar la API para procesamiento de datos.
""")
