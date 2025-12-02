import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import time
import json
from datetime import datetime

st.set_page_config(
    page_title="TikTok Scraper - Ventana Integrada",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 TikTok Scraper - Ventana de Navegador Integrada")
st.markdown("---")

# URL del backend
BACKEND_URL = "https://pahubisas.pythonanywhere.com"

# Estado
if 'scraping_active' not in st.session_state:
    st.session_state.scraping_active = False
if 'tiktok_data' not in st.session_state:
    st.session_state.tiktok_data = None

# Función para iframe de TikTok
def create_tiktok_iframe():
    """Crea un iframe con TikTok para login manual"""
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .browser-window {
                border: 3px solid #1e3a8a;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                margin: 20px auto;
                max-width: 1200px;
            }
            .browser-header {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: white;
                padding: 15px 25px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .browser-controls {
                display: flex;
                gap: 10px;
            }
            .browser-btn {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                cursor: pointer;
            }
            .red { background: #ff5f56; }
            .yellow { background: #ffbd2e; }
            .green { background: #27c93f; }
            .browser-url-bar {
                flex-grow: 1;
                background: white;
                margin: 0 20px;
                padding: 8px 15px;
                border-radius: 20px;
                color: #333;
                font-family: monospace;
                font-size: 14px;
            }
            .browser-content {
                height: 600px;
                background: white;
            }
            .instructions {
                background: #f0f9ff;
                padding: 20px;
                border-radius: 10px;
                margin: 20px;
                border-left: 5px solid #0ea5e9;
            }
            .instructions h4 {
                color: #0369a1;
                margin-bottom: 15px;
            }
            .instructions ol {
                color: #475569;
                line-height: 1.8;
            }
            .status-indicator {
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
                margin: 10px 0;
            }
            .status-waiting {
                background: #fef3c7;
                color: #92400e;
            }
            .status-logged {
                background: #d1fae5;
                color: #065f46;
            }
            .status-scraping {
                background: #dbeafe;
                color: #1e40af;
            }
        </style>
    </head>
    <body>
        <div class="instructions">
            <h4>📋 INSTRUCCIONES PARA SCRAPING MANUAL</h4>
            <ol>
                <li><strong>Inicia sesión</strong> en TikTok en la ventana de abajo</li>
                <li><strong>Navega</strong> a tu contenido (perfil o videos)</li>
                <li><strong>No cierres</strong> la ventana durante el proceso</li>
                <li><strong>Haz clic en "Continuar Scraping"</strong> cuando hayas iniciado sesión</li>
            </ol>
        </div>
        
        <div class="browser-window">
            <div class="browser-header">
                <div class="browser-controls">
                    <div class="browser-btn red"></div>
                    <div class="browser-btn yellow"></div>
                    <div class="browser-btn green"></div>
                </div>
                <div class="browser-url-bar" id="urlDisplay">https://www.tiktok.com/login</div>
                <div style="color: white; font-weight: bold;">
                    🎬 TikTok
                </div>
            </div>
            <div class="browser-content">
                <iframe 
                    id="tiktokFrame"
                    src="https://www.tiktok.com/login" 
                    style="width:100%; height:100%; border:none;"
                    allow="camera; microphone; autoplay; clipboard-write; encrypted-media;"
                    sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
                ></iframe>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px;">
            <div id="statusIndicator" class="status-indicator status-waiting">
                ⏳ Esperando inicio de sesión...
            </div>
            <br>
            <button id="continueBtn" 
                    style="padding: 15px 40px; 
                           background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                           color: white; 
                           border: none; 
                           border-radius: 10px; 
                           font-size: 18px; 
                           font-weight: bold; 
                           cursor: pointer;
                           box-shadow: 0 10px 25px rgba(30, 58, 138, 0.3);"
                    onclick="window.parent.postMessage({action: 'continue_scraping'}, '*')">
                🚀 Continuar Scraping
            </button>
        </div>
        
        <script>
            // Monitorear cambios en el iframe
            const frame = document.getElementById('tiktokFrame');
            const urlDisplay = document.getElementById('urlDisplay');
            const statusIndicator = document.getElementById('statusIndicator');
            const continueBtn = document.getElementById('continueBtn');
            
            // Verificar login cada 3 segundos
            setInterval(() => {
                try {
                    const currentUrl = frame.contentWindow.location.href;
                    urlDisplay.textContent = currentUrl;
                    
                    // Verificar si está logueado
                    if (currentUrl.includes('tiktok.com') && !currentUrl.includes('login')) {
                        statusIndicator.innerHTML = '✅ Sesión iniciada correctamente';
                        statusIndicator.className = 'status-indicator status-logged';
                        continueBtn.disabled = false;
                        continueBtn.style.opacity = '1';
                        
                        // Notificar al padre
                        window.parent.postMessage({
                            action: 'login_detected',
                            url: currentUrl
                        }, '*');
                    }
                } catch (e) {
                    // Error de cross-origin, ignorar
                }
            }, 3000);
            
            // Inicialmente deshabilitar botón
            continueBtn.disabled = true;
            continueBtn.style.opacity = '0.5';
            
            // Habilitar navegación manual
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'r') {
                    frame.contentWindow.location.reload();
                }
            });
        </script>
    </body>
    </html>
    """
    
    return html_code

# Botón principal
if st.button("🖥️ ABRIR VENTANA DE TIKTOK", type="primary", use_container_width=True):
    st.session_state.scraping_active = True

# Mostrar iframe si scraping está activo
if st.session_state.scraping_active:
    st.markdown("### 📱 Ventana de TikTok Integrada")
    st.markdown("""
    **ℹ️ Instrucciones:**
    1. Inicia sesión en la ventana de abajo
    2. Navega a tu contenido
    3. Haz clic en "Continuar Scraping"
    """)
    
    # Mostrar iframe
    components.html(create_tiktok_iframe(), height=800)
    
    # Botón para simular scraping (en Streamlit Cloud no podemos hacer scraping real)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 SIMULAR SCRAPING (Datos de Prueba)", use_container_width=True):
            # Generar datos de prueba REALISTAS
            with st.spinner("Generando datos de prueba..."):
                time.sleep(2)
                
                # Datos de prueba realistas
                test_data = []
                for i in range(15):
                    views = (i + 1) * 1000 + (i * 234)
                    likes = int(views * 0.15)
                    comments = int(likes * 0.1)
                    
                    test_data.append({
                        'duracion_video': f"{random.randint(0, 3)}:{random.randint(10, 59):02d}",
                        'titulo': f"Video REAL #{i+1} - Contenido auténtico de TikTok",
                        'fecha_publicacion': f"{random.randint(1, 30)} {random.choice(['ene', 'feb', 'mar'])}",
                        'privacidad': random.choice(['Todo el mundo', 'Solo yo']),
                        'visualizaciones': f"{views:,}",
                        'me_gusta': f"{likes:,}",
                        'comentarios': f"{comments:,}"
                    })
                
                # Enviar al backend para procesamiento
                response = requests.post(
                    f"{BACKEND_URL}/process",
                    json={"videos": test_data},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.tiktok_data = result.get("data", [])
                    st.success(f"✅ {len(test_data)} videos procesados")
                else:
                    st.error("Error al procesar datos")
    
    with col2:
        if st.button("📊 VER DATOS PROCESADOS", use_container_width=True):
            if st.session_state.tiktok_data:
                df = pd.DataFrame(st.session_state.tiktok_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No hay datos procesados")

# Mostrar resultados si existen
if st.session_state.tiktok_data:
    st.markdown("---")
    st.subheader("📊 Resultados del Scraping")
    
    df = pd.DataFrame(st.session_state.tiktok_data)
    
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

# Información
st.markdown("---")
st.info("""
**⚠️ NOTA TÉCNICA IMPORTANTE:**

Streamlit Cloud **NO permite**:
- Abrir ventanas reales del navegador
- Ejecutar Selenium
- Acceder al sistema de archivos del cliente

**SOLUCIÓN ACTUAL:**
1. Ventana de TikTok integrada (iframe)
2. Login MANUAL del usuario
3. Simulación de scraping con datos realistas
4. Procesamiento real en backend

**Para scraping COMPLETAMENTE AUTOMÁTICO:**
- Ejecutar aplicación LOCALMENTE con Selenium
- O usar servidor dedicado con acceso a navegador real
""")
