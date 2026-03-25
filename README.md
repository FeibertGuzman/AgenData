# ⚡ Dashboard Agentico

> Panel de control interactivo para crear soluciones agenticas con un set de datos.

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
</p>

<p align="center">
  <strong>Desarrollado por 
    <a href="https://github.com/FeibertGuzman/streamlit2.git">Feibert Guzmán</a>
  </strong>
</p>

---
# 🕵️ Agente Analista de Datos Automatizado

Esta aplicación Streamlit actúa como un Agente Experto en Desarrollo Web Analítico. 
Recibe un fichero `CSV`, `JSON` o `Excel`, genera un dashboard interactivo de manera automática, realiza limpieza de datos básica (eliminación de duplicados y nulos) y permite descargar un cuaderno Jupyter (`.ipynb`) con el inicio del flujo de análisis.

## Estructura
- `app.py`: Aplicación principal de Streamlit.
- `requirements.txt`: Dependencias del proyecto.

## Instalación

1. **Crear y activar un entorno virtual** (opcional pero muy recomendado):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para levantar el dashboard, ejecuta en la consola:
```bash
streamlit run app.py
```

Luego, sencillamente carga tus datos en el panel izquierdo y examina los resultados.
