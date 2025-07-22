import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO

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

# Paso 1: Evaluación del colapso por exceso de parámetros
colapso = 0
mensaje_colapso = ""
if steam_pressure > 1.7:
    colapso += (steam_pressure - 1.7) * 0.1
    mensaje_colapso += "\n- Alta presión de vapor"
if temperatura_fija > 80:
    colapso += (temperatura_fija - 80) * 0.02
    mensaje_colapso += "\n- Temperatura FIXED SIDE elevada"
if temperatura_movil > 80:
    colapso += (temperatura_movil - 80) * 0.02
    mensaje_colapso += "\n- Temperatura MOBILE SIDE elevada"
if tiempo_vapor > 8:
    colapso += (tiempo_vapor - 8) * 0.05
    mensaje_colapso += "\n- Tiempo de vapor excesivo"

# Paso 2: Ajuste de expansión por condiciones ideales
expansion = 1.0
if steam_pressure > 1.2 and steam_pressure < 1.6 and temperatura_fija > 50 and temperatura_fija < 70 and temperatura_movil > 40 and temperatura_movil < 60:
    expansion += 0.03
    st.success("✅ Condiciones ideales detectadas. Ligeramente mayor expansión.")

# Paso 3: Contracción por enfriamiento desigual
contraccion = 0
if abs(temperatura_fija - temperatura_movil) > 20:
    contraccion += 0.02
    st.info("🔵 Diferencia térmica significativa: posible contracción en el molde.")

# Cálculos ajustados con efecto de colapso, expansión y contracción
peso = peso_base * (steam_pressure / 1.5) * (densidad_bead / 25) * (1 - colapso)
largo = largo_base * (1 - (steam_pressure - 1.5)*0.05) * (1 - colapso) * expansion * (1 - contraccion)
ancho = ancho_base * (1 - (steam_pressure - 1.5)*0.03) * (1 - colapso) * expansion * (1 - contraccion)

peso = max(round(peso, 2), 0)
largo = max(round(largo, 2), 0)
ancho = max(round(ancho, 2), 0)

# Mostrar advertencia de colapso si aplica
if mensaje_colapso:
    st.warning("⚠️ Posible colapso detectado debido a: " + mensaje_colapso)

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

# Paso 4: Gráfico de presión vs peso
fig2, ax2 = plt.subplots()
pressures = np.linspace(0.5, 2.0, 50)
pesos = peso_base * (pressures / 1.5) * (densidad_bead / 25) * (1 - colapso)
ax2.plot(pressures, pesos, color='darkgreen')
ax2.axvline(x=steam_pressure, linestyle='--', color='red', label='Presión actual')
ax2.set_title("Peso estimado según presión de vapor")
ax2.set_xlabel("Presión de vapor (bar)")
ax2.set_ylabel("Peso de la pieza (g)")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)

# Paso 5: Gráfico de diferencia térmica vs contracción
fig3, ax3 = plt.subplots()
deltas = np.linspace(0, 50, 100)
contracciones = [0.02 if d > 20 else 0 for d in deltas]
ax3.plot(deltas, contracciones, color='orange')
ax3.axvline(x=abs(temperatura_fija - temperatura_movil), linestyle='--', color='blue', label='Diferencia actual')
ax3.set_title("Contracción estimada según diferencia térmica")
ax3.set_xlabel("Diferencia entre FIXED y MOBILE SIDE (°C)")
ax3.set_ylabel("Factor de contracción")
ax3.grid(True)
ax3.legend()
st.pyplot(fig3)

# Paso 6: Exportar datos
resultados = pd.DataFrame({
    "Presión de Vapor (bar)": [steam_pressure],
    "Tiempo de Vapor (s)": [tiempo_vapor],
    "Temp FIXED (°C)": [temperatura_fija],
    "Temp MOBILE (°C)": [temperatura_movil],
    "Densidad Bead (g/L)": [densidad_bead],
    "Peso (g)": [peso],
    "Largo (mm)": [largo],
    "Ancho (mm)": [ancho]
})

st.subheader("📄 Exportar datos")
st.dataframe(resultados)

buffer = BytesIO()
resultados.to_excel(buffer, index=False)
buffer.seek(0)
st.download_button(
    label="📥 Descargar Excel con resultados",
    data=buffer,
    file_name="simulador_resultado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.caption("Versión inicial del simulador. Autor: Miguel Verástegui")
