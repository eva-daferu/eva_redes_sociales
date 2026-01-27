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

def verificar_backend():
    """Verifica el estado de todos los endpoints"""
    endpoints = {
        "Datos principales": BACKEND_URL,
        "Seguidores": FOLLOWERS_URL,
        "Pauta": PAUTA_URL,
        "Gráfica 1": GRAFICA1_URL,
        "Gráfica 2": GRAFICA2_URL
    }
    
    status = {}
    for nombre, url in endpoints.items():
        try:
            r = requests.get(url, timeout=10)
            status[nombre] = {
                "estado": "✅ Conectado" if r.status_code == 200 else f"❌ Error {r.status_code}",
                "url": url,
                "codigo": r.status_code,
                "datos": r.json() if r.status_code == 200 else None
            }
        except Exception as e:
            status[nombre] = {
                "estado": f"❌ Error: {str(e)[:50]}...",
                "url": url,
                "codigo": "N/A",
                "datos": None
            }
    
    return status

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
# FUNCIONES DE DATOS DE EJEMPLO PARA GRÁFICAS
#############################################

def generar_datos_ejemplo_grafica1():
    """Genera datos de ejemplo para la gráfica 1"""
    import numpy as np
    
    # Generar datos de días válidos
    np.random.seed(42)  # Para reproducibilidad
    dias_validos = []
    for i in range(45):
        costo = np.random.randint(10000, 250000)
        seguidores = int(costo * np.random.uniform(0.003, 0.02))
        dias_validos.append({
            "Costo": float(costo),
            "Seguidores_Impacto": float(seguidores),
            "Neto_Diario_Real": float(seguidores)
        })
    
    # Generar curva promedio
    curva_15k = []
    for inv in range(15000, 250001, 15000):
        seg_prom = int(inv * np.random.uniform(0.008, 0.012))
        cps = inv / seg_prom if seg_prom > 0 else 0
        dias_para_meta = 1000 / (seg_prom / 30) if seg_prom > 0 else 0
        curva_15k.append({
            "Inversion_promedio": float(inv),
            "Seguidores_promedio": float(seg_prom),
            "CPS_curva": float(cps),
            "Dias_para_meta": float(dias_para_meta),
            "Dias": int(np.random.randint(3, 15))
        })
    
    # Punto óptimo (aproximadamente en el 70% del rango)
    opt_idx = int(len(curva_15k) * 0.7)
    if opt_idx < len(curva_15k):
        opt_point = curva_15k[opt_idx]
    else:
        opt_point = curva_15k[-1]
    
    # Calcular promedios
    costos = [d["Costo"] for d in dias_validos]
    seguidores = [d["Seguidores_Impacto"] for d in dias_validos]
    
    return {
        "status": "success",
        "tables": {
            "df_merge_fecha": [],
            "dias_validos": dias_validos,
            "curva_15k": curva_15k
        },
        "parameters": {
            "STEP": 15000,
            "BREAK_X": 80000.0,
            "K": 0.28,
            "IMPACT_DAYS": 3,
            "USE_IMPACT": True,
            "OPT_CPS_TOL": 0.20
        },
        "results_summary": {
            "total_dias_validos": len(dias_validos),
            "cps_minimo": 85.5,
            "cps_maximo": 215.3
        },
        "calc": {
            "INV_mean": float(np.mean(costos)),
            "SEG_mean": float(np.mean(seguidores)),
            "opt": {
                "Inversion_promedio": opt_point["Inversion_promedio"],
                "Seguidores_promedio": opt_point["Seguidores_promedio"],
                "CPS_curva": opt_point["CPS_curva"],
                "Dias_para_meta": opt_point["Dias_para_meta"],
                "Dias": opt_point["Dias"]
            },
            "cps_min_curva": 85.5,
            "cps_max_tol": 102.6
        }
    }

def generar_datos_ejemplo_grafica2():
    """Genera datos de ejemplo para el heatmap"""
    import numpy as np
    
    # Días de la semana y semanas
    dias_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    weeks = [f"2025-W{i:02d}" for i in range(1, 9)]
    
    # Generar datos más realistas
    np.random.seed(42)
    
    # Patrón semanal: mejores días (Miércoles a Viernes), peores (Lunes y Domingo)
    base_pattern = [1.5, 1.3, 1.0, 0.8, 0.9, 1.2, 1.6]  # Multiplicadores de CPS
    
    vals_cps_raw = np.zeros((7, 8))
    vals_seg = np.zeros((7, 8))
    
    for i, dia in enumerate(dias_order):
        for j in range(8):
            # CPS base con patrón semanal + variación aleatoria
            cps_base = 150 * base_pattern[i]
            cps_var = np.random.uniform(0.8, 1.2)
            cps = cps_base * cps_var
            
            # Seguidores: más en días buenos
            seg_base = 1000 / base_pattern[i]  # Inversamente proporcional al CPS
            seg_var = np.random.uniform(0.7, 1.3)
            seg = int(seg_base * seg_var)
            
            # Añadir algunos NaN (20% de probabilidad)
            if np.random.random() < 0.2:
                vals_cps_raw[i, j] = np.nan
                vals_seg[i, j] = np.nan
            else:
                vals_cps_raw[i, j] = cps
                vals_seg[i, j] = seg
    
    # CPS clip para visualización
    vals_cps_clip = np.copy(vals_cps_raw)
    finite_mask = np.isfinite(vals_cps_raw)
    if np.any(finite_mask):
        p5 = np.nanpercentile(vals_cps_raw, 5)
        p95 = np.nanpercentile(vals_cps_raw, 95)
        vals_cps_clip = np.clip(vals_cps_clip, p5, p95)
    
    # Resumen por día
    sum_day = []
    for i, dia in enumerate(dias_order):
        # Filtrar valores finitos
        valid_mask = np.isfinite(vals_seg[i, :]) & np.isfinite(vals_cps_raw[i, :])
        
        if np.any(valid_mask):
            costos_dia = np.nansum(vals_seg[i, valid_mask] * vals_cps_raw[i, valid_mask])
            seguidores_dia = np.nansum(vals_seg[i, valid_mask])
            cps_dia = costos_dia / seguidores_dia if seguidores_dia > 0 else np.nan
        else:
            costos_dia = 0
            seguidores_dia = 0
            cps_dia = np.nan
        
        sum_day.append({
            "Dia_Semana": dia,
            "Costo_sum": float(costos_dia),
            "Seguidores_sum": float(seguidores_dia),
            "CPS_total_dia": float(cps_dia) if not np.isnan(cps_dia) else np.nan
        })
    
    return {
        "status": "success",
        "plot_data": {
            "vals_cps_raw": vals_cps_raw.tolist(),
            "vals_seg": vals_seg.tolist(),
            "vals_cps_clip": vals_cps_clip.tolist(),
            "dias_order": dias_order,
            "weeks": weeks
        },
        "tables": {
            "sum_day": sum_day
        }
    }

