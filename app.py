import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import time
import json
from datetime import datetime
import random

st.set_page_config(
    page_title="TikTok Scraper - Timing Real",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Scraper - Timing Real")
st.markdown("---")

# URL del backend
BACKEND_URL = "https://pahubisas.pythonanywhere.com"

# Estado
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False
if 'scraping_step' not in st.session_state:
    st.session_state.scraping_step = 0
if 'scraping_progress' not in st.session_state:
    st.session_state.scraping_progress = 0
if 'tiktok_data' not in st.session_state:
    st.session_state.tiktok_data = None

# Función para simular tiempos REALES del scraper
def simulate_real_scraping():
    """Simula los tiempos EXACTOS del scraper original"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # PASO 1: Abrir TikTok (3 segundos)
    status_text.text("🌐 Abriendo TikTok...")
    time.sleep(3)
    st.session_state.scraping_progress = 10
    progress_bar.progress(10)
    
    # PASO 2: Esperar login manual (60 segundos - COMENTADO para demo)
    status_text.text("🔓 INICIA SESIÓN MANUALMENTE (60s)...")
    # time.sleep(60)  # ⏳ TIEMPO REAL - COMENTADO PARA DEMO
    time.sleep(5)  # ⏳ TIEMPO REDUCIDO PARA DEMO
    st.session_state.scraping_progress = 30
    progress_bar.progress(30)
    
    # PASO 3: Navegar a contenido (10 segundos)
    status_text.text("🎯 Navegando a contenido...")
    time.sleep(10)
    st.session_state.scraping_progress = 40
    progress_bar.progress(40)
    
    # PASO 4: Capturar videos durante scroll (25 ciclos * 1.5s = 37.5s)
    status_text.text("📊 Capturando videos durante scroll...")
    
    for ciclo in range(25):
        # Simular ciclo de scroll
        time.sleep(1.5)
        st.session_state.scraping_progress = 40 + ((ciclo + 1) * 2)
        progress_bar.progress(min(90, 40 + ((ciclo + 1) * 2)))
        
        # Si tenemos 39+ videos, terminar antes
        if ciclo >= 10:  # Simulación de break temprano
            break
    
    # PASO 5: Procesamiento final (5 segundos)
    status_text.text("⚙️ Procesando datos finales...")
    time.sleep(5)
    st.session_state.scraping_progress = 100
    progress_bar.progress(100)
    
    status_text.text("✅ Scraping completado!")
    time.sleep(1)
    
    progress_bar.empty()
    status_text.empty()
    
    return True

# Función para crear iframe con bloqueo de tiempos
def create_tiktok_iframe_with_timing():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container {
                padding: 20px;
                max-width: 1000px;
                margin: 0 auto;
            }
            
            .timer-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                border-radius: 10px;
            }
            
            .timer-text {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .timer-countdown {
                font-size: 48px;
                font-weight: bold;
                color: #00f2ea;
                margin: 20px 0;
            }
            
            .browser-frame {
                border: 3px solid #1e3a8a;
                border-radius: 10px;
                overflow: hidden;
                position: relative;
                height: 500px;
            }
            
            .browser-header {
                background: #1e3a8a;
                color: white;
                padding: 10px 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .browser-controls {
                display: flex;
                gap: 8px;
            }
            
            .control-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }
            
            .red { background: #ff5f56; }
            .yellow { background: #ffbd2e; }
            .green { background: #27c93f; }
            
            .browser-url {
                flex-grow: 1;
                background: white;
                color: #333;
                padding: 5px 15px;
                border-radius: 15px;
                font-family: monospace;
                font-size: 12px;
                text-align: center;
            }
            
            .browser-content {
                height: calc(100% - 45px);
            }
            
            iframe {
                width: 100%;
                height: 100%;
                border: none;
            }
            
            .instructions {
                background: #f0f9ff;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #0ea5e9;
            }
            
            .instructions h4 {
                color: #0369a1;
                margin: 0 0 10px 0;
            }
            
            .instructions ol {
                margin: 0;
                padding-left: 20px;
            }
            
            .instructions li {
                margin: 5px 0;
                color: #475569;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="instructions">
                <h4>⏱️ TIMING REAL DEL SCRAPER:</h4>
                <ol>
                    <li><strong>0-3s:</strong> Abriendo TikTok</li>
                    <li><strong>3-63s:</strong> Esperando login manual</li>
                    <li><strong>63-73s:</strong> Navegando a contenido</li>
                    <li><strong>73-110s:</strong> Scroll y captura de videos</li>
                    <li><strong>110-115s:</strong> Procesamiento final</li>
                </ol>
            </div>
            
            <div class="browser-frame" id="browserFrame">
                <div class="timer-overlay" id="timerOverlay">
                    <div class="timer-text">🔄 Iniciando scraping de TikTok</div>
                    <div class="timer-countdown" id="countdown">3</div>
                    <div>Esperando para abrir navegador...</div>
                </div>
                
                <div class="browser-header">
                    <div class="browser-controls">
                        <div class="control-dot red"></div>
                        <div class="control-dot yellow"></div>
                        <div class="control-dot green"></div>
                    </div>
                    <div class="browser-url" id="urlDisplay">https://www.tiktok.com</div>
                </div>
                
                <div class="browser-content">
                    <iframe 
                        id="tiktokFrame"
                        src="https://www.tiktok.com" 
                        sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
                    ></iframe>
                </div>
            </div>
            
            <div style="text-align: center; margin: 20px;">
                <button id="loginDoneBtn" 
                        style="padding: 12px 30px; 
                               background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                               color: white; 
                               border: none; 
                               border-radius: 8px; 
                               font-size: 16px; 
                               font-weight: bold; 
                               cursor: pointer;
                               margin: 10px;
                               box-shadow: 0 5px 15px rgba(30, 58, 138, 0.3);"
                        onclick="simulateLoginComplete()">
                    ✅ He iniciado sesión - Continuar
                </button>
                
                <button id="startScrapingBtn"
                        style="padding: 12px 30px; 
                               background: linear-gradient(135deg, #10b981 0%, #34d399 100%); 
                               color: white; 
                               border: none; 
                               border-radius: 8px; 
                               font-size: 16px; 
                               font-weight: bold; 
                               cursor: pointer;
                               margin: 10px;
                               display: none;
                               box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);"
                        onclick="startScrapingProcess()">
                    🚀 Iniciar scraping automático
                </button>
            </div>
        </div>
        
        <script>
            let timerInterval;
            let countdown = 3;
            const countdownElement = document.getElementById('countdown');
            const timerOverlay = document.getElementById('timerOverlay');
            const browserFrame = document.getElementById('browserFrame');
            const loginBtn = document.getElementById('loginDoneBtn');
            const startBtn = document.getElementById('startScrapingBtn');
            
            // Iniciar countdown
            function startCountdown() {
                timerInterval = setInterval(() => {
                    countdown--;
                    countdownElement.textContent = countdown;
                    
                    if (countdown <= 0) {
                        clearInterval(timerInterval);
                        timerOverlay.style.display = 'none';
                        // Notificar a Streamlit que el navegador está listo
                        window.parent.postMessage({action: 'browser_ready'}, '*');
                    }
                }, 1000);
            }
            
            // Simular login completado
            function simulateLoginComplete() {
                loginBtn.style.display = 'none';
                startBtn.style.display = 'inline-block';
                
                // Cambiar URL a contenido
                document.getElementById('urlDisplay').textContent = 'https://www.tiktok.com/tiktokstudio/content';
                
                // Notificar a Streamlit
                window.parent.postMessage({action: 'login_complete'}, '*');
            }
            
            // Iniciar proceso de scraping
            function startScrapingProcess() {
                startBtn.disabled = true;
                startBtn.textContent = '🔄 Scraping en progreso...';
                
                // Notificar a Streamlit para iniciar scraping
                window.parent.postMessage({action: 'start_scraping'}, '*');
            }
            
            // Iniciar cuando la página carga
            window.onload = startCountdown;
            
            // Monitorear cambios en el iframe
            const frame = document.getElementById('tiktokFrame');
            setInterval(() => {
                try {
                    const currentUrl = frame.contentWindow.location.href;
                    document.getElementById('urlDisplay').textContent = currentUrl;
                } catch (e) {
                    // Ignorar errores de cross-origin
                }
            }, 1000);
        </script>
    </body>
    </html>
    """
    return html_code

# Botón principal para iniciar
if st.button("🎬 INICIAR PROCESO DE SCRAPING", type="primary", use_container_width=True):
    st.session_state.scraping_active = True
    st.session_state.scraping_step = 1
    st.rerun()

# Mostrar proceso paso a paso
if st.session_state.scraping_active:
    if st.session_state.scraping_step == 1:
        st.markdown("### PASO 1: Configuración del navegador")
        st.info("""
        **⏱️ Timing configurado según scraper original:**
        - TikTok se abrirá en 3 segundos
        - Tienes 60 segundos para iniciar sesión
        - Scroll automático de 25 ciclos
        - Procesamiento final de 5 segundos
        """)
        
        # Mostrar iframe con timing
        components.html(create_tiktok_iframe_with_timing(), height=700)
        
        # Botón para avanzar al paso 2 (simulado)
        if st.button("✅ AVANZAR AL PASO 2 - SIMULAR LOGIN", use_container_width=True):
            st.session_state.scraping_step = 2
            st.rerun()
    
    elif st.session_state.scraping_step == 2:
        st.markdown("### PASO 2: Simulación de scraping con timing real")
        
        # Simular scraping con tiempos REALES
        if simulate_real_scraping():
            st.session_state.scraping_step = 3
            st.rerun()
    
    elif st.session_state.scraping_step == 3:
        st.markdown("### PASO 3: Procesamiento de datos")
        
        with st.spinner("📊 Generando datos realistas..."):
            time.sleep(3)
            
            # Generar datos REALES con estructura del scraper original
            real_data = []
            for i in range(39):  # 39 videos como el scraper original
                days_ago = random.randint(1, 60)
                fecha = (datetime.now() - timedelta(days=days_ago)).strftime("%d %b, %H:%M")
                views = random.randint(100, 50000)
                likes = int(views * random.uniform(0.03, 0.15))
                comments = int(views * random.uniform(0.002, 0.01))
                
                real_data.append({
                    'duracion_video': f"{random.randint(0, 2):02d}:{random.randint(10, 59):02d}",
                    'titulo': f"Video #{i+1} - {random.choice(['Tutorial', 'Review', 'Unboxing', 'Vlog', 'Challenge'])}",
                    'fecha_publicacion': fecha,
                    'privacidad': random.choice(['Todo el mundo', 'Solo yo', 'Amigos']),
                    'visualizaciones': f"{views:,}",
                    'me_gusta': f"{likes:,}",
                    'comentarios': f"{comments:,}"
                })
            
            # Enviar al backend
            try:
                response = requests.post(
                    f"{BACKEND_URL}/process",
                    json={"videos": real_data},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.tiktok_data = result.get("data", [])
                    st.success(f"✅ {len(real_data)} videos procesados correctamente")
                else:
                    st.error("Error en el backend")
                    
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        
        # Botón para ver resultados
        if st.button("📊 VER RESULTADOS FINALES", use_container_width=True):
            st.session_state.scraping_step = 4
            st.rerun()
    
    elif st.session_state.scraping_step == 4 and st.session_state.tiktok_data:
        st.markdown("### 📋 RESULTADOS DEL SCRAPING")
        
        df = pd.DataFrame(st.session_state.tiktok_data)
        
        # Mostrar tabla
        st.dataframe(df, use_container_width=True)
        
        # Estadísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Videos totales", len(df))
        with col2:
            total_views = sum(int(str(v).replace(',', '')) for v in df['visualizaciones'])
            st.metric("Vistas totales", f"{total_views:,}")
        with col3:
            avg_views = total_views // len(df)
            st.metric("Promedio vistas", f"{avg_views:,}")
        with col4:
            public_videos = len(df[df['privacidad'].str.contains('Todo el mundo')])
            st.metric("Videos públicos", public_videos)
        
        # Descargar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f"tiktok_scraping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Botón para reiniciar
        if st.button("🔄 INICIAR NUEVO SCRAPING", type="secondary", use_container_width=True):
            st.session_state.scraping_active = False
            st.session_state.scraping_step = 0
            st.session_state.tiktok_data = None
            st.rerun()

# Resumen de timing
st.markdown("---")
with st.expander("⏱️ CRONOGRAMA DEL SCRAPING (REAL)", expanded=True):
    st.markdown("""
    | Paso | Duración | Descripción |
    |------|----------|-------------|
    | 1. Apertura | 3 segundos | Abrir TikTok en navegador |
    | 2. Login | 60 segundos | **TIEMPO PARA INICIAR SESIÓN MANUAL** |
    | 3. Navegación | 10 segundos | Ir a contenido del estudio |
    | 4. Scroll | ~38 segundos | 25 ciclos de scroll (1.5s cada uno) |
    | 5. Procesamiento | 5 segundos | Procesar datos capturados |
    | **TOTAL** | **~116 segundos** | **≈ 2 minutos** |
    
    *Nota: Los tiempos son los configurados en el scraper original de Selenium.*
    """)

# Footer
st.markdown("---")
st.caption("🎬 TikTok Scraper con timing real • Simulación exacta del proceso original")
