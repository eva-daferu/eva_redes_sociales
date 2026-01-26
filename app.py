import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import numpy as np
import io

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# CONEXIÓN A BACKEND REAL
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/followers"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/pauta_anuncio"

def cargar_datos_backend():
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

def cargar_datos_seguidores():
    """Carga datos de seguidores desde el endpoint específico"""
    try:
        r = requests.get(FOLLOWERS_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Convertir a DataFrame
        df_followers = pd.DataFrame(data.get("data", []))
        
        # Procesar datos
        if "Fecha" in df_followers.columns:
            df_followers["Fecha"] = pd.to_datetime(
                df_followers["Fecha"],
                dayfirst=True,
                errors="coerce"
            )
        
        # Convertir números
        if "Seguidores_Totales" in df_followers.columns:
            df_followers["Seguidores_Totales"] = pd.to_numeric(df_followers["Seguidores_Totales"], errors="coerce")
        
        return df_followers
        
    except Exception as e:
        st.error(f"Error al conectar con el backend de seguidores: {str(e)}")
        return pd.DataFrame()

def cargar_datos_pauta():
    """Carga datos de pauta publicitaria"""
    try:
        r = requests.get(PAUTA_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Convertir a DataFrame
        df_pauta = pd.DataFrame(data.get("data", []))
        
        # Procesar datos si existen
        if not df_pauta.empty:
            # Asegurar nombres de columnas
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores'] = df_pauta['Seguidores']
            
            # Formatear coste anuncio (sin decimales)
            if "coste_anuncio" in df_pauta.columns:
                df_pauta["coste_anuncio"] = pd.to_numeric(df_pauta["coste_anuncio"], errors="coerce").fillna(0).astype(int)
            
            # Formatear otras columnas
            for col in ["visualizaciones_videos", "nuevos_seguidores"]:
                if col in df_pauta.columns:
                    df_pauta[col] = pd.to_numeric(df_pauta[col], errors="coerce").fillna(0).astype(int)
            
            # Procesar fecha - FORMATO CORRECTO PARA CRUCE
            if "fecha" in df_pauta.columns:
                # Intentar múltiples formatos de fecha
                df_pauta["fecha"] = pd.to_datetime(
                    df_pauta["fecha"], 
                    errors='coerce',
                    dayfirst=True  # Asumir día primero
                )
        
        return df_pauta
        
    except Exception as e:
        return pd.DataFrame()

#############################################
# FUNCIONES PARA LAS NUEVAS GRÁFICAS (CORREGIDAS)
#############################################

def procesar_datos_graficas():
    """Procesa datos directamente desde los archivos Excel"""
    try:
        # Descargar archivos Excel directamente
        fh_response = requests.get("https://pahubisas.pythonanywhere.com/FollowerHistory.xlsx")
        bp_response = requests.get("https://pahubisas.pythonanywhere.com/base_pautas.xlsx")
        
        if fh_response.status_code != 200 or bp_response.status_code != 200:
            return None, None, None
        
        # Leer los archivos Excel
        fh = pd.read_excel(io.BytesIO(fh_response.content))
        bp = pd.read_excel(io.BytesIO(bp_response.content))
        
        # Función para convertir a número
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
                    s = s.replace(".", "").replace(",", ".")
            try:
                return float(s)
            except Exception:
                return np.nan
        
        # Procesar fechas
        fh["Fecha"] = pd.to_datetime(fh["Fecha"], dayfirst=True, errors="coerce")
        bp["fecha"] = pd.to_datetime(bp["fecha"], dayfirst=True, errors="coerce")
        
        # Convertir columnas numéricas
        for col in ["Costo", "Visualizaciones", "Seguidores"]:
            if col in bp.columns:
                bp[col] = bp[col].apply(to_num).astype("float64")
        
        fh["Seguidores_Totales"] = fh["Seguidores_Totales"].apply(to_num).astype("float64")
        
        # Renombrar y unir
        fh = fh.rename(columns={"Fecha": "fecha", "Seguidores_Totales": "Neto_Diario_Real"})
        fh = fh[["fecha", "Neto_Diario_Real"]].copy()
        
        # Unir los datos
        df = pd.merge(bp, fh, on="fecha", how="left").sort_values("fecha").reset_index(drop=True)
        
        return df, fh, bp
        
    except Exception as e:
        st.error(f"Error procesando datos para gráficas: {str(e)}")
        return None, None, None

def crear_grafica_inversion_vs_seguidores(df, platform_name):
    """Crea la gráfica de inversión vs seguidores IDÉNTICA a grafica.txt"""
    try:
        if df is None or df.empty:
            return None
        
        # Filtrar datos válidos
        df_valid = df[(df["Costo"] > 0) & (df["Neto_Diario_Real"].notna())].copy()
        
        if df_valid.empty:
            return None
        
        # Crear rangos de inversión (igual que en grafica.txt)
        STEP = 15000
        cmin = float(df_valid["Costo"].min())
        cmax = float(df_valid["Costo"].max())
        start = float(np.floor(cmin / STEP) * STEP)
        end = float(np.ceil(cmax / STEP) * STEP) + STEP
        bins = np.arange(start, end + 1, STEP)
        
        df_valid["Costo_bin"] = pd.cut(df_valid["Costo"], bins=bins, include_lowest=True, right=False)
        
        # Calcular promedios por rango
        curve = df_valid.groupby("Costo_bin", observed=True).agg(
            Inversion_promedio=("Costo", "mean"),
            Seguidores_promedio=("Neto_Diario_Real", "mean"),
            Dias=("Costo", "count"),
        ).reset_index(drop=True).sort_values("Inversion_promedio").reset_index(drop=True)
        
        # Calcular CPS
        curve["CPS_curva"] = np.nan
        mc = (curve["Inversion_promedio"] > 0) & (curve["Seguidores_promedio"] > 0)
        curve.loc[mc, "CPS_curva"] = (curve.loc[mc, "Inversion_promedio"] / curve.loc[mc, "Seguidores_promedio"]).astype("float64")
        
        # Encontrar punto óptimo (simplificado)
        if not curve.empty:
            opt_row = curve.loc[curve['Seguidores_promedio'].idxmax()]
            opt_x = float(opt_row["Inversion_promedio"])
            opt_y = float(opt_row["Seguidores_promedio"])
            opt_cps = float(opt_row["CPS_curva"]) if not pd.isna(opt_row["CPS_curva"]) else 0
        else:
            opt_x, opt_y, opt_cps = 0, 0, 0
        
        # Crear gráfica
        fig = go.Figure()
        
        # 1. Puntos reales (días individuales)
        fig.add_trace(go.Scatter(
            x=df_valid["Costo"],
            y=df_valid["Neto_Diario_Real"],
            mode='markers',
            name='Días reales',
            marker=dict(
                size=8,
                color='#60a5fa',
                opacity=0.3,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Costo: $%{x:,.0f}</b><br>Seguidores: %{y:,.0f}<extra></extra>'
        ))
        
        # 2. Línea de la curva (promedios por rango)
        fig.add_trace(go.Scatter(
            x=curve["Inversion_promedio"],
            y=curve["Seguidores_promedio"],
            mode='lines+markers',
            name='Curva promedio',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=10, color='#f59e0b', symbol='circle'),
            hovertemplate='<b>Inversión: $%{x:,.0f}</b><br>Seguidores: %{y:,.0f}<br>Días: %{customdata[0]}<extra></extra>',
            customdata=curve[['Dias']].values
        ))
        
        # 3. Punto óptimo
        if opt_x > 0 and opt_y > 0:
            fig.add_trace(go.Scatter(
                x=[opt_x],
                y=[opt_y],
                mode='markers',
                name='Punto óptimo',
                marker=dict(
                    size=20,
                    color='#22c55e',
                    symbol='star',
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>ÓPTIMO</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata[0]:,.0f}<extra></extra>',
                customdata=[[opt_cps]]
            ))
        
        # 4. Líneas de promedio general
        mean_inv = df_valid["Costo"].mean()
        mean_seg = df_valid["Neto_Diario_Real"].mean()
        
        fig.add_trace(go.Scatter(
            x=[mean_inv, mean_inv],
            y=[0, mean_seg],
            mode='lines',
            name='Promedio inversión',
            line=dict(color='#22d3ee', width=2, dash='dot'),
            showlegend=False,
            hovertemplate='Promedio inversión: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, mean_inv],
            y=[mean_seg, mean_seg],
            mode='lines',
            name='Promedio seguidores',
            line=dict(color='#22d3ee', width=2, dash='dot'),
            showlegend=False,
            hovertemplate='Promedio seguidores: %{y:,.0f}<extra></extra>'
        ))
        
        # Configurar layout
        fig.update_layout(
            title=f'📈 {platform_name} - Análisis de Inversión vs Seguidores',
            height=600,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='closest',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title="Inversión ($)",
                tickformat="$,.0f",
                gridcolor='#f1f5f9',
                showgrid=True,
                zeroline=False
            ),
            yaxis=dict(
                title="Seguidores Netos",
                gridcolor='#f1f5f9',
                showgrid=True,
                zeroline=False
            ),
            annotations=[
                dict(
                    x=mean_inv,
                    y=mean_seg,
                    xref="x",
                    yref="y",
                    text="Promedio",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40,
                    bgcolor="white",
                    bordercolor="#22d3ee",
                    borderwidth=1,
                    borderpad=4
                )
            ] if mean_inv > 0 and mean_seg > 0 else []
        )
        
        # Agregar etiquetas a los puntos de la curva
        for i, row in curve.iterrows():
            if not pd.isna(row["Inversion_promedio"]) and not pd.isna(row["Seguidores_promedio"]):
                fig.add_annotation(
                    x=row["Inversion_promedio"],
                    y=row["Seguidores_promedio"],
                    text=f"{row['Dias']} días",
                    showarrow=True,
                    arrowhead=1,
                    arrowsize=1,
                    arrowwidth=1,
                    arrowcolor="#f59e0b",
                    ax=0,
                    ay=-20,
                    bgcolor="white",
                    bordercolor="#f59e0b",
                    borderwidth=1,
                    borderpad=4,
                    font=dict(size=10)
                )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creando gráfica de inversión: {str(e)}")
        return None

def crear_heatmap_cps(df, platform_name):
    """Crea el heatmap de CPS IDÉNTICO a grafica2.txt"""
    try:
        if df is None or df.empty:
            return None
        
        # Filtrar datos válidos
        df_valid = df[(df["Costo"] > 0) & (df["Neto_Diario_Real"].notna())].copy()
        
        if df_valid.empty:
            return None
        
        # Preparar datos para heatmap
        df_heat = df_valid.copy()
        
        # Calcular CPS
        df_heat["CPS"] = df_heat["Costo"] / df_heat["Neto_Diario_Real"]
        
        # Extraer día de semana y semana ISO
        df_heat["Dia_Semana"] = df_heat["fecha"].dt.day_name()
        df_heat["ISO_Year"] = df_heat["fecha"].dt.isocalendar().year
        df_heat["ISO_Week"] = df_heat["fecha"].dt.isocalendar().week
        
        # Mapear días al español
        dias_map = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        df_heat["Dia_Semana"] = df_heat["Dia_Semana"].map(dias_map)
        
        # Crear clave de semana
        df_heat["WeekKey"] = df_heat["ISO_Year"].astype(str) + "-W" + df_heat["ISO_Week"].astype(str).str.zfill(2)
        
        # Calcular seguidores positivos (solo positivos para CPS)
        df_heat["Seg_pos"] = np.where(df_heat["Neto_Diario_Real"] > 0, df_heat["Neto_Diario_Real"], 0.0)
        
        # Agregar por día y semana
        agg = df_heat.groupby(["Dia_Semana", "WeekKey"], as_index=False).agg(
            Costo_sum=("Costo", "sum"),
            Seguidores_sum=("Neto_Diario_Real", "sum"),
            Seguidores_pos_sum=("Seg_pos", "sum")
        )
        
        # Calcular CPS por celda
        agg["CPS_cell"] = np.where(
            agg["Seguidores_pos_sum"] > 0,
            agg["Costo_sum"] / agg["Seguidores_pos_sum"],
            np.nan
        )
        
        # Crear pivot table
        pivot_cps = agg.pivot(index="Dia_Semana", columns="WeekKey", values="CPS_cell")
        pivot_seg = agg.pivot(index="Dia_Semana", columns="WeekKey", values="Seguidores_sum")
        
        # Ordenar días de semana
        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        pivot_cps = pivot_cps.reindex(dias_orden)
        pivot_seg = pivot_seg.reindex(dias_orden)
        
        # Obtener valores
        vals_cps = pivot_cps.values.astype(float)
        vals_seg = pivot_seg.values.astype(float)
        
        # Normalizar color (recorte p5–p95 como en grafica2.txt)
        flat = vals_cps[np.isfinite(vals_cps)]
        if flat.size > 0:
            p5 = np.nanpercentile(flat, 5)
            p95 = np.nanpercentile(flat, 95)
            vals_cps_clip = np.clip(vals_cps, p5, p95)
        else:
            vals_cps_clip = vals_cps
        
        # Función para formatear números
        def fmt_int_or_dash(x):
            if x is None or (isinstance(x, float) and np.isnan(x)):
                return "—"
            try:
                return f"{int(round(float(x))):,}".replace(",", ".")
            except Exception:
                return "—"
        
        # Crear texto para cada celda
        text_matrix = []
        for i in range(len(dias_orden)):
            row_texts = []
            for j in range(len(pivot_cps.columns)):
                cps_v = vals_cps[i, j] if i < vals_cps.shape[0] and j < vals_cps.shape[1] else np.nan
                seg_v = vals_seg[i, j] if i < vals_seg.shape[0] and j < vals_seg.shape[1] else np.nan
                if np.isfinite(cps_v) or np.isfinite(seg_v):
                    line1 = f"CPS {fmt_int_or_dash(cps_v)}"
                    line2 = f"Seg {fmt_int_or_dash(seg_v)}"
                    row_texts.append(f"{line1}<br>{line2}")
                else:
                    row_texts.append("")
            text_matrix.append(row_texts)
        
        # Crear heatmap
        fig = go.Figure(data=go.Heatmap(
            z=vals_cps_clip,
            x=pivot_cps.columns,
            y=pivot_cps.index,
            text=text_matrix,
            texttemplate="%{text}",
            textfont={"size": 10},
            colorscale='Viridis',
            colorbar=dict(title="CPS ($)", titleside="right"),
            hovertemplate='<b>Día: %{y}</b><br>Semana: %{x}<br>CPS: $%{z:.0f}<extra></extra>',
            showscale=True
        ))
        
        # Layout
        fig.update_layout(
            title=f'🔥 {platform_name} - Heatmap CPS (Costo por Seguidor)',
            height=600,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                title="Semana (ISO)",
                tickangle=45,
                tickmode='array',
                tickvals=list(range(len(pivot_cps.columns))),
                ticktext=pivot_cps.columns,
                gridcolor='#f1f5f9',
                showgrid=True
            ),
            yaxis=dict(
                title="Día de la Semana",
                gridcolor='#f1f5f9',
                showgrid=True
            ),
            annotations=[
                dict(
                    x=0.5,
                    y=1.08,
                    xref="paper",
                    yref="paper",
                    text="CPS bajo = mejor | Negro = sin inversión o sin seguidores positivos",
                    showarrow=False,
                    font=dict(size=12, color="#666")
                )
            ]
        )
        
        # Agregar grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        # Calcular resumen por día (barra derecha como en grafica2.txt)
        sum_day = df_heat.groupby("Dia_Semana", as_index=False).agg(
            Costo_sum=("Costo", "sum"),
            Seguidores_sum=("Neto_Diario_Real", "sum"),
            Seguidores_pos_sum=("Seg_pos", "sum")
        )
        
        sum_day["CPS_total_dia"] = np.where(
            sum_day["Seguidores_pos_sum"] > 0,
            sum_day["Costo_sum"] / sum_day["Seguidores_pos_sum"],
            np.nan
        )
        
        sum_day = sum_day.set_index("Dia_Semana").reindex(dias_orden).reset_index()
        
        # Crear gráfica de barras para resumen por día
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            x=sum_day["CPS_total_dia"],
            y=sum_day["Dia_Semana"],
            orientation='h',
            marker_color='#3B82F6',
            opacity=0.7,
            hovertemplate='<b>%{y}</b><br>CPS: $%{x:,.0f}<br>Seguidores: %{customdata[0]:,.0f}<extra></extra>',
            customdata=sum_day[['Seguidores_sum']].values
        ))
        
        fig2.update_layout(
            title=f'📊 {platform_name} - Resumen por Día',
            height=600,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title="CPS total por día"),
            yaxis=dict(title="Día de la Semana")
        )
        
        return fig, fig2
        
    except Exception as e:
        st.error(f"Error creando heatmap CPS: {str(e)}")
        return None, None

