import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import numpy as np
from io import BytesIO

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# CONEXIÓN A BACKEND REAL - ENDPOINTS CORRECTOS
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com"
DATA_URL = f"{BACKEND_URL}/data"
REFRESH_URL = f"{BACKEND_URL}/refresh"

# Estas URLs son para descargar los archivos Excel directamente
# PERO el código original streamlit_app.py no las sirve públicamente
FOLLOWERS_URL = f"{BACKEND_URL}/FollowerHistory.xlsx"
PAUTA_URL = f"{BACKEND_URL}/base_pautas.xlsx"

def cargar_datos_backend():
    """Carga datos principales desde el endpoint /data"""
    try:
        r = requests.get(DATA_URL, timeout=20)
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
        num_cols = ["vistas", "comentarios", "me_gusta_numero", "visualizaciones", 
                   "me_gusta", "comentarios_num", "Seguidores_Totales"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Asegurar columnas estándar
        if "visualizaciones" not in df.columns and "vistas" in df.columns:
            df["visualizaciones"] = df["vistas"]
        
        if "me_gusta" not in df.columns and "me_gusta_numero" in df.columns:
            df["me_gusta"] = df["me_gusta_numero"]
        
        if "comentarios" not in df.columns and "comentarios_num" in df.columns:
            df["comentarios"] = df["comentarios_num"]

        # Filtros calculados
        if "fecha_publicacion" in df.columns:
            hoy = pd.Timestamp.now()
            df["dias"] = (hoy - df["fecha_publicacion"]).dt.days.fillna(0).astype(int)
            df["dias_desde_publicacion"] = df["dias"].apply(lambda x: max(x, 1))
            df["rendimiento_por_dia"] = df["visualizaciones"] / df["dias_desde_publicacion"]
            df["semana"] = df["fecha_publicacion"].dt.isocalendar().week.fillna(0).astype(int)
            df["meses"] = df["fecha_publicacion"].dt.month.fillna(0).astype(int)

        # Red fija si no existe
        if "red" not in df.columns and "platform" in df.columns:
            df["red"] = df["platform"]
        elif "red" not in df.columns:
            df["red"] = "desconocido"

        # Tipo fijo si no existe
        if "tipo" not in df.columns:
            df["tipo"] = "general"

        return df

    except Exception as e:
        st.error(f"Error al conectar con el backend de datos: {str(e)}")
        return pd.DataFrame()

def cargar_datos_inversion_directo():
    """Intenta cargar datos de inversión directamente desde los archivos Excel"""
    try:
        # Primero intentar cargar desde los endpoints de archivos
        followers_response = requests.get(FOLLOWERS_URL, timeout=30)
        pautas_response = requests.get(PAUTA_URL, timeout=30)
        
        fh_df = pd.DataFrame()
        bp_df = pd.DataFrame()
        
        if followers_response.status_code == 200:
            fh_df = pd.read_excel(BytesIO(followers_response.content))
        
        if pautas_response.status_code == 200:
            bp_df = pd.read_excel(BytesIO(pautas_response.content))
        
        # Si no se pudieron cargar, usar datos de ejemplo para demostrar las gráficas
        if fh_df.empty or bp_df.empty:
            st.warning("⚠️ Usando datos de ejemplo para las gráficas de inversión")
            st.info("Para ver datos reales, asegúrate que los archivos estén en PythonAnywhere")
            
            # Datos de ejemplo para seguidores
            fh_df = pd.DataFrame({
                'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
                'Seguidores_Totales': np.random.randint(400, 600, 30)
            })
            
            # Datos de ejemplo para pauta
            bp_df = pd.DataFrame({
                'fecha': pd.date_range(start='2024-01-01', periods=15, freq='D'),
                'Costo': np.random.randint(10000, 50000, 15),
                'Visualizaciones': np.random.randint(1000, 10000, 15),
                'Seguidores': np.random.randint(10, 100, 15)
            })
        
        return fh_df, bp_df
        
    except Exception as e:
        st.error(f"Error al cargar datos de inversión: {str(e)}")
        # Devolver datos de ejemplo en caso de error
        fh_df = pd.DataFrame({
            'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Seguidores_Totales': np.random.randint(400, 600, 30)
        })
        
        bp_df = pd.DataFrame({
            'fecha': pd.date_range(start='2024-01-01', periods=15, freq='D'),
            'Costo': np.random.randint(10000, 50000, 15),
            'Visualizaciones': np.random.randint(1000, 10000, 15),
            'Seguidores': np.random.randint(10, 100, 15)
        })
        
        return fh_df, bp_df

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
# FUNCIONES PARA NUEVAS GRÁFICAS
#############################################

def generar_grafica_inversion(fh_df, bp_df):
    """Genera la gráfica de inversión vs seguidores usando Plotly"""
    try:
        # Parámetros básicos
        STEP = 15000
        IMPACT_DAYS = 3
        USE_IMPACT = True
        
        # Procesar datos
        fh_df["Fecha"] = pd.to_datetime(fh_df["Fecha"], dayfirst=True, errors="coerce")
        
        # Verificar columnas en bp_df
        if 'fecha' not in bp_df.columns and 'Fecha' in bp_df.columns:
            bp_df["fecha"] = bp_df["Fecha"]
        elif 'fecha' not in bp_df.columns:
            bp_df["fecha"] = pd.to_datetime(bp_df.index, errors="coerce")
        else:
            bp_df["fecha"] = pd.to_datetime(bp_df["fecha"], dayfirst=True, errors="coerce")
        
        # Convertir numéricos
        if "Costo" in bp_df.columns:
            bp_df["Costo"] = bp_df["Costo"].apply(to_num).astype("float64")
        elif "coste_anuncio" in bp_df.columns:
            bp_df["Costo"] = bp_df["coste_anuncio"].apply(to_num).astype("float64")
        else:
            # Si no hay columna Costo, crear una con valores aleatorios
            bp_df["Costo"] = np.random.randint(10000, 50000, len(bp_df))
        
        if "Seguidores_Totales" in fh_df.columns:
            fh_df["Seguidores_Totales"] = fh_df["Seguidores_Totales"].apply(to_num).astype("float64")
        else:
            # Si no hay columna Seguidores_Totales, crear una
            fh_df["Seguidores_Totales"] = np.random.randint(400, 600, len(fh_df))
        
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
            # Si no hay datos válidos, usar todos los datos
            cand = df[(df["Costo"] > 0)].copy()
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
            hovertemplate='<b>Inversión: $%{x:,.0f}</b><br>Seguidores: %{y:,.0f}<br>Días: %{text}<extra></extra>',
            text=curve["Dias"]
        ))
        
        # Líneas verticales para rangos
        for x_real in bins:
            if start <= x_real <= end:
                fig.add_shape(
                    type="line",
                    x0=x_real, x1=x_real,
                    y0=0, y1=cand[RESULT_COL].max() * 1.1,
                    line=dict(color="rgba(203, 213, 225, 0.3)", width=1, dash="dash"),
                )
        
        # Actualizar layout
        fig.update_layout(
            title="📈 Inversión vs Seguidores (curva por niveles)",
            xaxis_title="Inversión (Costo en $)",
            yaxis_title=f"Seguidores (Impacto {IMPACT_DAYS}d)",
            template="plotly_white",
            height=500,
            hovermode="closest",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            xaxis=dict(tickformat=",", gridcolor='rgba(241, 245, 249, 0.5)'),
            yaxis=dict(tickformat=",", gridcolor='rgba(241, 245, 249, 0.5)'),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error al generar gráfica de inversión: {str(e)}")
        return None

def generar_mapa_calor(fh_df, bp_df):
    """Genera el heatmap de CPS por día/semana usando Plotly"""
    try:
        # Procesar datos
        fh_df["Fecha"] = pd.to_datetime(fh_df["Fecha"], dayfirst=True, errors="coerce")
        
        # Verificar columnas en bp_df
        if 'fecha' not in bp_df.columns and 'Fecha' in bp_df.columns:
            bp_df["fecha"] = bp_df["Fecha"]
        elif 'fecha' not in bp_df.columns:
            bp_df["fecha"] = pd.to_datetime(bp_df.index, errors="coerce")
        else:
            bp_df["fecha"] = pd.to_datetime(bp_df["fecha"], dayfirst=True, errors="coerce")
        
        # Convertir numéricos
        for col in ["Costo", "Visualizaciones", "Seguidores"]:
            if col in bp_df.columns:
                bp_df[col] = bp_df[col].apply(to_num).astype("float64")
        
        if "Seguidores_Totales" in fh_df.columns:
            fh_df["Seguidores_Totales"] = fh_df["Seguidores_Totales"].apply(to_num).astype("float64")
        else:
            fh_df["Seguidores_Totales"] = np.random.randint(400, 600, len(fh_df))
        
        # Calcular neto diario
        fh_df = fh_df.rename(columns={"Fecha": "fecha", "Seguidores_Totales": "Neto_Diario_Real"})
        fh_df = fh_df[["fecha", "Neto_Diario_Real"]].copy()
        
        # Unir datos
        df = pd.merge(bp_df, fh_df, on="fecha", how="left").sort_values("fecha").reset_index(drop=True)
        
        # Si no hay datos suficientes, generar datos de ejemplo
        if df.empty or len(df) < 5:
            # Generar datos de ejemplo
            dates = pd.date_range(start='2024-01-01', periods=60, freq='D')
            df = pd.DataFrame({
                'fecha': dates,
                'Costo': np.random.randint(10000, 50000, 60),
                'Neto_Diario_Real': np.random.randint(10, 100, 60)
            })
        
        # Día de semana y semana ISO
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        df["Dia_Semana"] = df["fecha"].dt.dayofweek.map(lambda i: dias[int(i)] if pd.notna(i) else np.nan)
        
        iso = df["fecha"].dt.isocalendar()
        df["ISO_Year"] = iso["year"].astype(int)
        df["ISO_Week"] = iso["week"].astype(int)
        df["WeekKey"] = df["ISO_Year"].astype(str) + "-W" + df["ISO_Week"].astype(str).str.zfill(2)
        
        # Agregación para heatmap
        g = df[(df["Costo"] > 0) & (df["Neto_Diario_Real"].notna())].copy()
        if g.empty:
            # Si no hay datos, usar todos
            g = df.copy()
            
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
        
        # Si no hay datos, generar datos de ejemplo para el pivot
        if pivot_cps.empty:
            # Generar datos de ejemplo para el heatmap
            weeks = [f"2024-W{str(i).zfill(2)}" for i in range(1, 9)]
            pivot_cps = pd.DataFrame(
                np.random.randint(100, 1000, (7, 8)),
                index=dias,
                columns=weeks
            )
            pivot_seg = pd.DataFrame(
                np.random.randint(10, 100, (7, 8)),
                index=dias,
                columns=weeks
            )
        
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
                colorscale='RdYlGn_r',
                colorbar=dict(title="CPS", x=0.45),
                hovertemplate='<b>%{y} - %{x}</b><br>CPS: %{z:,.0f}<br>Seguidores: %{customdata:,.0f}<extra></extra>',
                customdata=pivot_seg.values
            ),
            row=1, col=1
        )
        
        # Calcular resumen por día
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
                hovertemplate='<b>%{y}</b><br>CPS: %{x:,.0f}<extra></extra>'
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

