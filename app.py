import streamlit as st
import pandas as pd
import json
import io
import plotly.express as px
import nbformat as nbf

# Configuracion de la pagina
st.set_page_config(page_title="Agente Analista de Datos", layout="wide", page_icon="🕵️")

st.title("🕵️ Agente Analista de Datos Automatizado")
st.markdown("Sube un archivo **CSV, JSON o Excel** para generar un dashboard interactivo, realizar limpieza básica y descargar un cuaderno Jupyter (.ipynb) con tu análisis.")

def generate_notebook(filename, columns):
    """Genera el contenido de un cuaderno de Jupyter basado en el DataFrame cargado."""
    nb = nbf.v4.new_notebook()
    
    # Celda de Markdown de introduccion
    texto_md = f"# Análisis de Datos: {filename}\nEste cuaderno fue generado automáticamente por el Agente Analista de Datos."
    nb['cells'].append(nbf.v4.new_markdown_cell(texto_md))
    
    # Celda de imports
    imports = "import pandas as pd\nimport plotly.express as px\nimport matplotlib.pyplot as plt\nimport seaborn as sns"
    nb['cells'].append(nbf.v4.new_code_cell(imports))
    
    # Celda de carga de datos
    ext = filename.split('.')[-1]
    if ext == 'csv':
        carga = f"df = pd.read_csv('{filename}')\ndf.head()"
    elif ext == 'json':
        carga = f"df = pd.read_json('{filename}')\ndf.head()"
    else:
        carga = f"df = pd.read_excel('{filename}')\ndf.head()"
        
    intro_carga = "# Asegúrate de que el archivo se encuentre en el mismo directorio que este cuaderno para cargarlo correctamente."
    nb['cells'].append(nbf.v4.new_code_cell(f"{intro_carga}\n{carga}"))
    
    # Info de las columnas
    cols_str = "', '".join(columns)
    celda_cols = f"# Las columnas detectadas son:\n# ['{cols_str}']\ndf.info()"
    nb['cells'].append(nbf.v4.new_code_cell(celda_cols))
    
    # Limpieza propuesta
    limpieza = "# Limpieza basica (puedes descomentar para aplicar)\n# df = df.drop_duplicates()\n# df = df.dropna()"
    nb['cells'].append(nbf.v4.new_code_cell(limpieza))
    
    # Estadisticas
    estadisticas = "# Estadisticas Descriptivas\ndf.describe()"
    nb['cells'].append(nbf.v4.new_code_cell(estadisticas))
    
    buffer = io.StringIO()
    nbf.write(nb, buffer)
    return buffer.getvalue()

# Barra lateral para carga de archivos
uploaded_file = st.sidebar.file_uploader("📥 Sube tu dataset aquí:", type=["csv", "json", "xlsx"])

if uploaded_file is not None:
    try:
        # Cargar los datos segun la extension
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                try:
                    df = pd.read_csv(uploaded_file, encoding='latin-1')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='cp1252')
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            
        st.success(f"Archivo `{uploaded_file.name}` cargado correctamente! ({df.shape[0]} filas, {df.shape[1]} columnas)")
        
        # Opciones de Limpieza
        st.subheader("🧹 Limpieza de Datos")
        col_clean1, col_clean2 = st.columns(2)
        
        with col_clean1:
            if st.checkbox("Eliminar duplicados"):
                filas_antes = df.shape[0]
                df = df.drop_duplicates()
                st.info(f"Se eliminaron {filas_antes - df.shape[0]} filas duplicadas.")
                
        with col_clean2:
            if st.checkbox("Eliminar filas con valores nulos (NA)"):
                filas_antes = df.shape[0]
                df = df.dropna()
                st.info(f"Se eliminaron {filas_antes - df.shape[0]} filas con NA.")
                
        # Vista de Datos
        st.subheader("👀 Vista Previa de los Datos")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Estadistica
        st.subheader("📊 Resumen Estadístico")
        st.dataframe(df.describe(), use_container_width=True)
        
        # Dashboard Automatico
        st.subheader("📈 Dashboard Interactivo")
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(numeric_cols) > 0:
            st.markdown("#### Histograma de Variable Numérica")
            num_var = st.selectbox("Selecciona la variable para el histograma:", numeric_cols)
            fig_hist = px.histogram(df, x=num_var, marginal="box", color_discrete_sequence=["#1f77b4"])
            st.plotly_chart(fig_hist, use_container_width=True)
            
            if len(numeric_cols) > 1:
                st.markdown("#### Gráfico de Dispersión (Relación entre 2 Variables Numéricas)")
                col_scatter1, col_scatter2 = st.columns(2)
                with col_scatter1:
                    x_var = st.selectbox("Variable X:", numeric_cols, index=0)
                with col_scatter2:
                    y_var = st.selectbox("Variable Y:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                
                fig_scatter = px.scatter(df, x=x_var, y=y_var, color_discrete_sequence=["#ff7f0e"], hover_data=df.columns)
                st.plotly_chart(fig_scatter, use_container_width=True)
                
        if len(categorical_cols) > 0:
            st.markdown("#### Frecuencia de Vabiable Categórica")
            cat_var = st.selectbox("Selecciona la variable categórica:", categorical_cols)
            cat_counts = df[cat_var].value_counts().reset_index()
            cat_counts.columns = [cat_var, 'Frecuencia']
            fig_bar = px.bar(cat_counts, x=cat_var, y='Frecuencia', color=cat_var)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Generar Notebook
        st.sidebar.markdown("---")
        st.sidebar.subheader("📓 Jupyter Notebook")
        st.sidebar.markdown("Genera un cuaderno listo con tu análisis.")
        
        notebook_str = generate_notebook(uploaded_file.name, list(df.columns))
        
        st.sidebar.download_button(
            label="Descargar Notebook (.ipynb)",
            data=notebook_str,
            file_name=f"Analisis_{uploaded_file.name.split('.')[0]}.ipynb",
            mime="application/x-ipynb+json"
        )
        
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("👈 Sube un archivo en el panel izquierdo para arrancar el agente analista de datos.")