#############################################
# FIN FUNCIONES GRÁFICAS
#############################################

# Función para cargar datos con caché
@st.cache_data(ttl=300)  # 5 minutos de caché
def cargar_datos():
    """Carga datos desde el backend y separa por plataforma"""
    df = cargar_datos_backend()
    df_followers = cargar_datos_seguidores()
    df_pauta = cargar_datos_pauta()
    
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
        
        # Datos de seguidores de ejemplo
        df_followers = pd.DataFrame({
            'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Seguidores_Totales': range(400, 430)
        })
        
        # Datos de pauta de ejemplo
        df_pauta = pd.DataFrame({
            'coste_anuncio': [641140],
            'visualizaciones_videos': [180500],
            'nuevos_seguidores': [4170],
            'fecha': ['2025-10-19']
        })
        
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
    
    return df, youtobe_data, tiktok_data, df_followers, df_pauta

# Estilos CSS mejorados con reducción de espacio (igual que antes)
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

# Sidebar (igual que antes)
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
        backend_test = requests.get(BACKEND_URL, timeout=5)
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
        # "Todo el período" no aplica filtro

# Verificar si hay datos
if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    
    if selected_platform != "general":
        with st.expander("🔍 Información de Depuración", expanded=False):
            st.write(f"**Plataforma seleccionada:** {selected_platform}")
            st.write(f"**Total registros en dataset:** {len(df_all)}")
            st.write(f"**Total registros YouTube/Youtobe:** {len(youtobe_df)}")
            st.write(f"**Total registros TikTok:** {len(tiktok_df)}")
    
    st.info("Conectando al backend para cargar datos en tiempo real...")
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
    
    if 'visualizaciones_videos' in df_pauta.columns:
        visualizaciones_videos_sum = df_pauta['visualizaciones_videos'].sum()
    
    if 'nuevos_seguidores' in df_pauta.columns:
        nuevos_seguidores_sum = df_pauta['nuevos_seguidores'].sum()
    
    # Función para formatear números con separador de miles
    def format_number(num):
        """Formatea números con separador de miles"""
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
    
    # Mostrar 3 tarjetas de métricas de pauta (eliminada VISUALIZACIONES PERFIL)
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
# SECCIÓN: NUEVAS GRÁFICAS DE INVERSIÓN Y CPS (solo para GENERAL y TikTok)
# ============================================================================
if selected_platform == "general" or selected_platform == "tiktok":
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
                📊 ANÁLISIS DE INVERSIÓN Y COSTO POR SEGUIDOR (CPS) - IDÉNTICO A LAS GRÁFICAS ORIGINALES
            </h3>
            <div style="color: #6b7280; font-size: 12px;">
                Gráficas exactas a las originales de Python
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Procesar datos para las gráficas
    datos_procesados, _, _ = procesar_datos_graficas()
    
    if datos_procesados is not None and not datos_procesados.empty:
        # Gráfica 1: Inversión vs Seguidores (IDÉNTICA a grafica.txt)
        fig_grafica1 = crear_grafica_inversion_vs_seguidores(datos_procesados, platform_name)
        if fig_grafica1:
            st.plotly_chart(fig_grafica1, use_container_width=True)
        
        # Gráfica 2: Heatmap CPS (IDÉNTICO a grafica2.txt)
        fig_grafica2, fig_grafica2_barras = crear_heatmap_cps(datos_procesados, platform_name)
        
        if fig_grafica2 and fig_grafica2_barras:
            # Mostrar ambas gráficas en columnas como en la original
            col_heatmap1, col_heatmap2 = st.columns([3, 1])
            
            with col_heatmap1:
                st.plotly_chart(fig_grafica2, use_container_width=True)
            
            with col_heatmap2:
                st.plotly_chart(fig_grafica2_barras, use_container_width=True)
        
        # Métricas de CPS
        if not datos_procesados.empty and 'Costo' in datos_procesados.columns and 'Neto_Diario_Real' in datos_procesados.columns:
            # Calcular CPS
            datos_procesados['CPS'] = datos_procesados['Costo'] / datos_procesados['Neto_Diario_Real']
            
            col_cps1, col_cps2, col_cps3, col_cps4 = st.columns(4)
            
            with col_cps1:
                cps_promedio = datos_procesados['CPS'].mean() if 'CPS' in datos_procesados.columns else 0
                st.metric("💰 CPS Promedio", f"${cps_promedio:,.0f}")
            
            with col_cps2:
                cps_min = datos_procesados['CPS'].min() if 'CPS' in datos_procesados.columns else 0
                st.metric("💰 CPS Mínimo", f"${cps_min:,.0f}")
            
            with col_cps3:
                cps_max = datos_procesados['CPS'].max() if 'CPS' in datos_procesados.columns else 0
                st.metric("💰 CPS Máximo", f"${cps_max:,.0f}")
            
            with col_cps4:
                dias_con_inversion = len(datos_procesados)
                st.metric("📅 Días con Inversión", f"{dias_con_inversion}")
    else:
        st.info("No hay suficientes datos para generar las gráficas de inversión y CPS")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# RESTO DEL CÓDIGO ORIGINAL (SIN CAMBIOS)
