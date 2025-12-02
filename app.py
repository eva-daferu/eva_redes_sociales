import streamlit as st
import requests
import json
import pandas as pd

API_BASE_URL = "https://pahubisas.pythonanywhere.com"


def ejecutar_healthcheck():
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=30)
        resp.raise_for_status()
        return True, resp.json()
    except Exception as e:
        return False, {"error": str(e)}


def ejecutar_test():
    try:
        resp = requests.get(f"{API_BASE_URL}/test", timeout=60)
        resp.raise_for_status()
        return True, resp.json()
    except Exception as e:
        return False, {"error": str(e)}


def ejecutar_scraper(cookies_json: str):
    try:
        cookies = json.loads(cookies_json)
    except Exception as e:
        return False, {"error": f"JSON de cookies inválido: {e}"}

    payload = {"cookies": cookies}

    try:
        resp = requests.post(
            f"{API_BASE_URL}/scrape",
            json=payload,
            timeout=900,  # hasta 15 minutos
        )
        resp.raise_for_status()
        return True, resp.json()
    except Exception as e:
        return False, {"error": str(e)}


def main():
    st.set_page_config(
        page_title="TikTok Scraper · PythonAnywhere",
        page_icon="🎬",
        layout="wide",
    )

    st.title("TikTok Scraper · PythonAnywhere")

    st.markdown(
        "Interfaz mínima para ejecutar el scraper real de TikTok hospedado en PythonAnywhere.\n\n"
        "- El login se hace manualmente en TikTok (no desde aquí).\n"
        "- Aquí solo se envían las cookies de sesión al backend para que ejecute el scraper."
    )

    st.markdown("---")

    col_health, col_test = st.columns(2)

    with col_health:
        if st.button("Probar conexión (/health)"):
            ok, data = ejecutar_healthcheck()
            if ok:
                st.success("Conexión OK")
            else:
                st.error("Error en /health")
            st.json(data)

    with col_test:
        if st.button("Probar modo demo (/test)"):
            ok, data = ejecutar_test()
            if ok:
                st.success("Respuesta /test recibida")
            else:
                st.error("Error en /test")
            st.json(data)

    st.markdown("---")
    st.subheader("Scraper real de TikTok (/scrape)")

    st.markdown(
        "1. Inicia sesión en TikTok desde tu navegador.\n"
        "2. Exporta tus **cookies de sesión** de TikTok.\n"
        "3. Pega abajo el JSON completo de cookies.\n"
        "4. Ejecuta el scraper (puede tardar de 1 a 3 minutos)."
    )

    cookies_input = st.text_area(
        "Pega aquí el JSON de cookies de TikTok",
        height=220,
        placeholder='[{"name": "sessionid", "value": "xxx", "domain": ".tiktok.com", "path": "/"}]',
    )

    ejecutar = st.button("Ejecutar scraper real (POST /scrape)")

    if ejecutar:
        if not cookies_input.strip():
            st.error("Debes pegar el JSON de cookies antes de ejecutar.")
            st.stop()

        with st.spinner("Ejecutando scraper en PythonAnywhere (puede tardar varios minutos)..."):
            ok, data = ejecutar_scraper(cookies_input)

        if not ok or data.get("status") in {"error"}:
            st.error("Error al ejecutar el scraper.")
            st.json(data)
            st.stop()

        st.success(f"Scraper finalizado. Registros recibidos: {data.get('count', 0)}")
        st.json(
            {
                "status": data.get("status"),
                "count": data.get("count"),
                "timestamp": data.get("timestamp"),
            }
        )

        registros = data.get("data", [])
        if registros:
            df = pd.DataFrame(registros)
            st.markdown("### Resultados reales del scraper")
            st.dataframe(df, use_container_width=True)

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Descargar resultados en CSV",
                data=csv_bytes,
                file_name="tiktok_scraper_resultados.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
