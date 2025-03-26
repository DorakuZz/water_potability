import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Cargar modelo y scaler
modelo = joblib.load('modelo_calidad_agua_completo.pkl')
scaler = modelo['scaler']

# Diccionario de traducción de variables
traducciones = {
    'ph': 'Potencial de Hidrógeno (pH)',
    'Hardness': 'Dureza del Agua',
    'Solids': 'Sólidos Totales',
    'Chloramines': 'Cloraminas',
    'Sulfate': 'Sulfatos',
    'Conductivity': 'Conductividad Eléctrica',
    'Organic_carbon': 'Carbono Orgánico',
    'Trihalomethanes': 'Trihalometanos',
    'Turbidity': 'Turbidez'
}

# Cargar datos originales para rangos
url = "https://raw.githubusercontent.com/DorakuZz/water_potability/refs/heads/main/water_potability.csv"
df_original = pd.read_csv(url)

def main():
    st.title("🚰 Predictor de Potabilidad del Agua")
    st.markdown("### Evalúa la calidad del agua con Machine Learning")

    # Sidebar con información
    st.sidebar.header("Parámetros de Entrada")
    st.sidebar.markdown("Ajusta los valores de cada característica")

    # Crear sliders para cada característica
    input_data = {}
    for columna in df_original.columns[:-1]:
        min_val = df_original[columna].min()
        max_val = df_original[columna].max()
        default_val = df_original[columna].median()
        
        input_data[columna] = st.sidebar.slider(
            traducciones.get(columna, columna),
            float(min_val), 
            float(max_val), 
            float(default_val)
        )

    # Botón de predicción
    if st.sidebar.button("Predecir Potabilidad del Agua"):
        # Convertir input a DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Escalar datos
        input_scaled = scaler.transform(input_df)
        
        # Predicción
        prediccion = modelo['modelo'].predict(input_scaled)[0]
        probabilidad = modelo['modelo'].predict_proba(input_scaled)[0]
        
        # Mostrar resultados
        st.header("Resultados de la Predicción")
        
        if prediccion == 1:
            st.success("✅ Agua Potable")
            st.info(f"Probabilidad de Potabilidad: {probabilidad[1]*100:.2f}%")
        else:
            st.error("❌ Agua No Potable")
            st.info(f"Probabilidad de No Potabilidad: {probabilidad[0]*100:.2f}%")
        
        # Gráfico de probabilidades
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[go.Pie(
            labels=['No Potable', 'Potable'], 
            values=probabilidad,
            textinfo='label+percent',
            marker_colors=['red', 'green']
        )])
        
        fig.update_layout(title='Probabilidades de Potabilidad')
        st.plotly_chart(fig)

    # Información adicional
    st.sidebar.markdown("""
    ### Sobre la Predicción
    - Modelo basado en Random Forest
    - Precisión superior al 68%
    - Usa 9 características para predecir
    """)

if __name__ == "__main__":
    main()
