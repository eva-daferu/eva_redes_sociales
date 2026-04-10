import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Calculadora + Cronograma",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================
st.markdown("""
<style>
    .titulo-principal {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .subtitulo {
        font-size: 14px;
        color: #666;
        margin-bottom: 18px;
    }
    .bloque {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 18px;
    }
    .calc-box {
        max-width: 520px;
        margin: 0 auto;
    }
    .calc-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 15px;
        overflow: hidden;
        border-radius: 12px;
    }
    .calc-table td {
        border: 1px solid #d9d9d9;
        padding: 9px 12px;
    }
    .calc-table td:first-child {
        background: #e10600;
        color: white;
        font-weight: 700;
        width: 58%;
    }
    .calc-table td:last-child {
        background: #f8f8f8;
        color: #111;
        text-align: right;
        font-weight: 600;
    }
    .seccion-titulo {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 10px;
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
    fecha_ts = pd.to_datetime(fecha_val, errors="coerce")
    if pd.isna(fecha_ts):
        return ""
    return dias[fecha_ts.weekday()]

def normalizar_tipo(tipo):
    if pd.isna(tipo):
        return ""
    return str(tipo).strip()

def marcar_columnas_por_tipo(tipo):
    marcas = {
        "Flyer": "",
        "Video": "",
        "Encuentas": "",
        "Comercial": ""
    }

    tipo_limpio = normalizar_tipo(tipo).lower()

    if tipo_limpio == "flyer":
        marcas["Flyer"] = "si"
    elif tipo_limpio == "video":
        marcas["Video"] = "si"
    elif tipo_limpio == "encuestas":
        marcas["Encuentas"] = "si"
    elif tipo_limpio == "comercial":
        marcas["Comercial"] = "si"
    elif tipo_limpio == "testeo":
        marcas["Flyer"] = "si"

    return marcas

def limpiar_editable(df):
    df = df.copy()

    if "Tipo" not in df.columns:
        df["Tipo"] = ""
    if "Fecha" not in df.columns:
        df["Fecha"] = pd.NaT
    if "Cantidad" not in df.columns:
        df["Cantidad"] = 1

    df["Tipo"] = df["Tipo"].astype("string")
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")

    return df[["Tipo", "Fecha", "Cantidad"]]

def cronograma_calculado(df_editable):
    df = limpiar_editable(df_editable)

    # Solo filas válidas para la tabla final
    df = df.dropna(subset=["Tipo", "Fecha", "Cantidad"]).copy()
    df = df[df["Tipo"].astype(str).str.strip() != ""].copy()
    df = df[df["Cantidad"] > 0].copy()

    if df.empty:
        return pd.DataFrame(columns=[
            "Tipo", "Fecha", "Dia", "Flyer", "Video", "Encuentas", "Comercial", "Cantidad"
        ])

    filas = []
    for _, row in df.iterrows():
        tipo = normalizar_tipo(row["Tipo"])
        fecha = pd.to_datetime(row["Fecha"], errors="coerce")
        cantidad = int(row["Cantidad"])

        marcas = marcar_columnas_por_tipo(tipo)

        filas.append({
            "Tipo": tipo,
            "Fecha": fecha,
            "Dia": nombre_dia_es(fecha),
            "Flyer": marcas["Flyer"],
            "Video": marcas["Video"],
            "Encuentas": marcas["Encuentas"],
            "Comercial": marcas["Comercial"],
            "Cantidad": cantidad
        })

    df_final = pd.DataFrame(filas)
    df_final["Fecha"] = pd.to_datetime(df_final["Fecha"], errors="coerce")
    df_final = df_final.sort_values(by="Fecha", ascending=True).reset_index(drop=True)

    return df_final

def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def formato_numero(valor, decimales=0):
    if decimales == 0:
        return f"{valor:,.0f}".replace(",", ".")
    return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_porcentaje(valor, decimales=0):
    return f"{valor * 100:.{decimales}f}%".replace(".", ",")

# =========================================================
# DATOS INICIALES
# =========================================================
def cronograma_inicial_editable():
    return pd.DataFrame([
        {"Tipo": "Testeo",    "Fecha": pd.to_datetime("2026-04-13"), "Cantidad": 6},
        {"Tipo": "Encuestas", "Fecha": pd.to_datetime("2026-04-20"), "Cantidad": 4},
        {"Tipo": "Comercial", "Fecha": pd.to_datetime("2026-05-11"), "Cantidad": 1},
        {"Tipo": "Video",     "Fecha": pd.to_datetime("2026-05-18"), "Cantidad": 1},
        {"Tipo": "Comercial", "Fecha": pd.to_datetime("2026-05-25"), "Cantidad": 1},
        {"Tipo": "Video",     "Fecha": pd.to_datetime("2026-05-27"), "Cantidad": 1},
        {"Tipo": "Flyer",     "Fecha": pd.to_datetime("2026-05-29"), "Cantidad": 1},
        {"Tipo": "Video",     "Fecha": pd.to_datetime("2026-06-01"), "Cantidad": 1},
        {"Tipo": "Flyer",     "Fecha": pd.to_datetime("2026-06-03"), "Cantidad": 1},
        {"Tipo": "Comercial", "Fecha": pd.to_datetime("2026-06-05"), "Cantidad": 1},
    ])

if "cronograma_editable" not in st.session_state:
    st.session_state["cronograma_editable"] = cronograma_inicial_editable()

# =========================================================
# TÍTULO
# =========================================================
st.markdown('<div class="titulo-principal">Calculadora de Inversión + Cronograma de Contenido</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Edita fecha, tipo y cantidad. El resto se calcula solo.</div>', unsafe_allow_html=True)

# =========================================================
# CALCULADORA
# =========================================================
st.markdown('<div class="seccion-titulo">Calculadora de inversión</div>', unsafe_allow_html=True)

col_esp_1, col_centro, col_esp_2 = st.columns([1.2, 1.6, 1.2])

with col_centro:
    st.markdown('<div class="calc-box">', unsafe_allow_html=True)

    inversion = st.number_input(
        "Inversión",
        min_value=0.0,
        value=1000000.0,
        step=1000.0,
        format="%.0f"
    )

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
        <tr><td>Inversión día</td><td>{formato_moneda(inversion_dia)}</td></tr>
        <tr><td>Inversión</td><td>{formato_moneda(inversion)}</td></tr>
        <tr><td>Impresiones</td><td>{formato_numero(impresiones)}</td></tr>
        <tr><td>CPM</td><td>{formato_moneda(cpm)}</td></tr>
        <tr><td>Clics: 1</td><td>{formato_numero(clics_1)}</td></tr>
        <tr><td>Clics: 2</td><td>{formato_numero(clics_2)}</td></tr>
        <tr><td>Ventas: 1</td><td>{formato_numero(ventas_1, 1)}</td></tr>
        <tr><td>Ventas: 2</td><td>{formato_numero(ventas_2, 1)}</td></tr>
        <tr><td>Efectividad 1</td><td>{formato_porcentaje(efectividad_1, 0)}</td></tr>
        <tr><td>Efectividad 2</td><td>{formato_numero(efectividad_2, 1)}</td></tr>
    </table>
    """
    st.markdown(tabla_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =========================================================
# CRONOGRAMA EDITABLE
# =========================================================
st.markdown('<div class="seccion-titulo">Cronograma de contenido</div>', unsafe_allow_html=True)

editor_df = st.data_editor(
    st.session_state["cronograma_editable"],
    key="editor_cronograma",
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    column_order=["Tipo", "Fecha", "Cantidad"],
    column_config={
        "Tipo": st.column_config.SelectboxColumn(
            "Tipo",
            options=["Testeo", "Encuestas", "Comercial", "Video", "Flyer"],
            required=True,
            width="medium"
        ),
        "Fecha": st.column_config.DateColumn(
            "Fecha",
            format="DD/MM/YYYY",
            required=True,
            width="medium"
        ),
        "Cantidad": st.column_config.NumberColumn(
            "Cantidad",
            min_value=1,
            step=1,
            required=True,
            width="small"
        )
    }
)

st.session_state["cronograma_editable"] = limpiar_editable(editor_df)

df_cronograma = cronograma_calculado(st.session_state["cronograma_editable"])

st.markdown("### Vista final")

if df_cronograma.empty:
    st.info("Agrega una fila en la tabla editable.")
else:
    df_mostrar = df_cronograma.copy()
    df_mostrar["Fecha"] = pd.to_datetime(df_mostrar["Fecha"]).dt.strftime("%d/%m/%Y")
    df_mostrar = df_mostrar[[
        "Tipo", "Fecha", "Dia", "Flyer", "Video", "Encuentas", "Comercial", "Cantidad"
    ]]

    st.dataframe(
        df_mostrar,
        use_container_width=True,
        hide_index=True
    )
