import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import requests
import numpy as np

warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard PRO",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

#############################################
# NUEVOS ENDPOINTS PARA GRÁFICAS
#############################################
BACKEND_URL = "https://pahubisas.pythonanywhere.com/data"
FOLLOWERS_URL = "https://pahubisas.pythonanywhere.com/followers"
PAUTA_URL = "https://pahubisas.pythonanywhere.com/pauta_anuncio"
GRAFICA1_URL = "https://pahubisas.pythonanywhere.com/grafica1"
GRAFICA2_URL = "https://pahubisas.pythonanywhere.com/grafica2"

def cargar_datos_backend():
    try:
        r = requests.get(BACKEND_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(data.get("data", []))
        
        if "fecha_publicacion" in df.columns:
            df["fecha_publicacion"] = pd.to_datetime(
                df["fecha_publicacion"],
                dayfirst=True,
                errors="coerce"
            )

        num_cols = ["vistas", "comentarios", "me_gusta_numero", "visualizaciones", 
                   "me_gusta", "comentarios_num", "Seguidores_Totales"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "visualizaciones" not in df.columns and "vistas" in df.columns:
            df["visualizaciones"] = df["vistas"]
        
        if "me_gusta" not in df.columns and "me_gusta_numero" in df.columns:
            df["me_gusta"] = df["me_gusta_numero"]
        
        if "comentarios" not in df.columns and "comentarios_num" in df.columns:
            df["comentarios"] = df["comentarios_num"]

        if "fecha_publicacion" in df.columns:
            hoy = pd.Timestamp.now()
            df["dias"] = (hoy - df["fecha_publicacion"]).dt.days.fillna(0).astype(int)
            df["dias_desde_publicacion"] = df["dias"].apply(lambda x: max(x, 1))
            df["rendimiento_por_dia"] = df["visualizaciones"] / df["dias_desde_publicacion"]
            df["semana"] = df["fecha_publicacion"].dt.isocalendar().week.fillna(0).astype(int)
            df["meses"] = df["fecha_publicacion"].dt.month.fillna(0).astype(int)

        if "red" not in df.columns and "platform" in df.columns:
            df["red"] = df["platform"]
        elif "red" not in df.columns:
            df["red"] = "desconocido"

        if "tipo" not in df.columns:
            df["tipo"] = "general"

        return df

    except Exception as e:
        st.error(f"Error al conectar con el backend de datos: {str(e)}")
        return pd.DataFrame()

def cargar_datos_seguidores():
    try:
        r = requests.get(FOLLOWERS_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        df_followers = pd.DataFrame(data.get("data", []))
        
        if "Fecha" in df_followers.columns:
            df_followers["Fecha"] = pd.to_datetime(
                df_followers["Fecha"],
                dayfirst=True,
                errors="coerce"
            )
        
        if "Seguidores_Totales" in df_followers.columns:
            df_followers["Seguidores_Totales"] = pd.to_numeric(df_followers["Seguidores_Totales"], errors="coerce")
        
        return df_followers
        
    except Exception as e:
        st.error(f"Error al conectar con el backend de seguidores: {str(e)}")
        return pd.DataFrame()

def cargar_datos_pauta():
    try:
        r = requests.get(PAUTA_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        df_pauta = pd.DataFrame(data.get("data", []))
        
        if not df_pauta.empty:
            if 'Costo' in df_pauta.columns:
                df_pauta['coste_anuncio'] = df_pauta['Costo']
            if 'Visualizaciones' in df_pauta.columns:
                df_pauta['visualizaciones_videos'] = df_pauta['Visualizaciones']
            if 'Seguidores' in df_pauta.columns:
                df_pauta['nuevos_seguidores'] = df_pauta['Seguidores']
            
            if "coste_anuncio" in df_pauta.columns:
                df_pauta["coste_anuncio"] = pd.to_numeric(df_pauta["coste_anuncio"], errors="coerce").fillna(0).astype(int)
            
            for col in ["visualizaciones_videos", "nuevos_seguidores"]:
                if col in df_pauta.columns:
                    df_pauta[col] = pd.to_numeric(df_pauta[col], errors="coerce").fillna(0).astype(int)
            
            if "fecha" in df_pauta.columns:
                df_pauta["fecha"] = pd.to_datetime(
                    df_pauta["fecha"], 
                    errors='coerce',
                    dayfirst=True
                )
        
        return df_pauta
        
    except Exception as e:
        return pd.DataFrame()

def cargar_datos_grafica1():
    try:
        r = requests.get(GRAFICA1_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        st.error(f"Error al cargar datos de gráfica 1: {str(e)}")
        return {"status": "error", "message": str(e)}

def cargar_datos_grafica2():
    try:
        r = requests.get(GRAFICA2_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        st.error(f"Error al cargar datos de gráfica 2: {str(e)}")
        return {"status": "error", "message": str(e)}

def formato_numero_original(valor):
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    try:
        return str(int(round(float(valor))))
    except Exception:
        return "—"

def formato_k_original(valor):
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    try:
        return f"{int(round(float(valor)/1000.0))}k"
    except Exception:
        return "—"

def formato_dias_original(valor):
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    try:
        v = float(valor)
        if v <= 0:
            return "—"
        return f"{v:.1f}"
    except Exception:
        return "—"

def crear_grafica1_interactiva(data_grafica1):
    if data_grafica1.get("status") != "success":
        st.error(f"No se pudo cargar la gráfica 1: {data_grafica1.get('message')}")
        return
    
    df_merge_fecha = pd.DataFrame(data_grafica1.get("tables", {}).get("df_merge_fecha", []))
    cand = pd.DataFrame(data_grafica1.get("tables", {}).get("dias_validos", []))
    curve = pd.DataFrame(data_grafica1.get("tables", {}).get("curva_15k", []))
    parameters = data_grafica1.get("parameters", {})
    
    calc_data = data_grafica1.get("calc", {})
    INV_mean = calc_data.get("INV_mean", 0)
    SEG_mean = calc_data.get("SEG_mean", 0)
    opt = calc_data.get("opt", {})
    cps_min = calc_data.get("cps_min_curva", 0)
    cps_max = calc_data.get("cps_max_tol", 0)
    
    if cand.empty or curve.empty:
        st.warning("No hay datos suficientes para generar la gráfica 1")
        return
    
    STEP = parameters.get("STEP", 15000)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
    TARGET_FOLLOWERS = parameters.get("TARGET_FOLLOWERS", 1000)
    OPT_CPS_TOL = parameters.get("OPT_CPS_TOL", 0.20)
    
    def x_warp(x):
        x = float(x)
        if x <= BREAK_X:
            return x
        return BREAK_X + (x - BREAK_X) * K
    
    cand["xw"] = cand["Costo"].apply(x_warp)
    curve["xw"] = curve["Inversion_promedio"].apply(x_warp)
    
    opt_x = opt.get("Inversion_promedio", 0)
    opt_y = opt.get("Seguidores_promedio", 0)
    opt_cps = opt.get("CPS_curva", 0)
    opt_dias_meta = opt.get("Dias_para_meta", 0)
    opt_dias = opt.get("Dias", 0)
    opt_xw = x_warp(opt_x)
    
    cmin = float(cand["Costo"].min())
    cmax = float(cand["Costo"].max())
    start = float(np.floor(cmin / STEP) * STEP)
    end = float(np.ceil(cmax / STEP) * STEP) + STEP
    bins = np.arange(start, end + 1, STEP)
    
    data_min = float(cand["Costo"].min())
    data_max = float(cand["Costo"].max())
    edge_ticks_real = np.unique(bins)
    edge_ticks_real = [x for x in edge_ticks_real if (x >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x <= (np.ceil(data_max/STEP)*STEP) + 1e-9)]
    edge_ticks_w = [x_warp(x) for x in edge_ticks_real]
    edge_tick_labels = [formato_k_original(x) for x in edge_ticks_real]
    
    MAX_X_TICKS = 12
    stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
    edge_ticks_real = edge_ticks_real[::stride]
    edge_ticks_w = edge_ticks_w[::stride]
    edge_tick_labels = edge_tick_labels[::stride]
    
    colors = {
        'fondo_figura': '#060913',
        'fondo_ejes': '#0b1020',
        'borde_ejes': '#334155',
        'texto': '#e0e7ff',
        'ticks': '#c7d2fe',
        'puntos_reales': '#60a5fa',
        'linea_curva': '#38bdf8',
        'puntos_curva': '#f59e0b',
        'linea_promedio': '#22d3ee',
        'punto_optimo': '#22c55e',
        'grid': 'rgba(255,255,255,0.15)'
    }
    
    fig = go.Figure()
    
    for x_real in bins:
        if x_real >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(data_max/STEP)*STEP) + 1e-9:
            fig.add_vline(
                x=x_warp(x_real),
                line_width=1.0,
                line_dash="dash",
                line_color="#cbd5e1",
                opacity=0.18
            )
    
    fig.add_trace(go.Scatter(
        x=cand["xw"],
        y=cand[RESULT_COL],
        mode='markers',
        name='Días reales',
        marker=dict(
            size=6,
            color=colors['puntos_reales'],
            opacity=0.12,
            line=dict(width=0)
        ),
        hovertemplate='<b>📅 Día Real</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=curve["xw"],
        y=curve["Seguidores_promedio"],
        mode='lines',
        name='Promedio esperado (por nivel inversión)',
        line=dict(color=colors['linea_curva'], width=2.8),
        opacity=0.95,
        hovertemplate='<b>📈 Curva promedio</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
        customdata=curve["CPS_curva"]
    ))
    
    LABEL_OFFSETS = [
        (18, 52), (18, -78),
        (-190, 52), (-190, -78),
        (60, 56), (60, -84),
        (-240, 56), (-240, -84),
        (110, 62), (110, -92),
        (-300, 62), (-300, -92),
        (0, 78), (0, -110),
        (160, 40), (160, -64),
        (-360, 40), (-360, -64),
    ]
    
    for idx, row in curve.iterrows():
        dias_meta = row.get("Dias_para_meta", np.nan)
        label_text = (
            f"Inv {formato_numero_original(row['Inversion_promedio'])}<br>"
            f"SEG {formato_numero_original(row['Seguidores_promedio'])}<br>"
            f"CPS {formato_numero_original(row['CPS_curva'])}<br>"
            f"{TARGET_FOLLOWERS} SEG ~ {formato_dias_original(dias_meta)} días<br>"
            f"Días {int(row['Dias'])}"
        )
        
        offset_idx = idx % len(LABEL_OFFSETS)
        dx, dy = LABEL_OFFSETS[offset_idx]
        
        fig.add_annotation(
            x=row["xw"],
            y=row["Seguidores_promedio"],
            text=label_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#94a3b8",
            ax=dx,
            ay=dy,
            font=dict(size=8, color="white", family="Arial"),
            bgcolor="#0b1020",
            bordercolor="#334155",
            borderwidth=1,
            borderpad=4,
            opacity=0.90,
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="middle"
        )
    
    fig.add_trace(go.Scatter(
        x=curve["xw"],
        y=curve["Seguidores_promedio"],
        mode='markers',
        name='Puntos promedio (hover/click)',
        marker=dict(
            size=12,
            color=colors['puntos_curva'],
            opacity=0.98,
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>🎯 Punto curva</b><br>Inv: $%{x:,.0f}<br>SEG: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
        customdata=curve["CPS_curva"],
        showlegend=True
    ))
    
    if opt_x > 0 and opt_y > 0:
        opt_label_text = (
            f"Óptimo<br>"
            f"Inv {formato_numero_original(opt_x)}<br>"
            f"SEG {formato_numero_original(opt_y)}<br>"
            f"CPS {formato_numero_original(opt_cps)}<br>"
            f"{TARGET_FOLLOWERS} SEG ~ {formato_dias_original(opt_dias_meta)} días<br>"
            f"CPS_min {formato_numero_original(cps_min)}<br>"
            f"CPS_max {formato_numero_original(cps_max)}"
        )
        
        fig.add_trace(go.Scatter(
            x=[opt_xw],
            y=[opt_y],
            mode='markers',
            name=f'Punto óptimo (max SEG dentro del mejor CPS, tol {int(OPT_CPS_TOL*100)}%)',
            marker=dict(
                size=25,
                color=colors['punto_optimo'],
                symbol='star',
                line=dict(width=1.8, color='white')
            ),
            hovertemplate='<b>⭐ PUNTO ÓPTIMO</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
            customdata=[opt_cps]
        ))
        
        OPT_LABEL_OFFSETS = [(-320, 70), (-360, 50), (-280, 90), (-260, 40), (-400, 70)]
        opt_dx, opt_dy = OPT_LABEL_OFFSETS[0]
        
        fig.add_annotation(
            x=opt_xw,
            y=opt_y,
            text=opt_label_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#94a3b8",
            ax=opt_dx,
            ay=opt_dy,
            font=dict(size=8, color="white", family="Arial"),
            bgcolor="#0b1020",
            bordercolor="#22c55e",
            borderwidth=1,
            borderpad=4,
            opacity=0.90,
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="middle"
        )
    
    fig.add_hline(
        y=SEG_mean,
        line_dash="dot",
        line_color=colors['linea_promedio'],
        line_width=2.0,
        opacity=0.8,
        annotation_text=f"Promedio SEG = {formato_numero_original(SEG_mean)}",
        annotation_position="top right",
        annotation_font=dict(size=10, color=colors['linea_promedio']),
        annotation_bgcolor=colors['fondo_ejes']
    )
    
    fig.add_vline(
        x=x_warp(INV_mean),
        line_dash="dot",
        line_color=colors['linea_promedio'],
        line_width=1.8,
        opacity=0.75,
        annotation_text=f"Promedio inversión = {formato_numero_original(INV_mean)}",
        annotation_position="top left",
        annotation_font=dict(size=10, color=colors['linea_promedio']),
        annotation_bgcolor=colors['fondo_ejes']
    )
    
    fig.update_layout(
        height=700,
        plot_bgcolor=colors['fondo_ejes'],
        paper_bgcolor=colors['fondo_figura'],
        font=dict(color=colors['texto'], size=12, family="Arial"),
        title=dict(
            text=f"Inversión vs Seguidores (curva por niveles) — Hover/Click en puntos naranjas<br>"
                 f"<span style='font-size:14px; color:#94a3b8'>Promedio SEG = {formato_numero_original(SEG_mean)} | Promedio INV = {formato_numero_original(INV_mean)}</span><br>"
                 f"<span style='font-size:12px; color:#94a3b8'>Impacto {IMPACT_DAYS}d | STEP ${STEP:,} | Compresión X: {BREAK_X/1000:.0f}k+ (K={K})</span>",
            font=dict(size=22, color='white', family="Arial Black"),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        xaxis=dict(
            title="",
            gridcolor=colors['grid'],
            tickvals=edge_ticks_w,
            ticktext=edge_tick_labels,
            tickfont=dict(size=11, color=colors['ticks']),
            zeroline=False,
            showgrid=True,
            gridwidth=0.6,
            range=[min(edge_ticks_w) - 1000, max(edge_ticks_w) + 1000]
        ),
        yaxis=dict(
            title=f"Seguidores ({'Impacto' if USE_IMPACT else 'Neto'} {IMPACT_DAYS}d)",
            gridcolor=colors['grid'],
            tickformat=",",
            tickfont=dict(size=11, color=colors['ticks']),
            title_font=dict(size=13, color=colors['texto'])
        ),
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(11, 16, 32, 0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(size=11, color=colors['texto'])
        ),
        margin=dict(l=60, r=40, t=120, b=60),
        showlegend=True
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=0.6, gridcolor=colors['grid'])
    fig.update_yaxes(showgrid=True, gridwidth=0.6, gridcolor=colors['grid'])
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Días válidos", f"{len(cand):,}")
    
    with col2:
        st.metric("💰 Inv promedio", f"${INV_mean:,.0f}")
    
    with col3:
        st.metric("👥 SEG promedio", f"{SEG_mean:,.0f}")
    
    with col4:
        st.metric("⭐ CPS mínimo", f"${cps_min:,.0f}")
    
    with col5:
        st.metric("🎯 CPS óptimo", f"${opt_cps:,.0f}", delta=f"Tol {int(OPT_CPS_TOL*100)}%")
    
    with st.expander("📋 Ver datos detallados de la curva (rangos de inversión)"):
        display_curve = curve.copy()
        display_curve["Inversion_promedio"] = display_curve["Inversion_promedio"].apply(lambda x: f"${x:,.0f}")
        display_curve["Seguidores_promedio"] = display_curve["Seguidores_promedio"].apply(lambda x: f"{x:,.0f}")
        display_curve["CPS_curva"] = display_curve["CPS_curva"].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A")
        display_curve["Dias_para_meta"] = display_curve["Dias_para_meta"].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        
        display_curve = display_curve.rename(columns={
            "Inversion_promedio": "💰 Inversión promedio",
            "Seguidores_promedio": "👥 Seguidores promedio",
            "CPS_curva": "📊 CPS",
            "Dias": "📅 Días en rango",
            "Dias_para_meta": f"⏱️ {TARGET_FOLLOWERS} SEG (días)"
        })
        
        st.dataframe(display_curve, use_container_width=True)

def crear_grafica2_interactiva(data_grafica2):
    if data_grafica2.get("status") != "success":
        st.error(f"No se pudo cargar la gráfica 2: {data_grafica2.get('message')}")
        return
    
    heatmap_data = data_grafica2.get("plot_data", {})
    summary_by_day = pd.DataFrame(data_grafica2.get("tables", {}).get("sum_day", []))
    
    if not heatmap_data:
        st.warning("No hay datos suficientes para generar el heatmap")
        return
    
    vals_cps_raw = np.array(heatmap_data.get("vals_cps_raw", []))
    vals_seg = np.array(heatmap_data.get("vals_seg", []))
    vals_cps_clip = np.array(heatmap_data.get("vals_cps_clip", []))
    dias_order = heatmap_data.get("dias_order", [])
    weeks = heatmap_data.get("weeks", [])
    
    if vals_cps_raw.size == 0:
        st.warning("Datos del heatmap incompletos")
        return
    
    def fmt_int_or_dash(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return "—"
        try:
            return f"{int(round(float(x))):,}".replace(",", ".")
        except Exception:
            return "—"
    
    colors = {
        'fondo_figura': '#060913',
        'fondo_ejes': '#0b1020',
        'borde_ejes': '#334155',
        'texto': '#e0e7ff',
        'ticks': '#c7d2fe',
        'texto_celda': 'white',
        'sombra_texto': 'rgba(0, 0, 0, 0.45)'
    }
    
    cps_flat = vals_cps_raw[np.isfinite(vals_cps_raw)]
    if len(cps_flat) > 0:
        p5 = np.nanpercentile(cps_flat, 5)
        p95 = np.nanpercentile(cps_flat, 95)
        zmin = p5
        zmax = p95
    else:
        zmin = 0
        zmax = 100
        p5 = p95 = 0
    
    text_matrix = []
    hover_text_matrix = []
    for i in range(len(vals_cps_raw)):
        row_text = []
        row_hover = []
        for j in range(len(vals_cps_raw[i])):
            cps_v = vals_cps_raw[i, j]
            seg_v = vals_seg[i, j]
            if np.isfinite(cps_v) and cps_v > 0:
                line1 = f"CPS {fmt_int_or_dash(cps_v)}"
                line2 = f"Seg {fmt_int_or_dash(seg_v)}"
                row_text.append(f"{line1}<br>{line2}")
                row_hover.append(f"CPS: ${cps_v:,.0f}<br>Seguidores: {seg_v:,.0f}")
            else:
                row_text.append("")
                row_hover.append("")
        text_matrix.append(row_text)
        hover_text_matrix.append(row_hover)
    
    try:
        fig = go.Figure(data=go.Heatmap(
            z=vals_cps_clip,
            x=weeks,
            y=dias_order,
            colorscale='RdYlGn_r',
            zmin=zmin,
            zmax=zmax,
            colorbar=dict(
                title="CPS (recortado p5–p95)",
                tickformat="$,.0f",
                len=0.8,
                thickness=15,
                tickfont=dict(size=10, color=colors['texto'])
            ),
            hovertemplate='<b>%{y} - %{x}</b><br>%{customdata}<extra></extra>',
            customdata=hover_text_matrix,
            text=text_matrix,
            texttemplate="%{text}",
            textfont=dict(size=9, color=colors['texto_celda'], family="Arial"),
            hoverongaps=False,
            showscale=True
        ))
        
        fig.update_layout(
            height=750,
            plot_bgcolor=colors['fondo_ejes'],
            paper_bgcolor=colors['fondo_figura'],
            font=dict(color=colors['texto'], size=12, family="Arial"),
            title=dict(
                text="Mapa de calor — CPS (Costo/Seguidor) + Seguidores (neto)<br>"
                     "<span style='font-size:14px; color:#94a3b8'>CPS bajo = mejor | Negro = sin inversión o sin seguidores positivos</span>",
                font=dict(size=22, color='white', family="Arial Black"),
                x=0.5,
                xanchor='center',
                y=0.95
            ),
            xaxis=dict(
                title="Semana ISO",
                tickangle=45,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=10, color=colors['ticks'], family="Arial"),
                title_font=dict(size=13, color=colors['texto']),
                side="top"
            ),
            yaxis=dict(
                title="Día de la semana",
                gridcolor='rgba(255,255,255,0.1)',
                autorange="reversed",
                tickfont=dict(size=12, color=colors['ticks'], family="Arial"),
                title_font=dict(size=13, color=colors['texto'])
            ),
            margin=dict(l=80, r=50, t=120, b=80)
        )
        
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=0.6, 
            gridcolor='rgba(255,255,255,0.15)',
            minor=dict(
                ticklen=4,
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.4
            )
        )
        
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=0.6, 
            gridcolor='rgba(255,255,255,0.15)',
            minor=dict(
                ticklen=4,
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                gridwidth=0.4
            )
        )
        
        fig.add_annotation(
            x=0.02, y=1.05,
            xref="paper", yref="paper",
            text="🟢 CPS BAJO = MEJOR EFICIENCIA",
            showarrow=False,
            font=dict(size=12, color="#10b981", family="Arial"),
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="#10b981",
            borderwidth=1,
            borderpad=4
        )
        
        fig.add_annotation(
            x=0.02, y=1.02,
            xref="paper", yref="paper",
            text="🔴 CPS ALTO = PEOR EFICIENCIA",
            showarrow=False,
            font=dict(size=12, color="#ef4444", family="Arial"),
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="#ef4444",
            borderwidth=1,
            borderpad=4
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
        
        if not summary_by_day.empty:
            dias_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            summary_by_day['Dia_Semana'] = pd.Categorical(
                summary_by_day['Dia_Semana'], 
                categories=dias_order, 
                ordered=True
            )
            summary_by_day = summary_by_day.sort_values('Dia_Semana')
            
            fig_bar = go.Figure()
            
            fig_bar.add_trace(go.Bar(
                x=summary_by_day["CPS_total_dia"],
                y=summary_by_day["Dia_Semana"],
                orientation='h',
                name="CPS por día",
                marker=dict(
                    color=summary_by_day["CPS_total_dia"],
                    colorscale='RdYlGn_r',
                    showscale=False,
                    cmin=np.nanpercentile(summary_by_day["CPS_total_dia"].dropna(), 5) if not summary_by_day["CPS_total_dia"].dropna().empty else 0,
                    cmax=np.nanpercentile(summary_by_day["CPS_total_dia"].dropna(), 95) if not summary_by_day["CPS_total_dia"].dropna().empty else 100,
                ),
                hovertemplate='<b>%{y}</b><br>CPS: $%{x:,.0f}<br>Seguidores: %{customdata:,.0f}<extra></extra>',
                customdata=summary_by_day["Seguidores_sum"],
                text=summary_by_day.apply(
                    lambda row: f"CPS {fmt_int_or_dash(row['CPS_total_dia'])}<br>Seg {fmt_int_or_dash(row['Seguidores_sum'])}" 
                    if not pd.isna(row['CPS_total_dia']) else "", 
                    axis=1
                ),
                textposition='outside',
                textfont=dict(size=10, color='white', family="Arial")
            ))
            
            fig_bar.update_layout(
                height=500,
                plot_bgcolor=colors['fondo_ejes'],
                paper_bgcolor=colors['fondo_figura'],
                font=dict(color=colors['texto'], size=12, family="Arial"),
                title=dict(
                    text="Resumen por día",
                    font=dict(size=20, color='white', family="Arial Black"),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title="CPS total por día",
                    gridcolor='rgba(255,255,255,0.18)',
                    tickprefix="$",
                    tickfont=dict(size=11, color=colors['ticks']),
                    title_font=dict(size=13, color=colors['texto'])
                ),
                yaxis=dict(
                    title="",
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=12, color=colors['ticks'], family="Arial"),
                    autorange="reversed"
                ),
                hovermode='y',
                margin=dict(l=20, r=50, t=80, b=80),
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with st.expander("📋 Ver datos detallados del heatmap"):
            if not summary_by_day.empty:
                display_summary = summary_by_day.copy()
                display_summary["Costo_sum"] = display_summary["Costo_sum"].apply(lambda x: f"${x:,.0f}")
                display_summary["Seguidores_sum"] = display_summary["Seguidores_sum"].apply(lambda x: f"{x:,.0f}")
                display_summary["CPS_total_dia"] = display_summary["CPS_total_dia"].apply(
                    lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
                )
                
                display_summary = display_summary.rename(columns={
                    "Dia_Semana": "📅 Día",
                    "Costo_sum": "💰 Costo total",
                    "Seguidores_sum": "👥 Seguidores total",
                    "CPS_total_dia": "📊 CPS total"
                })
                
                st.dataframe(display_summary, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error al crear heatmap: {str(e)}")
        heatmap_df = pd.DataFrame(vals_cps_raw, index=dias_order, columns=weeks)
        st.dataframe(heatmap_df.style.format("${:,.0f}"))

@st.cache_data(ttl=300)
def cargar_datos():
    df = cargar_datos_backend()
    df_followers = cargar_datos_seguidores()
    df_pauta = cargar_datos_pauta()
    
    if df.empty:
        st.warning("Usando datos de respaldo. El backend no está disponible.")
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
        df_followers = pd.DataFrame({
            'Fecha': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Seguidores_Totales': range(400, 430)
        })
        df_pauta = pd.DataFrame({
            'coste_anuncio': [641140],
            'visualizaciones_videos': [180500],
            'nuevos_seguidores': [4170],
            'fecha': ['2025-10-19']
        })
    else:
        if 'red' in df.columns:
            df['red'] = df['red'].astype(str).str.lower().str.strip()
        youtobe_data = df[df['red'] == 'youtobe'].copy()
        if youtobe_data.empty:
            youtobe_data = df[df['red'] == 'youtube'].copy()
        tiktok_data = df[df['red'] == 'tiktok'].copy()
    
    for df_data in [youtobe_data, tiktok_data]:
        if not df_data.empty and 'fecha_publicacion' in df_data.columns:
            hoy = pd.Timestamp.now()
            df_data['dias_desde_publicacion'] = (hoy - df_data['fecha_publicacion']).dt.days
            df_data['dias_desde_publicacion'] = df_data['dias_desde_publicacion'].apply(lambda x: max(x, 1))
            df_data['rendimiento_por_dia'] = df_data['visualizaciones'] / df_data['dias_desde_publicacion']
    
    return df, youtobe_data, tiktok_data, df_followers, df_pauta

st.markdown("""
<style>
.main { 
    padding: 0;
    padding-top: 0.5rem !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
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
.grafica-container {
    background: linear-gradient(135deg, #060913 0%, #0b1020 100%);
    border-radius: 16px;
    padding: 25px;
    margin: 20px 0;
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.grafica-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Arial Black', sans-serif;
}
.grafica-subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 25px;
    font-family: 'Arial', sans-serif;
}
</style>
""", unsafe_allow_html=True)

df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding: 0 10px;">
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); 
                    width: 55px; height: 55px; border-radius: 14px; 
                    display: flex; align-items: center; justify-content: center; 
                    margin: 0 auto 12px auto; font-size: 26px;">
            📊
        </div>
        <h2 style="color: white; margin-bottom: 4px; font-size: 20px; font-family: 'Arial Black', sans-serif;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 12px; margin: 0; font-family: 'Arial', sans-serif;">Social Media Analytics v3.2</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        backend_test = requests.get(BACKEND_URL, timeout=5)
        if backend_test.status_code == 200:
            st.markdown('<div class="backend-status backend-connected">✅ Backend Conectado</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Error: {backend_test.status_code}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Offline</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
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
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📊 GRÁFICAS AVANZADAS</p>', unsafe_allow_html=True)
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        if st.button("📈 Gráfica 1", key="grafica1_btn", use_container_width=True):
            st.session_state["show_grafica1"] = not st.session_state.get("show_grafica1", False)
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
    
    with col_graf2:
        if st.button("📊 Gráfica 2", key="grafica2_btn", use_container_width=True):
            st.session_state["show_grafica2"] = not st.session_state.get("show_grafica2", False)
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
    
    if st.session_state.get("show_grafica1", False) or st.session_state.get("show_grafica2", False):
        if st.button("⬅️ Volver a Dashboard", key="back_dashboard", use_container_width=True):
            if "show_grafica1" in st.session_state:
                st.session_state["show_grafica1"] = False
            if "show_grafica2" in st.session_state:
                st.session_state["show_grafica2"] = False
            st.rerun()

current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
st.markdown(f"""
<div class="dashboard-header">
    <h1 style="font-family: 'Arial Black', sans-serif;">📊 SOCIAL MEDIA DASHBOARD PRO</h1>
    <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px; font-weight: 400; font-family: 'Arial', sans-serif;">
        Analytics en Tiempo Real • Monitoreo de Performance • Insights Inteligentes
    </p>
    <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8; font-family: 'Arial', sans-serif;">
        Actualizado: {current_time}
    </div>
</div>
""", unsafe_allow_html=True)

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

if df.empty:
    st.error(f"⚠️ No hay datos disponibles para {platform_name}")
    if selected_platform != "general":
        with st.expander("🔍 Información de Depuración", expanded=False):
            st.write(f"**Plataforma seleccionada:** {selected_platform}")
            st.write(f"**Total registros en dataset:** {len(df_all)}")
            st.write(f"**Total registros YouTube/Youtobe:** {len(youtobe_df)}")
            st.write(f"**Total registros TikTok:** {len(tiktok_df)}")
    st.stop()

if st.session_state.get("show_grafica1", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📈 GRÁFICA 1: INVERSIÓN VS SEGUIDORES</div>
        <div class="grafica-subtitle">
            Análisis de eficiencia por nivel de inversión • CPS (Costo por Seguidor) • Punto óptimo
        </div>
    """, unsafe_allow_html=True)
    with st.spinner("Cargando datos de la gráfica 1..."):
        data_grafica1 = cargar_datos_grafica1()
        crear_grafica1_interactiva(data_grafica1)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

elif st.session_state.get("show_grafica2", False):
    st.markdown("""
    <div class="grafica-container">
        <div class="grafica-title">📊 GRÁFICA 2: HEATMAP CPS (COSTO POR SEGUIDOR)</div>
        <div class="grafica-subtitle">
            Análisis por día de semana y semana ISO • CPS bajo = mejor eficiencia
        </div>
    """, unsafe_allow_html=True)
    with st.spinner("Cargando datos de la gráfica 2..."):
        data_grafica2 = cargar_datos_grafica2()
        crear_grafica2_interactiva(data_grafica2)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

current_time_short = datetime.now().strftime('%H:%M')
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    st.markdown(f'<div style="font-size: 38px; text-align: center; color: {platform_color};">{platform_icon}</div>', unsafe_allow_html=True)

with col_header2:
    st.markdown(f'<h2 style="margin: 0; color: {platform_color}; font-size: 26px; text-align: center; font-family: Arial Black, sans-serif;">{platform_name} ANALYTICS</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; text-align: center; font-family: Arial, sans-serif;">{len(df)} contenidos analizados • Última actualización: {current_time_short}</p>', unsafe_allow_html=True)

with col_header3:
    st.markdown(f'''
    <div style="background: {platform_color}15; color: {platform_color}; padding: 8px 18px; 
                border-radius: 18px; font-size: 13px; font-weight: 600; text-align: center; 
                border: 1px solid {platform_color}30; font-family: Arial Black, sans-serif;">
        {len(df)} {platform_name} Posts
    </div>
    ''', unsafe_allow_html=True)

st.markdown("""
<div style="height: 20px;"></div>
""", unsafe_allow_html=True)
