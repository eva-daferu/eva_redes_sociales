import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Calculadora + Cronograma de Contenido",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .section-title {
        font-size: 22px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 18px;
    }
    .calc-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 16px;
    }
    .calc-table td {
        border: 1px solid #d9d9d9;
        padding: 10px 12px;
    }
    .calc-table td:first-child {
        background: #e10600;
        color: white;
        font-weight: 700;
        width: 55%;
    }
    .calc-table td:last-child {
        background: #f7f7f7;
        color: #111;
        text-align: right;
        font-weight: 600;
    }
    .box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def nombre_dia_es(fecha_val):
    dias = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo"
    }
    fecha_ts = pd.to_datetime(fecha_val)
    return dias[fecha_ts.weekday()]

def columnas_marcadas(tipo, columna_testeo=None):
    columnas = {
        "Flyer": "",
        "Video": "",
        "Encuentas": "",
        "Comercial": ""
    }

    if tipo == "Flyer":
        columnas["Flyer"] = "si"
    elif tipo == "Video":
        columnas["Video"] = "si"
    elif tipo == "Encuestas":
        columnas["Encuentas"] = "si"
    elif tipo == "Comercial":
        columnas["Comercial"] = "si"
    elif tipo == "Testeo" and columna_testeo in columnas:
        columnas[columna_testeo] = "si"

    return columnas

def construir_fila(tipo, fecha_val, cantidad, columna_testeo=None):
    marcas = columnas_marcadas(tipo, columna_testeo)
    return {
        "Tipo": tipo,
        "Fecha": pd.to_datetime(fecha_val),
        "Dia": nombre_dia_es(fecha_val),
        "Flyer": marcas["Flyer"],
        "Video": marcas["Video"],
        "Encuentas": marcas["Encuentas"],
        "Comercial": marcas["Comercial"],
        "Cantidad": int(cantidad)
    }

def detectar_columna_marcada(row):
    for col in ["Flyer", "Video", "Encuentas", "Comercial"]:
        if str(row.get(col, "")).strip().lower() == "si":
            return col
    return "Flyer"

def formatear_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def formatear_numero(valor, decimales=0):
    if decimales == 0:
        return f"{valor:,.0f}".replace(",", ".")
    return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatear_porcentaje(valor, decimales=0):
    return f"{valor * 100:.{decimales}f}%".replace(".", ",")

def ordenar_df(df):
    if df.empty:
        return df
    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.sort_values(by="Fecha", ascending=True).reset_index(drop=True)
    return df

# =========================================================
# DATOS INICIALES
# =========================================================
def cargar_cronograma_inicial():
    filas = [
        construir_fila("Testeo", "2026-04-13", 6, "Flyer"),
        construir_fila("Encuestas", "2026-04-20", 4),
        construir_fila("Comercial", "2026-05-11", 1),
        construir_fila("Video", "2026-05-18", 1),
        construir_fila("Comercial", "2026-05-25", 1),
        construir_fila("Video", "2026-05-27", 1),
        construir_fila("Flyer", "2026-05-29", 1),
        construir_fila("Video", "2026-06-01", 1),
        construir_fila("Flyer", "2026-06-03", 1),
        construir_fila("Comercial", "2026-06-05", 1),
    ]
    return ordenar_df(pd.DataFrame(filas))

if "cronograma_df" not in st.session_state:
    st.session_state["cronograma_df"] = cargar_cronograma_inicial()

if "mensaje_accion" not in st.session_state:
    st.session_state["mensaje_accion"] = ""

# =========================================================
# TÍTULO
# =========================================================
st.markdown('<div class="main-title">Calculadora de Inversión + Cronograma de Contenido</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Un solo input para inversión y un bloque para agregar, modificar o eliminar filas del cronograma.</div>', unsafe_allow_html=True)

# =========================================================
# BLOQUE 1 - CALCULADORA
# =========================================================
st.markdown('<div class="section-title">Calculadora de inversión</div>', unsafe_allow_html=True)

inversion = st.number_input(
    "Inversión",
    min_value=0.0,
    value=1000000.0,
    step=1000.0,
    format="%.0f"
)

# Fórmulas según tus valores de referencia
inversion_dia = inversion / 30 if inversion > 0 else 0
impresiones = inversion * 0.1373
cpm = inversion / (impresiones / 1000) if impresiones > 0 else 0
clics_1 = impresiones * 0.007
clics_2 = impresiones * 0.012
ventas_1 = clics_1 * 0.0157
ventas_2 = clics_2 * 0.0157
efectividad_1 = (ventas_1 / clics_1) if clics_1 > 0 else 0
efectividad_2 = clics_1 * 0.20

