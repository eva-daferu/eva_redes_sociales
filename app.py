import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

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
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124, 58, 237, 0.12), transparent 24%),
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.10), transparent 22%),
            linear-gradient(180deg, #f6f7fb 0%, #eef2ff 100%);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1320px;
    }

    .hero {
        background: linear-gradient(135deg, #21053d 0%, #2e1065 50%, #1e1b4b 100%);
        border-radius: 24px;
        padding: 28px 30px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 20px 45px rgba(37, 15, 77, 0.24);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 900;
        line-height: 1.05;
        margin: 0 0 8px 0;
        letter-spacing: -0.8px;
    }

    .hero-subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.82);
        margin: 0;
    }

    .section-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(6px);
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 6px;
        letter-spacing: -0.4px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 16px;
    }

    .calc-shell {
        max-width: 560px;
        margin: 0 auto;
    }

    .calc-top {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 52%, #16a34a 100%);
        padding: 18px 20px 10px 20px;
        border-radius: 22px;
        box-shadow: 0 16px 36px rgba(91, 33, 182, 0.24);
        margin-bottom: 14px;
    }

    .calc-top-title {
        font-size: 13px;
        font-weight: 900;
        color: rgba(255,255,255,0.92);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }

    .calc-top-text {
        font-size: 13px;
        color: rgba(255,255,255,0.82);
        margin-bottom: 4px;
    }

    .calc-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 8px;
        font-size: 15px;
    }

    .calc-table td {
        padding: 12px 14px;
    }

    .calc-table td:first-child {
        background: linear-gradient(135deg, #7e22ce 0%, #6d28d9 100%);
        color: white;
        font-weight: 800;
        border-radius: 14px 0 0 14px;
        width: 58%;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.16);
    }

    .calc-table td:last-child {
        background: white;
        color: #0f172a;
        text-align: right;
        font-weight: 900;
        border-radius: 0 14px 14px 0;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
    }

    .mini-note {
        font-size: 12px;
        color: #64748b;
        margin-top: 8px;
        text-align: center;
    }

    div[data-testid="stDataEditor"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.06) !important;
        background: white !important;
    }

    .editor-note {
        font-size: 12px;
        color: #64748b;
        margin-top: 8px;
    }

    .view-title {
        font-size: 22px;
        font-weight: 900;
        color: #111827;
        margin: 16px 0 10px 0;
    }

    label[data-testid="stWidgetLabel"] p {
        font-weight: 700 !important;
        color: #1f2937 !important;
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
        marcas["Flyer"] = "Si"
    elif tipo_limpio == "video":
        marcas["Video"] = "Si"
    elif tipo_limpio == "encuestas":
        marcas["Encuentas"] = "Si"
    elif tipo_limpio == "comercial":
        marcas["Comercial"] = "Si"
    elif tipo_limpio == "testeo":
        marcas["Flyer"] = "Si"

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

def render_cronograma_html(df):
    if df.empty:
        st.info("Agrega una fila en la tabla editable.")
        return

    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%d/%m/%Y")

    html = """
    <html>
    <head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: Inter, Segoe UI, Arial, sans-serif;
        }

        .table-wrap {
            width: 100%;
            overflow-x: auto;
            padding: 2px 2px 8px 2px;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
            font-size: 14px;
        }

        thead th {
            background: linear-gradient(135deg, #22053f 0%, #3b0764 70%, #2563eb 100%);
            color: white;
            padding: 14px 12px;
            text-align: left;
            font-weight: 900;
            letter-spacing: 0.2px;
            white-space: nowrap;
        }

        thead th:first-child { border-radius: 14px 0 0 14px; }
        thead th:last-child  { border-radius: 0 14px 14px 0; text-align: center; }

        tbody td {
            background: rgba(255,255,255,0.98);
            padding: 12px 12px;
            color: #111827;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: middle;
        }

        tbody td:first-child {
            border-left: 1px solid #e2e8f0;
            border-radius: 14px 0 0 14px;
            font-weight: 800;
        }

        tbody td:last-child {
            border-right: 1px solid #e2e8f0;
            border-radius: 0 14px 14px 0;
            text-align: center;
            font-weight: 900;
        }

        .row-active td {
            background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%) !important;
            border-top: 1px solid #86efac !important;
            border-bottom: 1px solid #86efac !important;
            box-shadow: 0 10px 24px rgba(34, 197, 94, 0.10);
        }

        .row-active td:first-child { border-left: 1px solid #86efac !important; }
        .row-active td:last-child  { border-right: 1px solid #86efac !important; }

        .tipo-pill {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 100%);
            color: #312e81;
            font-weight: 900;
            font-size: 12px;
        }

        .cantidad-pill {
            display: inline-block;
            min-width: 38px;
            padding: 7px 10px;
            border-radius: 12px;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            color: #1d4ed8;
            font-weight: 900;
        }

        .si-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            padding: 6px 12px;
            border-radius: 999px;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            font-weight: 900;
            box-shadow: 0 10px 22px rgba(34, 197, 94, 0.25);
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0%   { transform: scale(1); box-shadow: 0 10px 22px rgba(34, 197, 94, 0.20); }
            50%  { transform: scale(1.04); box-shadow: 0 12px 28px rgba(34, 197, 94, 0.34); }
            100% { transform: scale(1); box-shadow: 0 10px 22px rgba(34, 197, 94, 0.20); }
        }

        .center {
            text-align: center;
        }

        .empty-cell {
            color: #94a3b8;
        }
    </style>
    </head>
    <body>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Tipo</th>
                        <th>Fecha</th>
                        <th>Día</th>
                        <th>Flyer</th>
                        <th>Video</th>
                        <th>Encuentas</th>
                        <th>Comercial</th>
                        <th>Cantidad</th>
                    </tr>
                </thead>
                <tbody>
    """

    def badge_si(valor):
        return '<span class="si-badge">Si</span>' if str(valor).strip() == "Si" else '<span class="empty-cell"></span>'

    for _, row in df.iterrows():
        tiene_si = any(str(row[col]).strip() == "Si" for col in ["Flyer", "Video", "Encuentas", "Comercial"])
        clase = "row-active" if tiene_si else ""

        html += f"""
            <tr class="{clase}">
                <td><span class="tipo-pill">{row['Tipo']}</span></td>
                <td>{row['Fecha']}</td>
                <td>{row['Dia']}</td>
                <td class="center">{badge_si(row['Flyer'])}</td>
                <td class="center">{badge_si(row['Video'])}</td>
                <td class="center">{badge_si(row['Encuentas'])}</td>
                <td class="center">{badge_si(row['Comercial'])}</td>
                <td><span class="cantidad-pill">{row['Cantidad']}</span></td>
            </tr>
        """

    html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    alto = 140 + (len(df) * 62)
    components.html(html, height=max(alto, 240), scrolling=False)

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
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">¿Cuánto logras con tu inversión y tu cronograma de contenido?</div>
    <div class="hero-subtitle">Edita solo Tipo, Fecha y Cantidad. El resto se calcula automáticamente y la vista final se marca visualmente donde corresponda.</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CALCULADORA
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Calculadora de inversión</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Bloque compacto y centrado para mantener orden visual.</div>', unsafe_allow_html=True)

esp1, centro, esp2 = st.columns([1.2, 1.6, 1.2])

with centro:
    st.markdown("""
    <div class="calc-shell">
        <div class="calc-top">
            <div class="calc-top-title">Proyección rápida</div>
            <div class="calc-top-text">Ingresa el valor total de inversión y obtén el estimado automático.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    <div class="calc-shell">
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
        <div class="mini-note">La tabla quedó contenida para que no se vea ancha ni desordenada.</div>
    </div>
    """
    st.markdown(tabla_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# CRONOGRAMA
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Cronograma de contenido</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Puedes agregar, borrar o editar filas directamente. La vista final se recalcula sola.</div>', unsafe_allow_html=True)

editor_df = st.data_editor(
    st.session_state["cronograma_editable"],
    key="editor_cronograma",
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True,
    height=390,
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

st.markdown('<div class="editor-note">Aquí sí puedes eliminar filas directamente desde el editor dinámico.</div>', unsafe_allow_html=True)

st.session_state["cronograma_editable"] = limpiar_editable(editor_df)
df_cronograma = cronograma_calculado(st.session_state["cronograma_editable"])

st.markdown('<div class="view-title">Vista final</div>', unsafe_allow_html=True)
render_cronograma_html(df_cronograma)

st.markdown('</div>', unsafe_allow_html=True)
