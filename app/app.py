import streamlit as st

st.set_page_config(
    page_title="DAT4CCIÓN2026",
    layout="wide"
)



st.set_page_config(layout="wide")

# LOGO EN SIDEBAR (arriba del menú)
st.sidebar.image("assets/logo_umujer.png", use_container_width=True)


st.markdown("""
<h1 style='text-align: center; color:#6A1B9A;'>
Caracterización sociodemográfica de las personas desaparecidas en el marco del conflicto armado en Colombia: Una mirada interseccional, con base en el Universo de Personas dadas por Desaparecidas de la UBPD - Colombia
</h1>

<h3 style='text-align: center; color:gray;'>
Dat4cción – ONU Mujeres
</h3>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; font-size:18px'>
Este visor permite comprender la desaparición de mujeres desde una perspectiva territorial,
identificando patrones, dinámicas y desigualdades espaciales para apoyar la toma de decisiones.
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.markdown("""
**Área:**  
Violencia basada en género
""")

col2.markdown("""
**Categoría:**  
Dashboard funcional
""")

col3.markdown("""
**Enfoque:**  
Paz, Seguridad, Reparación, Justicia y Verdad.
""")


st.markdown("### Equipo")

col4, col5, col6 , col7 = st.columns(4)

col4.markdown("""
**César Cristancho Fajardo**  
Doctor en Demografía  

**Entidad:**  
Unidad de Búsqueda de Personas Dadas por Desaparecidas (UBPD)

**Contacto:**  
ccristanchof@unidadbusqueda.gov.co  ;
cacristanchof@gmail.com 
""")

col5.markdown("""
**Eurides Triana Triana**  
Estadístico – Master estudios de población  


**Entidad:**  
Unidad de Búsqueda de Personas Dadas por Desaparecidas (UBPD)

**Contacto:**  
etrianat@unidadbusqueda.gov.co ;
euridest@gmail.com 
""")

col6.markdown("""
**Laura Piedad Quintero Martinez**  
Politóloga – Especialista en Derechos Humanos  


**Entidad:**  
Unidad de Búsqueda de Personas Dadas por Desaparecidas (UBPD)

**Contacto:**  
lquinterom@unidadbusqueda.gov.co 
""")

col7.markdown("""
**Enys Yaridis Esteban Cruz**  
Administración de Empresas


**Entidad:**  
Unidad de Búsqueda de Personas Dadas por Desaparecidas (UBPD)

**Contacto:**  
eestebanc@unidadbusqueda.gov.co 
""")
st.markdown("### ¿Qué encontrará en este visor?")

st.markdown("""
- **Contexto**:  de  la fuente de los datos y descripción de los mismos
- **Panorama General**: Cifras globales y contexto nacional.

- **Evolución Temporal**: Análisis de tendencias por quinquenios y tasas de incidencia.

- **Trayectoria Vital**: Caracterización por edades y momentos de vida.

- **Intensidad Territorial**: Mapas de riesgo y análisis de origen vs. lugar de desaparición.
""")

st.markdown("""
<br>

<h3 style='text-align: center; color:#6A1B9A;'>
Cada dato representa una historia.  
Cada análisis, una oportunidad para encontrar.
</h3>
""", unsafe_allow_html=True)