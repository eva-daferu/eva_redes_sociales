import streamlit as st
import requests
import pandas as pd

API = "https://pahubisas.pythonanywhere.com/scrape"

st.set_page_config(page_title="TikTok Scraper", layout="wide")

st.title("TikTok Scraper")

if st.button("🔄 Conectar y ejecutar scraper"):
    with st.spinner("Ejecutando scraper real… puede tardar varios minutos"):
        try:
            r = requests.post(API, json={}, timeout=900)
            data = r.json()
        except Exception as e:
            st.error(f"Error ejecutando scraper: {e}")
            st.stop()

    if "data" not in data:
        st.error("El backend no retornó resultados válidos.")
        st.json(data)
        st.stop()

    st.success(f"Scraper finalizado. Registros: {data.get('count',0)}")

    df = pd.DataFrame(data["data"])
    st.dataframe(df, use_container_width=True)
