import streamlit as st

st.set_page_config(
    page_title="Calculadora de Inversión en Redes Sociales",
    page_icon="📊",
    layout="centered"
)

# -----------------------------
# CONFIG
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .sub-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 24px;
    }
    .calc-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 18px;
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
    .note {
        font-size: 12px;
        color: #666;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Calculadora de Inversión en Redes Sociales</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Ingresa solo el valor de inversión y el sistema calcula todo automáticamente.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# INPUT
# -----------------------------
inversion = st.number_input(
    "Inversión",
    min_value=0.0,
    value=1000000.0,
    step=1000.0,
    format="%.0f"
)

# -----------------------------
# CÁLCULOS
# -----------------------------
# Se usa inversión / 30 porque es lo que coincide con tu ejemplo:
# 1.000.000 / 30 = 33.333
inversion_dia = inversion / 30 if inversion > 0 else 0

impresiones = inversion * 0.1373
cpm = inversion / (impresiones / 1000) if impresiones > 0 else 0

clics_1 = impresiones * 0.007
clics_2 = impresiones * 0.012

ventas_1 = clics_1 * 0.0157
ventas_2 = clics_2 * 0.0157

efectividad_1 = (ventas_1 / clics_1) if clics_1 > 0 else 0
efectividad_2 = clics_1 * 0.20

# -----------------------------
# FORMATOS
# -----------------------------
def formato_moneda(valor: float) -> str:
    return f"$ {valor:,.0f}".replace(",", ".")

def formato_numero(valor: float, decimales: int = 0) -> str:
    if decimales == 0:
        return f"{valor:,.0f}".replace(",", ".")
    return f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_porcentaje(valor: float, decimales: int = 0) -> str:
    return f"{valor * 100:.{decimales}f}%".replace(".", ",")

# -----------------------------
# TABLA
# -----------------------------
tabla_html = f"""
<table class="calc-table">
    <tr>
        <td>Inversión día</td>
        <td>{formato_moneda(inversion_dia)}</td>
    </tr>
    <tr>
        <td>Inversión</td>
        <td>{formato_moneda(inversion)}</td>
    </tr>
    <tr>
        <td>Impresiones</td>
        <td>{formato_numero(impresiones)}</td>
    </tr>
    <tr>
        <td>CPM</td>
        <td>{formato_moneda(cpm)}</td>
    </tr>
    <tr>
        <td>Clics: 1</td>
        <td>{formato_numero(clics_1)}</td>
    </tr>
    <tr>
        <td>Clics: 2</td>
        <td>{formato_numero(clics_2)}</td>
    </tr>
    <tr>
        <td>Ventas: 1</td>
        <td>{formato_numero(ventas_1, 1)}</td>
    </tr>
    <tr>
        <td>Ventas: 2</td>
        <td>{formato_numero(ventas_2, 1)}</td>
    </tr>
    <tr>
        <td>Resultados Redes</td>
        <td>{formato_porcentaje(efectividad_1, 0)}</td>
    </tr>
    <tr>
        <td>Efectividad alcanzable</td>
        <td>{formato_numero(efectividad_2, 1)}</td>
    </tr>
</table>
"""

st.markdown(tabla_html, unsafe_allow_html=True)
