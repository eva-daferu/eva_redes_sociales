import streamlit as st
import requests
import pandas as pd
import time
import json
from datetime import datetime

# SOLO Streamlit - NO Flask aquí

st.set_page_config(
    page_title="TikTok Scraper Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Scraper Dashboard")
st.markdown("---")

# Configuración del backend
BACKEND_URL = "https://pahubisas.pythonanywhere.com"

# Verificar estado del backend
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if response.status_code == 200:
        st.sidebar.success("✅ Backend conectado")
    else:
        st.sidebar.error("❌ Backend no disponible")
except:
    st.sidebar.warning("⚠️ No se pudo verificar el backend")

st.subheader("🚀 Instrucciones para scraping LOCAL:")
st.markdown("""
1. **Ejecuta localmente** el script de scraping (requiere Selenium)
2. **Obtén los datos** de TikTok
3. **Pega los datos JSON** en el campo de abajo
4. **Haz clic en "Procesar Datos"**
""")

# Campo para pegar datos JSON
json_input = st.text_area(
    "📋 Datos JSON de TikTok:",
    height=200,
    placeholder='Pega aquí los datos JSON obtenidos del scraper local',
    help="Ejemplo: [{'titulo': 'Video 1', 'visualizaciones': '1,234', ...}]"
)

if st.button("🔧 Procesar Datos", type="primary", use_container_width=True):
    if not json_input:
        st.error("❌ Por favor, pega los datos JSON")
        st.stop()
    
    try:
        # Validar JSON
        data = json.loads(json_input)
        
        # Enviar al backend para procesamiento
        with st.spinner("📡 Enviando datos al backend..."):
            response = requests.post(
                f"{BACKEND_URL}/process",
                json={"videos": data},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("status") == "success":
                st.success("✅ Datos procesados exitosamente!")
                
                # Mostrar resultados
                data = result.get("data", [])
                count = result.get("count", 0)
                analytics = result.get("analytics", {})
                
                st.metric("Videos procesados", count)
                
                # Mostrar tabla
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Descargar CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name=f"tiktok_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Mostrar estadísticas
                    with st.expander("📊 Estadísticas"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total vistas", f"{analytics.get('total_views', 0):,}")
                        with col2:
                            st.metric("Total likes", f"{analytics.get('total_likes', 0):,}")
                        with col3:
                            st.metric("Engagement", f"{analytics.get('avg_engagement', 0):.1f}%")
            else:
                st.error(f"❌ Error: {result.get('error', 'Error desconocido')}")
        else:
            st.error(f"❌ Error HTTP {response.status_code}")
            
    except json.JSONDecodeError:
        st.error("❌ Formato JSON inválido")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Información
st.markdown("---")
with st.expander("ℹ️ Información", expanded=False):
    st.markdown("""
    ### 🔧 Arquitectura del sistema:
    
    **Backend (PythonAnywhere):**
    - URL: https://pahubisas.pythonanywhere.com
    - Tecnología: Flask API
    - Función: Procesar datos JSON
    
    **Frontend (Streamlit Cloud):**
    - URL: Esta aplicación
    - Tecnología: Streamlit
    - Función: Interfaz para procesar datos
    
    ### 📋 Para scraping REAL:
    1. Ejecuta el script de scraping localmente (requiere Selenium)
    2. Obtén los datos en formato JSON
    3. Pega los datos aquí para procesamiento
    4. Descarga los resultados en CSV
    
    ### ⚠️ Notas:
    - Streamlit Cloud NO puede ejecutar Selenium
    - El scraping debe hacerse LOCALMENTE
    - Esta app solo procesa los datos obtenidos
    """)
