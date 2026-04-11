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
st.title("📈 Evolución de la desaparición de mujeres")

st.markdown("""
Análisis de la evolución temporal de las desapariciones de mujeres en Colombia, evidenciando patrones históricos y momentos críticos del conflicto armado.
""")

# ========================
# GRÁFICA 1: ANUAL
# ========================
st.subheader("Registros anuales")

st.subheader("Registros anuales: Total PDD vs Mujeres")

fig_anual = px.line(
    temporal,
    x="anio_desapa",
    y=["total_pdd", "total_mujeres"],
    markers=True
)

# colores personalizados
fig_anual.update_traces(
    selector=dict(name="total_pdd"),
    line=dict(color="firebrick", width=3),
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

st.plotly_chart(fig_anual, use_container_width=True)

# ========================
# GRÁFICA 1: ANUAL
# ========================
st.subheader("Registros anuales solo Mujeres")

fig_anual = px.line(
    temporal,
    x="anio_desapa",
    y="total_mujeres",
    markers=True
)

fig_anual.update_traces(
    line=dict(color="darkblue", width=3),
    hovertemplate=
    "<b>Año:</b> %{x}<br>" +
    "<b>Casos:</b> %{y:,}<extra></extra>"
)

fig_anual.update_layout(
    height=400,
    xaxis_title="Año",
    yaxis_title="Número de casos"
)

st.plotly_chart(fig_anual, use_container_width=True)


# ========================
# GRÁFICA 2: ACUMULADO
# ========================
st.subheader("Acumulado histórico de desapariciones de Mujeres")

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

st.plotly_chart(fig_acum, use_container_width=True)


####### analisis 

st.markdown("""
### 📊 Lectura temporal

La evolución histórica de la desaparición de mujeres en el contexto del conflicto evidencia un incremento notable a partir de 1980, superando los cien casos anuales, lo que marca el inicio de una tendencia ascendente que se acelera de manera dramática durante la década de los noventa. Este crecimiento exponencial coincide con la agudización de las dinámicas de violencia, alcanzando un primer umbral crítico hacia 1995, antes de entrar en la fase más aguda de la crisis humanitaria reflejada en los datos.
El punto máximo de la serie histórica se localiza claramente en el año 2002, cuando el número de mujeres desaparecidas superó los mil trescientos casos en un solo año, representando el pico más alto de victimización registrado. Tras este periodo de máxima intensidad, se observa una fluctuación con una tendencia general al descenso, aunque con repuntes significativos hacia 2007 y 2012 que impidieron una reducción lineal de la violencia. Hacia el final del periodo, en 2016, las cifras muestran una reducción sostenida respecto al pico de principios de siglo, situándose por debajo de los quinientos casos anuales, aunque todavía muy por encima de los niveles registrados en las décadas iniciales del reporte.
            
            """)