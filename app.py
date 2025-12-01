import streamlit as st
import pandas as pd
import requests
import time
from io import BytesIO
import json

# Configuración
st.set_page_config(page_title="TikTok Dashboard", layout="wide")

# Estado
if 'tiktok_data' not in st.session_state:
    st.session_state.tiktok_data = None
if 'tiktok_connected' not in st.session_state:
    st.session_state.tiktok_connected = False

def main():
    st.title("📊 TikTok Analytics Dashboard")
    
    with st.sidebar:
        st.header("🔗 Conexión")
        
        if not st.session_state.tiktok_connected:
            st.info("Conecta tu cuenta de TikTok")
            
            # Opción 1: Usar cookies/sesión manual
            st.subheader("Opción 1: Sesión Manual")
            session_cookies = st.text_area("Cookies de sesión (opcional)", height=100)
            
            # Opción 2: Usar API de terceros
            st.subheader("Opción 2: API Externa")
            api_key = st.text_input("API Key (si usas servicio externo)")
            
            if st.button("🔗 Conectar", type="primary"):
                st.session_state.tiktok_connected = True
                st.success("✅ Modo demostración activado")
                st.rerun()
        else:
            st.success("✅ Conectado")
            if st.button("🚪 Desconectar"):
                st.session_state.tiktok_connected = False
                st.session_state.tiktok_data = None
                st.rerun()
    
    # Contenido principal
    if st.session_state.tiktok_connected:
        st.success("✅ Cuenta conectada en modo demostración")
        
        # Opciones de scraping
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Scraping con Selenium (Local)", type="primary"):
                st.warning("""
                **⚠️ Solo funciona LOCALMENTE**
                
                Para usar scraping real:
                
                1. Descarga el código
                2. Ejecuta LOCALMENTE con:
                   ```bash
                   pip install selenium pandas streamlit
                   ```
                3. Descarga ChromeDriver
                4. Modifica el código para apuntar a tu ChromeDriver
                
                **No funciona en Streamlit Cloud**
                """)
        
        with col2:
            if st.button("📡 Usar API Externa", type="secondary"):
                st.info("""
                **Opciones de API:**
                
                1. **RapidAPI TikTok**: API paga pero confiable
                2. **TikTok Scraper API**: Varios proveedores
                3. **Webhook personalizado**: Tu propio servidor
                
                **Costo:** $10-50/mes aprox.
                """)
        
        with col3:
            if st.button("📊 Ver Datos de Ejemplo", type="secondary"):
                # Crear datos de ejemplo REALES (no inventados, solo estructura)
                example_data = []
                
                # Solo mostramos la estructura, no datos
                st.info("""
                **Estructura de datos que obtendrías:**
                
                ```json
                {
                  "duracion_video": "01:33",
                  "titulo": "[Título real de tu video]",
                  "fecha_publicacion": "28 nov, 14:01",
                  "privacidad": "Todo el mundo",
                  "visualizaciones": "1,234",
                  "me_gusta": "156",
                  "comentarios": "23"
                }
                ```
                
                **Nota:** Estos son datos REALES que obtendrías al ejecutar localmente.
                """)
        
        # Instrucciones para scraping real
        st.markdown("---")
        st.subheader("🚀 Cómo ejecutar scraping REAL")
        
        with st.expander("📋 Instrucciones detalladas"):
            st.markdown("""
            ### Para scraping REAL (Local):
            
            1. **Descarga este código**
            ```bash
            git clone [tu-repositorio]
            cd tu-repositorio
            ```
            
            2. **Instala dependencias**
            ```bash
            pip install selenium pandas streamlit
            ```
            
            3. **Descarga ChromeDriver**
            - Ve a: https://chromedriver.chromium.org/
            - Descarga la versión que coincide con tu Chrome
            - Descomprime y coloca en una carpeta accesible
            
            4. **Modifica el código**
            ```python
            # En el scraper, cambia:
            # driver = webdriver.Chrome(options=options)
            # Por:
            driver = webdriver.Chrome(
                executable_path='/ruta/a/tu/chromedriver',
                options=options
            )
            ```
            
            5. **Ejecuta localmente**
            ```bash
            streamlit run app.py
            ```
            
            6. **Inicia sesión manualmente** cuando TikTok se abra
            """)
        
        # Mostrar datos si existen
        if st.session_state.tiktok_data is not None:
            st.subheader("📋 Datos Obtenidos")
            st.dataframe(st.session_state.tiktok_data)
    
    else:
        # Pantalla de bienvenida
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #010101 0%, #333333 100%); color: white; border-radius: 15px;">
            <i class="fab fa-tiktok" style="font-size: 80px; color: #00f2ea;"></i>
            <h1>Análisis Profesional de TikTok</h1>
            <p style="font-size: 18px;">Extrae métricas reales de tus videos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **📊 Lo que puedes analizar:**
            
            • Visualizaciones por video
            • Likes y comentarios
            • Tasa de engagement
            • Fechas de publicación
            • Duración de videos
            • Configuración de privacidad
            """)
        
        with col2:
            st.warning("""
            **⚠️ Limitación de Streamlit Cloud:**
            
            Streamlit Cloud NO permite:
            
            • Ejecutar navegadores (Chrome/Firefox)
            • Usar Selenium directamente
            • Acceder al sistema de archivos
            • Ejecutar procesos largos
            
            **Solución:** Ejecuta LOCALMENTE o usa API externa.
            """)

if __name__ == "__main__":
    main()
