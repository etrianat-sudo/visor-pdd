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
st.title("## 🧬 Ciclo de vida de las mujeres desaparecidas")
st.markdown("""
<small style='color: gray;'>
Distribución de la edad al momento de la desaparición, en el contexto del conflicto armado en Colombia.
</small>
""", unsafe_allow_html=True)

st.markdown("""
<small style='color: gray;'>
Interactúe con la gráfica desplazando el cursor sobre esta para visualizar el detalle de la información.
</small>
""", unsafe_allow_html=True)

fig = px.histogram(
    base,
    x="edad",
    nbins=60,
    opacity=0.85,
    color_discrete_sequence=["#8e44ad"]
)
fig.update_traces(
    marker_line_color="white",
    marker_line_width=1
)

fig.update_layout(
    height=450,
    xaxis_title="Edad",
    yaxis_title="Número de casos",
    bargap=0.05
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

tabla["Porcentaje"] = tabla["Total"] / tabla["Total"].sum() * 100

orden = ["Niñez", "Adolescencia", "Juventud", "Adultez", "Personas mayores"]
tabla["Ciclo"] = pd.Categorical(tabla["Ciclo"], categories=orden, ordered=True)
tabla = tabla.sort_values("Ciclo")

# SOLO porcentaje
tabla = tabla[["Ciclo", "Porcentaje"]]

tabla["Porcentaje"] = tabla["Porcentaje"].apply(lambda x: f"{x:.2f}%")



from PIL import Image
import os

rutaB = get_path("assets", "Info1.jpg")

#st.write("Ruta imagen:", rutaB)
#st.write("Existe:", os.path.exists(rutaB))

img = Image.open(rutaB)



col1, col2 = st.columns([1,1])

with col1:
    st.dataframe(tabla)

with col2:
    st.image(img, width=350)

st.markdown("""
### 📊 Clave de lectura

- La mayor concentración de casos se presenta en juventud y adultez  
- La adolescencia representa una proporción significativa del fenómeno  
- La niñez y las personas mayores tienen menor incidencia relativa  

**La desaparición afecta principalmente a población en edades productivas y reproductivas**
""")

###########################
# cohortes
#######################

cohortes = pd.read_excel(ruta, sheet_name="cohortes")

st.title("🧠 Análisis generacional de la desaparición de mujeres")

st.markdown("""
<small style='color: gray;'>
Relación entre año de desaparición, edad y cohortes de nacimiento.
</small>
""", unsafe_allow_html=True)

tipo = st.radio(
    "Seleccione población",
    ["Total PDD", "Mujeres"],
    horizontal=True
)


if tipo == "Total PDD":
    df = cohortes[cohortes["filtro"] == 1]
else:
    df = cohortes[cohortes["filtro"] == 2]

df = df[
    (df["anio_desapa"] >= 1985) &
    (df["anio_desapa"] <= 2016)
]

# 🔥 EL GRÁFICO VA FUERA DEL IF
fig = px.density_heatmap(
    df,
    x="anio_desapa",
    y="anio_nacimiento",
    z="casos",
    histfunc="sum",
    nbinsx=40,
    nbinsy=40,
    color_continuous_scale="Purples"
)

fig.update_layout(
    height=600,
    xaxis=dict(range=[1985, 2016]),
    yaxis=dict(range=[1950, 2005]),
    xaxis_title="Año de desaparición",
    yaxis_title="Año de nacimiento"
)
    
edades = [10, 20, 30, 40, 50, 60]

for edad in edades:
    x_vals = list(range(1985, 2017))
    y_vals = [x - edad for x in x_vals]

    fig.add_scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        line=dict(color="orange", width=1),
        showlegend=False
    )
   # 🔥 TEXTO (AQUÍ ESTÁ LA MAGIA)
    fig.add_annotation(
        x=2015,                    # donde aparece el texto
        y=2015 - edad,
        text=f"{edad} años",
        showarrow=False,
        font=dict(color="orange", size=15),
        textangle=-35              # inclinación tipo diagonal
    )


st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### 📊 Clave de lectura

- Seleccione población que desea visualizar PDD total o Mujeres  , PDD total( representa el total de personas dadas por desaparecidas)
- Los tonos más oscuros indican mayor concentración de casos  
- Las diagonales representan la edad al momento de la desaparición  
- La mayor intensidad se concentra entre finales de los 90 y principios de los 2000  

**El patrón evidencia una alta afectación en mujeres jóvenes durante el periodo más crítico del conflicto**
""")



####### analisis 

st.markdown("""
### 📊 Lectura temporal

Al observar el eje horizontal del año de desaparición en relación con las diagonales que marcan la edad, se hace evidente que la mayor densidad de casos, representada por los tonos púrpuras más intensos, se concentra entre los años 1995 y 2005. Esta densidad se ubica predominantemente entre las líneas entre los 10 y los 20 años, lo que confirma que el impacto más severo del conflicto recayó sobre mujeres que eran apenas adolescentes al momento de ser desaparecidas. 
Desde la perspectiva de las cohortes de nacimiento, situada en el eje vertical, el diagrama revela que las mujeres nacidas entre finales de la década de 1970 y mediados de los años 1980 fueron las más afectadas por este crimen. Al seguir la trayectoria de estas generaciones a lo largo del tiempo, se percibe que su paso por la etapa de la adolescencia y juventud temprana coincidió con el recrudecimiento de la violencia armada en el país alrededor del cambio de siglo. Esta superposición generacional explica por qué este grupo específico presenta la mayor acumulación de celdas oscuras, indicando una victimización sistemática que truncó las vidas de una generación entera de mujeres jóvenes.


            
            """)