import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import warnings
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from io import BytesIO

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard",
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
# FUNCIONES PARA NUEVAS GRÁFICAS
#############################################

def generar_grafica_inversion(fh_df, bp_df):
    """Genera la gráfica de inversión vs seguidores"""
    try:
        # Parámetros básicos
        STEP = 15000
        IMPACT_DAYS = 3
        USE_IMPACT = True
        BREAK_X = 80000.0
        K = 0.28
        
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
        
        # Crear gráfica
        plt.rcParams.update({
            "figure.facecolor": "#060913",
            "axes.facecolor": "#0b1020",
            "axes.edgecolor": "#334155",
            "axes.labelcolor": "#e0e7ff",
            "xtick.color": "#c7d2fe",
            "ytick.color": "#c7d2fe",
            "text.color": "#e0e7ff",
            "grid.alpha": 0.22,
            "grid.linewidth": 0.8,
            "font.size": 11
        })
        
        fig, ax = plt.subplots(figsize=(18, 6.0), dpi=175)
        ax.grid(True)
        
        # Función para compresión del eje X
        def x_warp(x):
            x = float(x)
            if x <= BREAK_X:
                return x
            return BREAK_X + (x - BREAK_X) * K
        
        # Preparar datos para gráfica
        cand["xw"] = cand["Costo"].apply(x_warp)
        curve["xw"] = curve["Inversion_promedio"].apply(x_warp)
        
        # Líneas de rango
        for x_real in bins:
            if x_real >= (np.floor(cmin/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(cmax/STEP)*STEP) + 1e-9:
                ax.axvline(x_warp(x_real), linewidth=1.0, linestyle="--", alpha=0.18, color="#cbd5e1", zorder=1)
        
        # Scatter plot de días reales
        ax.scatter(cand["xw"], cand[RESULT_COL], s=30, alpha=0.12, color="#60a5fa", label="Días reales", zorder=2)
        
        # Línea de tendencia
        ax.plot(curve["xw"], curve["Seguidores_promedio"], linewidth=2.8, alpha=0.95, color="#38bdf8",
                label="Promedio esperado (por nivel inversión)", zorder=5)
        
        # Puntos de la curva
        ax.scatter(
            curve["xw"], curve["Seguidores_promedio"],
            s=120, alpha=0.98, color="#f59e0b",
            label="Puntos promedio",
            zorder=6
        )
        
        # Configurar ejes
        xmin_w = x_warp(float(np.nanmin(cand["Costo"])))
        xmax_w = x_warp(float(np.nanmax(cand["Costo"])))
        pad = (xmax_w - xmin_w) * 0.04 if xmax_w > xmin_w else 1.0
        
        # Etiquetas de eje X
        edge_ticks_real = np.unique(bins)
        edge_ticks_real = [x for x in edge_ticks_real if (x >= (np.floor(cmin/STEP)*STEP) - 1e-9 and x <= (np.ceil(cmax/STEP)*STEP) + 1e-9)]
        edge_ticks_w = [x_warp(x) for x in edge_ticks_real]
        
        def fmt_k(x):
            if x is None or (isinstance(x, float) and np.isnan(x)):
                return "—"
            try:
                return f"{int(round(float(x)/1000.0))}k"
            except Exception:
                return "—"
        
        edge_tick_labels = [fmt_k(x) for x in edge_ticks_real]
        
        MAX_X_TICKS = 12
        stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
        edge_ticks_real = edge_ticks_real[::stride]
        edge_ticks_w = edge_ticks_w[::stride]
        edge_tick_labels = edge_tick_labels[::stride]
        
        ax.set_xticks(edge_ticks_w)
        ax.set_xticklabels(edge_tick_labels, rotation=0)
        ax.set_xlim(xmin_w - pad, xmax_w + pad)
        
        # Títulos y etiquetas
        impact_label = f"Impacto {IMPACT_DAYS}d" if USE_IMPACT else "Neto día"
        ax.set_title("📈 Inversión vs Seguidores (curva por niveles)")
        ax.set_ylabel(f"Seguidores ({impact_label})")
        
        # Leyenda
        leg = ax.legend(loc="upper left", frameon=True)
        leg.get_frame().set_facecolor("#0b1020")
        leg.get_frame().set_edgecolor("#334155")
        for t in leg.get_texts():
            t.set_color("#e0e7ff")
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.error(f"Error al generar gráfica: {str(e)}")
        return None

def generar_mapa_calor(fh_df, bp_df):
    """Genera el heatmap de CPS por día/semana"""
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
        
        vals_cps = pivot_cps.values.astype(float)
        vals_seg = pivot_seg.values.astype(float)
        
        # Normalizar colores (recorte p5–p95)
        flat = vals_cps[np.isfinite(vals_cps)]
        if flat.size == 0:
            return None
        
        p5 = np.nanpercentile(flat, 5)
        p95 = np.nanpercentile(flat, 95)
        vals_cps_clip = np.clip(vals_cps, p5, p95)
        
        # Crear heatmap
        plt.rcParams.update({
            "figure.facecolor": "#060913",
            "axes.facecolor": "#0b1020",
            "axes.edgecolor": "#334155",
            "axes.labelcolor": "#e0e7ff",
            "xtick.color": "#c7d2fe",
            "ytick.color": "#c7d2fe",
            "text.color": "#e0e7ff",
            "font.size": 11
        })
        
        weeks = list(pivot_cps.columns)
        n_rows = len(dias)
        n_cols = len(weeks)
        
        fig = plt.figure(figsize=(22, 7), dpi=190)
        gs = fig.add_gridspec(1, 2, width_ratios=[4.6, 1.4], wspace=0.08)
        
        # Heatmap principal
        ax = fig.add_subplot(gs[0, 0])
        im = ax.imshow(vals_cps_clip, aspect="auto")
        
        ax.set_title(
            "🗺️ Mapa de Calor - CPS (Costo/Seguidor) + Seguidores\nCPS bajo = mejor | Negro = sin datos",
            pad=14
        )
        
        ax.set_yticks(range(n_rows))
        ax.set_yticklabels(dias)
        
        ax.set_xticks(range(n_cols))
        ax.set_xticklabels(weeks, rotation=45, ha="right")
        
        ax.set_xticks(np.arange(-.5, n_cols, 1), minor=True)
        ax.set_yticks(np.arange(-.5, n_rows, 1), minor=True)
        ax.grid(which="minor", linewidth=0.6, alpha=0.15)
        ax.tick_params(which="minor", bottom=False, left=False)
        
        # Texto en celdas
        txt_fx = [pe.withStroke(linewidth=1.2, foreground=(0, 0, 0, 0.45))]
        
        def fmt_int_or_dash(x):
            if x is None or (isinstance(x, float) and np.isnan(x)):
                return "—"
            try:
                return f"{int(round(float(x))):,}".replace(",", ".")
            except Exception:
                return "—"
        
        for i in range(n_rows):
            for j in range(n_cols):
                cps_v = vals_cps[i, j]
                seg_v = vals_seg[i, j]
                if np.isfinite(cps_v) or np.isfinite(seg_v):
                    line1 = f"CPS {fmt_int_or_dash(cps_v)}"
                    line2 = f"Seg {fmt_int_or_dash(seg_v)}"
                    t = ax.text(
                        j, i,
                        f"{line1}\n{line2}",
                        ha="center", va="center",
                        fontsize=7.7,
                        color="white",
                        alpha=1.0
                    )
                    t.set_path_effects(txt_fx)
        
        # Barra de color
        cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
        cbar.set_label("CPS (recortado p5–p95)")
        
        # Barras derecha (resumen por día)
        axr = fig.add_subplot(gs[0, 1])
        axr.grid(True, axis="x", alpha=0.18)
        
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
        
        ypos = np.arange(n_rows)
        cps_day = sum_day["CPS_total_dia"].to_numpy(dtype=float)
        seg_day = sum_day["Seguidores_sum"].to_numpy(dtype=float)
        
        axr.barh(ypos, cps_day, alpha=0.75)
        axr.set_yticks(ypos)
        axr.set_yticklabels([""] * n_rows)
        axr.set_xlabel("CPS total por día")
        axr.set_title("Resumen por día", pad=10)
        
        # Texto en barras
        for i in range(n_rows):
            cpsv = cps_day[i]
            segv = seg_day[i]
            line = f"CPS {fmt_int_or_dash(cpsv)} | Seg {fmt_int_or_dash(segv)}"
            x_text = 0 if not np.isfinite(cpsv) else cpsv
            tt = axr.text(
                x_text, i,
                f"  {line}",
                va="center", ha="left",
                fontsize=9,
                color="white",
                alpha=1.0
            )
            tt.set_path_effects(txt_fx)
        
        plt.tight_layout()
        return fig
        
    except Exception as e:
        st.error(f"Error al generar heatmap: {str(e)}")
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

st.title("📊 Dashboard Social Media - TikTok")

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
        if st.button("🔄 Generar Gráfica de Inversión"):
            with st.spinner("Generando gráfica..."):
                fig_inversion = generar_grafica_inversion(fh_df, bp_df)
                if fig_inversion:
                    st.pyplot(fig_inversion)
                    
                    # Opción para descargar
                    buf = BytesIO()
                    fig_inversion.savefig(buf, format="png", dpi=150, bbox_inches='tight')
                    st.download_button(
                        label="📥 Descargar Gráfica",
                        data=buf.getvalue(),
                        file_name=f"inversion_vs_seguidores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
                else:
                    st.warning("No se pudo generar la gráfica. Verifique los datos.")
        else:
            st.info("👆 Presiona el botón para generar la gráfica de inversión")
    else:
        st.warning("Se necesitan datos de seguidores y pauta para esta gráfica")

# Tab 3: Mapa de calor CPS
with tab3:
    st.subheader("🗺️ Mapa de Calor - Costo por Seguidor (CPS)")
    
    if not fh_df.empty and not bp_df.empty:
        if st.button("🔄 Generar Mapa de Calor"):
            with st.spinner("Generando mapa de calor..."):
                fig_heatmap = generar_mapa_calor(fh_df, bp_df)
                if fig_heatmap:
                    st.pyplot(fig_heatmap)
                    
                    # Opción para descargar
                    buf = BytesIO()
                    fig_heatmap.savefig(buf, format="png", dpi=150, bbox_inches='tight')
                    st.download_button(
                        label="📥 Descargar Mapa",
                        data=buf.getvalue(),
                        file_name=f"mapa_calor_cps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
                else:
                    st.warning("No se pudo generar el mapa de calor. Verifique los datos.")
        else:
            st.info("👆 Presiona el botón para generar el mapa de calor")
    else:
        st.warning("Se necesitan datos de seguidores y pauta para esta gráfica")

# Footer
st.markdown("---")
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>📊 Dashboard Social Media • Datos en tiempo real • Actualizado: {current_time}</p>
    <p><small>Conectado a: {BACKEND_URL}</small></p>
</div>
""", unsafe_allow_html=True)
