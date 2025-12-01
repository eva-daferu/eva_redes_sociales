import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Conectar Redes", layout="wide")

# ====== ESTILOS HTML (idénticos al modal-frame original) ======

modal_css = """
<style>
    body { background-color: #f7fafc !important; }

    .modal-frame {
        max-width: 600px;
        margin: 40px auto;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        padding: 40px;
        text-align: center;
    }

    .modal-title {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 20px;
    }

    .modal-subtitle {
        font-size: 18px;
        line-height: 1.6;
        color: #4a5568;
        margin-bottom: 40px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }

    .iframe-box {
        width: 100%;
        height: 630px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-top: 25px;
    }
</style>
"""

st.markdown(modal_css, unsafe_allow_html=True)

# ====================
#       UI
# ====================

st.title("Conectar Redes Sociales")

col1, col2, col3, col4, col5 = st.columns(5)

def mostrar_modal(url):
    st.markdown(
        """
        <div class="modal-frame">
            <h1 class="modal-title">Autenticación TikTok</h1>
            <p class="modal-subtitle">
                Inicia sesión directamente en la ventana integrada para continuar.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Marco de la web embebida
    components.iframe(url, width=600, height=630, scrolling=True)


# ====================
#   BOTÓN TIKTOK
# ====================

with col3:
    if st.button("TikTok"):
        # URL EXACTA QUE ABRE TU SELENIUM
        mostrar_modal("https://www.tiktok.com/login")


