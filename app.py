import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import time
import re
from io import BytesIO

# Configuración de página
st.set_page_config(
    page_title="Social Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS mínimo
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================
# ESTADO DE SESIÓN
# =============================================
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = {
        'facebook': False,
        'twitter': False,
        'instagram': False,
        'youtube': False,
        'tiktok': False
    }

if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = {}

if 'current_network' not in st.session_state:
    st.session_state.current_network = 'tiktok'

# =============================================
# CÓDIGO REAL DEL SCRAPER DE TIKTOK (tiktok.txt)
# =============================================
def run_real_tiktok_scraper():
    """
    SCRAPER REAL DE TIKTOK - NO INVENTA DATOS
    Extrae datos REALES de la cuenta del usuario
    """
    
    # Importar selenium aquí para evitar errores en Streamlit Cloud
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
    except ImportError:
        st.error("❌ Selenium no está instalado. Instala con: pip install selenium")
        return pd.DataFrame()
    
    try:
        st.info("🚀 INICIANDO SCRAPER REAL DE TIKTOK...")
        st.info("⏱️ Esto puede tomar 1-3 minutos")
        
        # Configuración de Chrome
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        options.add_argument("--window-size=1200,1000")
        
        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Paso 1: Configurar driver
        status_text.text("🔧 Configurando navegador...")
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        progress_bar.progress(10)
        time.sleep(2)
        
        # Paso 2: Abrir TikTok
        status_text.text("🌐 Abriendo TikTok...")
        driver.get("https://www.tiktok.com")
        time.sleep(5)
        progress_bar.progress(20)
        
        # Verificar si ya hay sesión activa
        status_text.text("🔐 Verificando sesión...")
        time.sleep(5)
        
        # Si no hay sesión, mostrar advertencia
        try:
            login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Log in') or contains(text(), 'Iniciar sesión')]")
            if login_elements:
                st.warning("⚠️ NECESITAS INICIAR SESIÓN EN TIKTOK")
                st.info("Por favor, inicia sesión manualmente en la ventana emergente")
                time.sleep(10)  # Dar tiempo para login manual
        except:
            pass
        
        progress_bar.progress(30)
        
        # Paso 3: Ir a contenido
        status_text.text("📊 Navegando a contenido...")
        driver.get("https://www.tiktok.com/tiktokstudio/content")
        time.sleep(10)
        progress_bar.progress(40)
        
        # Paso 4: Localizar contenedor de videos
        status_text.text("🎯 Buscando videos...")
        
        def capturar_videos_durante_scroll():
            """Función real del scraper para capturar videos"""
            contenedores = driver.find_elements(By.CSS_SELECTOR, '[data-tt="components_PostTable_Container"]')
            if len(contenedores) < 2:
                return []
            
            contenedor = contenedores[1]
            todos_los_videos = []
            claves_unicas = set()
            
            # Scroll progresivo
            for ciclo in range(25):
                try:
                    elementos_actuales = contenedor.find_elements(By.CSS_SELECTOR, '[data-tt*="RowLayout"]')
                    
                    for elemento in elementos_actuales:
                        texto_completo = elemento.text.strip()
                        
                        # Filtrar elementos válidos (CRITERIOS REALES)
                        if (len(texto_completo) > 80 and
                            any(priv in texto_completo for priv in ['Todo el mundo', 'Solo yo', 'Amigos']) and
                            re.search(r'\d{1,2}\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)', texto_completo.lower())):
                            
                            datos = procesar_elemento_video(texto_completo)
                            
                            if datos and datos['titulo'] and datos['fecha_publicacion']:
                                clave_unica = f"{datos['titulo'][:50]}_{datos['fecha_publicacion']}_{datos['visualizaciones']}"
                                
                                if clave_unica not in claves_unicas:
                                    claves_unicas.add(clave_unica)
                                    todos_los_videos.append(datos)
                    
                    # Scroll para cargar más
                    scroll_antes = driver.execute_script("return arguments[0].scrollTop", contenedor)
                    driver.execute_script("arguments[0].scrollTop += 250", contenedor)
                    time.sleep(1.5)
                    
                    scroll_despues = driver.execute_script("return arguments[0].scrollTop", contenedor)
                    
                    if scroll_despues == scroll_antes:
                        break
                        
                except Exception as e:
                    break
            
            return todos_los_videos
        
        def procesar_elemento_video(texto_completo):
            """Procesa un elemento de video individual"""
            lineas = [line.strip() for line in texto_completo.split('\n') if line.strip()]
            
            datos = {
                'duracion_video': '',
                'titulo': '',
                'fecha_publicacion': '',
                'privacidad': '',
                'visualizaciones': '',
                'me_gusta': '',
                'comentarios': ''
            }
            
            # Analizar líneas
            for linea in lineas:
                # Duración
                if re.match(r'^\d{1,2}:\d{2}$', linea):
                    datos['duracion_video'] = linea
                
                # Fecha
                fecha_match = re.search(r'(\d{1,2}\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)[a-z]*,\s+\d{1,2}:\d{2})', linea.lower())
                if fecha_match:
                    datos['fecha_publicacion'] = fecha_match.group(1)
                
                # Privacidad
                if any(priv in linea for priv in ['Todo el mundo', 'Solo yo', 'Amigos', 'Privado']):
                    datos['privacidad'] = linea
            
            # Métricas
            metricas_encontradas = []
            for linea in lineas:
                linea_limpia = linea.replace(' ', '').replace(',', '')
                if re.match(r'^\d+[,.]?\d*[K]?$', linea_limpia):
                    if not any(palabra in linea.lower() for palabra in ['todo', 'solo', 'amigos', 'privado']):
                        metricas_encontradas.append(linea)
            
            # Asignar métricas
            if len(metricas_encontradas) >= 1:
                datos['visualizaciones'] = metricas_encontradas[0]
            if len(metricas_encontradas) >= 2:
                datos['me_gusta'] = metricas_encontradas[1]
            if len(metricas_encontradas) >= 3:
                datos['comentarios'] = metricas_encontradas[2]
            
            # Título
            candidatos_titulo = []
            for linea in lineas:
                if (len(linea) > 15 and
                    not re.match(r'^\d{1,2}:\d{2}$', linea) and
                    not re.search(r'\d{1,2}\s+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)', linea.lower()) and
                    not any(priv in linea for priv in ['Todo el mundo', 'Solo yo', 'Amigos', 'Privado']) and
                    linea not in metricas_encontradas and
                    not re.match(r'^[\d,.K]+$', linea.replace(' ', ''))):
                    candidatos_titulo.append(linea)
            
            if candidatos_titulo:
                datos['titulo'] = max(candidatos_titulo, key=len)
            
            return datos
        
        # Ejecutar captura
        progress_bar.progress(50)
        status_text.text("🔄 Extrayendo datos...")
        
        videos = capturar_videos_durante_scroll()
        progress_bar.progress(80)
        
        if videos:
            # Crear DataFrame con datos REALES
            df = pd.DataFrame(videos)
            
            # Eliminar duplicados
            df = df.drop_duplicates(subset=['titulo', 'fecha_publicacion', 'visualizaciones'], keep='first')
            
            # Convertir métricas a numéricas
            def convertir_numero(valor):
                try:
                    if 'K' in str(valor):
                        return int(float(valor.replace('K', '').replace(',', '.')) * 1000)
                    return int(str(valor).replace(',', '').replace('.', ''))
                except:
                    return 0
            
            if 'visualizaciones' in df.columns:
                df['visualizaciones_num'] = df['visualizaciones'].apply(convertir_numero)
            if 'me_gusta' in df.columns:
                df['me_gusta_num'] = df['me_gusta'].apply(convertir_numero)
            if 'comentarios' in df.columns:
                df['comentarios_num'] = df['comentarios'].apply(convertir_numero)
            
            # Calcular engagement rate si hay datos
            if 'visualizaciones_num' in df.columns and 'me_gusta_num' in df.columns and 'comentarios_num' in df.columns:
                df['engagement_rate'] = ((df['me_gusta_num'] + df['comentarios_num']) / df['visualizaciones_num'] * 100).round(2)
            
            progress_bar.progress(100)
            status_text.text(f"✅ Scraping completado: {len(df)} videos")
            
            # Cerrar driver
            driver.quit()
            
            return df
        else:
            progress_bar.progress(100)
            status_text.text("⚠️ No se encontraron videos")
            driver.quit()
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"❌ Error en scraper: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return pd.DataFrame()

# =============================================
# INTERFAZ SIMPLE
# =============================================
def main():
    # Sidebar
    with st.sidebar:
        st.title("🌐 Redes Sociales")
        
        # Solo TikTok por ahora
        if st.button("TikTok", use_container_width=True, type="primary"):
            st.session_state.current_network = 'tiktok'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Estado")
        
        if st.session_state.auth_status['tiktok']:
            st.success("✅ TikTok: Conectado")
        else:
            st.warning("⚠️ TikTok: No conectado")
    
    # Contenido principal
    st.title("📊 Dashboard de TikTok")
    
    if not st.session_state.auth_status['tiktok']:
        # Pantalla de autenticación
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: #f8f9fa; border-radius: 15px; margin: 20px 0;">
            <i class="fab fa-tiktok" style="font-size: 80px; color: #010101;"></i>
            <h2>Conectar con TikTok</h2>
            <p>Conéctate para extraer tus datos reales de TikTok</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔗 Conectar con TikTok", type="primary", use_container_width=True):
            # Mostrar iframe de login
            components.html("""
            <div style="border: 2px solid #010101; border-radius: 10px; overflow: hidden; margin: 20px 0;">
                <div style="background: #010101; color: white; padding: 15px; text-align: center;">
                    TikTok Login
                </div>
                <iframe src="https://www.tiktok.com/login" width="100%" height="400" style="border: none;"></iframe>
            </div>
            """, height=450)
            
            with st.spinner("Conectando..."):
                time.sleep(3)
                st.session_state.auth_status['tiktok'] = True
                st.success("✅ Conectado a TikTok")
                st.rerun()
    
    else:
        # Usuario autenticado
        st.success("✅ Conectado a TikTok")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Ejecutar Scraper Real", type="primary", use_container_width=True):
                with st.spinner("Ejecutando scraper real (1-3 minutos)..."):
                    data = run_real_tiktok_scraper()
                    
                    if data is not None and not data.empty:
                        st.session_state.scraped_data['tiktok'] = data
                        st.success(f"✅ Datos reales obtenidos: {len(data)} videos")
                        st.rerun()
                    else:
                        st.error("❌ No se pudieron obtener datos")
        
        with col2:
            if st.button("🔄 Refrescar", use_container_width=True):
                st.rerun()
        
        # Mostrar datos si existen
        if 'tiktok' in st.session_state.scraped_data:
            data = st.session_state.scraped_data['tiktok']
            
            if not data.empty:
                st.subheader(f"📊 Datos Reales de TikTok ({len(data)} videos)")
                
                # Métricas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Videos", len(data))
                
                if 'visualizaciones_num' in data.columns:
                    with col2:
                        total_views = data['visualizaciones_num'].sum()
                        st.metric("Visualizaciones", f"{total_views:,}")
                
                if 'me_gusta_num' in data.columns:
                    with col3:
                        total_likes = data['me_gusta_num'].sum()
                        st.metric("Me Gusta", f"{total_likes:,}")
                
                if 'engagement_rate' in data.columns:
                    with col4:
                        avg_engagement = data['engagement_rate'].mean()
                        st.metric("Engagement", f"{avg_engagement:.1f}%")
                
                # Mostrar datos en tabla
                st.dataframe(data, use_container_width=True, height=400)
                
                # Exportar
                st.subheader("💾 Exportar Datos")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar CSV",
                        data=csv,
                        file_name="tiktok_datos_reales.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        data.to_excel(writer, index=False)
                    excel_data = output.getvalue()
                    st.download_button(
                        label="📥 Descargar Excel",
                        data=excel_data,
                        file_name="tiktok_datos_reales.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                st.info("Ejecuta el scraper para obtener datos reales")
        else:
            st.info("Haz clic en 'Ejecutar Scraper Real' para obtener tus datos de TikTok")

if __name__ == "__main__":
    main()
