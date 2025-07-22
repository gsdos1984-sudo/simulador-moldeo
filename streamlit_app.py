import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Simulador de Moldeo", layout="wide")

st.title("🧪 Simulador de Moldeo EPS")
st.markdown("""
Este simulador muestra cómo ciertos parámetros afectan el **peso**, **largo** y **ancho** de una pieza moldeada.
""")

# Entrada de parámetros
st.sidebar.header("Parámetros de entrada")
steam_pressure = st.sidebar.slider("Presión de vapor (bar)", 0.5, 2.0, 1.5, 0.1)
tiempo_vapor = st.sidebar.slider("Tiempo de vapor (s)", 1, 10, 5)
temperatura_fija = st.sidebar.slider("Temperatura FIXED SIDE (°C)", 30, 100, 61)
temperatura_movil = st.sidebar.slider("Temperatura MOBILE SIDE (°C)", 30, 100, 45)
densidad_bead = st.sidebar.slider("Densidad del bead (g/L)", 15, 35, 25)

# Fórmulas simuladas para ilustración
peso_base = 1800  # gramos
largo_base = 1200  # mm
ancho_base = 800   # mm

# Cálculos simples
peso = peso_base * (steam_pressure / 1.5) * (densidad_bead / 25)
largo = largo_base * (1 - (steam_pressure - 1.5)*0.05)
ancho = ancho_base * (1 - (steam_pressure - 1.5)*0.03)

peso = round(peso, 2)
largo = round(largo, 2)
ancho = round(ancho, 2)

# Mostrar resultados
col1, col2, col3 = st.columns(3)
col1.metric("📦 Peso de la pieza (g)", peso)
col2.metric("📏 Largo (mm)", largo)
col3.metric("📐 Ancho (mm)", ancho)

# Visualización
fig, ax = plt.subplots()
rectangle = plt.Rectangle((0, 0), ancho, largo, fc='lightblue', edgecolor='black')
ax.add_patch(rectangle)
ax.set_xlim(0, 2000)
ax.set_ylim(0, 2000)
ax.set_title("Vista superior de la pieza moldeada")
ax.set_xlabel("Ancho (mm)")
ax.set_ylabel("Largo (mm)")
ax.set_aspect('equal')
st.pyplot(fig)

st.caption("Versión inicial del simulador. Autor: Miguel Verástegui")
