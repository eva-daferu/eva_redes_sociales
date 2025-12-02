import streamlit as st
import requests
import json

API = "https://pahubisas.pythonanywhere.com"

st.set_page_config(page_title="TikTok Scraper", layout="centered")

st.title("Conexión PythonAnywhere ✓")


# ------------------------------
# CHEQUEO BÁSICO
# ------------------------------
col1, col2 = st.columns(2)

if col1.button("Health check"):
    r = requests.get(f"{API}/health")
    st.json(r.json())

if col2.button("Demo /test"):
    r = requests.get(f"{API}/test")
    st.json(r.json())


# ------------------------------
# SCRAPER REAL (POST)
# ------------------------------
st.subheader("Scraper POST /scrape")

cookies_text = st.text_area(
    "Pega JSON de cookies aquí",
    height=200,
    placeholder='[{"name":"sessionid","value":"abc","domain":".tiktok.com"}]'
)

if st.button("Ejecutar Scrape"):
    try:
        cookies = json.loads(cookies_text)
    except:
        st.error("JSON inválido")
        st.stop()

    payload = {"cookies": cookies}
    r = requests.post(f"{API}/scrape", json=payload)

    try:
        data = r.json()
        st.json(data)
    except:
        st.error("Respuesta no JSON")
