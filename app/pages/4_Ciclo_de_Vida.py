import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

import os

def get_path(*paths):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base, *paths)

ruta = get_path("data", "data_universo_pdd.xlsx")

base = pd.read_excel(ruta, sheet_name="base_pdd")

# ========================
# LIMPIEZA
# ========================
base["edad"] = pd.to_numeric(base["edad"], errors="coerce")
base = base.dropna(subset=["edad"])

# ========================
# SOLO MUJERES (opcional)
# ========================
base = base[base["sexo"] == "MUJER"]

# ========================
# GRÁFICA
# ========================
st.title("🧬 Desaparicion de las Mujeres según el Ciclo de vida")

fig = px.histogram(
    base,
    x="edad",
    nbins=60,
    opacity=0.7,
    color_discrete_sequence=["purple"]
)

# ========================
# LÍNEAS DE CICLO DE VIDA
# ========================
lineas = [
    (11, "Niñez"),
    (17, "Adolescencia"),
    (28, "Juventud"),
    (59, "Adultez")
]

for x, label in lineas:
    fig.add_vline(
        x=x,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text=label,
        annotation_position="top"
    )

fig.update_layout(
    height=500,
    xaxis_title="Edad",
    yaxis_title="Frecuencia"
)

st.plotly_chart(fig, use_container_width=True)

# ========================
# CLASIFICACIÓN DE EDAD
# ========================
def clasificar_edad(edad):
    if edad <= 11:
        return "Niñez"
    elif edad <= 17:
        return "Adolescencia"
    elif edad <= 28:
        return "Juventud"
    elif edad <= 59:
        return "Adultez"
    else:
        return "Personas mayores"

base["Ciclo"] = base["edad"].apply(clasificar_edad)

# ========================
# TABLA RESUMEN
# ========================
tabla = base.groupby("Ciclo").size().reset_index(name="Total")

# calcular porcentaje
tabla["Porcentaje"] = tabla["Total"] / tabla["Total"].sum() * 100

# ordenar
orden = ["Niñez", "Adolescencia", "Juventud", "Adultez", "Personas mayores"]
tabla["Ciclo"] = pd.Categorical(tabla["Ciclo"], categories=orden, ordered=True)
tabla = tabla.sort_values("Ciclo")

st.markdown("### 📋 Distribución por ciclo de vida")

# formateo bonito
tabla["Total"] = tabla["Total"].apply(lambda x: f"{x:,}")
tabla["Porcentaje"] = tabla["Porcentaje"].apply(lambda x: f"{x:.2f}%")

st.dataframe(tabla, use_container_width=True)




from PIL import Image
import os

rutaB = get_path("assets", "Info1.jpg")

st.write("Ruta imagen:", rutaB)
st.write("Existe:", os.path.exists(rutaB))

img = Image.open(rutaB)

st.image(img, use_container_width=True)