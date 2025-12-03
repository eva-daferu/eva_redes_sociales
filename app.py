import streamlit as st
import os
import glob

st.set_page_config(page_title="Buscar Archivo", layout="wide")

st.title("🔍 BUSCAR ARCHIVO base_tiktok.xlsx")
st.markdown("---")

# Posibles rutas a verificar
possible_paths = [
    r"C:\Users\diana\OneDrive\Documentos\WasaFlete\Eva\descargas\base_tiktok.xlsx",
    r"C:\Users\diana\Documents\WasaFlete\Eva\descargas\base_tiktok.xlsx",
    r"C:\Users\diana\OneDrive\Documentos\WasaFlete\base_tiktok.xlsx",
    r"C:\Users\diana\Downloads\base_tiktok.xlsx",
    r"C:\Users\diana\Desktop\base_tiktok.xlsx",
    r"D:\base_tiktok.xlsx",
    r"E:\base_tiktok.xlsx",
]

st.subheader("📁 Buscando archivo en rutas posibles:")

found_path = None
for path in possible_paths:
    exists = os.path.exists(path)
    status = "✅ EXISTE" if exists else "❌ NO EXISTE"
    st.write(f"`{path}` → {status}")
    
    if exists:
        found_path = path
        break

if found_path:
    st.success(f"🎯 ARCHIVO ENCONTRADO EN: `{found_path}`")
    
    # Mostrar información del archivo
    file_size = os.path.getsize(found_path) / 1024 / 1024  # MB
    st.write(f"**Tamaño:** {file_size:.2f} MB")
    
    # Intentar cargar
    try:
        import pandas as pd
        df = pd.read_excel(found_path, nrows=5)
        st.success("✅ Archivo se puede leer correctamente")
        st.write(f"**Filas (muestra):** {len(df)}")
        st.write(f"**Columnas:** {list(df.columns)}")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error al leer: {str(e)}")
        
else:
    st.error("❌ ARCHIVO NO ENCONTRADO EN NINGUNA RUTA")
    
    st.subheader("🔍 Búsqueda en todo el sistema (puede tardar):")
    
    if st.button("🔎 BUSCAR ARCHIVO EN TODO EL SISTEMA"):
        import subprocess
        st.info("Buscando... esto puede tomar varios minutos")
        
        # Buscar en disco C:
        try:
            result = subprocess.run(
                ['cmd', '/c', 'dir', '/s', '/b', 'C:\\*base_tiktok*.xlsx'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                st.success("📂 ARCHIVOS ENCONTRADOS:")
                files = result.stdout.strip().split('\n')
                for file in files[:10]:  # Mostrar primeros 10
                    if file:
                        st.write(f"`{file}`")
            else:
                st.warning("No se encontraron archivos con ese nombre")
                
        except Exception as e:
            st.error(f"Error en búsqueda: {str(e)}")

st.markdown("---")
st.subheader("📋 Instrucciones para encontrar la ruta:")
st.info("""
1. **Abre el Explorador de Archivos**
2. **Navega hasta base_tiktok.xlsx**
3. **Haz clic en la barra de direcciones**
4. **Copia la ruta COMPLETA**
5. **Pégala aquí:** (usando `r"TU_RUTA_COMPLETA"`)

Ejemplo: `r"C:\\Users\\diana\\Documentos\\mi_archivo.xlsx"`
""")

# Entrada manual de ruta
st.subheader("✏️ Ingresar ruta MANUALMENTE:")
user_path = st.text_input("Pega la ruta COMPLETA aquí:", value=r"C:\")

if user_path and os.path.exists(user_path):
    st.success(f"✅ Ruta válida: `{user_path}`")
    st.session_state.excel_path = user_path
    st.write("**Ahora usa esta ruta en el código principal:**")
    st.code(f'EXCEL_PATH = r"{user_path}"', language='python')
else:
    st.warning("❌ La ruta no existe o no es válida")

st.markdown("---")
st.info("""
**Resumen:**
1. Encuentra la ruta REAL con este código
2. Copia la ruta que funcione
3. Usa esa ruta en el código principal
4. El archivo DEBE existir físicamente en tu computadora
""")
