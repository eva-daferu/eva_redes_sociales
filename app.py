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
    """Genera datos de ejemplo para la gráfica 1 usando la misma lógica de grafica Principal.txt"""
    import numpy as np
    
    # Crear datos realistas basados en los datos reales del usuario
    # Basado en los datos: inversiones reales entre ~$10,000 y ~$70,000
    
    # Generar 30 días de datos
    np.random.seed(42)
    n_dias = 30
    
    # Patrón realista: la mayoría de días con inversión baja, algunos picos
    inversiones_base = np.random.lognormal(9, 0.5, n_dias)  # Media alrededor de $10,000
    # Añadir algunos picos ocasionales
    picos = np.random.choice(n_dias, size=5, replace=False)
    inversiones_base[picos] = inversiones_base[picos] * np.random.uniform(2, 4, 5)
    
    # Seguidores proporcionales a la inversión pero con rendimiento decreciente
    seguidores_base = inversiones_base * np.random.uniform(0.01, 0.03, n_dias)
    # Añadir variabilidad
    seguidores_base = seguidores_base * np.random.uniform(0.7, 1.3, n_dias)
    
    # Crear DataFrame de días válidos
    dias_validos = []
    for i in range(n_dias):
        costo = max(10000, min(80000, inversiones_base[i]))
        seguidores = max(50, min(2000, seguidores_base[i]))
        dias_validos.append({
            "Costo": float(costo),
            "Seguidores_Impacto": float(seguidores),
            "Neto_Diario_Real": float(seguidores),
            "CPS_real": float(costo / seguidores) if seguidores > 0 else np.nan
        })
    
    # Filtrar solo días válidos (costo > 0, seguidores > 0)
    dias_validos = [d for d in dias_validos if d["Costo"] > 0 and d["Seguidores_Impacto"] > 0]
    
    # Calcular rangos de inversión (STEP = 15000)
    STEP = 15000
    BREAK_X = 80000.0
    K = 0.28
    
    # Obtener min y max de costos
    costos = [d["Costo"] for d in dias_validos]
    cmin = min(costos)
    cmax = max(costos)
    
    # Crear bins
    start = np.floor(cmin / STEP) * STEP
    end = np.ceil(cmax / STEP) * STEP + STEP
    bins = np.arange(start, end + 1, STEP)
    
    # Agrupar por bins
    curva_data = []
    for i in range(len(bins) - 1):
        bin_min = bins[i]
        bin_max = bins[i + 1]
        
        # Filtrar días en este bin
        dias_en_bin = [d for d in dias_validos if bin_min <= d["Costo"] < bin_max]
        
        if len(dias_en_bin) > 0:
            inv_prom = np.mean([d["Costo"] for d in dias_en_bin])
            seg_prom = np.mean([d["Seguidores_Impacto"] for d in dias_en_bin])
            cps_curva = inv_prom / seg_prom if seg_prom > 0 else np.nan
            dias_meta = 1000 / (seg_prom / 30) if seg_prom > 0 else np.nan
            
            curva_data.append({
                "Inversion_promedio": float(inv_prom),
                "Seguidores_promedio": float(seg_prom),
                "CPS_curva": float(cps_curva),
                "Dias_para_meta": float(dias_meta),
                "Dias": len(dias_en_bin)
            })
    
    # Calcular promedios generales
    inv_mean = np.mean([d["Costo"] for d in dias_validos])
    seg_mean = np.mean([d["Seguidores_Impacto"] for d in dias_validos])
    
    # Encontrar punto óptimo (simplificado)
    if curva_data:
        # Ordenar por CPS (menor es mejor) y luego por seguidores
        curva_ordenada = sorted(curva_data, key=lambda x: (x["CPS_curva"], -x["Seguidores_promedio"]))
        opt_point = curva_ordenada[0] if curva_ordenada else None
    else:
        opt_point = None
    
    return {
        "status": "success",
        "tables": {
            "df_merge_fecha": [],
            "dias_validos": dias_validos,
            "curva_15k": curva_data
        },
        "parameters": {
            "STEP": STEP,
            "BREAK_X": BREAK_X,
            "K": K,
            "IMPACT_DAYS": 3,
            "USE_IMPACT": True,
            "OPT_CPS_TOL": 0.20,
            "OPT_MIN_DAYS": 3,
            "TARGET_FOLLOWERS": 1000
        },
        "results_summary": {
            "total_dias_validos": len(dias_validos),
            "cps_minimo": 85.5,
            "cps_maximo": 215.3
        },
        "calc": {
            "INV_mean": float(inv_mean) if dias_validos else 0,
            "SEG_mean": float(seg_mean) if dias_validos else 0,
            "opt": opt_point,
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

# FUNCIONES DE FORMATO IDÉNTICAS A grafica Principal.txt
def fmt_int_plain(x):
    """Formato de números igual al original (gráfica.txt)"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    try:
        return str(int(round(float(x))))
    except Exception:
        return "—"

def fmt_k(x):
    """Formato en 'k' igual al original (gráfica.txt)"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    try:
        return f"{int(round(float(x)/1000.0))}k"
    except Exception:
        return "—"

def fmt_days(x):
    """Formato de días igual al original"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    try:
        v = float(x)
        if v <= 0:
            return "—"
        return f"{v:.1f}"
    except Exception:
        return "—"

# FUNCIONES DE CÁLCULO IDÉNTICAS A grafica Principal.txt
def x_warp(x, BREAK_X=80000.0, K=0.28):
    """Compresión del eje X - IGUAL A grafica Principal.txt"""
    x = float(x)
    if x <= BREAK_X:
        return x
    return BREAK_X + (x - BREAK_X) * K

def pick_optimal_point_seg_then_cps(df_curve, min_days=3, cps_tol=0.20):
    """Selecciona punto óptimo - IGUAL A grafica Principal.txt"""
    d = df_curve.copy()
    
    # Filtrar puntos válidos
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
        return None, None, None
    
    # Calcular CPS mínimo y máximo con tolerancia
    cps_min = float(d["CPS_curva"].min())
    cps_max = cps_min * (1.0 + float(cps_tol))
    
    # Filtrar puntos dentro de la tolerancia de CPS
    d2 = d[d["CPS_curva"] <= cps_max].copy()
    if d2.empty:
        d2 = d.copy()
    
    # Ordenar por: 1) Mayor seguidores, 2) Menor CPS, 3) Menor inversión
    d2 = d2.sort_values(
        by=["Seguidores_promedio", "CPS_curva", "Inversion_promedio"],
        ascending=[False, True, True]
    )
    
    return d2.iloc[0].copy(), cps_min, cps_max

def procesar_datos_grafica1_local(df_merge_fecha, parameters):
    """
    Procesa los datos localmente usando la misma lógica que grafica Principal.txt
    """
    if df_merge_fecha.empty:
        return None, None, None, None, None, None
    
    # Extraer parámetros
    STEP = parameters.get("STEP", 15000)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    OPT_MIN_DAYS = parameters.get("OPT_MIN_DAYS", 3)
    OPT_CPS_TOL = parameters.get("OPT_CPS_TOL", 0.20)
    TARGET_FOLLOWERS = parameters.get("TARGET_FOLLOWERS", 1000)
    
    # Asegurar columnas necesarias
    df = df_merge_fecha.copy()
    
    # 1. Calcular Neto_Diario_Real (diferencia de seguidores)
    if 'Seguidores_Totales' in df.columns:
        df = df.sort_values('fecha')
        df['Neto_Diario_Real'] = df['Seguidores_Totales'].diff()
        # Reemplazar valores negativos o cero con NaN
        df.loc[df['Neto_Diario_Real'] <= 0, 'Neto_Diario_Real'] = np.nan
    
    # 2. Calcular Seguidores_Impacto (suma en ventana de IMPACT_DAYS)
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
    
    # 3. Filtrar días válidos (Costo > 0 y resultado > 0)
    cand = df[(df["Costo"] > 0) & (df[RESULT_COL].notna()) & (df[RESULT_COL] > 0)].copy()
    if cand.empty:
        st.warning("No hay días válidos después del procesamiento local")
        return None, None, None, None, None, None
    
    # Calcular CPS real
    cand["CPS_real"] = cand["Costo"] / cand[RESULT_COL]
    
    # Calcular promedios generales
    INV_mean = float(cand["Costo"].mean())
    SEG_mean = float(cand[RESULT_COL].mean())
    
    # 4. Agrupar por rangos de inversión (STEP)
    cmin = float(cand["Costo"].min())
    cmax = float(cand["Costo"].max())
    start = float(np.floor(cmin / STEP) * STEP)
    end = float(np.ceil(cmax / STEP) * STEP) + STEP
    bins = np.arange(start, end + 1, STEP)
    
    # Asignar bins
    cand["Costo_bin"] = pd.cut(cand["Costo"], bins=bins, include_lowest=True, right=False)
    
    # Calcular curva por rangos
    curve = cand.groupby("Costo_bin", observed=True).agg(
        Inversion_promedio=("Costo", "mean"),
        Seguidores_promedio=(RESULT_COL, "mean"),
        Dias=("Costo", "count"),
    ).reset_index(drop=True).sort_values("Inversion_promedio").reset_index(drop=True)
    
    # Calcular CPS de la curva
    curve["CPS_curva"] = np.nan
    mc = (curve["Inversion_promedio"] > 0) & (curve["Seguidores_promedio"] > 0)
    curve.loc[mc, "CPS_curva"] = (curve.loc[mc, "Inversion_promedio"] / curve.loc[mc, "Seguidores_promedio"]).astype("float64")
    
    # Calcular días para meta
    curve["Dias_para_meta"] = np.nan
    mt = curve["Seguidores_promedio"].notna() & (curve["Seguidores_promedio"] > 0)
    curve.loc[mt, "Dias_para_meta"] = (float(TARGET_FOLLOWERS) / curve.loc[mt, "Seguidores_promedio"]).astype("float64")
    
    # 5. Encontrar punto óptimo
    opt, cps_min, cps_max = pick_optimal_point_seg_then_cps(curve, min_days=OPT_MIN_DAYS, cps_tol=OPT_CPS_TOL)
    
    if opt is not None:
        opt_x = float(opt["Inversion_promedio"])
        opt_y = float(opt["Seguidores_promedio"])
        opt_cps = float(opt["CPS_curva"])
        opt_days_meta = float(opt["Dias_para_meta"]) if pd.notna(opt.get("Dias_para_meta", np.nan)) else np.nan
    else:
        opt_x = 0
        opt_y = 0
        opt_cps = 0
        opt_days_meta = 0
    
    # 6. Aplicar compresión del eje X
    cand["xw"] = cand["Costo"].apply(lambda x: x_warp(x, BREAK_X, K))
    curve["xw"] = curve["Inversion_promedio"].apply(lambda x: x_warp(x, BREAK_X, K))
    opt_xw = x_warp(opt_x, BREAK_X, K) if opt_x > 0 else 0
    
    return cand, curve, INV_mean, SEG_mean, opt, cps_min, cps_max, opt_x, opt_y, opt_cps, opt_days_meta, opt_xw

def crear_grafica1_interactiva(data_grafica1):
    """Crea la gráfica 1 interactiva - IDÉNTICA A grafica Principal.txt"""
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
    
    # Extraer datos COMPLETOS del backend
    df_merge_fecha = pd.DataFrame(data_grafica1.get("tables", {}).get("df_merge_fecha", []))
    cand_backend = pd.DataFrame(data_grafica1.get("tables", {}).get("dias_validos", []))
    curve_backend = pd.DataFrame(data_grafica1.get("tables", {}).get("curva_15k", []))
    parameters = data_grafica1.get("parameters", {})
    
    # Extraer parámetros clave
    STEP = parameters.get("STEP", 15000)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
    OPT_MIN_DAYS = parameters.get("OPT_MIN_DAYS", 3)
    OPT_CPS_TOL = parameters.get("OPT_CPS_TOL", 0.20)
    
    # DECISIÓN: Usar procesamiento local si tenemos df_merge_fecha, sino usar datos del backend
    if not df_merge_fecha.empty and 'Costo' in df_merge_fecha.columns and 'Seguidores_Totales' in df_merge_fecha.columns:
        st.info("📊 Procesando datos localmente con lógica de grafica Principal.txt")
        
        # Procesar datos localmente
        resultado = procesar_datos_grafica1_local(df_merge_fecha, parameters)
        if resultado[0] is not None:
            cand, curve, INV_mean, SEG_mean, opt, cps_min, cps_max, opt_x, opt_y, opt_cps, opt_days_meta, opt_xw = resultado
            
            # Actualizar datos del backend con nuestros cálculos
            cand_backend = cand
            curve_backend = curve
            
            # Crear objeto opt para consistencia
            if opt is not None:
                opt_dict = {
                    "Inversion_promedio": opt_x,
                    "Seguidores_promedio": opt_y,
                    "CPS_curva": opt_cps,
                    "Dias_para_meta": opt_days_meta,
                    "Dias": int(opt["Dias"]) if "Dias" in opt else OPT_MIN_DAYS
                }
            else:
                opt_dict = {}
        else:
            # Si el procesamiento local falla, usar datos del backend
            st.warning("Procesamiento local falló. Usando datos del backend.")
            cand = cand_backend
            curve = curve_backend
            opt_dict = data_grafica1.get("calc", {}).get("opt", {})
            INV_mean = data_grafica1.get("calc", {}).get("INV_mean", 0)
            SEG_mean = data_grafica1.get("calc", {}).get("SEG_mean", 0)
            cps_min = data_grafica1.get("calc", {}).get("cps_min_curva", 0)
            cps_max = data_grafica1.get("calc", {}).get("cps_max_tol", 0)
            
            # Calcular valores del punto óptimo
            opt_x = opt_dict.get("Inversion_promedio", 0)
            opt_y = opt_dict.get("Seguidores_promedio", 0)
            opt_cps = opt_dict.get("CPS_curva", 0)
            opt_days_meta = opt_dict.get("Dias_para_meta", 0)
            opt_xw = x_warp(opt_x, BREAK_X, K) if opt_x > 0 else 0
    else:
        # Usar datos del backend directamente
        cand = cand_backend
        curve = curve_backend
        opt_dict = data_grafica1.get("calc", {}).get("opt", {})
        INV_mean = data_grafica1.get("calc", {}).get("INV_mean", 0)
        SEG_mean = data_grafica1.get("calc", {}).get("SEG_mean", 0)
        cps_min = data_grafica1.get("calc", {}).get("cps_min_curva", 0)
        cps_max = data_grafica1.get("calc", {}).get("cps_max_tol", 0)
        
        # Calcular valores del punto óptimo
        opt_x = opt_dict.get("Inversion_promedio", 0)
        opt_y = opt_dict.get("Seguidores_promedio", 0)
        opt_cps = opt_dict.get("CPS_curva", 0)
        opt_days_meta = opt_dict.get("Dias_para_meta", 0)
        opt_xw = x_warp(opt_x, BREAK_X, K) if opt_x > 0 else 0
        
        # Aplicar compresión del eje X a los datos del backend
        if not cand.empty and "Costo" in cand.columns:
            cand["xw"] = cand["Costo"].apply(lambda x: x_warp(x, BREAK_X, K))
        
        if not curve.empty and "Inversion_promedio" in curve.columns:
            curve["xw"] = curve["Inversion_promedio"].apply(lambda x: x_warp(x, BREAK_X, K))
    
    # Verificar que tenemos datos
    if cand.empty or curve.empty:
        st.warning("No hay datos suficientes para generar la gráfica 1")
        
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Intentar de nuevo", key="retry_graf1"):
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="force_example_graf1"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # Asegurar que tenemos la columna RESULT_COL
    if RESULT_COL not in cand.columns:
        if "Seguidores_Impacto" in cand.columns:
            RESULT_COL = "Seguidores_Impacto"
        elif "Neto_Diario_Real" in cand.columns:
            RESULT_COL = "Neto_Diario_Real"
        elif len(cand.columns) > 1:
            # Usar la segunda columna como fallback
            for col in cand.columns:
                if col != "Costo" and col != "CPS_real":
                    RESULT_COL = col
                    break
    
    # Calcular ticks del eje X (IGUAL AL ORIGINAL)
    if not cand.empty and "Costo" in cand.columns:
        data_min = float(cand["Costo"].min())
        data_max = float(cand["Costo"].max())
        
        # Generar bins
        start = float(np.floor(data_min / STEP) * STEP)
        end = float(np.ceil(data_max / STEP) * STEP) + STEP
        bins = np.arange(start, end + 1, STEP)
        
        # Filtrar bins visibles
        edge_ticks_real = np.unique(bins)
        edge_ticks_real = [x for x in edge_ticks_real if (x >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x <= (np.ceil(data_max/STEP)*STEP) + 1e-9)]
        edge_ticks_w = [x_warp(x, BREAK_X, K) for x in edge_ticks_real]
        edge_tick_labels = [fmt_k(x) for x in edge_ticks_real]
        
        # Limitar número de ticks
        MAX_X_TICKS = 12
        stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
        edge_ticks_real = edge_ticks_real[::stride]
        edge_ticks_w = edge_ticks_w[::stride]
        edge_tick_labels = edge_tick_labels[::stride]
    else:
        # Valores por defecto si no hay datos
        edge_ticks_w = []
        edge_tick_labels = []
    
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
    if 'bins' in locals():
        for x_real in bins:
            if x_real >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(data_max/STEP)*STEP) + 1e-9:
                fig.add_vline(
                    x=x_warp(x_real, BREAK_X, K),
                    line_width=1.0,
                    line_dash="dash",
                    line_color="#cbd5e1",
                    opacity=0.18
                )
    
    # 2. Puntos de días reales (scatter) - EXACTAMENTE IGUAL AL ORIGINAL
    if "xw" in cand.columns and RESULT_COL in cand.columns:
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
    if "xw" in curve.columns and "Seguidores_promedio" in curve.columns:
        fig.add_trace(go.Scatter(
            x=curve["xw"],
            y=curve["Seguidores_promedio"],
            mode='lines',
            name='Promedio esperado (por nivel inversión)',
            line=dict(color=colors['linea_curva'], width=2.8),
            opacity=0.95,
            hovertemplate='<b>📈 Curva promedio</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
            customdata=curve["CPS_curva"] if "CPS_curva" in curve.columns else [0] * len(curve)
        ))
    
    # 4. Puntos de la curva promedio (NARANJAS - VISIBLES SIEMPRE)
    if "xw" in curve.columns and "Seguidores_promedio" in curve.columns:
        for idx, row in curve.iterrows():
            # Crear etiqueta para cada punto (IGUAL AL ORIGINAL)
            dias_meta = row.get("Dias_para_meta", np.nan)
            label_text = (
                f"Inv {fmt_int_plain(row.get('Inversion_promedio', 0))}<br>"
                f"SEG {fmt_int_plain(row.get('Seguidores_promedio', 0))}<br>"
                f"CPS {fmt_int_plain(row.get('CPS_curva', 0))}<br>"
                f"1000 SEG ~ {fmt_days(dias_meta)} días<br>"
                f"Días {int(row.get('Dias', 0))}"
            )
            
            # POSICIONES FIJAS PARA ETIQUETAS
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
    if "xw" in curve.columns and "Seguidores_promedio" in curve.columns:
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
            customdata=curve["CPS_curva"] if "CPS_curva" in curve.columns else [0] * len(curve),
            showlegend=True
        ))
    
    # 6. Punto óptimo (ESTRELLA VERDE)
    if opt_x > 0 and opt_y > 0:
        # Texto del punto óptimo (IGUAL AL ORIGINAL)
        opt_label_text = (
            f"Óptimo<br>"
            f"Inv {fmt_int_plain(opt_x)}<br>"
            f"SEG {fmt_int_plain(opt_y)}<br>"
            f"CPS {fmt_int_plain(opt_cps)}<br>"
            f"1000 SEG ~ {fmt_days(opt_days_meta)} días<br>"
            f"CPS_min {fmt_int_plain(cps_min)}<br>"
            f"CPS_max {fmt_int_plain(cps_max)}"
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
        
        # Añadir etiqueta del punto óptimo (POSICIÓN FIJA)
        opt_offsets = [(-320, 70), (-360, 50), (-280, 90), (-260, 40), (-400, 70)]
        opt_dx, opt_dy = opt_offsets[0]
        
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
        annotation_text=f"Promedio SEG = {fmt_int_plain(SEG_mean)}",
        annotation_position="top right",
        annotation_font=dict(size=10, color=colors['linea_promedio']),
        annotation_bgcolor=colors['fondo_ejes']
    )
    
    # Línea vertical de promedio INV
    fig.add_vline(
        x=x_warp(INV_mean, BREAK_X, K),
        line_dash="dot",
        line_color=colors['linea_promedio'],
        line_width=1.8,
        opacity=0.75,
        annotation_text=f"Promedio inversión = {fmt_int_plain(INV_mean)}",
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
            tickvals=edge_ticks_w if len(edge_ticks_w) > 0 else None,
            ticktext=edge_tick_labels if len(edge_tick_labels) > 0 else None,
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
        if not curve.empty:
            display_curve = curve.copy()
            # Formatear como en el gráfico original
            if "Inversion_promedio" in display_curve.columns:
                display_curve["Inversion_promedio"] = display_curve["Inversion_promedio"].apply(lambda x: f"${x:,.0f}")
            if "Seguidores_promedio" in display_curve.columns:
                display_curve["Seguidores_promedio"] = display_curve["Seguidores_promedio"].apply(lambda x: f"{x:,.0f}")
            if "CPS_curva" in display_curve.columns:
                display_curve["CPS_curva"] = display_curve["CPS_curva"].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A")
            if "Dias_para_meta" in display_curve.columns:
                display_curve["Dias_para_meta"] = display_curve["Dias_para_meta"].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
            
            # Renombrar columnas
            rename_map = {}
            if "Inversion_promedio" in display_curve.columns:
                rename_map["Inversion_promedio"] = "💰 Inversión promedio"
            if "Seguidores_promedio" in display_curve.columns:
                rename_map["Seguidores_promedio"] = "👥 Seguidores promedio"
            if "CPS_curva" in display_curve.columns:
                rename_map["CPS_curva"] = "📊 CPS"
            if "Dias" in display_curve.columns:
                rename_map["Dias"] = "📅 Días en rango"
            if "Dias_para_meta" in display_curve.columns:
                rename_map["Dias_para_meta"] = "⏱️ 1000 SEG (días)"
            
            display_curve = display_curve.rename(columns=rename_map)
            
            st.dataframe(display_curve, use_container_width=True)
        else:
            st.info("No hay datos de curva para mostrar")
    
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
                
                if not cand.empty:
                    st.write(f"**Días válidos ({len(cand)} registros):**")
                    st.dataframe(cand.head(20))
                
                if not curve.empty:
                    st.write("**Curva completa:**")
                    st.dataframe(curve)

# [El resto del código permanece igual...]

# (Continúa con el resto del código de app.py sin cambios desde aquí)