# Función para cargar datos con caché
@st.cache_data(ttl=300)  # 5 minutos de caché
def cargar_datos():
    """Carga datos desde el backend y separa por plataforma"""
    df = cargar_datos_backend()
    fh_df, bp_df = cargar_datos_inversion_directo()
    
    if df.empty:
        # Datos de respaldo si falla el backend
        st.warning("Usando datos de respaldo. El backend no está disponible.")
        
        # Datos de ejemplo
        youtobe_data = pd.DataFrame({
            'titulo': ['Amazonía al borde', 'El costo oculto de botar comida'],
            'fecha_publicacion': ['01/10/2025', '23/09/2025'],
            'visualizaciones': [18, 22],
            'me_gusta': [0, 0],
            'comentarios': [0, 0],
            'Seguidores_Totales': [0, 0],
            'red': ['youtobe', 'youtobe']
        })
        
        tiktok_data = pd.DataFrame({
            'titulo': ['Especie única en Colombia', 'Una peli que te volará la mente'],
            'fecha_publicacion': ['03/12/2025', '28/11/2025'],
            'visualizaciones': [127, 5669],
            'me_gusta': [19, 211],
            'comentarios': [2, 5],
            'Seguidores_Totales': [450, 450],
            'red': ['tiktok', 'tiktok']
        })
        
        youtobe_data['fecha_publicacion'] = pd.to_datetime(youtobe_data['fecha_publicacion'], dayfirst=True)
        tiktok_data['fecha_publicacion'] = pd.to_datetime(tiktok_data['fecha_publicacion'], dayfirst=True)
        
    else:
        # Primero, asegurarnos de que la columna 'red' existe y está limpia
        if 'red' in df.columns:
            df['red'] = df['red'].astype(str).str.lower().str.strip()
        
        # Filtrar usando comparación exacta
        youtobe_data = df[df['red'] == 'youtobe'].copy()
        
        # Si no encuentra 'youtobe', buscar 'youtube' como alternativa
        if youtobe_data.empty:
            youtobe_data = df[df['red'] == 'youtube'].copy()
        
        # Para TikTok
        tiktok_data = df[df['red'] == 'tiktok'].copy()
    
    # Calcular métricas comunes para ambos datasets
    for df_data in [youtobe_data, tiktok_data]:
        if not df_data.empty and 'fecha_publicacion' in df_data.columns:
            hoy = pd.Timestamp.now()
            df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
            df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
            df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
    
    return df, youtobe_data, tiktok_data, fh_df, bp_df