# ============================================================================

# SECCIÓN: GRÁFICA DE SEGUIDORES Y PAUTA (solo para GENERAL y TikTok)
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
        # Preparar datos de pauta si existen
        if not df_pauta.empty:
            # Asegurar que tenemos las columnas necesarias de pauta
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores_pauta'] = df_pauta['Seguidores']
            
            # Convertir fecha en pauta al mismo formato que en followers
            df_pauta['fecha'] = pd.to_datetime(df_pauta['fecha'], errors='coerce')
            
            # Agrupar por fecha para sumar valores duplicados
            df_pauta_agg = df_pauta.groupby('fecha').agg({
                'coste_anuncio': 'sum',
                'visualizaciones_videos': 'sum',
                'nuevos_seguidores_pauta': 'sum'
            }).reset_index()
            
            # Fusionar por fecha - CORRECCIÓN: USAR OUTER JOIN PARA VER TODAS LAS FECHAS
            df_merged = pd.merge(df_followers, df_pauta_agg, left_on='Fecha', right_on='fecha', how='outer')
            
            # Ordenar por fecha
            df_merged = df_merged.sort_values('Fecha')
            
            # Rellenar valores faltantes
            if 'Seguidores_Totales' in df_merged.columns:
                df_merged['Seguidores_Totales'] = df_merged['Seguidores_Totales'].fillna(method='ffill').fillna(0)
            
            if 'coste_anuncio' in df_merged.columns:
                df_merged['coste_anuncio'] = df_merged['coste_anuncio'].fillna(0)
            
            if 'visualizaciones_videos' in df_merged.columns:
                df_merged['visualizaciones_videos'] = df_merged['visualizaciones_videos'].fillna(0)
            
            if 'nuevos_seguidores_pauta' in df_merged.columns:
                df_merged['nuevos_seguidores_pauta'] = df_merged['nuevos_seguidores_pauta'].fillna(0)
        else:
            df_merged = df_followers.copy()
            df_merged['coste_anuncio'] = 0
            df_merged['visualizaciones_videos'] = 0
            df_merged['nuevos_seguidores_pauta'] = 0
        
        # Crear gráfica de 4 líneas
        fig_followers = go.Figure()
        
        # 1. Seguidores Totales (línea principal)
        fig_followers.add_trace(go.Scatter(
            x=df_merged['Fecha'],
            y=df_merged['Seguidores_Totales'],
            mode='lines+markers',
            name='👥 Seguidores Totales',
            marker=dict(
                size=8,
                color='#000000',
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            line=dict(color='#000000', width=3),
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Seguidores Totales: %{y:,}<extra></extra>'
        ))
        
        # 2. Seguidores Pauta (si existe)
        if 'nuevos_seguidores_pauta' in df_merged.columns:
            fig_followers.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['nuevos_seguidores_pauta'],
                mode='lines+markers',
                name='👥 Seguidores Pauta',
                marker=dict(
                    size=6,
                    color='#10b981',
                    symbol='diamond'
                ),
                line=dict(color='#10b981', width=2, dash='dot'),
                hovertemplate='Seguidores Pauta: %{y:,}<extra></extra>',
                yaxis='y1'
            ))
        
        # 3. Costo de Pauta (barras, eje secundario)
        if 'coste_anuncio' in df_merged.columns:
            fig_followers.add_trace(go.Bar(
                x=df_merged['Fecha'],
                y=df_merged['coste_anuncio'],
                name='💰 Costo Pauta',
                marker=dict(
                    color='#ef4444',
                    opacity=0.7
                ),
                hovertemplate='Costo Pauta: $%{y:,}<extra></extra>',
                yaxis='y2'
            ))
        
        # 4. Visualizaciones de Pauta (eje secundario)
        if 'visualizaciones_videos' in df_merged.columns:
            fig_followers.add_trace(go.Scatter(
                x=df_merged['Fecha'],
                y=df_merged['visualizaciones_videos'],
                mode='lines+markers',
                name='👁️ Visualizaciones Pauta',
                marker=dict(
                    size=6,
                    color='#3B82F6',
                    symbol='triangle-up'
                ),
                line=dict(color='#3B82F6', width=2, dash='dash'),
                hovertemplate='Visualizaciones Pauta: %{y:,}<extra></extra>',
                yaxis='y2'
            ))
        
        # Configurar layout con eje secundario
        fig_followers.update_layout(
            height=450,
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
                title="Costo ($) / Visualizaciones",
                overlaying='y',
                side='right',
                gridcolor='rgba(241, 245, 249, 0.5)',
                showgrid=False,
                title_font=dict(color='#ef4444')
            )
        )
        
        st.plotly_chart(fig_followers, use_container_width=True)
        
        # Estadísticas de seguidores y pauta
        if len(df_merged) > 0:
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            with col_f1:
                latest_followers = df_merged['Seguidores_Totales'].iloc[-1] if len(df_merged) > 0 else 0
                st.metric("👥 Últimos seguidores", f"{latest_followers:,}")
            
            with col_f2:
                if 'nuevos_seguidores_pauta' in df_merged.columns:
                    total_nuevos_seguidores = df_merged['nuevos_seguidores_pauta'].sum()
                    st.metric("👥 Seguidores Pauta", f"{total_nuevos_seguidores:,}")
                else:
                    st.metric("👥 Seguidores Pauta", "N/D")
            
            with col_f3:
                if 'coste_anuncio' in df_merged.columns:
                    total_costo = df_merged['coste_anuncio'].sum()
                    st.metric("💰 Costo total pauta", f"${total_costo:,}")
                else:
                    st.metric("💰 Costo pauta", "N/D")
            
            with col_f4:
                if 'visualizaciones_videos' in df_merged.columns:
                    total_visualizaciones = df_merged['visualizaciones_videos'].sum()
                    st.metric("👁️ Visualizaciones pauta", f"{total_visualizaciones:,}")
                else:
                    st.metric("👁️ Visualizaciones", "N/D")
    
    except Exception as e:
        st.warning(f"Error al generar gráfica combinada: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 1: PERFORMANCE OVER TIME - GRÁFICA MULTI-LÍNEA MEJORADA
st.markdown("""
<div class="performance-chart">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #1f2937; font-size: 20px;">
            📈 PERFORMANCE OVER TIME - EVOLUCIÓN DETALLADA
        </h3>
        <div style="color: #6b7280; font-size: 12px;">
            Gráfica multi-línea interactiva
        </div>
    </div>
""", unsafe_allow_html=True)

try:
    if not df.empty and 'fecha_publicacion' in df.columns:
        # Crear DataFrame para gráficas diarias
        df_sorted = df.sort_values('fecha_publicacion')
        
        # Agrupar por fecha
        daily_stats = df_sorted.groupby('fecha_publicacion').agg({
            'visualizaciones': 'sum',
            'me_gusta': 'sum',
            'comentarios': 'sum',
            'rendimiento_por_dia': 'mean'
        }).reset_index()
        
        # Crear gráfica multi-línea con subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '📊 Evolución Diaria de Visualizaciones',
                '❤️ Evolución Diaria de Likes',
                '💬 Evolución Diaria de Comentarios',
                '🚀 Rendimiento Promedio Diario'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'scatter'}],
                [{'type': 'scatter'}, {'type': 'scatter'}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Visualizaciones
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['visualizaciones'],
                mode='lines+markers',
                name='Visualizaciones',
                line=dict(color='#3B82F6', width=3),
                marker=dict(size=6, color='#3B82F6'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>👁️ Views: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ),
            row=1, col=1
        )
        
        # 2. Likes
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['me_gusta'],
                mode='lines+markers',
                name='Likes',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6, color='#10b981'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>❤️ Likes: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ),
            row=1, col=2
        )
        
        # 3. Comentarios
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['comentarios'],
                mode='lines+markers',
                name='Comentarios',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=6, color='#8b5cf6'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>💬 Comments: %{y:,}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.1)'
            ),
            row=2, col=1
        )
        
        # 4. Rendimiento diario
        fig.add_trace(
            go.Scatter(
                x=daily_stats['fecha_publicacion'],
                y=daily_stats['rendimiento_por_dia'],
                mode='lines+markers',
                name='Rendimiento/Día',
                line=dict(color='#f59e0b', width=3),
                marker=dict(size=6, color='#f59e0b'),
                hovertemplate='<b>📅 %{x|%d/%m/%Y}</b><br>🚀 Perf/Día: %{y:.1f}<extra></extra>',
                fill='tozeroy',
                fillcolor='rgba(245, 158, 11, 0.1)'
            ),
            row=2, col=2
        )
        
        # Actualizar layout
        fig.update_layout(
            height=750,
            showlegend=False,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=100, b=40),
            title_font=dict(size=16),
            font=dict(size=12),
            hovermode='x unified'
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Visualizaciones", row=1, col=1)
        fig.update_xaxes(title_text="Fecha", row=1, col=2)
        fig.update_yaxes(title_text="Likes", row=1, col=2)
        fig.update_xaxes(title_text="Fecha", row=2, col=1)
        fig.update_yaxes(title_text="Comentarios", row=2, col=1)
        fig.update_xaxes(title_text="Fecha", row=2, col=2)
        fig.update_yaxes(title_text="Rendimiento/Día", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas resumidas debajo del gráfico
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            max_views_day = daily_stats.loc[daily_stats['visualizaciones'].idxmax(), 'fecha_publicacion']
            max_views = daily_stats['visualizaciones'].max()
            st.metric("📅 Día con más Views", max_views_day.strftime('%d/%m/%Y'), f"{max_views:,}")
        
        with col_stats2:
            max_likes_day = daily_stats.loc[daily_stats['me_gusta'].idxmax(), 'fecha_publicacion']
            max_likes = daily_stats['me_gusta'].max()
            st.metric("📅 Día con más Likes", max_likes_day.strftime('%d/%m/%Y'), f"{max_likes:,}")
        
        with col_stats3:
            max_comments_day = daily_stats.loc[daily_stats['comentarios'].idxmax(), 'fecha_publicacion']
            max_comments = daily_stats['comentarios'].max()
            st.metric("📅 Día con más Comments", max_comments_day.strftime('%d/%m/%Y'), f"{max_comments:,}")
        
        with col_stats4:
            max_perf_day = daily_stats.loc[daily_stats['rendimiento_por_dia'].idxmax(), 'fecha_publicacion']
            max_perf = daily_stats['rendimiento_por_dia'].max()
            st.metric("📅 Mejor rendimiento/día", max_perf_day.strftime('%d/%m/%Y'), f"{max_perf:.1f}")
        
except Exception as e:
    st.warning(f"Error al generar gráficas: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 2: CONTENT PERFORMANCE DATA - TABLA COMPLETA
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
    
    # AGREGAR COLUMNA DE SEGUIDORES_TOTALES SI EXISTE
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
    
    # AGREGAR CONFIGURACIÓN PARA SEGUIDORES TOTALES
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
    
    # Estadísticas de la tabla
    col_table1, col_table2, col_table3, col_table4 = st.columns(4)
    
    with col_table1:
        avg_views = display_df['👁️ VISUALIZACIONES'].mean() if '👁️ VISUALIZACIONES' in display_df.columns else 0
        st.metric("📊 Views promedio", f"{avg_views:,.0f}")
    
    with col_table2:
        avg_likes = display_df['❤️ LIKES'].mean() if '❤️ LIKES' in display_df.columns else 0
        st.metric("📊 Likes promedio", f"{avg_likes:,.0f}")
    
    with col_table3:
        avg_comments = display_df['💬 COMENTARIOS'].mean() if '💬 COMENTARIOS' in display_df.columns else 0
        st.metric("📊 Comments promedio", f"{avg_comments:,.0f}")
    
    with col_table4:
        avg_perf = display_df['🚀 REND/DÍA'].mean() if '🚀 REND/DÍA' in display_df.columns else 0
        st.metric("📊 Rendimiento promedio", f"{avg_perf:.1f}")
    
    # AGREGAR ESTADÍSTICA DE SEGUIDORES SI EXISTE
    if '👥 SEGUIDORES TOTALES' in display_df.columns:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col_followers1, col_followers2, col_followers3, col_followers4 = st.columns(4)
        
        with col_followers1:
            total_seguidores = display_df['👥 SEGUIDORES TOTALES'].sum() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Total Seguidores", f"{total_seguidores:,}")
        
        with col_followers2:
            avg_seguidores = display_df['👥 SEGUIDORES TOTALES'].mean() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Promedio/Post", f"{avg_seguidores:,.0f}")
        
        with col_followers3:
            max_seguidores = display_df['👥 SEGUIDORES TOTALES'].max() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Máximo", f"{max_seguidores:,}")
        
        with col_followers4:
            min_seguidores = display_df['👥 SEGUIDORES TOTALES'].min() if '👥 SEGUIDORES TOTALES' in display_df.columns else 0
            st.metric("👥 Mínimo", f"{min_seguidores:,}")
    
else:
    st.info("No hay datos para mostrar en la tabla")

st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 3: ANÁLISIS DETALLADO EN DOS COLUMNAS
col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 18px;">
                📊 PERFORMANCE ANALYTICS
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if not df.empty and 'rendimiento_por_dia' in df.columns:
        # Análisis de distribución por rendimiento
        q75 = df['rendimiento_por_dia'].quantile(0.75)
        q50 = df['rendimiento_por_dia'].quantile(0.50)
        q25 = df['rendimiento_por_dia'].quantile(0.25)
        
        high_perf = len(df[df['rendimiento_por_dia'] > q75])
        medium_high_perf = len(df[(df['rendimiento_por_dia'] > q50) & (df['rendimiento_por_dia'] <= q75)])
        medium_low_perf = len(df[(df['rendimiento_por_dia'] > q25) & (df['rendimiento_por_dia'] <= q50)])
        low_perf = len(df[df['rendimiento_por_dia'] <= q25])
        
        # Gráfico de pastel
        labels = ['🟢 Alto', '🟡 Medio-Alto', '🟠 Medio-Bajo', '🔴 Bajo']
        values = [high_perf, medium_high_perf, medium_low_perf, low_perf]
        colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            height=320,
            showlegend=False,
            template='plotly_white',
            margin=dict(l=20, r=20, t=40, b=20),
            title_text="Distribución por Nivel de Rendimiento",
            title_font=dict(size=14)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Estadísticas detalladas
        high_perf_pct = (high_perf / total_posts * 100) if total_posts > 0 else 0
        medium_high_pct = (medium_high_perf / total_posts * 100) if total_posts > 0 else 0
        medium_low_pct = (medium_low_perf / total_posts * 100) if total_posts > 0 else 0
        low_perf_pct = (low_perf / total_posts * 100) if total_posts > 0 else 0
        
        st.markdown(f"""
        <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                    border-radius: 12px; border-left: 4px solid #3B82F6;">
            <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 15px;">📈 ANÁLISIS DE PERFORMANCE</h4>
            <div style="color: #4b5563; font-size: 13px;">
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟢 Alto rendimiento:</span>
                    <span style="font-weight: 700; color: #10b981;">{high_perf} posts ({high_perf_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟡 Medio-Alto:</span>
                    <span style="font-weight: 700; color: #f59e0b;">{medium_high_perf} posts ({medium_high_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🟠 Medio-Bajo:</span>
                    <span style="font-weight: 700; color: #f97316;">{medium_low_perf} posts ({medium_low_pct:.1f}%)</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">🔴 Bajo rendimiento:</span>
                    <span style="font-weight: 700; color: #ef4444;">{low_perf} posts ({low_perf_pct:.1f}%)</span>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                    <span style="display: inline-block; width: 160px;">📊 Rendimiento promedio:</span>
                    <span style="font-weight: 700; color: #3B82F6;">{df['rendimiento_por_dia'].mean():.1f} views/día</span>
                </div>
                <div style="margin-top: 6px;">
                    <span style="display: inline-block; width: 160px;">🚀 Mejor rendimiento:</span>
                    <span style="font-weight: 700; color: #8b5cf6;">{df['rendimiento_por_dia'].max():.1f} views/día</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("No hay datos para análisis de performance")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_analysis2:
    st.markdown("""
    <div class="performance-chart" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 18px;">
                📈 KEY METRICS - MÉTRICAS CLAVE
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Calcular métricas detalladas
        metrics_detailed = []
        
        # Métricas de visualizaciones
        if 'visualizaciones' in df.columns:
            metrics_detailed.append(('👁️ Avg. Views/Post', f"{df['visualizaciones'].mean():.0f}"))
            metrics_detailed.append(('👁️ Median Views', f"{df['visualizaciones'].median():.0f}"))
            metrics_detailed.append(('👁️ Std Dev Views', f"{df['visualizaciones'].std():.0f}"))
            metrics_detailed.append(('👁️ Min Views', f"{df['visualizaciones'].min():,}"))
            metrics_detailed.append(('👁️ Max Views', f"{df['visualizaciones'].max():,}"))
        
        # Métricas de engagement
        if 'me_gusta' in df.columns:
            metrics_detailed.append(('❤️ Avg. Likes/Post', f"{df['me_gusta'].mean():.1f}"))
            metrics_detailed.append(('❤️ Max Likes', f"{df['me_gusta'].max():,}"))
        
        if 'comentarios' in df.columns:
            metrics_detailed.append(('💬 Avg. Comments/Post', f"{df['comentarios'].mean():.1f}"))
            metrics_detailed.append(('💬 Max Comments', f"{df['comentarios'].max():,}"))
        
        # Métricas de seguidores si existen
        if 'Seguidores_Totales' in df.columns:
            metrics_detailed.append(('👥 Avg. Followers/Post', f"{df['Seguidores_Totales'].mean():.0f}"))
            metrics_detailed.append(('👥 Total Followers', f"{df['Seguidores_Totales'].sum():,}"))
        
        # Métricas de tiempo
        if 'dias_desde_publicacion' in df.columns:
            metrics_detailed.append(('📅 Avg. Content Age', f"{df['dias_desde_publicacion'].mean():.0f} días"))
            metrics_detailed.append(('📅 Newest Post', f"{df['dias_desde_publicacion'].min()} días"))
            metrics_detailed.append(('📅 Oldest Post', f"{df['dias_desde_publicacion'].max()} días"))
        
        # Métricas de rendimiento
        if 'rendimiento_por_dia' in df.columns:
            metrics_detailed.append(('🚀 Avg. Daily Perf.', f"{df['rendimiento_por_dia'].mean():.1f}"))
            metrics_detailed.append(('🚀 Median Daily Perf.', f"{df['rendimiento_por_dia'].median():.1f}"))
        
        # Engagement rate detallado
        metrics_detailed.append(('💬 Engagement Rate', f"{engagement_rate:.2f}%"))
        
        if total_views > 0 and total_likes > 0:
            like_to_view_ratio = (total_likes / total_views) * 100
            metrics_detailed.append(('👍 Like/View Ratio', f"{like_to_view_ratio:.2f}%"))
        
        if total_comments > 0 and total_likes > 0:
            comment_to_like_ratio = (total_comments / total_likes) * 100
            metrics_detailed.append(('💬 Comment/Like Ratio', f"{comment_to_like_ratio:.2f}%"))
        
        # Mostrar métricas en tabla mejorada
        for i, (metric, value) in enumerate(metrics_detailed):
            bg_color = "#ffffff" if i % 2 == 0 else "#f8fafc"
            icon = metric.split(' ')[0]
            metric_name = ' '.join(metric.split(' ')[1:])
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 12px 14px; background: {bg_color}; 
                        border-radius: 8px; margin: 3px 0; border: 1px solid #e5e7eb;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 16px;">{icon}</span>
                    <span style="color: #4b5563; font-size: 13px; font-weight: 500;">{metric_name}</span>
                </div>
                <span style="font-weight: 700; color: #1f2937; font-size: 14px;">
                    {value}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis de engagement avanzado
        st.markdown("""
        <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                    border-radius: 12px; border-left: 4px solid #0ea5e9;">
            <h4 style="margin: 0 0 10px 0; color: #374151; font-size: 15px;">📊 ANÁLISIS DE ENGAGEMENT AVANZADO</h4>
            <div style="color: #4b5563; font-size: 13px;">
        """, unsafe_allow_html=True)
        
        engagement_html = ""
        
        if total_views > 0:
            like_rate = (total_likes / total_views * 100) if 'me_gusta' in df.columns else 0
            comment_rate = (total_comments / total_views * 100) if 'comentarios' in df.columns else 0
            
            engagement_html += f"""
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">👍 Tasa de Likes:</span>
                    <span style="font-weight: 700; color: #10b981;">{like_rate:.2f}%</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">💬 Tasa de Comentarios:</span>
                    <span style="font-weight: 700; color: #3B82F6;">{comment_rate:.2f}%</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="display: inline-block; width: 160px;">📊 Total Engagement:</span>
                    <span style="font-weight: 700; color: #8b5cf6;">{(like_rate + comment_rate):.2f}%</span>
                </div>
            """
        
        if total_likes > 0 and total_comments > 0:
            like_to_comment_ratio = total_likes / total_comments
            engagement_html += f"""
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e5e7eb;">
                    <span style="display: inline-block; width: 160px;">⚖️ Ratio Likes/Comments:</span>
                    <span style="font-weight: 700; color: #EC4899;">{like_to_comment_ratio:.1f}</span>
                </div>
            """
        
        if engagement_html:
            st.markdown(engagement_html, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    else:
        st.info("No hay datos para métricas clave")
    
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
