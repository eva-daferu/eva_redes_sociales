
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
            radial-gradient(circle at top left, rgba(124, 58, 237, 0.10), transparent 24%),
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.08), transparent 22%),
            linear-gradient(180deg, #f6f7fb 0%, #eef2ff 100%);
    }

    .block-container {
        padding-top: 0.9rem;
        padding-bottom: 1.4rem;
        max-width: 1380px;
    }

    .hero {
        background: linear-gradient(135deg, #21053d 0%, #2e1065 50%, #1e1b4b 100%);
        border-radius: 22px;
        padding: 20px 24px;
        color: white;
        margin-bottom: 14px;
        box-shadow: 0 18px 40px rgba(37, 15, 77, 0.22);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .hero-title {
        font-size: 29px;
        font-weight: 900;
        line-height: 1.05;
        margin: 0 0 6px 0;
        letter-spacing: -0.8px;
    }

    .hero-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.82);
        margin: 0;
    }

    .section-card {
        background: rgba(255,255,255,0.90);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.07);
        backdrop-filter: blur(6px);
        margin-bottom: 14px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 8px;
        letter-spacing: -0.35px;
    }

    .calc-top {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 52%, #16a34a 100%);
        padding: 14px 16px 10px 16px;
        border-radius: 18px;
        box-shadow: 0 14px 30px rgba(91, 33, 182, 0.22);
        margin-bottom: 12px;
    }

    .calc-top-title {
        font-size: 12px;
        font-weight: 900;
        color: rgba(255,255,255,0.95);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }

    .calc-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 6px;
        font-size: 14px;
    }

    .calc-table td {
        padding: 10px 12px;
    }

    .calc-table td:first-child {
        background: linear-gradient(135deg, #7e22ce 0%, #6d28d9 100%);
        color: white;
        font-weight: 800;
        border-radius: 12px 0 0 12px;
        width: 58%;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.14);
    }

    .calc-table td:last-child {
        background: white;
        color: #0f172a;
        text-align: right;
        font-weight: 900;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
    }

    div[data-testid="stDataEditor"] {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05) !important;
        background: white !important;
    }

    .view-title {
        font-size: 20px;
        font-weight: 900;
        color: #111827;
        margin: 0 0 8px 0;
    }

    .editor-note {
        font-size: 11px;
        color: #64748b;
        margin-top: 6px;
    }

    .stExpander {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        background: rgba(255,255,255,0.90) !important;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05) !important;
    }

    .stExpander summary {
        font-weight: 800 !important;
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

def semana_del_mes(fecha_val):
    fecha_ts = pd.to_datetime(fecha_val, errors="coerce")
    if pd.isna(fecha_ts):
        return ""
    return int(((fecha_ts.day - 1) // 7) + 1)

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
            "Tipo", "Fecha", "Semana", "Dia", "Flyer", "Video", "Encuentas", "Comercial", "Cantidad"
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
            "Semana": semana_del_mes(fecha),
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
        st.info("Agrega una fila en el cronograma.")
        return

    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%d/%m/%Y")

    html = """
    <html>
    <head>
    <style>
        body {
            margin: 0;
            padding: 0 0 14px 0;
            background: transparent;
            font-family: Inter, Segoe UI, Arial, sans-serif;
        }

        .table-wrap {
            width: 100%;
            overflow-x: auto;
            padding: 0 0 8px 0;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
            font-size: 13px;
        }

        thead th {
            background: linear-gradient(135deg, #22053f 0%, #3b0764 70%, #2563eb 100%);
            color: white;
            padding: 12px 10px;
            text-align: left;
            font-weight: 900;
            letter-spacing: 0.15px;
            white-space: nowrap;
        }

        thead th:first-child { border-radius: 12px 0 0 12px; }
        thead th:last-child  { border-radius: 0 12px 12px 0; text-align: center; }

        tbody td {
            background: rgba(255,255,255,0.98);
            padding: 10px 10px;
            color: #111827;
            border-top: 1px solid #e2e8f0;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: middle;
        }

        tbody td:first-child {
            border-left: 1px solid #e2e8f0;
            border-radius: 12px 0 0 12px;
            font-weight: 800;
        }

        tbody td:last-child {
            border-right: 1px solid #e2e8f0;
            border-radius: 0 12px 12px 0;
            text-align: center;
            font-weight: 900;
        }

        .row-active td {
            background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%) !important;
            border-top: 1px solid #86efac !important;
            border-bottom: 1px solid #86efac !important;
            box-shadow: 0 8px 18px rgba(34, 197, 94, 0.08);
        }

        .row-active td:first-child { border-left: 1px solid #86efac !important; }
        .row-active td:last-child  { border-right: 1px solid #86efac !important; }

        .tipo-pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: linear-gradient(135deg, #ede9fe 0%, #dbeafe 100%);
            color: #312e81;
            font-weight: 900;
            font-size: 11px;
        }

        .cantidad-pill {
            display: inline-block;
            min-width: 32px;
            padding: 6px 8px;
            border-radius: 10px;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            color: #1d4ed8;
            font-weight: 900;
        }

        .semana-pill {
            display: inline-block;
            min-width: 40px;
            padding: 6px 8px;
            border-radius: 10px;
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            color: #92400e;
            font-weight: 900;
        }

        .si-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 36px;
            padding: 5px 10px;
            border-radius: 999px;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            font-weight: 900;
            box-shadow: 0 8px 18px rgba(34, 197, 94, 0.22);
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0%   { transform: scale(1); box-shadow: 0 8px 18px rgba(34, 197, 94, 0.18); }
            50%  { transform: scale(1.03); box-shadow: 0 10px 22px rgba(34, 197, 94, 0.28); }
            100% { transform: scale(1); box-shadow: 0 8px 18px rgba(34, 197, 94, 0.18); }
        }

        .center { text-align: center; }
        .empty-cell { color: #94a3b8; }
    </style>
    </head>
    <body>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Tipo</th>
                        <th>Fecha</th>
                        <th>Semana</th>
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
                <td class="center"><span class="semana-pill">S{row['Semana']}</span></td>
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

    alto = max(280, 120 + (len(df) * 66))
    components.html(html, height=alto, scrolling=False)

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

if "inversion_valor" not in st.session_state:
    st.session_state["inversion_valor"] = 1000000.0

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">¿Cuánto logras con tu inversión y tu cronograma de contenido?</div>
    <div class="hero-subtitle">Vista final visible desde el inicio.</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LAYOUT
# =========================================================
col_izq, col_der = st.columns([1.8, 1], gap="medium")

with col_izq:
    final_slot = st.container()
    editor_slot = st.container()

    with editor_slot:
        with st.expander("Cronograma de contenido", expanded=False):
            editor_df = st.data_editor(
                st.session_state["cronograma_editable"],
                key="editor_cronograma",
                num_rows="dynamic",
                hide_index=True,
                use_container_width=True,
                height=320,
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
            st.markdown('<div class="editor-note">Aquí puedes agregar, borrar o editar filas.</div>', unsafe_allow_html=True)
            st.session_state["cronograma_editable"] = limpiar_editable(editor_df)

    with final_slot:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="view-title">Vista final</div>', unsafe_allow_html=True)
        df_cronograma = cronograma_calculado(st.session_state["cronograma_editable"])
        render_cronograma_html(df_cronograma)
        st.markdown('</div>', unsafe_allow_html=True)

with col_der:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Proyección rápida</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="calc-top">
        <div class="calc-top-title">Proyección rápida</div>
    </div>
    """, unsafe_allow_html=True)

    inversion = st.number_input(
        "Inversión",
        min_value=0.0,
        value=float(st.session_state["inversion_valor"]),
        step=1000.0,
        format="%.0f",
        key="input_inversion"
    )
    st.session_state["inversion_valor"] = inversion

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