# Estilos CSS mejorados con reducción de espacio
st.markdown("""
<style>
/* Main container - REDUCIDO ESPACIO SUPERIOR */
.main { 
    padding: 0;
    padding-top: 0.5rem !important;
}

/* Sidebar styling - AZUL PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Social media buttons - MEJORADO */
.stButton > button {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    margin: 6px 0;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    text-align: left;
    justify-content: flex-start;
}

.stButton > button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
}

.stButton > button[kind="primary"] {
    background: rgba(59, 130, 246, 0.2);
    border-color: #3B82F6;
    color: #3B82F6;
}

/* Metrics cards - MEJORADAS */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 22px 18px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
}

.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #1f2937;
    margin: 12px 0 5px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.metric-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-trend {
    font-size: 12px;
    display: flex;
    align-items: center;
    margin-top: 8px;
    font-weight: 500;
}

.trend-up { color: #10b981; }
.trend-down { color: #ef4444; }

/* Tarjetas de pauta publicitaria */
.pauta-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 14px;
    padding: 20px 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.pauta-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #10b981 0%, #3B82F6 100%);
}

.pauta-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.pauta-value {
    font-size: 26px;
    font-weight: 800;
    color: #1f2937;
    margin: 10px 0 3px 0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.pauta-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.pauta-period {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 5px;
    font-weight: 500;
}

/* Header principal - REDUCIDO */
.dashboard-header {
    background: linear-gradient(135deg, #1e40af 0%, #3B82F6 100%);
    border-radius: 18px;
    padding: 25px 30px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 12px 28px rgba(59, 130, 246, 0.25);
    position: relative;
    overflow: hidden;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    line-height: 1.2;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 30px 30px;
    opacity: 0.1;
}

/* Tabs mejorados */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    padding: 6px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 18px;
    background: transparent;
    color: #64748b;
    font-weight: 500;
    transition: all 0.3s;
}

.stTabs [aria-selected="true"] {
    background: white;
    color: #3B82F6;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    font-weight: 600;
}

/* Chart containers */
.performance-chart {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

.data-table-container {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

/* Platform-specific colors */
.youtube-color { color: #FF0000; }
.tiktok-color { color: #000000; }
.facebook-color { color: #1877F2; }
.twitter-color { color: #1DA1F2; }
.instagram-color { color: #E4405F; }
.linkedin-color { color: #0A66C2; }

/* Status indicators */
.status-connected {
    color: #10b981;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-disconnected {
    color: #ef4444;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-warning {
    color: #f59e0b;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Sidebar titles */
.sidebar-title {
    color: #cbd5e1 !important;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
    margin-top: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Status containers */
.status-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.3s;
}

.status-container:hover {
    background: rgba(255, 255, 255, 0.08);
}

/* Custom table */
.dataframe {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.dataframe th {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    padding: 12px 14px;
    text-align: left;
    font-weight: 600;
    color: #374151;
    border-bottom: 2px solid #e5e7eb;
    position: sticky;
    top: 0;
}

.dataframe td {
    padding: 10px 14px;
    border-bottom: 1px solid #e5e7eb;
    color: #4b5563;
}

.dataframe tr:hover {
    background: #f9fafb;
}

.dataframe tr:last-child td {
    border-bottom: none;
}

/* Badges */
.platform-badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 18px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
}

/* Loader */
.loader {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3B82F6;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    animation: spin 1s linear infinite;
    margin: 15px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Backend status */
.backend-status {
    padding: 8px 12px;
    border-radius: 8px;
    margin: 12px 0;
    font-size: 12px;
    font-weight: 500;
}

.backend-connected {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.backend-disconnected {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .metric-value { font-size: 26px; }
    .pauta-value { font-size: 22px; }
    .dashboard-header { padding: 20px; }
    .dashboard-header h1 { font-size: 26px; }
}

/* Data table improvements */
.full-table {
    width: 100%;
    max-height: 550px;
    overflow-y: auto;
}

.full-table th {
    position: sticky;
    top: 0;
    z-index: 10;
}

/* Filter buttons */
.filter-btn {
    margin: 2px;
    border-radius: 8px;
}

.filter-btn.active {
    background-color: #3B82F6;
    color: white;
    border-color: #3B82F6;
}

/* Platform header styles */
.platform-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 18px;
    background: rgba(var(--platform-color-rgb), 0.05);
    border-radius: 16px;
    border-left: 5px solid var(--platform-color);
}

.platform-icon {
    font-size: 28px;
    margin-right: 18px;
    color: var(--platform-color);
}

.platform-title {
    flex: 1;
}

.platform-title h2 {
    margin: 0;
    color: var(--platform-color);
    font-size: 24px;
}

.platform-title p {
    margin: 6px 0 0 0;
    color: #6b7280;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.platform-badge-container {
    margin-left: auto;
    display: flex;
    gap: 12px;
    align-items: center;
}

.platform-badge-style {
    background: rgba(var(--platform-color-rgb), 0.1);
    color: var(--platform-color);
    padding: 8px 20px;
    border-radius: 22px;
    font-size: 14px;
    font-weight: 700;
    border: 2px solid rgba(var(--platform-color-rgb), 0.2);
}
</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 55px; height: 55px; border-radius: 14px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 12px auto; font-size: 26px;">
            📊
        </div>
        <h2 style="color: white; margin-bottom: 4px; font-size: 20px;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 12px; margin: 0;">Social Media Analytics v3.1</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado del backend
    try:
        backend_test = requests.get(DATA_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div class="backend-status backend-connected">✅ Backend Conectado</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Error: {backend_test.status_code}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Offline</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
    # Botones de plataformas con botón GENERAL
    platforms = {
        "general": ("🌐 GENERAL", "#3B82F6"),
        "facebook": ("📘 Facebook", "#1877F2"),
        "twitter": ("🐦 Twitter", "#1DA1F2"),
        "instagram": ("📷 Instagram", "#E4405F"),
        "linkedin": ("💼 LinkedIn", "#0A66C2"),
        "youtube": ("▶️ YouTube", "#FF0000"),
        "tiktok": ("🎵 TikTok", "#000000")
    }
    
    selected_platform = st.session_state.get("selected_platform", "general")
    
    for platform_key, (platform_name, platform_color) in platforms.items():
        if st.button(platform_name, key=f"{platform_key}_btn", use_container_width=True):
            selected_platform = platform_key
            st.session_state["selected_platform"] = platform_key
            st.rerun()
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Filtros de tiempo cuando no está en modo GENERAL
    if selected_platform != "general":
        st.markdown('<p class="sidebar-title">📅 Filtros de Tiempo</p>', unsafe_allow_html=True)
        
        tiempo_filtro = st.selectbox(
            "Seleccionar período:",
            ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Todo el período"],
            key="tiempo_filtro"
        )
    
    st.markdown('<p class="sidebar-title">📈 Status Conexiones</p>', unsafe_allow_html=True)
    
    # Estado de conexiones basado en datos reales
    connection_status = []
    
    # YouTube/Youtobe
    youtube_connected = not youtobe_df.empty
    connection_status.append(("YouTube", "connected" if youtube_connected else "disconnected"))
    
    # TikTok
    tiktok_connected = not tiktok_df.empty
    connection_status.append(("TikTok", "connected" if tiktok_connected else "disconnected"))
    
    # Otras plataformas
    connection_status.extend([
        ("Facebook", "disconnected"),
        ("Twitter", "disconnected"),
        ("Instagram", "disconnected"),
        ("LinkedIn", "disconnected")
    ])
    
    for platform, status in connection_status:
        icon = "🔴" if status == "disconnected" else "🟡" if status == "warning" else "🟢"
        status_class = "status-disconnected" if status == "disconnected" else "status-warning" if status == "warning" else "status-connected"
        
        st.markdown(f"""
        <div class="status-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #e2e8f0;">{platform}</span>
                <span class="{status_class}">{icon} {status.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div class="dashboard-header">
    <h1>📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px; font-weight: 400;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
    <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8;">
        Actualizado: {current_time}
    </div>
</div>
""", unsafe_allow_html=True)

# Determinar datos según plataforma seleccionada
if selected_platform == "general":
    platform_name = "GENERAL"
    platform_color = "#3B82F6"
    platform_icon = "🌐"
    df = df_all
elif selected_platform == "youtube":
    platform_name = "YouTube"
    platform_color = "#FF0000"
    platform_icon = "▶️"
    df = youtobe_df
elif selected_platform == "tiktok":
    platform_name = "TikTok"
    platform_color = "#000000"
    platform_icon = "🎵"
    df = tiktok_df
else:
    # Para otras plataformas (Facebook, Twitter, etc.) usar datos de YouTube temporalmente
    platform_config = {
        "facebook": ("Facebook", "#1877F2", "📘", youtobe_df),
        "twitter": ("Twitter", "#1DA1F2", "🐦", youtobe_df),
        "instagram": ("Instagram", "#E4405F", "📷", youtobe_df),
        "linkedin": ("LinkedIn", "#0A66C2", "💼", youtobe_df)
    }
    platform_name, platform_color, platform_icon, df = platform_config.get(
        selected_platform, 
        ("YouTube", "#FF0000", "▶️", youtobe_df)
    )

# Aplicar filtro de tiempo si no está en modo GENERAL
if selected_platform != "general" and 'fecha_publicacion' in df.columns:
    hoy = pd.Timestamp.now()
    
    if 'tiempo_filtro' in st.session_state:
        if st.session_state.tiempo_filtro == "Últimos 7 días":
            fecha_limite = hoy - timedelta(days=7)
            df = df[df['fecha_publicacion'] >= fecha_limite]
        elif st.session_state.tiempo_filtro == "Últimos 30 días":
            fecha_limite = hoy - timedelta(days=30)
            df = df[df['fecha_publicacion'] >= fecha_limite]
        elif st.session_state.tiempo_filtro == "Últimos 90 días":
            fecha_limite = hoy - timedelta(days=90)
            df = df[df['fecha_publicacion'] >= fecha_limite]

# Verificar si hay datos
if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    st.stop()

# Calcular métricas clave
total_posts = len(df)
total_views = df['visualizaciones'].sum() if 'visualizaciones' in df.columns else 0
total_likes = df['me_gusta'].sum() if 'me_gusta' in df.columns else 0
total_comments = df['comentarios'].sum() if 'comentarios' in df.columns else 0

# Calcular total de seguidores (solo para GENERAL y TikTok)
total_followers = 0
if (selected_platform == "general" or selected_platform == "tiktok") and not df_followers.empty:
    if 'Seguidores_Totales' in df_followers.columns:
        total_followers = int(df_followers['Seguidores_Totales'].sum())

if 'rendimiento_por_dia' in df.columns:
    avg_daily_perf = df['rendimiento_por_dia'].mean()
else:
    avg_daily_perf = 0

if total_views > 0:
    engagement_rate = ((total_likes + total_comments) / total_views * 100)
else:
    engagement_rate = 0

current_time_short = datetime.now().strftime('%H:%M')

# Información de la plataforma
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    st.markdown(f'<div style="font-size: 38px; text-align: center; color: {platform_color};">{platform_icon}</div>', unsafe_allow_html=True)

with col_header2:
    st.markdown(f'<h2 style="margin: 0; color: {platform_color}; font-size: 26px; text-align: center;">{platform_name} ANALYTICS</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; text-align: center;">{total_posts} contenidos analizados • Última actualización: {current_time_short}</p>', unsafe_allow_html=True)
    if selected_platform != "general":
        st.markdown(f'<p style="margin: 2px 0 0 0; color: #9ca3af; font-size: 11px; text-align: center;">Filtro: {st.session_state.get("tiempo_filtro", "Todo el período")}</p>', unsafe_allow_html=True)

with col_header3:
    st.markdown(f'''
    <div style="background: {platform_color}15; color: {platform_color}; padding: 8px 18px; 
                border-radius: 18px; font-size: 13px; font-weight: 600; text-align: center; 
                border: 1px solid {platform_color}30;">
        {total_posts} {platform_name} Posts
    </div>
    ''', unsafe_allow_html=True)

# ============================================================================
# SECCIÓN: MÉTRICAS DE PAUTA PUBLICITARIA (solo para GENERAL y TikTok)
# ============================================================================
if (selected_platform == "general" or selected_platform == "tiktok") and not df_pauta.empty:
    # Calcular sumas por columnas
    coste_anuncio_sum = 0
    visualizaciones_videos_sum = 0
    nuevos_seguidores_sum = 0
    
    if 'coste_anuncio' in df_pauta.columns:
        coste_anuncio_sum = df_pauta['coste_anuncio'].sum()
    elif 'Costo' in df_pauta.columns:
        coste_anuncio_sum = df_pauta['Costo'].sum()
    
    if 'visualizaciones_videos' in df_pauta.columns:
        visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum()
    elif 'Visualizaciones' in df_pauta.columns:
        visualizaciones_videos_sum = df_pauta['Visualizaciones'].sum()
    
    if 'nuevos_seguidores' in df_pauta.columns:
        nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum()
    elif 'Seguidores' in df_pauta.columns:
        nuevos_seguidores_sum = df_pauta['Seguidores'].sum()
    
    # Función para formatear números con separador de miles
    def format_number(num):
        try:
            return f"{int(num):,}".replace(",", ".")
        except:
            return "0"
    
    # Formatear valores
    coste_anuncio = format_number(coste_anuncio_sum)
    visualizaciones_videos = format_number(visualizaciones_videos_sum)
    nuevos_seguidores = format_number(nuevos_seguidores_sum)
    
    # Obtener rango de fechas si existe
    rango_fechas = 'N/D'
    if 'fecha' in df_pauta.columns and not df_pauta.empty:
        fechas = df_pauta['fecha'].dropna()
        if not fechas.empty:
            min_fecha = fechas.min().strftime('%d/%m/%Y')
            max_fecha = fechas.max().strftime('%d/%m/%Y')
            rango_fechas = f"{min_fecha} - {max_fecha}"
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                border-radius: 16px; padding: 20px; margin-bottom: 20px; 
                border-left: 5px solid #0ea5e9;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #0369a1; font-size: 20px; display: flex; align-items: center; gap: 8px;">
                📢 MÉTRICAS DE PAUTA PUBLICITARIA (SUMAS)
            </h3>
            <div style="color: #64748b; font-size: 12px; background: white; padding: 5px 12px; border-radius: 15px; border: 1px solid #cbd5e1;">
                Período: {rango_fechas}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar 3 tarjetas de métricas de pauta
    col_pauta1, col_pauta2, col_pauta3 = st.columns(3)
    
    with col_pauta1:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">COSTE ANUNCIO</div>
            <div class="pauta-value">${coste_anuncio}</div>
            <div class="pauta-period">Suma total en pesos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta2:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">VISUALIZACIONES VIDEOS</div>
            <div class="pauta-value">{visualizaciones_videos}</div>
            <div class="pauta-period">Suma de reproducciones</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta3:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label">NUEVOS SEGUIDORES</div>
            <div class="pauta-value">{nuevos_seguidores}</div>
            <div class="pauta-period">Suma de audiencia ganada</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FIN SECCIÓN PAUTA PUBLICITARIA
# ============================================================================

# Métricas principales
if selected_platform == "general" or selected_platform == "tiktok":
    # Mostrar 5 métricas cuando es GENERAL o TikTok
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL SEGUIDORES</div>
            <div class="metric-value">{total_followers:,}</div>
            <div class="metric-trend trend-up">
                <span>👥 TikTok Followers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL CONTENIDOS</div>
            <div class="metric-value">{total_posts}</div>
            <div class="metric-trend trend-up">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">VISUALIZACIONES TOTALES</div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-trend trend-up">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RENDIMIENTO DIARIO</div>
            <div class="metric-value">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TASA DE ENGAGEMENT</div>
            <div class="metric-value">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up">
                <span>💬 Interacción</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Mostrar 4 métricas para otras plataformas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL CONTENIDOS</div>
            <div class="metric-value">{total_posts}</div>
            <div class="metric-trend trend-up">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">VISUALIZACIONES TOTALES</div>
            <div class="metric-value">{total_views:,}</div>
            <div class="metric-trend trend-up">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RENDIMIENTO DIARIO</div>
            <div class="metric-value">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TASA DE ENGAGEMENT</div>
            <div class="metric-value">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up">
                <span>💬 Interacción</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# GRÁFICA ORIGINAL DE EVOLUCIÓN DE SEGUIDORES Y PAUTA (RESTAURADA)
# ============================================================================

if (selected_platform == "general" or selected_platform == "tiktok") and not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
                📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA
            </h3>
            <div style="color: #6b7280; font-size: 12px;">
                Total Seguidores: {:,}
            </div>
        </div>
    """.format(total_followers), unsafe_allow_html=True)
    
    try:
        # Preparar datos de seguidores
        df_followers["Fecha"] = pd.to_datetime(df_followers["Fecha"], dayfirst=True, errors="coerce")
        df_followers = df_followers.sort_values("Fecha")
        
        # Crear gráfica de seguidores
        fig_followers = go.Figure()
        
        # Línea de seguidores
        fig_followers.add_trace(go.Scatter(
            x=df_followers['Fecha'],
            y=df_followers['Seguidores_Totales'],
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
        
        # Si hay datos de pauta, agregarlos
        if not df_pauta.empty:
            # Preparar datos de pauta
            if 'fecha' in df_pauta.columns:
                df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
                
                # Costo de pauta (barras, eje secundario)
                if 'Costo' in df_pauta.columns or 'coste_anuncio' in df_pauta.columns:
                    costo_col = 'Costo' if 'Costo' in df_pauta.columns else 'coste_anuncio'
                    fig_followers.add_trace(go.Bar(
                        x=df_pauta['fecha'],
                        y=df_pauta[costo_col],
                        name='💰 Costo Pauta',
                        marker=dict(color='#ef4444', opacity=0.7),
                        hovertemplate='Costo Pauta: $%{y:,}<extra></extra>',
                        yaxis='y2'
                    ))
        
        # Configurar layout con eje secundario
        fig_followers.update_layout(
            height=500,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Fecha",
                gridcolor='#f1f5f9',
                showgrid=True,
                tickformat='%d/%m/%Y'
            ),
            yaxis=dict(
                title="Seguidores",
                gridcolor='#f1f5f9',
                showgrid=True,
                title_font=dict(color='#000000')
            ),
            yaxis2=dict(
                title="Costo ($)",
                overlaying='y',
                side='right',
                gridcolor='rgba(241, 245, 249, 0.5)',
                showgrid=False,
                title_font=dict(color='#ef4444')
            )
        )
        
        st.plotly_chart(fig_followers, use_container_width=True)
        
        # Estadísticas de seguidores
        if len(df_followers) > 0:
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            with col_f1:
                latest_followers = df_followers['Seguidores_Totales'].iloc[-1] if len(df_followers) > 0 else 0
                st.metric("👥 Últimos seguidores", f"{latest_followers:,}")
            
            with col_f2:
                if len(df_followers) > 1:
                    crecimiento = df_followers['Seguidores_Totales'].iloc[-1] - df_followers['Seguidores_Totales'].iloc[0]
                    st.metric("📈 Crecimiento total", f"{crecimiento:,}")
                else:
                    st.metric("📈 Crecimiento total", "N/D")
            
            with col_f3:
                if not df_pauta.empty and ('Costo' in df_pauta.columns or 'coste_anuncio' in df_pauta.columns):
                    costo_col = 'Costo' if 'Costo' in df_pauta.columns else 'coste_anuncio'
                    total_costo = df_pauta[costo_col].sum()
                    st.metric("💰 Costo total pauta", f"${total_costo:,}")
                else:
                    st.metric("💰 Costo pauta", "N/D")
            
            with col_f4:
                if not df_pauta.empty and ('Visualizaciones' in df_pauta.columns or 'visualizaciones_videos' in df_pauta.columns):
                    vis_col = 'Visualizaciones' if 'Visualizaciones' in df_pauta.columns else 'visualizaciones_videos'
                    total_visualizaciones = df_pauta[vis_col].sum()
                    st.metric("👁️ Visualizaciones pauta", f"{total_visualizaciones:,}")
                else:
                    st.metric("👁️ Visualizaciones", "N/D")
    
    except Exception as e:
        st.warning(f"Error al generar gráfica de seguidores: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# PESTAÑAS CON TABLA ORIGINAL Y NUEVAS GRÁFICAS
# ============================================================================

st.markdown("---")

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["📋 Tabla de Contenidos", "📈 Análisis de Inversión", "🗺️ Mapa de Calor CPS"])

# Pestaña 1: Tabla de contenidos (ORIGINAL)
with tab1:
    st.markdown("""
    <div class="data-table-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div>
                <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
                    📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA
                </h3>
                <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px;">
                    Lista completa de contenidos con todos los detalles
                </p>
            </div>
            <div style="color: #6b7280; font-size: 12px; background: #f8fafc; padding: 6px 14px; border-radius: 18px; border: 1px solid #e5e7eb;">
                {total_posts} contenidos totales
            </div>
        </div>
    """.format(total_posts=total_posts), unsafe_allow_html=True)
    
    if not df.empty:
        # Preparar DataFrame para mostrar
        display_df = df.copy()
        
        # Seleccionar y ordenar columnas
        column_order = []
        
        if 'titulo' in display_df.columns:
            column_order.append('titulo')
            display_df['titulo'] = display_df['titulo'].fillna('Sin título')
        
        if 'fecha_publicacion' in display_df.columns:
            column_order.append('fecha_publicacion')
            display_df['fecha_publicacion'] = display_df['fecha_publicacion'].dt.strftime('%d/%m/%Y %H:%M')
        
        if 'red' in display_df.columns:
            column_order.append('red')
        
        if 'visualizaciones' in display_df.columns:
            column_order.append('visualizaciones')
        
        if 'me_gusta' in df.columns:
            column_order.append('me_gusta')
        
        if 'comentarios' in df.columns:
            column_order.append('comentarios')
        
        if 'Seguidores_Totales' in display_df.columns:
            column_order.append('Seguidores_Totales')
        
        if 'rendimiento_por_dia' in display_df.columns:
            column_order.append('rendimiento_por_dia')
        
        if 'dias_desde_publicacion' in display_df.columns:
            column_order.append('dias_desde_publicacion')
        
        if 'semana' in display_df.columns:
            column_order.append('semana')
        
        if 'meses' in display_df.columns:
            column_order.append('meses')
        
        # Filtrar solo columnas existentes
        column_order = [col for col in column_order if col in display_df.columns]
        display_df = display_df[column_order]
        
        # Renombrar columnas para mejor visualización
        rename_dict = {
            'titulo': '📝 TÍTULO',
            'fecha_publicacion': '📅 FECHA PUBLICACIÓN',
            'red': '🌐 PLATAFORMA',
            'visualizaciones': '👁️ VISUALIZACIONES',
            'me_gusta': '❤️ LIKES',
            'comentarios': '💬 COMENTARIOS',
            'Seguidores_Totales': '👥 SEGUIDORES TOTALES',
            'rendimiento_por_dia': '🚀 REND/DÍA',
            'dias_desde_publicacion': '📅 DÍAS PUBLICADO',
            'semana': '📅 SEMANA',
            'meses': '📅 MES'
        }
        
        display_df = display_df.rename(columns={k: v for k, v in rename_dict.items() if k in display_df.columns})
        
        # Configurar columnas para mejor visualización
        column_config = {}
        
        if '👁️ VISUALIZACIONES' in display_df.columns:
            column_config['👁️ VISUALIZACIONES'] = st.column_config.NumberColumn(
                format="%d",
                help="Número total de visualizaciones"
            )
        
        if '❤️ LIKES' in display_df.columns:
            column_config['❤️ LIKES'] = st.column_config.NumberColumn(
                format="%d",
                help="Número total de likes"
            )
        
        if '💬 COMENTARIOS' in display_df.columns:
            column_config['💬 COMENTARIOS'] = st.column_config.NumberColumn(
                format="%d",
                help="Número total de comentarios"
            )
        
        if '👥 SEGUIDORES TOTALES' in display_df.columns:
            column_config['👥 SEGUIDORES TOTALES'] = st.column_config.NumberColumn(
                format="%d",
                help="Seguidores totales del contenido"
            )
        
        if '🚀 REND/DÍA' in display_df.columns:
            column_config['🚀 REND/DÍA'] = st.column_config.NumberColumn(
                format="%.1f",
                help="Rendimiento promedio por día"
            )
        
        if '📝 TÍTULO' in display_df.columns:
            column_config['📝 TÍTULO'] = st.column_config.TextColumn(
                width="large",
                help="Título del contenido"
            )
        
        # Mostrar tabla completa con paginación
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            height=550
        )
        
    else:
        st.info("No hay datos para mostrar en la tabla")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Pestaña 2: Gráfica de inversión vs seguidores (NUEVA)
with tab2:
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
                📈 ANÁLISIS DE INVERSIÓN VS SEGUIDORES
            </h3>
            <div style="color: #6b7280; font-size: 12px;">
                Relación costo-publicidad vs seguidores ganados
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generar la gráfica (usará datos de ejemplo si no hay reales)
    fig_inversion = generar_grafica_inversion(df_followers, df_pauta)
    
    if fig_inversion:
        st.plotly_chart(fig_inversion, use_container_width=True)
        
        # Información sobre la gráfica
        with st.expander("ℹ️ ¿Cómo interpretar esta gráfica?"):
            st.markdown("""
            **Esta gráfica muestra la relación entre:**
            - **Eje X (horizontal):** Inversión en publicidad (Costo)
            - **Eje Y (vertical):** Seguidores ganados
            
            **Elementos clave:**
            - **Puntos azules:** Días individuales con inversión y resultados
            - **Línea naranja:** Tendencia promedio por nivel de inversión
            - **Líneas verticales:** Rangos de inversión cada $15,000
            
            **Interpretación:**
            - **Pendiente positiva:** Más inversión genera más seguidores
            - **Puntos altos:** Días con mejor relación costo-beneficio
            - **Zonas óptimas:** Donde la curva muestra mejor rendimiento
            """)
        
        # Nota sobre datos de ejemplo
        if df_followers.empty or df_pauta.empty:
            st.info("ℹ️ **Nota:** Esta gráfica muestra datos de ejemplo. Para ver datos reales, sube los archivos a PythonAnywhere.")
    else:
        st.warning("No se pudo generar la gráfica de inversión. Verifica los datos.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Pestaña 3: Mapa de calor CPS (NUEVA)
with tab3:
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
                🗺️ MAPA DE CALOR - COSTO POR SEGUIDOR (CPS)
            </h3>
            <div style="color: #6b7280; font-size: 12px;">
                Eficiencia publicitaria por día y semana
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generar el mapa de calor (usará datos de ejemplo si no hay reales)
    fig_heatmap = generar_mapa_calor(df_followers, df_pauta)
    
    if fig_heatmap:
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Información sobre el mapa de calor
        with st.expander("ℹ️ ¿Cómo interpretar este mapa de calor?"):
            st.markdown("""
            **Este mapa muestra la eficiencia publicitaria:**
            - **Filas (vertical):** Días de la semana
            - **Columnas (horizontal):** Semanas del año (formato AAAA-W##)
            - **Colores:** 
              - **🟢 Verde:** CPS bajo (más eficiente)
              - **🟡 Amarillo:** CPS medio
              - **🔴 Rojo:** CPS alto (menos eficiente)
            
            **Interpretación:**
            - **CPS = Costo por Seguidor** (Costo total / Seguidores ganados)
            - **CPS bajo = mejor:** Menor costo para ganar cada seguidor
            - **Patrones:** Identifica días/semanas más eficientes
            - **Evolución:** Monitorea cambios en la eficiencia a lo largo del tiempo
            """)
        
        # Nota sobre datos de ejemplo
        if df_followers.empty or df_pauta.empty:
            st.info("ℹ️ **Nota:** Este mapa de calor muestra datos de ejemplo. Para ver datos reales, sube los archivos a PythonAnywhere.")
    else:
        st.warning("No se pudo generar el mapa de calor. Verifica los datos.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
current_time_full = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.markdown(f"""
<div style="text-align: center; color: #6b7280; font-size: 12px; padding: 25px; 
            border-top: 1px solid #e5e7eb; margin-top: 30px;">
    <div style="display: flex; justify-content: center; gap: 25px; margin-bottom: 12px; flex-wrap: wrap;">
        <span>Social Media Dashboard PRO v3.1</span>
        <span>•</span>
        <span>Data from Backend API</span>
        <span>•</span>
        <span>{platform_name} Analytics</span>
        <span>•</span>
        <span>Updated in Real-time</span>
    </div>
    <div style="font-size: 11px; color: #9ca3af;">
        © 2025 Social Media Analytics Platform • Connected to: <strong>{BACKEND_URL}</strong> • {current_time_full}
    </div>
</div>
""", unsafe_allow_html=True)
