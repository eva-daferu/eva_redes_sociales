import streamlit as st
import webbrowser

st.set_page_config(page_title="Conexión Redes", layout="centered")

st.title("Conectar Redes Sociales")

st.write("Selecciona una red social para abrir la ventana de acceso.")

def abrir(url):
    webbrowser.open_new(url)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Facebook"):
        abrir("https://www.facebook.com/login")

with col2:
    if st.button("Instagram"):
        abrir("https://www.instagram.com/accounts/login/")

with col3:
    if st.button("TikTok"):
        abrir("https://www.tiktok.com/login")

with col4:
    if st.button("Twitter"):
        abrir("https://twitter.com/login")

with col5:
    if st.button("LinkedIn"):
        abrir("https://www.linkedin.com/login")
