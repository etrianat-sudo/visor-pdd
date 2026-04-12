import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ========================
# CARGAR DATOS
# ========================
ruta = "data/data_universo_pdd.xlsx"
temporal = pd.read_excel(ruta, sheet_name="temporal")

# ========================
# LIMPIAR DATOS
# ========================
temporal = temporal.sort_values("anio_desapa")

# ========================
# TÍTULO
# ========================
st.title("📈 Análisis de la evolución temporal de desaparicion de Mujeres")

st.markdown("""
Patrones y momentos críticos: Análisis temporal de las desapariciones de mujeres en el marco del conflicto armado en Colombia.
""")

# ========================
# GRÁFICA 1:  acomulado ACUMULADO
# ========================
st.subheader("Impacto del conflicto armado: Acumulado histórico de desapariciones de mujeres por año de ocurrencia.")

st.markdown("""
<small style='color: gray;'>
Interactúe con la gráfica desplazando el cursor sobre la curva para visualizar el detalle de la información.
</small>
""", unsafe_allow_html=True)


fig_acum = px.line(
    temporal,
    x="anio_desapa",
    y="acumulado",
    markers=True
)

fig_acum.update_traces(
    line=dict(color="darkblue", width=3),
    hovertemplate=
    "<b>Año:</b> %{x}<br>" +
    "<b>Acumulado:</b> %{y:,}<extra></extra>"
)

fig_acum.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis_title="Total acumulado"
)

# ========================
# LÍNEAS 
# ========================
lineas = [
    (2016, "2016 Firma de los acuerdos de paz"),
]

for x, label in lineas:
    fig_acum.add_vline(
        x=x,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text=label,
        annotation_position="top"
    )


st.plotly_chart(fig_acum, use_container_width=True)


# ========================
# GRÁFICA 2:  ANUAL
# ========================
st.markdown("### 📊 Registros anuales")

st.subheader("Cantidad de desapareciones por año: Representación de la mujer frente al total de Personas Dadas por Desaparecidas")

st.markdown("""
<small style='color: gray;'>
Interactúe con la gráfica desplazando el cursor sobre la curva para visualizar el detalle de la información.
</small>
""", unsafe_allow_html=True)

fig_anual = px.line(
    temporal,
    x="anio_desapa",
    y=["total_pdd", "total_mujeres"],
    markers=True
)

# colores personalizados
fig_anual.update_traces(
    selector=dict(name="total_pdd"),
    line=dict(color="#8e44ad", width=3),
)

fig_anual.update_traces(
    selector=dict(name="total_mujeres"),
    line=dict(color="darkblue", width=3),
)

# hover personalizado
fig_anual.update_traces(
    hovertemplate=
    "<b>Año:</b> %{x}<br>" +
    "<b>Total de PDD:</b> %{y:,}<extra></extra>"
)

fig_anual.update_layout(
    height=450,
    xaxis_title="Año",
    yaxis_title="Número de casos",
    legend_title="Serie"
)

# ========================
# LÍNEAS 
# ========================
lineas = [
    (2003, "         Periodo desmovilización paramilitares"),
    (2006, "")
]

for x, label in lineas:
    fig_anual.add_vline(
        x=x,
        line_width=2,
        line_dash="dash",
        line_color="gray",
        annotation_text=label,
        annotation_position="top"
    )



col1, col2 = st.columns(2)

with col1:
    st.markdown("**Total PDD vs Mujeres**")
    st.plotly_chart(fig_anual, use_container_width=True)

with col2:
    fig_mujeres = px.line(
        temporal,
        x="anio_desapa",
        y="total_mujeres",
        markers=True
    )

    fig_mujeres.update_traces(
        line=dict(color="darkblue", width=3)
    )

    fig_mujeres.update_layout(
        height=350,
        xaxis_title="Año",
        yaxis_title="Casos"
    )

    st.markdown("**Mujeres por año**")
    st.plotly_chart(fig_mujeres, use_container_width=True)





####### analisis 

st.markdown("""
### 📊 Lectura temporal

La evolución histórica de la desaparición de mujeres en el contexto del conflicto evidencia un incremento notable a partir de 1980, superando los cien casos anuales, lo que marca el inicio de una tendencia ascendente que se acelera de manera dramática durante la década de los noventa. Este crecimiento exponencial coincide con la agudización de las dinámicas de violencia, alcanzando un primer umbral crítico hacia 1995, antes de entrar en la fase más aguda de la crisis humanitaria reflejada en los datos.
El punto máximo de la serie histórica se localiza claramente en el año 2002, cuando el número de mujeres desaparecidas superó los mil trescientos casos en un solo año, representando el pico más alto de victimización registrado. Tras este periodo de máxima intensidad, se observa una fluctuación con una tendencia general al descenso, aunque con repuntes significativos hacia 2007 y 2012 que impidieron una reducción lineal de la violencia. Hacia el final del periodo, en 2016, las cifras muestran una reducción sostenida respecto al pico de principios de siglo, situándose por debajo de los quinientos casos anuales, aunque todavía muy por encima de los niveles registrados en las décadas iniciales del reporte.
            
            """)