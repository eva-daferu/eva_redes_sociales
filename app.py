import streamlit as st
import pandas as pd
import requests
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Social Media Dashboard", layout="wide", page_icon="📊")


@st.cache_data
def cargar_backend():
    try:
        url = "http://pahubisas.pythonanywhere.com/data"
        r = requests.get(url, timeout=20)
        js = r.json()

        if js.get("status") != "success":
            return pd.DataFrame(), {}
        return pd.DataFrame(js["data"]), js["analytics"]

    except Exception:
        return pd.DataFrame(), {}


df, analytics = cargar_backend()


if df.empty:
    st.error("No se pudieron cargar datos desde el backend.")
    st.stop()


df["fecha_publicacion"] = pd.to_datetime(df["fecha_publicacion"], errors="coerce")
df["dias_desde_publicacion"] = (pd.Timestamp.now() - df["fecha_publicacion"]).dt.days
df["dias_desde_publicacion"] = df["dias_desde_publicacion"].fillna(1).astype(int)
df["rendimiento_por_dia"] = df["visualizaciones"] / df["dias_desde_publicacion"]


st.title("📊 SOCIAL MEDIA DASHBOARD")
st.subheader(f"Total videos: {len(df)} — Views: {df['visualizaciones'].sum():,}")


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Videos", len(df))

with col2:
    st.metric("Total Views", f"{df['visualizaciones'].sum():,}")

with col3:
    st.metric("Avg Views per Video", f"{df['visualizaciones'].mean():.0f}")

with col4:
    engagement_rate = (
        (df["me_gusta"].sum() + df["comentarios"].sum())
        / df["visualizaciones"].sum() * 100
        if df["visualizaciones"].sum() > 0 else 0
    )
    st.metric("Engagement Rate", f"{engagement_rate:.2f}%")


st.markdown("### 📈 Top 10 Videos")
top = df.nlargest(10, "visualizaciones")[
    ["titulo", "fecha_publicacion", "visualizaciones", "me_gusta", "comentarios", "rendimiento_por_dia"]
]
top["fecha_publicacion"] = top["fecha_publicacion"].dt.strftime("%Y-%m-%d")

st.table(top)


st.markdown("### 🧮 Estadísticas Generales")

st.json(analytics)