tabla_html = f"""
<table class="calc-table">
    <tr>
        <td>Inversión día</td>
        <td>{formatear_moneda(inversion_dia)}</td>
    </tr>
    <tr>
        <td>Inversión</td>
        <td>{formatear_moneda(inversion)}</td>
    </tr>
    <tr>
        <td>Impresiones</td>
        <td>{formatear_numero(impresiones)}</td>
    </tr>
    <tr>
        <td>CPM</td>
        <td>{formatear_moneda(cpm)}</td>
    </tr>
    <tr>
        <td>Clics: 1</td>
        <td>{formatear_numero(clics_1)}</td>
    </tr>
    <tr>
        <td>Clics: 2</td>
        <td>{formatear_numero(clics_2)}</td>
    </tr>
    <tr>
        <td>Ventas: 1</td>
        <td>{formatear_numero(ventas_1, 1)}</td>
    </tr>
    <tr>
        <td>Ventas: 2</td>
        <td>{formatear_numero(ventas_2, 1)}</td>
    </tr>
    <tr>
        <td>Efectividad 1</td>
        <td>{formatear_porcentaje(efectividad_1, 0)}</td>
    </tr>
    <tr>
        <td>Efectividad 2</td>
        <td>{formatear_numero(efectividad_2, 1)}</td>
    </tr>
</table>
"""
st.markdown(tabla_html, unsafe_allow_html=True)

st.divider()

# =========================================================
# BLOQUE 2 - CRONOGRAMA DE CONTENIDO
# =========================================================
st.markdown('<div class="section-title">Cronograma de contenido</div>', unsafe_allow_html=True)

df = st.session_state["cronograma_df"].copy()
df = ordenar_df(df)
st.session_state["cronograma_df"] = df

opciones_selector = ["Nueva fila"]
mapa_filas = {}

for idx, row in df.iterrows():
    fecha_txt = pd.to_datetime(row["Fecha"]).strftime("%d/%m/%Y")
    etiqueta = f"Fila {idx + 1} | {fecha_txt} | {row['Tipo']}"
    opciones_selector.append(etiqueta)
    mapa_filas[etiqueta] = idx

seleccion = st.selectbox("Selecciona una fila", opciones_selector)

fila_idx = None
tipo_default = "Flyer"
fecha_default = date.today()
cantidad_default = 1
columna_testeo_default = "Flyer"

if seleccion != "Nueva fila":
    fila_idx = mapa_filas[seleccion]
    fila = df.loc[fila_idx]
    tipo_default = str(fila["Tipo"])
    fecha_default = pd.to_datetime(fila["Fecha"]).date()
    cantidad_default = int(fila["Cantidad"])
    columna_testeo_default = detectar_columna_marcada(fila)

tipos_disponibles = ["Testeo", "Encuestas", "Comercial", "Video", "Flyer"]

with st.form("form_cronograma"):
    c1, c2, c3 = st.columns(3)

    with c1:
        tipo = st.selectbox(
            "Tipo",
            tipos_disponibles,
            index=tipos_disponibles.index(tipo_default) if tipo_default in tipos_disponibles else 0
        )

    with c2:
        fecha = st.date_input("Fecha", value=fecha_default)

    with c3:
        cantidad = st.number_input("Cantidad", min_value=1, value=int(cantidad_default), step=1)

    columna_testeo = None
    if tipo == "Testeo":
        opciones_testeo = ["Flyer", "Video", "Encuentas", "Comercial"]
        columna_testeo = st.selectbox(
            "Columna a marcar para Testeo",
            opciones_testeo,
            index=opciones_testeo.index(columna_testeo_default) if columna_testeo_default in opciones_testeo else 0
        )

    b1, b2, b3 = st.columns(3)
    agregar = b1.form_submit_button("Agregar fila", use_container_width=True)
    modificar = b2.form_submit_button("Modificar fila", use_container_width=True, disabled=fila_idx is None)
    eliminar = b3.form_submit_button("Eliminar fila", use_container_width=True, disabled=fila_idx is None)

if agregar:
    nueva_fila = construir_fila(tipo, fecha, cantidad, columna_testeo)
    st.session_state["cronograma_df"] = ordenar_df(
        pd.concat([st.session_state["cronograma_df"], pd.DataFrame([nueva_fila])], ignore_index=True)
    )
    st.session_state["mensaje_accion"] = "Fila agregada"
    st.rerun()

if modificar and fila_idx is not None:
    fila_actualizada = construir_fila(tipo, fecha, cantidad, columna_testeo)
    for col, val in fila_actualizada.items():
        st.session_state["cronograma_df"].at[fila_idx, col] = val
    st.session_state["cronograma_df"] = ordenar_df(st.session_state["cronograma_df"])
    st.session_state["mensaje_accion"] = "Fila modificada"
    st.rerun()

if eliminar and fila_idx is not None:
    st.session_state["cronograma_df"] = ordenar_df(
        st.session_state["cronograma_df"].drop(index=fila_idx).reset_index(drop=True)
    )
    st.session_state["mensaje_accion"] = "Fila eliminada"
    st.rerun()

if st.session_state["mensaje_accion"]:
    st.success(st.session_state["mensaje_accion"])
    st.session_state["mensaje_accion"] = ""

# =========================================================
# TABLA FINAL
# =========================================================
st.markdown("### Cronograma")

df_mostrar = st.session_state["cronograma_df"].copy()
df_mostrar["Fecha"] = pd.to_datetime(df_mostrar["Fecha"]).dt.strftime("%d/%m/%Y")
df_mostrar = df_mostrar[["Tipo", "Fecha", "Dia", "Flyer", "Video", "Encuentas", "Comercial", "Cantidad"]]

st.dataframe(
    df_mostrar,
    use_container_width=True,
    hide_index=True
)
