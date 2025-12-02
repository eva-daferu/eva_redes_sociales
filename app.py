import streamlit as st
import requests
import pandas as pd
import time
import json
import os

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
    value="https://tuusuario.pythonanywhere.com",
    help="URL de tu API desplegada en PythonAnywhere"
)

# Sección para cookies simplificada
st.subheader("🔐 Configuración de Sesión")

with st.expander("📋 Cómo obtener las cookies de TikTok", expanded=False):
    st.markdown("""
    1. **Inicia sesión en TikTok** en tu navegador
    2. **Abre las Herramientas de Desarrollo** (F12)
    3. **Ve a la pestaña Application/Storage**
    4. **Busca las cookies** en Storage > Cookies > https://www.tiktok.com
    5. **Copia todas las cookies** como JSON
    """)

cookies_input = st.text_area(
    "🍪 Cookies de sesión (formato JSON):",
    height=150,
    placeholder='[{"name": "sessionid", "value": "tu_sesion_id", "domain": ".tiktok.com"}, ...]',
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
        # Validar formato JSON
        cookies_json = json.loads(cookies_input)
    except json.JSONDecodeError:
        st.error("❌ Formato JSON inválido. Asegúrate de que las cookies estén en formato JSON correcto.")
        st.stop()
    
    # Configurar la barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Paso 1: Conectando al backend
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
            timeout=180
        )
    except requests.exceptions.ConnectionError:
        st.error("❌ No se puede conectar al backend. Verifica la URL.")
        st.stop()
    except requests.exceptions.Timeout:
        st.error("❌ Tiempo de espera agotado. El scraping está tomando demasiado tiempo.")
        st.stop()
    
    progress_bar.progress(40)
    
    # Paso 3: Procesando respuesta
    status_text.text("⚙️ Procesando respuesta del scraper...")
    time.sleep(1)
    progress_bar.progress(60)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get("status") == "success":
            progress_bar.progress(80)
            status_text.text("✅ Scraping completado exitosamente!")
            time.sleep(1)
            progress_bar.progress(100)
            status_text.text("")
            
            # Mostrar resultados
            data = result.get("data", [])
            count = result.get("count", 0)
            
            if count > 0:
                st.success(f"🎉 Se encontraron {count} videos")
                
                # Mostrar tabla
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # Botones de descarga
                col1, col2 = st.columns(2)
                
                with col1:
                    # Descargar CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name=f"tiktok_metrics_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    # Opción de descarga desde backend
                    if result.get("csv_path"):
                        download_url = f"{BACKEND_URL.rstrip('/')}/download?path={result.get('csv_path')}"
                        st.markdown(f'<a href="{download_url}" target="_blank"><button style="width:100%;background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">📁 Descargar desde Servidor</button></a>', unsafe_allow_html=True)
                
                # Mostrar resumen
                with st.expander("📊 Resumen de Métricas"):
                    if 'visualizaciones_num' in df.columns:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Vistas Totales", f"{df['visualizaciones_num'].sum():,}")
                        with col2:
                            st.metric("Likes Totales", f"{df['me_gusta_num'].sum():,}")
                        with col3:
                            st.metric("Comentarios Totales", f"{df['comentarios_num'].sum():,}")
                        
                        if 'engagement_rate' in df.columns:
                            avg_engagement = df['engagement_rate'].mean()
                            st.metric("Engagement Promedio", f"{avg_engagement:.2f}%")
            else:
                st.warning("⚠️ No se encontraron videos. Verifica las cookies de sesión.")
        
        else:
            st.error(f"❌ Error en el scraping: {result.get('error', 'Error desconocido')}")
    
    else:
        try:
            error_data = response.json()
            st.error(f"❌ Error del servidor: {error_data.get('error', 'Error desconocido')}")
        except:
            st.error(f"❌ Error HTTP {response.status_code}: {response.text}")
    
    # Limpiar barra de progreso
    progress_bar.empty()

elif not (BACKEND_URL and cookies_input):
    st.warning("⚠️ Completa la URL del backend y las cookies para habilitar el scraper")

# Sección de información
st.markdown("---")
with st.expander("ℹ️ Información", expanded=False):
    st.markdown("""
    ### 📋 Funcionamiento:
    1. **Configura** la URL de tu backend en PythonAnywhere
    2. **Obtén las cookies** de sesión de TikTok
    3. **Haz clic en "Conectar y Ejecutar Scraper"**
    4. **Espera** mientras se ejecuta el scraping (1-3 minutos)
    5. **Visualiza y descarga** los resultados
    
    ### 🔧 Requisitos del Backend:
    - API desplegada en PythonAnywhere
    - Selenium y ChromeDriver configurados
    - Endpoint `/scrape` disponible
    
    ### ⚠️ Notas:
    - Las cookies deben ser válidas y de una sesión activa
    - El scraping puede tardar 1-3 minutos
    - No compartas tus cookies públicamente
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
