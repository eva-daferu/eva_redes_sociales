import streamlit as st
import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="TikTok Scraper",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Scraper Dashboard")
st.markdown("---")

# Configuración
BACKEND_URL = "https://pahubisas.pythonanywhere.com"

# Estado
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None

# Pasos del scraper original
steps = [
    ("🔄 Abriendo TikTok...", 3),
    ("🔓 INICIA SESIÓN MANUALMENTE", 60),
    ("🎯 Navegando a contenido...", 10),
    ("🎯 CAPTURANDO VIDEOS DURANTE SCROLL...", 0),
]

# Ciclos de scroll
for i in range(1, 26):
    steps.append((f"🔄 Ciclo {i}/25", 1.5))

steps.append(("🔍 VERIFICACIÓN FINAL...", 3))
steps.append(("🎉 CAPTURA COMPLETADA!", 2))

# Función principal
def run_scraper_simulation():
    """Simula el scraper original paso a paso"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_steps = len(steps)
    
    for step_idx, (message, wait_time) in enumerate(steps):
        # Actualizar estado
        status_text.text(message)
        progress = int((step_idx + 1) / total_steps * 100)
        progress_bar.progress(progress)
        
        # Esperar tiempo del paso
        if wait_time > 0:
            time.sleep(wait_time)
    
    # Finalizar
    progress_bar.empty()
    status_text.empty()
    
    return True

# Botón principal
if st.button("🚀 EJECUTAR SCRAPER DE TIKTOK", type="primary", use_container_width=True):
    st.session_state.scraping_active = True

# Mostrar simulación si está activa
if st.session_state.scraping_active:
    # Ejecutar simulación
    if run_scraper_simulation():
        
        # Generar datos de prueba
        with st.spinner("📊 Generando datos de prueba..."):
            time.sleep(2)
            
            # Crear 39 videos como el scraper original
            videos = []
            for i in range(39):
                days_ago = random.randint(1, 30)
                date = (datetime.now() - timedelta(days=days_ago)).strftime("%d %b, %H:%M")
                views = random.randint(100, 50000)
                likes = int(views * random.uniform(0.03, 0.15))
                comments = int(views * random.uniform(0.002, 0.01))
                
                videos.append({
                    'duracion_video': f"{random.randint(0, 2)}:{random.randint(10, 59):02d}",
                    'titulo': f"Video #{i+1} - Contenido de TikTok",
                    'fecha_publicacion': date,
                    'privacidad': random.choice(['Todo el mundo', 'Solo yo', 'Amigos']),
                    'visualizaciones': f"{views:,}",
                    'me_gusta': f"{likes:,}",
                    'comentarios': f"{comments:,}"
                })
            
            # Enviar al backend
            try:
                response = requests.post(
                    f"{BACKEND_URL}/process",
                    json={"videos": videos},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.scraped_data = result.get("data", [])
                    st.success(f"✅ Procesamiento completado: {len(videos)} videos")
                else:
                    st.error(f"Error del backend: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        
        st.session_state.scraping_active = False

# Mostrar resultados si existen
if st.session_state.scraped_data:
    st.markdown("---")
    st.subheader("📋 RESULTADOS DEL SCRAPING")
    
    df = pd.DataFrame(st.session_state.scraped_data)
    
    # Mostrar tabla
    st.dataframe(df, use_container_width=True)
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Videos", len(df))
    with col2:
        total_views = sum(int(str(v).replace(',', '')) for v in df['visualizaciones'])
        st.metric("Vistas Totales", f"{total_views:,}")
    with col3:
        public_videos = len(df[df['privacidad'] == 'Todo el mundo'])
        st.metric("Videos Públicos", public_videos)
    
    # Descargar
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"tiktok_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Botón para reiniciar
    if st.button("🔄 NUEVO SCRAPING", type="secondary", use_container_width=True):
        st.session_state.scraping_active = False
        st.session_state.scraped_data = None
        st.rerun()

# Información
st.markdown("---")
st.info("""
**🔧 Sistema de scraping simulado que sigue el timing exacto del scraper original.**

**Backend activo:** https://pahubisas.pythonanywhere.com
""")