#############################################
# FUNCIONES PARA CARGAR GRÁFICAS AVANZADAS
#############################################

def cargar_datos_grafica1():
    """Carga datos para la gráfica 1: Inversión vs Seguidores"""
    # Verificar si debemos usar datos de ejemplo
    if st.session_state.get("use_test_data", False):
        st.info("📊 Usando datos de ejemplo para Gráfica 1")
        return generar_datos_ejemplo_grafica1()
    
    try:
        r = requests.get(GRAFICA1_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Verificar estructura básica
        if data.get("status") != "success":
            st.warning("Backend no retornó status 'success'. Usando datos de ejemplo.")
            return generar_datos_ejemplo_grafica1()
        
        # Verificar que tenga los datos mínimos
        tables = data.get("tables", {})
        if not tables or not tables.get("dias_validos") or not tables.get("curva_15k"):
            st.warning("Datos incompletos del backend. Usando datos de ejemplo.")
            return generar_datos_ejemplo_grafica1()
            
        return data
        
    except Exception as e:
        st.warning(f"Error al cargar datos de gráfica 1: {str(e)[:100]}... Usando datos de ejemplo.")
        return generar_datos_ejemplo_grafica1()

def cargar_datos_grafica2():
    """Carga datos para la gráfica 2: Heatmap CPS"""
    # Verificar si debemos usar datos de ejemplo
    if st.session_state.get("use_test_data", False):
        st.info("📊 Usando datos de ejemplo para Gráfica 2")
        return generar_datos_ejemplo_grafica2()
    
    try:
        r = requests.get(GRAFICA2_URL, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        # Verificar estructura básica
        if data.get("status") != "success":
            st.warning("Backend no retornó status 'success'. Usando datos de ejemplo.")
            return generar_datos_ejemplo_grafica2()
        
        # Verificar que tenga los datos mínimos
        plot_data = data.get("plot_data", {})
        if not plot_data or not plot_data.get("vals_cps_raw"):
            st.warning("Datos incompletos del backend. Usando datos de ejemplo.")
            return generar_datos_ejemplo_grafica2()
            
        return data
        
    except Exception as e:
        st.warning(f"Error al cargar datos de gráfica 2: {str(e)[:100]}... Usando datos de ejemplo.")
        return generar_datos_ejemplo_grafica2()

def formato_numero_original(valor):
    """Formato de números igual al original (gráfica.txt)"""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    try:
        return str(int(round(float(valor))))
    except Exception:
        return "—"

def formato_k_original(valor):
    """Formato en 'k' igual al original (gráfica.txt)"""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    try:
        return f"{int(round(float(valor)/1000.0))}k"
    except Exception:
        return "—"

def crear_grafica1_interactiva(data_grafica1):
    """Crea la gráfica 1 interactiva - IDÉNTICA AL ORIGINAL"""
    if not data_grafica1 or data_grafica1.get("status") != "success":
        st.error("No se pudo cargar la gráfica 1: Datos inválidos o vacíos")
        
        # Mostrar botón para recargar
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Recargar datos", key="reload_graf1"):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="use_example_graf1"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # Extraer datos COMPLETOS del backend
    df_merge_fecha = pd.DataFrame(data_grafica1.get("tables", {}).get("df_merge_fecha", []))
    cand = pd.DataFrame(data_grafica1.get("tables", {}).get("dias_validos", []))
    curve = pd.DataFrame(data_grafica1.get("tables", {}).get("curva_15k", []))
    parameters = data_grafica1.get("parameters", {})
    summary = data_grafica1.get("results_summary", {})
    
    # Extraer datos del cálculo
    calc_data = data_grafica1.get("calc", {})
    INV_mean = calc_data.get("INV_mean", 0)
    SEG_mean = calc_data.get("SEG_mean", 0)
    opt = calc_data.get("opt", {})
    cps_min = calc_data.get("cps_min_curva", 0)
    cps_max = calc_data.get("cps_max_tol", 0)
    
    if cand.empty or curve.empty:
        st.warning("No hay datos suficientes para generar la gráfica 1")
        
        # Mostrar información de depuración
        with st.expander("🔍 Información de depuración"):
            st.write(f"Días válidos: {len(cand)} registros")
            st.write(f"Curva 15k: {len(curve)} registros")
            st.write(f"Parámetros: {parameters}")
            
            if not cand.empty:
                st.write("Primeras filas de días válidos:")
                st.dataframe(cand.head())
            
            if not curve.empty:
                st.write("Primeras filas de curva:")
                st.dataframe(curve.head())
        
        # Botones de acción
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Intentar de nuevo", key="retry_graf1"):
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="force_example_graf1"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # PARÁMETROS DEL GRÁFICO ORIGINAL
    STEP = parameters.get("STEP", 15000)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
    
    # Asegurar que las columnas necesarias existan
    if RESULT_COL not in cand.columns and "Seguidores_Impacto" in cand.columns:
        RESULT_COL = "Seguidores_Impacto"
    elif RESULT_COL not in cand.columns and "Neto_Diario_Real" in cand.columns:
        RESULT_COL = "Neto_Diario_Real"
    elif RESULT_COL not in cand.columns and len(cand.columns) > 1:
        # Usar la segunda columna como fallback
        RESULT_COL = cand.columns[1]
    
    # Función de compresión del eje X (IGUAL AL ORIGINAL)
    def x_warp(x):
        x = float(x)
        if x <= BREAK_X:
            return x
        return BREAK_X + (x - BREAK_X) * K
    
    # Aplicar compresión a los datos
    cand["xw"] = cand["Costo"].apply(x_warp)
    curve["xw"] = curve["Inversion_promedio"].apply(x_warp)
    
    # Datos del punto óptimo
    opt_x = opt.get("Inversion_promedio", 0)
    opt_y = opt.get("Seguidores_promedio", 0)
    opt_cps = opt.get("CPS_curva", 0)
    opt_dias_meta = opt.get("Dias_para_meta", 0)
    opt_dias = opt.get("Dias", 0)
    opt_xw = x_warp(opt_x)
    
    # Generar ticks del eje X (IGUAL AL ORIGINAL)
    cmin = float(cand["Costo"].min())
    cmax = float(cand["Costo"].max())
    start = float(np.floor(cmin / STEP) * STEP)
    end = float(np.ceil(cmax / STEP) * STEP) + STEP
    bins = np.arange(start, end + 1, STEP)
    
    # Filtrar bins visibles
    data_min = float(cand["Costo"].min())
    data_max = float(cand["Costo"].max())
    edge_ticks_real = np.unique(bins)
    edge_ticks_real = [x for x in edge_ticks_real if (x >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x <= (np.ceil(data_max/STEP)*STEP) + 1e-9)]
    edge_ticks_w = [x_warp(x) for x in edge_ticks_real]
    edge_tick_labels = [formato_k_original(x) for x in edge_ticks_real]
    
    # Limitar número de ticks (igual que original)
    MAX_X_TICKS = 12
    stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
    edge_ticks_real = edge_ticks_real[::stride]
    edge_ticks_w = edge_ticks_w[::stride]
    edge_tick_labels = edge_tick_labels[::stride]
    
    # Colores del gráfico original (EXACTAMENTE IGUALES)
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
        'punto_optimo': '#22c55e'
    }
    
    # Crear figura con FONDO AZUL OSCURO
    fig = go.Figure()
    
    # 1. Agregar líneas verticales para los bins (rangos de inversión)
    for x_real in bins:
        if x_real >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(data_max/STEP)*STEP) + 1e-9:
            fig.add_vline(
                x=x_warp(x_real),
                line_width=1.0,
                line_dash="dash",
                line_color="#cbd5e1",
                opacity=0.18
            )
    
    # 2. Puntos de días reales (scatter) - EXACTAMENTE IGUAL AL ORIGINAL
    fig.add_trace(go.Scatter(
        x=cand["xw"],
        y=cand[RESULT_COL],
        mode='markers',
        name='Días reales',
        marker=dict(
            size=6,
            color=colors['puntos_reales'],
            opacity=0.12,  # EXACTO: alpha=0.12
            line=dict(width=0)
        ),
        hovertemplate='<b>📅 Día Real</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<extra></extra>'
    ))
    
    # 3. Línea de curva promedio
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
    
    # 4. Puntos de la curva promedio (NARANJAS - VISIBLES SIEMPRE)
    for idx, row in curve.iterrows():
        # Crear etiqueta para cada punto (IGUAL AL ORIGINAL)
        dias_meta = row.get("Dias_para_meta", np.nan)
        label_text = (
            f"Inv {formato_numero_original(row['Inversion_promedio'])}<br>"
            f"SEG {formato_numero_original(row['Seguidores_promedio'])}<br>"
            f"CPS {formato_numero_original(row['CPS_curva'])}<br>"
            f"1000 SEG ~ {dias_meta:.1f} días<br>"
            f"Días {int(row['Dias'])}"
        )
        
        # POSICIONES FIJAS PARA ETIQUETAS (simulando el algoritmo greedy del original)
        offsets = [
            (18, 52), (18, -78), (-190, 52), (-190, -78),
            (60, 56), (60, -84), (-240, 56), (-240, -84),
            (110, 62), (110, -92), (-300, 62), (-300, -92),
            (0, 78), (0, -110), (160, 40), (160, -64),
            (-360, 40), (-360, -64)
        ]
        
        # Usar un offset basado en la posición del punto
        offset_idx = idx % len(offsets)
        dx, dy = offsets[offset_idx]
        
        # Añadir anotación SIEMPRE VISIBLE
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
            opacity=0.90
        )
    
    # 5. Puntos naranjas de la curva (MARCADORES VISIBLES)
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
    
    # 6. Punto óptimo (ESTRELLA VERDE)
    if opt_x > 0 and opt_y > 0:
        # Texto del punto óptimo (IGUAL AL ORIGINAL)
        opt_label_text = (
            f"Óptimo<br>"
            f"Inv {formato_numero_original(opt_x)}<br>"
            f"SEG {formato_numero_original(opt_y)}<br>"
            f"CPS {formato_numero_original(opt_cps)}<br>"
            f"1000 SEG ~ {opt_dias_meta:.1f} días<br>"
            f"CPS_min {formato_numero_original(cps_min)}<br>"
            f"CPS_max {formato_numero_original(cps_max)}"
        )
        
        # Añadir punto óptimo (ESTRELLA)
        fig.add_trace(go.Scatter(
            x=[opt_xw],
            y=[opt_y],
            mode='markers',
            name=f'Punto óptimo (max SEG dentro del mejor CPS, tol {int(parameters.get("OPT_CPS_TOL", 0.20)*100)}%)',
            marker=dict(
                size=25,
                color=colors['punto_optimo'],
                symbol='star',
                line=dict(width=1.8, color='white')
            ),
            hovertemplate='<b>⭐ PUNTO ÓPTIMO</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
            customdata=[opt_cps]
        ))
        
        # Añadir etiqueta del punto óptimo (POSICIÓN FIJA)
        opt_offsets = [(-320, 70), (-360, 50), (-280, 90), (-260, 40), (-400, 70)]
        opt_dx, opt_dy = opt_offsets[0]  # Usar primera posición
        
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
            opacity=0.90
        )
    
    # 7. Líneas de promedio general
    # Línea horizontal de promedio SEG
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
    
    # Línea vertical de promedio INV
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
    
    # Configurar layout COMPLETAMENTE IGUAL AL ORIGINAL
    fig.update_layout(
        height=700,
        plot_bgcolor=colors['fondo_ejes'],
        paper_bgcolor=colors['fondo_figura'],
        font=dict(color=colors['texto'], size=12, family="Arial"),
        title=dict(
            text=f"Inversión vs Seguidores (curva por niveles) — Hover/Click en puntos naranjas<br>"
                 f"<span style='font-size:14px; color:#94a3b8'>Impacto {IMPACT_DAYS}d | STEP ${STEP:,} | Compresión X: {BREAK_X/1000:.0f}k+ (K={K})</span>",
            font=dict(size=22, color='white', family="Arial Black"),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(255,255,255,0.1)',
            tickvals=edge_ticks_w,
            ticktext=edge_tick_labels,
            tickfont=dict(size=11, color=colors['ticks']),
            zeroline=False,
            showgrid=True,
            gridwidth=0.6
        ),
        yaxis=dict(
            title=f"Seguidores ({'Impacto' if USE_IMPACT else 'Neto'} {IMPACT_DAYS}d)",
            gridcolor='rgba(255,255,255,0.1)',
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
    
    # Añadir grid horizontal
    fig.update_xaxes(showgrid=True, gridwidth=0.6, gridcolor='rgba(255,255,255,0.15)')
    fig.update_yaxes(showgrid=True, gridwidth=0.6, gridcolor='rgba(255,255,255,0.15)')
    
    # Mostrar gráfica
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    # Mostrar información adicional en tarjetas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📊 Días válidos",
            f"{len(cand):,}",
            help="Total de días con inversión y seguidores positivos"
        )
    
    with col2:
        st.metric(
            "💰 Inv promedio",
            f"${INV_mean:,.0f}",
            help="Inversión promedio por día válido"
        )
    
    with col3:
        st.metric(
            "👥 SEG promedio",
            f"{SEG_mean:,.0f}",
            help="Seguidores promedio por día válido"
        )
    
    with col4:
        st.metric(
            "⭐ CPS mínimo",
            f"${cps_min:,.0f}",
            help="CPS mínimo encontrado en la curva"
        )
    
    with col5:
        cps_tol = parameters.get('OPT_CPS_TOL', 0.20)
        st.metric(
            "🎯 CPS óptimo",
            f"${opt_cps:,.0f}",
            delta=f"Tol {int(cps_tol*100)}%",
            help=f"Costo por seguidor en el punto óptimo (tolerancia {int(cps_tol*100)}%)"
        )
    
    # Mostrar tabla de datos de la curva
    with st.expander("📋 Ver datos detallados de la curva (rangos de inversión)"):
        display_curve = curve.copy()
        # Formatear como en el gráfico original
        display_curve["Inversion_promedio"] = display_curve["Inversion_promedio"].apply(lambda x: f"${x:,.0f}")
        display_curve["Seguidores_promedio"] = display_curve["Seguidores_promedio"].apply(lambda x: f"{x:,.0f}")
        display_curve["CPS_curva"] = display_curve["CPS_curva"].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A")
        display_curve["Dias_para_meta"] = display_curve["Dias_para_meta"].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
        
        # Renombrar columnas
        display_curve = display_curve.rename(columns={
            "Inversion_promedio": "💰 Inversión promedio",
            "Seguidores_promedio": "👥 Seguidores promedio",
            "CPS_curva": "📊 CPS",
            "Dias": "📅 Días en rango",
            "Dias_para_meta": "⏱️ 1000 SEG (días)"
        })
        
        st.dataframe(display_curve, use_container_width=True)
        
    # Botón para cambiar entre datos reales y de ejemplo
    st.markdown("---")
    col_switch1, col_switch2 = st.columns(2)
    
    with col_switch1:
        if st.session_state.get("use_test_data", False):
            if st.button("🔄 Cambiar a datos reales", key="switch_to_real"):
                st.session_state["use_test_data"] = False
                st.rerun()
        else:
            if st.button("🧪 Usar datos de ejemplo", key="switch_to_example"):
                st.session_state["use_test_data"] = True
                st.rerun()
    
    with col_switch2:
        if st.button("📊 Ver datos crudos", key="show_raw_data"):
            with st.expander("📁 Datos crudos de la gráfica"):
                st.write("**Parámetros:**", parameters)
                st.write("**Resumen:**", summary)
                st.write("**Cálculos:**", calc_data)
                
                st.write("**Días válidos (primeras 10 filas):**")
                st.dataframe(cand.head(10))
                
                st.write("**Curva completa:**")
                st.dataframe(curve)

def crear_grafica2_interactiva(data_grafica2):
    """Crea la gráfica 2 interactiva (Heatmap CPS) - IDÉNTICA AL ORIGINAL"""
    if not data_grafica2 or data_grafica2.get("status") != "success":
        st.error("No se pudo cargar la gráfica 2: Datos inválidos o vacíos")
        
        # Mostrar botón para recargar
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Recargar datos", key="reload_graf2"):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="use_example_graf2"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # Extraer datos COMPLETOS del backend
    heatmap_data = data_grafica2.get("plot_data", {})
    summary_by_day = pd.DataFrame(data_grafica2.get("tables", {}).get("sum_day", []))
    
    if not heatmap_data:
        st.warning("No hay datos suficientes para generar el heatmap")
        
        # Botones de acción
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Intentar de nuevo", key="retry_graf2"):
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="force_example_graf2"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # Extraer matrices del heatmap
    vals_cps_raw = np.array(heatmap_data.get("vals_cps_raw", []))
    vals_seg = np.array(heatmap_data.get("vals_seg", []))
    vals_cps_clip = np.array(heatmap_data.get("vals_cps_clip", []))
    dias_order = heatmap_data.get("dias_order", [])
    weeks = heatmap_data.get("weeks", [])
    
    if vals_cps_raw.size == 0 or len(dias_order) == 0 or len(weeks) == 0:
        st.warning("Datos del heatmap incompletos")
        
        # Mostrar información de depuración
        with st.expander("🔍 Información de depuración"):
            st.write(f"Tamaño vals_cps_raw: {vals_cps_raw.shape}")
            st.write(f"Días order: {len(dias_order)}")
            st.write(f"Semanas: {len(weeks)}")
            st.write(f"Sum day: {len(summary_by_day)} registros")
        
        return
    
    # Función para formatear números (IGUAL AL ORIGINAL)
    def fmt_int_or_dash(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return "—"
        try:
            return f"{int(round(float(x))):,}".replace(",", ".")
        except Exception:
            return "—"
    
    # Colores del gráfico original (EXACTAMENTE IGUALES)
    colors = {
        'fondo_figura': '#060913',
        'fondo_ejes': '#0b1020',
        'borde_ejes': '#334155',
        'texto': '#e0e7ff',
        'ticks': '#c7d2fe',
        'texto_celda': 'white',
        'sombra_texto': 'rgba(0, 0, 0, 0.45)'
    }
    
    # Calcular percentiles para recorte de color (p5-p95) IGUAL AL ORIGINAL
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
    
    # Crear texto para cada celda - ETIQUETAS SIEMPRE VISIBLES (IGUAL AL ORIGINAL)
    text_matrix = []
    hover_text_matrix = []
    for i in range(len(vals_cps_raw)):
        row_text = []
        row_hover = []
        for j in range(len(vals_cps_raw[i])):
            cps_v = vals_cps_raw[i, j]
            seg_v = vals_seg[i, j]
            if np.isfinite(cps_v) and cps_v > 0:
                # Formato EXACTO: CPS y Seg en dos líneas
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
        # Crear heatmap con colores invertidos (RdYlGn_r) - IGUAL AL ORIGINAL
        fig = go.Figure(data=go.Heatmap(
            z=vals_cps_clip,
            x=weeks,
            y=dias_order,
            colorscale='RdYlGn_r',  # EXACTO: rojo (malo) a verde (bueno) INVERTIDO
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
        
        # Configurar layout - FONDO AZUL OSCURO IGUAL AL ORIGINAL
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
                autorange="reversed",  # IGUAL AL ORIGINAL: Lunes arriba
                tickfont=dict(size=12, color=colors['ticks'], family="Arial"),
                title_font=dict(size=13, color=colors['texto'])
            ),
            margin=dict(l=80, r=50, t=120, b=80)
        )
        
        # Añadir grid como en el original (líneas finas)
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
        
        # Añadir anotaciones para explicar colores
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
        
        # Mostrar heatmap
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
        
        # Gráfico de barras para resumen por día (BARRA DERECHA) - IGUAL AL ORIGINAL
        if not summary_by_day.empty:
            # Ordenar por día de semana (Lunes a Domingo) - IGUAL AL ORIGINAL
            dias_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            summary_by_day['Dia_Semana'] = pd.Categorical(
                summary_by_day['Dia_Semana'], 
                categories=dias_order, 
                ordered=True
            )
            summary_by_day = summary_by_day.sort_values('Dia_Semana')
            
            # Crear gráfico de barras HORIZONTAL - IGUAL AL ORIGINAL (barra derecha)
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
                    autorange="reversed"  # IGUAL AL ORIGINAL: Lunes arriba
                ),
                hovermode='y',
                margin=dict(l=20, r=50, t=80, b=80),
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Mostrar tabla de resumen por día
        with st.expander("📋 Ver datos detallados del heatmap"):
            if not summary_by_day.empty:
                display_summary = summary_by_day.copy()
                # Formatear
                display_summary["Costo_sum"] = display_summary["Costo_sum"].apply(lambda x: f"${x:,.0f}")
                display_summary["Seguidores_sum"] = display_summary["Seguidores_sum"].apply(lambda x: f"{x:,.0f}")
                display_summary["CPS_total_dia"] = display_summary["CPS_total_dia"].apply(
                    lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
                )
                
                # Renombrar
                display_summary = display_summary.rename(columns={
                    "Dia_Semana": "📅 Día",
                    "Costo_sum": "💰 Costo total",
                    "Seguidores_sum": "👥 Seguidores total",
                    "CPS_total_dia": "📊 CPS total"
                })
                
                st.dataframe(display_summary, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error al crear heatmap: {str(e)}")
        st.info("Mostrando datos en formato de tabla como respaldo...")
        
        # Mostrar datos en tabla como respaldo
        if len(vals_cps_raw) > 0 and len(weeks) > 0:
            heatmap_df = pd.DataFrame(vals_cps_raw, index=dias_order, columns=weeks)
            st.dataframe(heatmap_df.style.format("${:,.0f}"))
    
    # Botón para cambiar entre datos reales y de ejemplo
    st.markdown("---")
    col_switch1, col_switch2 = st.columns(2)
    
    with col_switch1:
        if st.session_state.get("use_test_data", False):
            if st.button("🔄 Cambiar a datos reales", key="switch_to_real_2"):
                st.session_state["use_test_data"] = False
                st.rerun()
        else:
            if st.button("🧪 Usar datos de ejemplo", key="switch_to_example_2"):
                st.session_state["use_test_data"] = True
                st.rerun()
    
    with col_switch2:
        if st.button("📊 Ver datos crudos", key="show_raw_data_2"):
            with st.expander("📁 Datos crudos del heatmap"):
                st.write("**Días order:**", dias_order)
                st.write("**Semanas:**", weeks)
                
                if len(vals_cps_raw) > 0:
                    st.write(f"**Matriz CPS raw (forma: {vals_cps_raw.shape}):**")
                    st.write(vals_cps_raw)
                
                if not summary_by_day.empty:
                    st.write("**Resumen por día:**")
                    st.dataframe(summary_by_day)

#############################################
# FIN FUNCIONES GRÁFICAS COMPLETAMENTE REESCRITAS
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

/* Gráficas avanzadas - CONTENEDOR AZUL OSCURO */
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

/* Tabs para gráficas */
.grafica-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 25px;
    flex-wrap: wrap;
}

.grafica-tab {
    padding: 12px 24px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    color: #cbd5e1;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-family: 'Arial', sans-serif;
}

.grafica-tab:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.grafica-tab.active {
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    color: white;
    border-color: transparent;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

/* Botones de acción */
.action-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 8px;
    background: linear-gradient(135deg, #10b981 0%, #3B82F6 100%);
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    text-decoration: none;
    font-family: 'Arial', sans-serif;
}

.action-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

/* Tooltips */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted #666;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #1e293b;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
    border: 1px solid #334155;
    font-family: 'Arial', sans-serif;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Etiquetas de gráficas */
.chart-label {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    color: white !important;
}

.heatmap-cell {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    font-size: 10px !important;
}

/* Leyenda mejorada */
.legend-item {
    font-family: 'Arial', sans-serif !important;
    font-weight: 600 !important;
}

/* Ejes mejorados */
.axis-label {
    font-family: 'Arial Black', sans-serif !important;
    font-weight: 800 !important;
    color: #c7d2fe !important;
}

/* Texto en gráficas */
.chart-text {
    font-family: 'Arial', sans-serif !important;
    font-weight: 500 !important;
}

/* Botones de control gráficas */
.control-button {
    margin: 5px;
    padding: 8px 16px;
    border-radius: 8px;
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    font-family: 'Arial', sans-serif;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.control-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.control-button.secondary {
    background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
}

</style>
""", unsafe_allow_html=True)

# Cargar datos
df_all, youtobe_df, tiktok_df, df_followers, df_pauta = cargar_datos()

# Inicializar estado de sesión para datos de ejemplo
if "use_test_data" not in st.session_state:
    st.session_state["use_test_data"] = False

if "selected_platform" not in st.session_state:
    st.session_state["selected_platform"] = "general"

if "show_grafica1" not in st.session_state:
    st.session_state["show_grafica1"] = False

if "show_grafica2" not in st.session_state:
    st.session_state["show_grafica2"] = False

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
        <h2 style="color: white; margin-bottom: 4px; font-size: 20px; font-family: 'Arial Black', sans-serif;">DASHBOARD PRO</h2>
        <p style="color: #94a3b8; font-size: 12px; margin: 0; font-family: 'Arial', sans-serif;">Social Media Analytics v3.2</p>
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
        st.markdown(f'<div class="backend-status backend-disconnected">⚠️ Backend Offline: {str(e)[:50]}</div>', unsafe_allow_html=True)
    
    # Estado de datos de ejemplo
    if st.session_state.get("use_test_data", False):
        st.markdown('<div class="backend-status backend-connected">🧪 Usando datos de ejemplo</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">🔗 Panel Professional</p>', unsafe_allow_html=True)
    
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
    
    # Nueva sección para gráficas avanzadas
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📊 GRÁFICAS AVANZADAS</p>', unsafe_allow_html=True)
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        if st.button("📈 Gráfica 1", key="grafica1_btn", use_container_width=True, 
                    help="Inversión vs Seguidores - Análisis de eficiencia"):
            st.session_state["show_grafica1"] = True
            st.session_state["show_grafica2"] = False
            st.rerun()
    
    with col_graf2:
        if st.button("📊 Gráfica 2", key="grafica2_btn", use_container_width=True,
                    help="Heatmap CPS - Análisis por día y semana"):
            st.session_state["show_grafica2"] = True
            st.session_state["show_grafica1"] = False
            st.rerun()
    
    # Botón para verificar backend
    if st.button("🔍 Verificar Backend", key="check_backend", use_container_width=True):
        with st.spinner("Verificando endpoints..."):
            status = verificar_backend()
            with st.expander("Resultados de verificación", expanded=True):
                for nombre, info in status.items():
                    st.write(f"**{nombre}:** {info['estado']}")
                    st.write(f"URL: `{info['url']}`")
                    if info['datos']:
                        st.write(f"Datos: {str(info['datos'])[:100]}...")
                    st.divider()
    
    # Botón para datos de ejemplo
    if st.session_state.get("use_test_data", False):
        if st.button("🔄 Cambiar a datos reales", key="switch_to_real_sidebar", use_container_width=True):
            st.session_state["use_test_data"] = False
            st.rerun()
    else:
        if st.button("🧪 Usar datos de ejemplo", key="use_example_sidebar", use_container_width=True):
            st.session_state["use_test_data"] = True
            st.rerun()
    
    # Botón para ocultar gráficas
    if st.session_state.get("show_grafica1", False) or st.session_state.get("show_grafica2", False):
        if st.button("⬅️ Volver a Dashboard", key="back_dashboard", use_container_width=True):
            st.session_state["show_grafica1"] = False
            st.session_state["show_grafica2"] = False
            st.rerun()
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # Filtros de tiempo cuando no está en modo GENERAL
    if selected_platform != "general":
        st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📅 Filtros de Tiempo</p>', unsafe_allow_html=True)
        
        tiempo_filtro = st.selectbox(
            "Seleccionar período:",
            ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Todo el período"],
            key="tiempo_filtro"
        )
    
    st.markdown('<p class="sidebar-title" style="font-family: Arial Black, sans-serif;">📈 Status Conexiones</p>', unsafe_allow_html=True)
    
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
                <span style="color: #e2e8f0; font-family: 'Arial', sans-serif;">{platform}</span>
                <span class="{status_class}" style="font-family: 'Arial', sans-serif;">{icon} {status.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Contenido principal
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

# ================================================================
# SECCIÓN: GRÁFICAS AVANZADAS (si están activadas)
# ================================================================

# Gráfica 1: Inversión vs Seguidores
if st.session_state.get("show_grafica1", False):
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 style="font-family: 'Arial Black', sans-serif;">📈 GRÁFICA 1: INVERSIÓN VS SEGUIDORES</h1>
        <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px; font-weight: 400; font-family: 'Arial', sans-serif;">
            Análisis de eficiencia por nivel de inversión • CPS (Costo por Seguidor) • Punto óptimo
        </p>
        <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8; font-family: 'Arial', sans-serif;">
            Actualizado: {current_time}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Cargando datos de la gráfica 1..."):
        data_grafica1 = cargar_datos_grafica1()
        crear_grafica1_interactiva(data_grafica1)
    
    st.stop()

# Gráfica 2: Heatmap CPS
elif st.session_state.get("show_grafica2", False):
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 style="font-family: 'Arial Black', sans-serif;">📊 GRÁFICA 2: HEATMAP CPS (COSTO POR SEGUIDOR)</h1>
        <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 15px; font-weight: 400; font-family: 'Arial', sans-serif;">
            Análisis por día de semana y semana ISO • CPS bajo = mejor eficiencia
        </p>
        <div style="position: absolute; bottom: 15px; right: 25px; font-size: 13px; opacity: 0.8; font-family: 'Arial', sans-serif;">
            Actualizado: {current_time}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Cargando datos de la gráfica 2..."):
        data_grafica2 = cargar_datos_grafica2()
        crear_grafica2_interactiva(data_grafica2)
    
    st.stop()

# ================================================================
# DASHBOARD NORMAL (si no se están mostrando gráficas avanzadas)
# ================================================================

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
    
    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Recargar datos", key="reload_main"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("🧪 Usar datos de ejemplo", key="use_example_main"):
            st.session_state["use_test_data"] = True
            st.rerun()
    
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
        total_followers = int(df_followers['Seguidores_Totales'].iloc[-1] if len(df_followers) > 0 else 0)

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
    st.markdown(f'<h2 style="margin: 0; color: {platform_color}; font-size: 26px; text-align: center; font-family: Arial Black, sans-serif;">{platform_name} ANALYTICS</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; text-align: center; font-family: Arial, sans-serif;">{total_posts} contenidos analizados • Última actualización: {current_time_short}</p>', unsafe_allow_html=True)
    if selected_platform != "general":
        st.markdown(f'<p style="margin: 2px 0 0 0; color: #9ca3af; font-size: 11px; text-align: center; font-family: Arial, sans-serif;">Filtro: {st.session_state.get("tiempo_filtro", "Todo el período")}</p>', unsafe_allow_html=True)

with col_header3:
    st.markdown(f'''
    <div style="background: {platform_color}15; color: {platform_color}; padding: 8px 18px; 
                border-radius: 18px; font-size: 13px; font-weight: 600; text-align: center; 
                border: 1px solid {platform_color}30; font-family: Arial Black, sans-serif;">
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
            <h3 style="margin: 0; color: #0369a1; font-size: 20px; display: flex; align-items: center; gap: 8px; font-family: Arial Black, sans-serif;">
                📢 MÉTRICAS DE PAUTA PUBLICITARIA (SUMAS)
            </h3>
            <div style="color: #64748b; font-size: 12px; background: white; padding: 5px 12px; border-radius: 15px; border: 1px solid #cbd5e1; font-family: Arial, sans-serif;">
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
            <div class="pauta-label" style="font-family: Arial, sans-serif;">COSTE ANUNCIO</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">${coste_anuncio}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma total en pesos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta2:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES VIDEOS</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">{visualizaciones_videos}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma de reproducciones</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pauta3:
        st.markdown(f"""
        <div class="pauta-card">
            <div class="pauta-label" style="font-family: Arial, sans-serif;">NUEVOS SEGUIDORES</div>
            <div class="pauta-value" style="font-family: Arial Black, sans-serif;">{nuevos_seguidores}</div>
            <div class="pauta-period" style="font-family: Arial, sans-serif;">Suma de audiencia ganada</div>
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
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL SEGUIDORES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_followers:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👥 TikTok Followers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL CONTENIDOS</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_posts}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES TOTALES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_views:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">RENDIMIENTO DIARIO</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TASA DE ENGAGEMENT</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
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
            <div class="metric-label" style="font-family: Arial, sans-serif;">TOTAL CONTENIDOS</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_posts}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>📈 Contenido Activo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">VISUALIZACIONES TOTALES</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{total_views:,}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>👁️ Alcance Total</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">RENDIMIENTO DIARIO</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{avg_daily_perf:.1f}</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>🚀 Views/Día</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="font-family: Arial, sans-serif;">TASA DE ENGAGEMENT</div>
            <div class="metric-value" style="font-family: Arial Black, sans-serif;">{engagement_rate:.2f}%</div>
            <div class="metric-trend trend-up" style="font-family: Arial, sans-serif;">
                <span>💬 Interacción</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# SECCIÓN: GRÁFICA DE SEGUIDORES Y PAUTA (solo para GENERAL y TikTok)
if (selected_platform == "general" or selected_platform == "tiktok") and not df_followers.empty and 'Fecha' in df_followers.columns and 'Seguidores_Totales' in df_followers.columns:
    st.markdown("""
    <div class="performance-chart">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
                📈 EVOLUCIÓN DE SEGUIDORES TIKTOK Y MÉTRICAS DE PAUTA
            </h3>
            <div style="color: #6b7280; font-size: 12px; font-family: Arial, sans-serif;">
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
        <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
            📈 PERFORMANCE OVER TIME - EVOLUCIÓN DETALLADA
        </h3>
        <div style="color: #6b7280; font-size: 12px; font-family: Arial, sans-serif;">
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
            <h3 style="margin: 0; color: #1f2937; font-size: 20px; font-family: Arial Black, sans-serif;">
                📊 CONTENT PERFORMANCE DATA - TABLA COMPLETA
            </h3>
            <p style="margin: 4px 0 0 0; color: #6b7280; font-size: 13px; font-family: Arial, sans-serif;">
                Lista completa de contenidos con todos los detalles
            </p>
        </div>
        <div style="color: #6b7280; font-size: 12px; background: #f8fafc; padding: 6px 14px; border-radius: 18px; border: 1px solid #e5e7eb; font-family: Arial, sans-serif;">
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
            <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-family: Arial Black, sans-serif;">
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
            <h4 style="margin: 0 0 12px 0; color: #374151; font-size: 15px; font-family: Arial Black, sans-serif;">📈 ANÁLISIS DE PERFORMANCE</h4>
            <div style="color: #4b5563; font-size: 13px; font-family: Arial, sans-serif;">
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
            <h3 style="margin: 0; color: #1f2937; font-size: 18px; font-family: Arial Black, sans-serif;">
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
                    <span style="color: #4b5563; font-size: 13px; font-weight: 500; font-family: Arial, sans-serif;">{metric_name}</span>
                </div>
                <span style="font-weight: 700; color: #1f2937; font-size: 14px; font-family: Arial Black, sans-serif;">
                    {value}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis de engagement avanzado
        st.markdown("""
        <div style="margin-top: 18px; padding: 18px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                    border-radius: 12px; border-left: 4px solid #0ea5e9;">
            <h4 style="margin: 0 0 10px 0; color: #374151; font-size: 15px; font-family: Arial Black, sans-serif;">📊 ANÁLISIS DE ENGAGEMENT AVANZADO</h4>
            <div style="color: #4b5563; font-size: 13px; font-family: Arial, sans-serif;">
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
    <div style="display: flex; justify-content: center; gap: 25px; margin-bottom: 12px; flex-wrap: wrap; font-family: Arial, sans-serif;">
        <span>Social Media Dashboard PRO v3.2</span>
        <span>•</span>
        <span>Data from Backend API</span>
        <span>•</span>
        <span>{platform_name} Analytics</span>
        <span>•</span>
        <span>Updated in Real-time</span>
        <span>•</span>
        <span>Gráficas Avanzadas: Inversión vs Seguidores • Heatmap CPS</span>
    </div>
    <div style="font-size: 11px; color: #9ca3af; font-family: Arial, sans-serif;">
        © 2025 Social Media Analytics Platform • Connected to: <strong>{BACKEND_URL}</strong> • {current_time_full}
    </div>
</div>
""", unsafe_allow_html=True)
