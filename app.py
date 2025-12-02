import streamlit as st
import requests
import pandas as pd

API = "https://pahubisas.pythonanywhere.com/scrape"

st.set_page_config(
    page_title="TikTok Scraper",
    layout="wide"
)

st.title("TikTok Scraper · PythonAnywhere")

cookies_input = st.text_area(
    "Pega aquí el JSON de cookies de sesión de TikTok",
    height=150,
    placeholder='[{"name":"sessionid","value":"XXX","domain":".tiktok.com","path":"/"}]'
)

if st.button("Conectar y ejecutar scraper"):
    with st.spinner("Ejecutando scraper (1–3 min)…"):

        try:
            payload = {"cookies_json": cookies_input}
            resp = requests.post(
                API,
                json=payload,
                timeout=900
            )
            data = resp.json()
        except Exception as e:
            st.error(str(e))
            st.stop()

        if "data" not in data:
            st.error("No llegaron datos desde el backend.")
            st.json(data)
            st.stop()

        registros = data["data"]
        if not registros:
            st.warning("Scraper terminó sin resultados.")
            st.json(data)
            st.stop()

        df = pd.DataFrame(registros)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar CSV",
            csv,
            "tiktok_scrape_resultados.csv",
            "text/csv"
        )
