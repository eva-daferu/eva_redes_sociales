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
# CONSTANTES PARA ETIQUETAS (IGUAL AL ORIGINAL)
#############################################
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

OPT_LABEL_OFFSETS = [(-320, 70), (-360, 50), (-280, 90), (-260, 40), (-400, 70)]

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
    
    # Generar datos de días válidos REALISTAS (valores bajos como en el ejemplo real)
    np.random.seed(42)  # Para reproducibilidad
    
    # Valores REALISTAS - inversiones bajas como en el ejemplo real
    dias_validos = []
    inversiones_realistas = [15000, 25000, 30000, 18000, 22000, 28000, 32000, 19000, 21000]
    for i, inv_base in enumerate(inversiones_realistas):
        # Variación del 20% alrededor del valor base
        costo = np.random.randint(int(inv_base * 0.8), int(inv_base * 1.2))
        # Seguidores proporcionales (entre 100-300 como en ejemplo real)
        seguidores = np.random.randint(100, 300)
        dias_validos.append({
            "Costo": float(costo),
            "Seguidores_Impacto": float(seguidores),
            "Neto_Diario_Real": float(seguidores)
        })
    
    # Agregar algunos días más
    for i in range(10):
        costo = np.random.randint(10000, 35000)
        seguidores = np.random.randint(50, 250)
        dias_validos.append({
            "Costo": float(costo),
            "Seguidores_Impacto": float(seguidores),
            "Neto_Diario_Real": float(seguidores)
        })
    
    # Generar curva promedio CON VALORES REALISTAS
    curva_15k = []
    for inv in range(15000, 100001, 15000):
        # Seguidores proporcionales a la inversión (valores realistas bajos)
        seg_prom = int(inv * np.random.uniform(0.005, 0.015))
        cps = inv / seg_prom if seg_prom > 0 else 0
        dias_para_meta = 1000 / (seg_prom / 30) if seg_prom > 0 else 0
        dias_en_rango = np.random.randint(2, 8)  # Pocos días por rango (realista)
        curva_15k.append({
            "Inversion_promedio": float(inv),
            "Seguidores_promedio": float(seg_prom),
            "CPS_curva": float(cps),
            "Dias_para_meta": float(dias_para_meta),
            "Dias": int(dias_en_rango)
        })
    
    # Calcular promedios REALES desde los datos generados
    costos = [d["Costo"] for d in dias_validos]
    seguidores = [d["Seguidores_Impacto"] for d in dias_validos]
    
    # Punto óptimo (aproximadamente en el 60% del rango)
    opt_idx = int(len(curva_15k) * 0.6)
    if opt_idx < len(curva_15k):
        opt_point = curva_15k[opt_idx]
    else:
        opt_point = curva_15k[-1]
    
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
            "OPT_MIN_DAYS": 3,
            "OPT_CPS_TOL": 0.20,
            "TARGET_FOLLOWERS": 1000
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
    """Crea la gráfica 1 interactiva - CON CÁLCULOS CORREGIDOS"""
    if not data_grafica1 or data_grafica1.get("status") != "success":
        st.error("No se pudo cargar la gráfica 1: Datos inválidos o vacíos")
        
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
    
    # Extraer datos del backend
    df_merge_fecha = pd.DataFrame(data_grafica1.get("tables", {}).get("df_merge_fecha", []))
    cand_raw = pd.DataFrame(data_grafica1.get("tables", {}).get("dias_validos", []))
    curve_raw = pd.DataFrame(data_grafica1.get("tables", {}).get("curva_15k", []))
    parameters = data_grafica1.get("parameters", {})
    summary = data_grafica1.get("results_summary", {})
    calc_data = data_grafica1.get("calc", {})
    
    # Parámetros CRÍTICOS (tomar del código original si no vienen)
    STEP = parameters.get("STEP", 15000)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    OPT_MIN_DAYS = parameters.get("OPT_MIN_DAYS", 3)
    OPT_CPS_TOL = parameters.get("OPT_CPS_TOL", 0.20)
    TARGET_FOLLOWERS = parameters.get("TARGET_FOLLOWERS", 1000)
    
    # COLUMNA RESULTADO CORRECTA (igual que original)
    RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
    
    # =========================================================================
    # CÁLCULOS CORREGIDOS - IGUAL AL CÓDIGO ORIGINAL
    # =========================================================================
    
    # Función de compresión X (igual que original)
    def x_warp(x):
        x = float(x)
        if x <= BREAK_X:
            return x
        return BREAK_X + (x - BREAK_X) * K
    
    # Función para encontrar punto óptimo (igual que original)
    def pick_optimal_point_seg_then_cps(df_curve, min_days=3, cps_tol=0.20):
        d = df_curve.copy()
        
        # Filtrar puntos válidos (igual que original)
        m = (
            d["Inversion_promedio"].notna() &
            d["Seguidores_promedio"].notna() &
            d["CPS_curva"].notna() &
            (d["Inversion_promedio"] > 0) &
            (d["Seguidores_promedio"] > 0) &
            (d["CPS_curva"] > 0) &
            (d["Dias"] >= int(min_days))
        )
        d = d[m].copy()
        
        if d.empty:
            # Si no hay puntos válidos, usar los primeros disponibles
            d = df_curve.copy()
            if d.empty:
                return None, 0, 0
        
        # Calcular CPS mínimo y máximo con tolerancia
        cps_min = float(d["CPS_curva"].min())
        cps_max = cps_min * (1.0 + float(cps_tol))
        
        # Filtrar por CPS dentro de la tolerancia
        d2 = d[d["CPS_curva"] <= cps_max].copy()
        if d2.empty:
            d2 = d.copy()
        
        # Ordenar: primero por más seguidores, luego por menor CPS, luego por menor inversión
        d2 = d2.sort_values(
            by=["Seguidores_promedio", "CPS_curva", "Inversion_promedio"],
            ascending=[False, True, True]
        )
        
        return d2.iloc[0].copy(), cps_min, cps_max
    
    # PROCESAR DATOS DE ENTRADA
    cand = cand_raw.copy()
    curve = curve_raw.copy()
    
    # Asegurar que tenemos las columnas necesarias en cand
    if cand.empty:
        st.error("No hay días válidos para calcular la gráfica")
        return
    
    # Asegurar columnas en cand
    required_cand_cols = ["Costo", RESULT_COL]
    for col in required_cand_cols:
        if col not in cand.columns:
            st.error(f"Falta columna requerida en días válidos: {col}")
            st.write("Columnas disponibles en cand:", cand.columns.tolist())
            return
    
    # Asegurar columnas en curve
    required_curve_cols = ["Inversion_promedio", "Seguidores_promedio", "CPS_curva", "Dias"]
    for col in required_curve_cols:
        if col not in curve.columns:
            st.error(f"Falta columna requerida en curva: {col}")
            st.write("Columnas disponibles en curve:", curve.columns.tolist())
            return
    
    # Calcular promedios reales desde cand (NO usar los que vienen)
    INV_mean = float(cand["Costo"].mean())
    SEG_mean = float(cand[RESULT_COL].mean())
    
    # Asegurar que la curva tenga CPS calculado correctamente
    if "CPS_curva" not in curve.columns or curve["CPS_curva"].isna().all():
        mask = (curve["Inversion_promedio"] > 0) & (curve["Seguidores_promedio"] > 0)
        curve.loc[mask, "CPS_curva"] = curve.loc[mask, "Inversion_promedio"] / curve.loc[mask, "Seguidores_promedio"]
    
    # Asegurar que la curva tenga días para meta
    if "Dias_para_meta" not in curve.columns:
        mask = curve["Seguidores_promedio"].notna() & (curve["Seguidores_promedio"] > 0)
        curve.loc[mask, "Dias_para_meta"] = TARGET_FOLLOWERS / curve.loc[mask, "Seguidores_promedio"]
    
    # Encontrar punto óptimo (CALCULARLO, no usar el que viene)
    opt, cps_min, cps_max = pick_optimal_point_seg_then_cps(
        curve, 
        min_days=OPT_MIN_DAYS, 
        cps_tol=OPT_CPS_TOL
    )
    
    if opt is not None:
        opt_x = float(opt["Inversion_promedio"])
        opt_y = float(opt["Seguidores_promedio"])
        opt_cps = float(opt["CPS_curva"])
        opt_dias_meta = float(opt.get("Dias_para_meta", 0))
        opt_dias = int(opt.get("Dias", 0))
    else:
        # Valores por defecto si no se puede calcular
        opt_x = 0
        opt_y = 0
        opt_cps = 0
        opt_dias_meta = 0
        opt_dias = 0
    
    # Aplicar compresión X a los datos
    cand["xw"] = cand["Costo"].apply(x_warp)
    curve["xw"] = curve["Inversion_promedio"].apply(x_warp)
    opt_xw = x_warp(opt_x) if opt_x > 0 else 0
    
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
    
    # Limitar número de ticks
    MAX_X_TICKS = 12
    stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
    edge_ticks_real = edge_ticks_real[::stride]
    edge_ticks_w = edge_ticks_w[::stride]
    edge_tick_labels = edge_tick_labels[::stride]
    
    # =========================================================================
    # CREAR GRÁFICA (DISEÑO IDÉNTICO)
    # =========================================================================
    
    # Colores del gráfico original
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
    
    # Crear figura
    fig = go.Figure()
    
    # 1. Agregar líneas verticales para los bins
    for x_real in bins:
        if x_real >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(data_max/STEP)*STEP) + 1e-9:
            fig.add_vline(
                x=x_warp(x_real),
                line_width=1.0,
                line_dash="dash",
                line_color="#cbd5e1",
                opacity=0.18
            )
    
    # 2. Puntos de días reales
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
    
    # 4. Puntos de la curva promedio con etiquetas
    for idx, row in curve.iterrows():
        # Solo mostrar etiquetas para puntos con datos válidos
        if pd.isna(row["Inversion_promedio"]) or pd.isna(row["Seguidores_promedio"]):
            continue
            
        # Crear etiqueta (formato original)
        dias_meta = row.get("Dias_para_meta", np.nan)
        label_text = (
            f"Inv {formato_numero_original(row['Inversion_promedio'])}<br>"
            f"SEG {formato_numero_original(row['Seguidores_promedio'])}<br>"
            f"CPS {formato_numero_original(row['CPS_curva'])}<br>"
            f"1000 SEG ~ {dias_meta:.1f} días<br>"
            f"Días {int(row['Dias'])}"
        )
        
        # Usar offset basado en la posición
        offset_idx = idx % len(LABEL_OFFSETS)
        dx, dy = LABEL_OFFSETS[offset_idx]
        
        # Añadir anotación
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
    
    # 5. Puntos naranjas de la curva (marcadores visibles)
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
    
    # 6. Punto óptimo (ESTRELLA VERDE) - solo si existe
    if opt_x > 0 and opt_y > 0:
        # Texto del punto óptimo
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
        
        # Añadir etiqueta del punto óptimo
        opt_offset_idx = 0
        opt_dx, opt_dy = OPT_LABEL_OFFSETS[opt_offset_idx]
        
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
    
    # Configurar layout
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
    
    # =========================================================================
    # INFORMACIÓN ADICIONAL CON CÁLCULOS CORRECTOS
    # =========================================================================
    
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
            help="Inversión promedio por día válido (calculado desde datos)"
        )
    
    with col3:
        st.metric(
            "👥 SEG promedio",
            f"{SEG_mean:,.0f}",
            help="Seguidores promedio por día válido (calculado desde datos)"
        )
    
    with col4:
        st.metric(
            "⭐ CPS mínimo",
            f"${cps_min:,.0f}",
            help="CPS mínimo encontrado en la curva"
        )
    
    with col5:
        st.metric(
            "🎯 CPS óptimo",
            f"${opt_cps:,.0f}",
            delta=f"Tol {int(OPT_CPS_TOL*100)}%",
            help=f"Costo por seguidor en el punto óptimo (tolerancia {int(OPT_CPS_TOL*100)}%)"
        )
    
    # Mostrar tabla de datos de la curva CON VALORES REALES
    with st.expander("📋 Ver datos detallados de la curva (rangos de inversión) - VALORES REALES"):
        display_curve = curve.copy()
        
        # Formatear como en el gráfico original
        display_curve["Inversion_promedio"] = display_curve["Inversion_promedio"].apply(
            lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["Seguidores_promedio"] = display_curve["Seguidores_promedio"].apply(
            lambda x: f"{x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["CPS_curva"] = display_curve["CPS_curva"].apply(
            lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["Dias_para_meta"] = display_curve["Dias_para_meta"].apply(
            lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A"
        )
        
        # Renombrar columnas
        display_curve = display_curve.rename(columns={
            "Inversion_promedio": "💰 Inversión promedio",
            "Seguidores_promedio": "👥 Seguidores promedio",
            "CPS_curva": "📊 CPS",
            "Dias": "📅 Días en rango",
            "Dias_para_meta": "⏱️ 1000 SEG (días)"
        })
        
        st.dataframe(display_curve, use_container_width=True)
        
        # Mostrar información de parámetros
        st.info(f"""
        **Parámetros usados:**
        - STEP: ${STEP:,}
        - Impacto días: {IMPACT_DAYS}
        - Uso impacto: {USE_IMPACT}
        - Mínimo días para óptimo: {OPT_MIN_DAYS}
        - Tolerancia CPS: {int(OPT_CPS_TOL*100)}%
        - Compresión X: {BREAK_X/1000:.0f}k+ (K={K})
        """)
    
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
        if st.button("📊 Ver datos crudos y cálculos", key="show_raw_data"):
            with st.expander("📁 Datos crudos y cálculos detallados"):
                st.write("**Parámetros usados:**", parameters)
                st.write("**Resumen del backend:**", summary)
                st.write("**Cálculos realizados:**", {
                    "INV_mean": INV_mean,
                    "SEG_mean": SEG_mean,
                    "cps_min": cps_min,
                    "cps_max": cps_max,
                    "opt_x": opt_x,
                    "opt_y": opt_y,
                    "opt_cps": opt_cps,
                    "opt_dias_meta": opt_dias_meta,
                    "opt_dias": opt_dias
                })
                
                st.write("**Días válidos (primeras 10 filas):**")
                st.dataframe(cand[["Costo", RESULT_COL]].head(10))
                
                st.write("**Curva completa con cálculos:**")
                st.dataframe(curve)
                
                # Mostrar advertencia si los datos parecen incorrectos
                if INV_mean > 200000:
                    st.warning("⚠️ **ADVERTENCIA:** La inversión promedio parece muy alta. Verificar los datos de entrada.")
                if len(cand) < 5:
                    st.warning("⚠️ **ADVERTENCIA:** Muy pocos días válidos. Los resultados pueden no ser confiables.")

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
