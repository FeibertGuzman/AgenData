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
