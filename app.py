import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
import requests
import numpy as np
from io import BytesIO

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard TikTok - Métricas",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# CONEXIÓN A BACKEND REAL
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/FollowerHistory.xlsx"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/base_pautas.xlsx"

def cargar_datos_backend():
    """Carga datos principales desde el backend"""
    try:
        r = requests.get(BACKEND_URL, timeout=20)
        r.raise_for_status()
        data = r.json()

        # Data principal
        df = pd.DataFrame(data.get("data", []))

        # Normalización básica
        if "fecha_publicacion" in df.columns:
            df["fecha_publicacion"] = pd.to_datetime(
                df["fecha_publicacion"],
                dayfirst=True,
                errors="coerce"
            )

        # Convertir números
        num_cols = ["visualizaciones", "me_gusta", "comentarios"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Red fija si no existe
        if "red" not in df.columns:
            df["red"] = "tiktok"

        return df

    except Exception as e:
        st.error(f"Error al conectar con el backend: {str(e)}")
        return pd.DataFrame()

def cargar_datos_inversion():
    """Carga datos de inversión desde archivos Excel"""
    try:
        # Descargar archivos desde PythonAnywhere
        followers_response = requests.get(FOLLOWERS_URL, timeout=30)
        pautas_response = requests.get(PAUTA_URL, timeout=30)
        
        if followers_response.status_code != 200 or pautas_response.status_code != 200:
            return pd.DataFrame(), pd.DataFrame()
        
        # Leer archivos Excel desde bytes
        fh_df = pd.read_excel(BytesIO(followers_response.content))
        bp_df = pd.read_excel(BytesIO(pautas_response.content))
        
        return fh_df, bp_df
        
    except Exception as e:
        st.error(f"Error al cargar datos de inversión: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

# Función para convertir valores a números
def to_num(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return np.nan
    if isinstance(v, (int, float, np.integer, np.floating)):
        return float(v)
    s = str(v).strip()
    if s == "":
        return np.nan
    s = s.replace("$", "").replace("COP", "").replace("cop", "").replace(" ", "")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        if "," in s and "." not in s:
            s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return np.nan

#############################################
# FUNCIONES PARA NUEVAS GRÁFICAS (USANDO PLOTLY)
#############################################

def generar_grafica_inversion_plotly(fh_df, bp_df):
    """Genera la gráfica de inversión vs seguidores usando Plotly"""
    try:
        # Parámetros básicos
        STEP = 15000
        IMPACT_DAYS = 3
        USE_IMPACT = True
        
        # Procesar datos de seguidores
        fh_df["Fecha"] = pd.to_datetime(fh_df["Fecha"], dayfirst=True, errors="coerce")
        bp_df["fecha"] = pd.to_datetime(bp_df["fecha"], dayfirst=True, errors="coerce")
        
        # Convertir numéricos
        if "Costo" in bp_df.columns:
            bp_df["Costo"] = bp_df["Costo"].apply(to_num).astype("float64")
        
        if "Seguidores_Totales" in fh_df.columns:
            fh_df["Seguidores_Totales"] = fh_df["Seguidores_Totales"].apply(to_num).astype("float64")
        
        # Calcular neto diario
        fh_df = fh_df.dropna(subset=["Fecha"]).sort_values("Fecha").reset_index(drop=True)
        fh_df["Neto_Diario_Real"] = fh_df["Seguidores_Totales"].diff()
        fh_df.loc[fh_df["Neto_Diario_Real"] <= 0, "Neto_Diario_Real"] = np.nan
        
        fh_df = fh_df.rename(columns={"Fecha": "fecha"})
        fh_df = fh_df[["fecha", "Seguidores_Totales", "Neto_Diario_Real"]].copy()
        
        # Unir datos
        df = pd.merge(bp_df, fh_df, on="fecha", how="left").sort_values("fecha").reset_index(drop=True)
        
        # Calcular impacto
        if IMPACT_DAYS < 1:
            IMPACT_DAYS = 1
            
        neto = df["Neto_Diario_Real"].astype("float64")
        impact = np.full(len(df), np.nan, dtype="float64")
        for i in range(len(df)):
            s = 0.0
            ok = False
            for k in range(IMPACT_DAYS):
                j = i + k
                if j >= len(df):
                    break
                v = neto.iloc[j]
                if pd.notna(v) and v > 0:
                    s += float(v)
                    ok = True
            impact[i] = s if ok else np.nan
        
        df["Seguidores_Impacto"] = impact
        RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
        
        # Filtrar datos válidos
        cand = df[(df["Costo"] > 0) & (df[RESULT_COL].notna()) & (df[RESULT_COL] > 0)].copy()
        if cand.empty:
            return None
        
        # Agrupar por rangos de inversión
        cmin = float(cand["Costo"].min())
        cmax = float(cand["Costo"].max())
        start = float(np.floor(cmin / STEP) * STEP)
        end = float(np.ceil(cmax / STEP) * STEP) + STEP
        bins = np.arange(start, end + 1, STEP)
        
        cand["Costo_bin"] = pd.cut(cand["Costo"], bins=bins, include_lowest=True, right=False)
        
        curve = cand.groupby("Costo_bin", observed=True).agg(
            Inversion_promedio=("Costo", "mean"),
            Seguidores_promedio=(RESULT_COL, "mean"),
            Dias=("Costo", "count"),
        ).reset_index(drop=True).sort_values("Inversion_promedio").reset_index(drop=True)
        
        # Crear gráfica con Plotly
        fig = go.Figure()
        
        # Puntos de días reales
        fig.add_trace(go.Scatter(
            x=cand["Costo"],
            y=cand[RESULT_COL],
            mode='markers',
            name='Días reales',
            marker=dict(
                size=8,
                color='#60a5fa',
                opacity=0.4,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Costo: $%{x:,.0f}</b><br>Seguidores: %{y:,.0f}<extra></extra>'
        ))
        
        # Línea de promedio
        fig.add_trace(go.Scatter(
            x=curve["Inversion_promedio"],
            y=curve["Seguidores_promedio"],
            mode='lines+markers',
            name='Promedio por nivel',
            line=dict(color='#f59e0b', width=3),
            marker=dict(
                size=12,
                color='#f59e0b',
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>Inversión promedio: $%{x:,.0f}</b><br>Seguidores promedio: %{y:,.0f}<br>Días en rango: %{text}<extra></extra>',
            text=curve["Dias"]
        ))
        
        # Líneas verticales para rangos
        for x_real in bins:
            if x_real >= start and x_real <= end:
                fig.add_shape(
                    type="line",
                    x0=x_real, x1=x_real,
                    y0=0, y1=cand[RESULT_COL].max() * 1.1,
                    line=dict(
                        color="rgba(203, 213, 225, 0.3)",
                        width=1,
                        dash="dash",
                    ),
                )
        
        # Actualizar layout
        fig.update_layout(
            title="📈 Inversión vs Seguidores (curva por niveles)",
            xaxis_title="Inversión (Costo)",
            yaxis_title=f"Seguidores (Impacto {IMPACT_DAYS}d)",
            template="plotly_white",
            height=600,
            hovermode="closest",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            xaxis=dict(
                tickformat=",",
                gridcolor='rgba(241, 245, 249, 0.5)'
            ),
            yaxis=dict(
                tickformat=",",
                gridcolor='rgba(241, 245, 249, 0.5)'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error al generar gráfica: {str(e)}")
        return None

def generar_mapa_calor_plotly(fh_df, bp_df):
    """Genera el heatmap de CPS por día/semana usando Plotly"""
    try:
        # Procesar datos
        fh_df["Fecha"] = pd.to_datetime(fh_df["Fecha"], dayfirst=True, errors="coerce")
        bp_df["fecha"] = pd.to_datetime(bp_df["fecha"], dayfirst=True, errors="coerce")
        
        # Convertir numéricos
        for col in ["Costo", "Visualizaciones", "Seguidores"]:
            if col in bp_df.columns:
                bp_df[col] = bp_df[col].apply(to_num).astype("float64")
        
        fh_df["Seguidores_Totales"] = fh_df["Seguidores_Totales"].apply(to_num).astype("float64")
        
        # Calcular neto diario
        fh_df = fh_df.rename(columns={"Fecha": "fecha", "Seguidores_Totales": "Neto_Diario_Real"})
        fh_df = fh_df[["fecha", "Neto_Diario_Real"]].copy()
        
        # Unir datos
        df = pd.merge(bp_df, fh_df, on="fecha", how="left").sort_values("fecha").reset_index(drop=True)
        
        # Día de semana y semana ISO
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        df["Dia_Semana"] = df["fecha"].dt.dayofweek.map(lambda i: dias[int(i)] if pd.notna(i) else np.nan)
        
        iso = df["fecha"].dt.isocalendar()
        df["ISO_Year"] = iso["year"].astype(int)
        df["ISO_Week"] = iso["week"].astype(int)
        df["WeekKey"] = df["ISO_Year"].astype(str) + "-W" + df["ISO_Week"].astype(str).str.zfill(2)
        
        # Agregación para heatmap
        g = df[(df["Costo"] > 0) & (df["Neto_Diario_Real"].notna())].copy()
        g["Seg_pos"] = np.where(g["Neto_Diario_Real"] > 0, g["Neto_Diario_Real"], 0.0)
        
        agg = g.groupby(["Dia_Semana", "WeekKey"], as_index=False).agg(
            Costo_sum=("Costo", "sum"),
            Seguidores_sum=("Neto_Diario_Real", "sum"),
            Seguidores_pos_sum=("Seg_pos", "sum")
        )
        
        agg["CPS_cell"] = np.where(
            agg["Seguidores_pos_sum"] > 0,
            agg["Costo_sum"] / agg["Seguidores_pos_sum"],
            np.nan
        )
        
        # Pivot tables
        pivot_cps = agg.pivot(index="Dia_Semana", columns="WeekKey", values="CPS_cell").reindex(dias)
        pivot_seg = agg.pivot(index="Dia_Semana", columns="WeekKey", values="Seguidores_sum").reindex(dias)
        
        # Crear mapa de calor con Plotly
        weeks = list(pivot_cps.columns)
        
        # Heatmap para CPS
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("🗺️ Mapa de Calor - CPS (Costo por Seguidor)", "📊 Resumen por Día"),
            column_widths=[0.7, 0.3],
            horizontal_spacing=0.1
        )
        
        # Mapa de calor principal
        fig.add_trace(
            go.Heatmap(
                z=pivot_cps.values,
                x=weeks,
                y=dias,
                colorscale='RdYlGn_r',  # Rojo-Amarillo-Verde invertido (rojo = malo, verde = bueno)
                zmin=pivot_cps.values[np.isfinite(pivot_cps.values)].min() if np.any(np.isfinite(pivot_cps.values)) else 0,
                zmax=pivot_cps.values[np.isfinite(pivot_cps.values)].max() if np.any(np.isfinite(pivot_cps.values)) else 1,
                colorbar=dict(title="CPS", x=0.45),
                hovertemplate='<b>%{y} - %{x}</b><br>CPS: %{z:,.0f}<br>Seguidores: %{customdata:,.0f}<extra></extra>',
                customdata=pivot_seg.values,
                text=pivot_cps.applymap(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A").values,
                texttemplate="%{text}",
                textfont={"size": 10}
            ),
            row=1, col=1
        )
        
        # Calcular resumen por día para gráfico de barras
        sum_day = g.groupby("Dia_Semana", as_index=False).agg(
            Costo_sum=("Costo", "sum"),
            Seguidores_sum=("Neto_Diario_Real", "sum"),
            Seguidores_pos_sum=("Seg_pos", "sum")
        )
        
        sum_day["CPS_total_dia"] = np.where(
            sum_day["Seguidores_pos_sum"] > 0,
            sum_day["Costo_sum"] / sum_day["Seguidores_pos_sum"],
            np.nan
        )
        
        sum_day = sum_day.set_index("Dia_Semana").reindex(dias).reset_index()
        
        # Gráfico de barras por día
        fig.add_trace(
            go.Bar(
                y=dias,
                x=sum_day["CPS_total_dia"],
                orientation='h',
                name='CPS por día',
                marker_color='#3B82F6',
                hovertemplate='<b>%{y}</b><br>CPS: %{x:,.0f}<extra></extra>',
                text=sum_day["CPS_total_dia"].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"),
                textposition='outside'
            ),
            row=1, col=2
        )
        
        # Actualizar layout
        fig.update_layout(
            height=500,
            template="plotly_white",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        fig.update_xaxes(title_text="Semanas", row=1, col=1)
        fig.update_yaxes(title_text="Días", row=1, col=1)
        fig.update_xaxes(title_text="CPS", row=1, col=2)
        fig.update_yaxes(title_text="", row=1, col=2)
        
        return fig
        
    except Exception as e:
        st.error(f"Error al generar mapa de calor: {str(e)}")
        return None

#############################################
# CARGA DE DATOS
#############################################

# Cargar datos
df = cargar_datos_backend()
fh_df, bp_df = cargar_datos_inversion()

# Filtrar solo TikTok
tiktok_df = df[df['red'] == 'tiktok'].copy() if not df.empty else pd.DataFrame()

# Calcular métricas básicas
total_contenidos = len(tiktok_df) if not tiktok_df.empty else 0
total_visualizaciones = tiktok_df['visualizaciones'].sum() if not tiktok_df.empty and 'visualizaciones' in tiktok_df.columns else 0

# Calcular métricas de inversión
coste_anuncio = 0
visualizaciones_videos = 0
nuevos_seguidores = 0
total_seguidores = 0

if not bp_df.empty:
    if 'Costo' in bp_df.columns:
        coste_anuncio = bp_df['Costo'].sum()
    if 'Visualizaciones' in bp_df.columns:
        visualizaciones_videos = bp_df['Visualizaciones'].sum()
    if 'Seguidores' in bp_df.columns:
        nuevos_seguidores = bp_df['Seguidores'].sum()

if not fh_df.empty:
    if 'Seguidores_Totales' in fh_df.columns:
        total_seguidores = fh_df['Seguidores_Totales'].iloc[-1] if len(fh_df) > 0 else 0

# Formatear números para display
def format_number(num):
    try:
        return f"{int(num):,}".replace(",", ".")
    except:
        return "0"

#############################################
# INTERFAZ PRINCIPAL - SIMPLIFICADA
#############################################

st.title("📊 Dashboard TikTok - Métricas e Inversión")

# Métricas principales en 2 filas
st.subheader("📈 Métricas Principales")

# Primera fila de métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Coste Anuncio",
        value=f"${format_number(coste_anuncio)}",
        help="Inversión total en publicidad"
    )

with col2:
    st.metric(
        label="👁️ Visualizaciones Videos",
        value=format_number(visualizaciones_videos),
        help="Visualizaciones generadas por pauta"
    )

with col3:
    st.metric(
        label="📈 Nuevos Seguidores",
        value=format_number(nuevos_seguidores),
        help="Seguidores ganados por pauta"
    )

# Segunda fila de métricas
col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="👥 Total Seguidores",
        value=format_number(total_seguidores),
        help="Seguidores totales en TikTok"
    )

with col5:
    st.metric(
        label="🎬 Total Contenidos",
        value=format_number(total_contenidos),
        help="Videos publicados en TikTok"
    )

with col6:
    st.metric(
        label="👁️ Visualizaciones Totales",
        value=format_number(total_visualizaciones),
        help="Visualizaciones totales en TikTok"
    )

# Separador
st.markdown("---")

#############################################
# GRÁFICA DE EVOLUCIÓN DE SEGUIDORES
#############################################

st.subheader("📈 Evolución de Seguidores TikTok")

if not fh_df.empty and 'Fecha' in fh_df.columns and 'Seguidores_Totales' in fh_df.columns:
    try:
        # Procesar datos para gráfica
        fh_df["Fecha"] = pd.to_datetime(fh_df["Fecha"], dayfirst=True, errors="coerce")
        fh_df = fh_df.sort_values("Fecha")
        
        # Crear gráfica
        fig_followers = go.Figure()
        
        # Línea de seguidores
        fig_followers.add_trace(go.Scatter(
            x=fh_df['Fecha'],
            y=fh_df['Seguidores_Totales'],
            mode='lines+markers',
            name='👥 Seguidores Totales',
            marker=dict(
                size=8,
                color='#000000',
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            line=dict(color='#000000', width=3),
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores: %{y:,}<extra></extra>'
        ))
        
        # Configurar layout
        fig_followers.update_layout(
            height=500,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),
            hovermode='x unified',
            xaxis=dict(
                title="Fecha",
                gridcolor='#f1f5f9',
                showgrid=True,
                tickformat='%d/%m/%Y'
            ),
            yaxis=dict(
                title="Seguidores",
                gridcolor='#f1f5f9',
                showgrid=True
            )
        )
        
        st.plotly_chart(fig_followers, use_container_width=True)
        
    except Exception as e:
        st.warning(f"No se pudo generar la gráfica: {str(e)}")
else:
    st.info("No hay datos de seguidores disponibles")

# Separador
st.markdown("---")

#############################################
# PESTAÑAS CON NUEVAS GRÁFICAS Y TABLA
#############################################

tab1, tab2, tab3 = st.tabs(["📋 Tabla de Contenidos", "📈 Inversión vs Seguidores", "🗺️ Mapa de Calor CPS"])

# Tab 1: Tabla de contenidos
with tab1:
    st.subheader("📋 Contenidos de TikTok")
    
    if not tiktok_df.empty:
        # Seleccionar columnas relevantes
        display_cols = []
        if 'titulo' in tiktok_df.columns:
            display_cols.append('titulo')
        if 'fecha_publicacion' in tiktok_df.columns:
            display_cols.append('fecha_publicacion')
        if 'visualizaciones' in tiktok_df.columns:
            display_cols.append('visualizaciones')
        if 'me_gusta' in tiktok_df.columns:
            display_cols.append('me_gusta')
        if 'comentarios' in tiktok_df.columns:
            display_cols.append('comentarios')
        
        display_df = tiktok_df[display_cols].copy()
        
        # Formatear fecha
        if 'fecha_publicacion' in display_df.columns:
            display_df['fecha_publicacion'] = pd.to_datetime(display_df['fecha_publicacion'])
            display_df['fecha_publicacion'] = display_df['fecha_publicacion'].dt.strftime('%d/%m/%Y')
        
        # Renombrar columnas
        rename_dict = {
            'titulo': 'Título',
            'fecha_publicacion': 'Fecha',
            'visualizaciones': 'Vistas',
            'me_gusta': 'Likes',
            'comentarios': 'Comentarios'
        }
        display_df = display_df.rename(columns=rename_dict)
        
        # Mostrar tabla
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )
    else:
        st.info("No hay datos de contenidos disponibles")

# Tab 2: Gráfica de inversión vs seguidores
with tab2:
    st.subheader("📈 Análisis de Inversión vs Seguidores")
    
    if not fh_df.empty and not bp_df.empty:
        fig_inversion = generar_grafica_inversion_plotly(fh_df, bp_df)
        if fig_inversion:
            st.plotly_chart(fig_inversion, use_container_width=True)
            
            # Información adicional
            with st.expander("ℹ️ ¿Cómo interpretar esta gráfica?"):
                st.markdown("""
                **Esta gráfica muestra:**
                - **Puntos azules:** Días reales con inversión y seguidores ganados
                - **Línea naranja:** Promedio de seguidores por nivel de inversión
                - **Líneas verticales:** Rangos de inversión cada $15,000
                
                **Interpretación:**
                - **Costo/Seguidor bajo:** Eficiente (más seguidores por dinero)
                - **Puntos altos en la curva:** Niveles óptimos de inversión
                - **Tendencia creciente:** Más inversión genera más seguidores
                """)
        else:
            st.warning("No hay datos suficientes para generar la gráfica de inversión")
    else:
        st.warning("Se necesitan datos de seguidores y pauta para esta gráfica")

# Tab 3: Mapa de calor CPS
with tab3:
    st.subheader("🗺️ Mapa de Calor - Costo por Seguidor (CPS)")
    
    if not fh_df.empty and not bp_df.empty:
        fig_heatmap = generar_mapa_calor_plotly(fh_df, bp_df)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Información adicional
            with st.expander("ℹ️ ¿Cómo interpretar este mapa de calor?"):
                st.markdown("""
                **Este mapa de calor muestra:**
                - **Eje Y:** Días de la semana
                - **Eje X:** Semanas del año (formato AAAA-W##)
                - **Colores:** 
                  - **🟢 Verde:** CPS bajo (eficiente)
                  - **🟡 Amarillo:** CPS medio
                  - **🔴 Rojo:** CPS alto (ineficiente)
                
                **Interpretación:**
                - **CPS bajo = mejor:** Menos costo por cada seguidor ganado
                - **Patrones por día:** Identifica qué días son más eficientes
                - **Evolución semanal:** Ve cómo cambia la eficiencia semana a semana
                """)
        else:
            st.warning("No hay datos suficientes para generar el mapa de calor")
    else:
        st.warning("Se necesitan datos de seguidores y pauta para esta gráfica")

# Footer
st.markdown("---")
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>📊 Dashboard TikTok - Métricas e Inversión • Datos en tiempo real • Actualizado: {current_time}</p>
    <p><small>Conectado a: {BACKEND_URL}</small></p>
</div>
""", unsafe_allow_html=True)
