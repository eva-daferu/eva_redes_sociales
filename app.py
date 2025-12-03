import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Prueba Carga Excel", layout="wide")

# Ruta del Excel
EXCEL_PATH = r"C:\Users\diana\OneDrive\Documentos\WasaFlete\Eva\descargas\base_tiktok.xlsx"

st.title("🔍 PRUEBA CARGA EXCEL")
st.markdown("---")

# Mostrar información del archivo
st.subheader("📁 Información del Archivo")
st.write(f"**Ruta:** `{EXCEL_PATH}`")

# Verificar si el archivo existe
file_exists = os.path.exists(EXCEL_PATH)
st.write(f"**¿Existe el archivo?:** {'✅ SÍ' if file_exists else '❌ NO'}")

if not file_exists:
    st.error("❌ EL ARCHIVO NO EXISTE EN ESA RUTA")
    st.info("""
    **Posibles problemas:**
    1. La ruta está mal escrita
    2. El archivo fue movido
    3. OneDrive no está sincronizado
    """)
    st.stop()

# Intentar cargar el archivo
st.subheader("📊 Intentando cargar datos...")

try:
    # Leer el Excel
    df = pd.read_excel(EXCEL_PATH)
    
    # Mostrar información básica
    st.success(f"✅ Archivo cargado correctamente!")
    st.write(f"**Filas:** {len(df)}")
    st.write(f"**Columnas:** {len(df.columns)}")
    
    # Mostrar nombres de columnas
    st.subheader("📋 Columnas encontradas:")
    for i, col in enumerate(df.columns, 1):
        st.write(f"{i}. `{col}`")
    
    # Verificar columnas requeridas
    required_columns = ['duracion_video', 'titulo', 'fecha_publicacion', 
                       'privacidad', 'visualizaciones', 'me_gusta', 'comentarios']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.warning(f"⚠️ Columnas faltantes: {missing_columns}")
    else:
        st.success("✅ Todas las columnas requeridas están presentes")
    
    # Mostrar primeras filas
    st.subheader("👀 Primeras 5 filas del Excel:")
    st.dataframe(df.head(), use_container_width=True)
    
    # Mostrar tipos de datos
    st.subheader("🔧 Tipos de datos:")
    st.write(df.dtypes)
    
    # Botón para mostrar más datos
    if st.button("📈 MOSTRAR TODOS LOS DATOS"):
        st.subheader("📊 Todos los datos del Excel:")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Estadísticas simples
        st.subheader("📊 Estadísticas:")
        if 'visualizaciones' in df.columns:
            try:
                # Intentar convertir a numérico
                df['visualizaciones_num'] = pd.to_numeric(df['visualizaciones'].astype(str).str.replace(',', ''), errors='coerce')
                total_views = df['visualizaciones_num'].sum()
                st.metric("Total Visualizaciones", f"{total_views:,.0f}")
            except:
                st.write("No se pudieron calcular visualizaciones")
        
except Exception as e:
    st.error(f"❌ ERROR al cargar el archivo: {str(e)}")
    st.info("""
    **Posibles soluciones:**
    1. Verifica que el archivo no esté abierto en otro programa
    2. Revisa que sea un archivo Excel válido (.xlsx)
    3. Prueba a guardar una copia y cargar esa copia
    """)

st.markdown("---")
st.info("""
**Para probar en consola:**
```python
import pandas as pd
import os

path = r"C:\\Users\\diana\\OneDrive\\Documentos\\WasaFlete\\Eva\\descargas\\base_tiktok.xlsx"
print(f"Existe: {os.path.exists(path)}")
df = pd.read_excel(path)
print(f"Filas: {len(df)}")
print(f"Columnas: {list(df.columns)}")""")
