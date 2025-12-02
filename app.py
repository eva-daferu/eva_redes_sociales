import streamlit as st
import requests
import pandas as pd
import time
import json

st.set_page_config(
    page_title="TikTok Scraper Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Metrics Scraper")
st.markdown("---")

# Configuración del backend
BACKEND_URL = st.text_input(
    "🔗 URL del Backend (PythonAnywhere):",
    value="https://pahubisas.pythonanywhere.com",
    help="URL de tu API desplegada en PythonAnywhere"
)

st.subheader("🔐 Configuración de Sesión")

with st.expander("📋 Cómo obtener las cookies de TikTok", expanded=False):
    st.markdown("""
    1. **Inicia sesión en TikTok** en Chrome/Firefox
    2. **Abre DevTools** (F12)
    3. **Ve a Application > Storage > Cookies**
    4. **Selecciona https://www.tiktok.com**
    5. **Copia todas las cookies** como JSON
    """)

cookies_input = st.text_area(
    "🍪 Cookies de sesión (formato JSON):",
    height=150,
    placeholder='[{"name": "sessionid", "value": "abc123", "domain": ".tiktok.com"}, {"name": "tt_chain_token", "value": "def456", "domain": ".tiktok.com"}]',
    help="Pega aquí las cookies en formato JSON"
)

st.markdown("---")

# Botón principal
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_button = st.button(
        "🚀 Conectar y Ejecutar Scraper",
        type="primary",
        use_container_width=True,
        disabled=not (BACKEND_URL and cookies_input)
    )

if run_button:
    if not cookies_input:
        st.error("❌ Por favor, proporciona las cookies de sesión")
        st.stop()
    
    try:
        cookies_json = json.loads(cookies_input)
    except json.JSONDecodeError:
        st.error("❌ Formato JSON inválido. Asegúrate de que las cookies estén en formato JSON correcto.")
        st.stop()
    
    # Configurar barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Paso 1: Conectando
    status_text.text("🔗 Conectando al backend...")
    time.sleep(1)
    progress_bar.progress(20)
    
    # Paso 2: Enviando solicitud
    status_text.text("📡 Enviando solicitud de scraping...")
    try:
        response = requests.post(
            f"{BACKEND_URL.rstrip('/')}/scrape",
            json={"cookies": cookies_json},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
    except requests.exceptions.ConnectionError:
        st.error("❌ No se puede conectar al backend. Verifica la URL.")
        st.stop()
    
    progress_bar.progress(60)
    
    # Paso 3: Procesando
    status_text.text("⚙️ Procesando respuesta...")
    time.sleep(1)
    progress_bar.progress(80)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get("status") == "success":
            progress_bar.progress(100)
            status_text.text("✅ Scraping completado!")
            time.sleep(1)
            status_text.text("")
            
            # Mostrar resultados
            data = result.get("data", [])
            count = result.get("count", 0)
            
            if count > 0:
                st.success(f"🎉 Se encontraron {count} videos")
                
                # Mostrar tabla
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # Descargar CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv,
                    file_name=f"tiktok_metrics_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Mostrar resumen
                with st.expander("📊 Resumen"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Videos", count)
                    with col2:
                        try:
                            vistas = sum(int(str(v).replace(',', '').replace('K', '000')) for v in df['visualizaciones'] if str(v).replace(',', '').replace('K', '').replace('.', '').isdigit())
                            st.metric("Vistas totales", f"{vistas:,}")
                        except:
                            st.metric("Vistas totales", "N/A")
                    with col3:
                        try:
                            publicos = len(df[df['privacidad'].str.contains('Todo el mundo')])
                            st.metric("Videos públicos", publicos)
                        except:
                            st.metric("Videos públicos", "N/A")
            else:
                st.warning("⚠️ No se encontraron videos. Verifica las cookies.")
        
        else:
            st.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
    
    else:
        try:
            error_data = response.json()
            st.error(f"❌ Error del servidor: {error_data.get('error', 'Error desconocido')}")
        except:
            st.error(f"❌ Error HTTP {response.status_code}: {response.text}")
    
    progress_bar.empty()

elif not (BACKEND_URL and cookies_input):
    st.warning("⚠️ Completa la URL del backend y las cookies para habilitar el scraper")

# Información
st.markdown("---")
with st.expander("ℹ️ Información", expanded=False):
    st.markdown("""
    ### 📋 Funcionamiento:
    1. **Configura** la URL de tu backend
    2. **Obtén las cookies** de TikTok
    3. **Haz clic en "Conectar y Ejecutar Scraper"**
    4. **Visualiza y descarga** los resultados
    
    ### 🔧 Backend configurado:
    - **URL:** https://pahubisas.pythonanywhere.com
    - **Endpoints:** /scrape (POST), /health (GET)
    - **Formato:** JSON con cookies de sesión
    
    ### ⚠️ Notas:
    - Las cookies deben ser de una sesión activa
    - No compartas tus cookies públicamente
    - Los datos son de demostración (backend sin Selenium en PythonAnywhere)
    """)

# Estado del backend
if BACKEND_URL:
    try:
        health_response = requests.get(f"{BACKEND_URL.rstrip('/')}/health", timeout=5)
        if health_response.status_code == 200:
            st.sidebar.success("✅ Backend conectado")
        else:
            st.sidebar.error("❌ Backend no disponible")
    except:
        st.sidebar.warning("⚠️ No se pudo verificar el backend")
