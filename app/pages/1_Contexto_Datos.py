
import streamlit as st


# LOGO EN SIDEBAR (arriba del menú)
st.sidebar.image("assets/logo_umujer.png", use_container_width=True)

st.markdown("""
<h1 style='text-align: center; color:#6A1B9A;'>
Caracterización sociodemográfica de las personas desaparecidas en el marco del conflicto armado en Colombia: Una mirada interseccional, con base en el Universo de Personas dadas por Desaparecidas de la UBPD - Colombia
</h1>
""", unsafe_allow_html=True)

st.markdown("""
 La desaparición de mujeres en Colombia representa una de las fracturas más profundas y silenciosas del tejido social en el marco del conflicto armado interno.  Presentamos una caracterización demográfica de las mujeres dadas por desaparecidas en el contexto y razón conflicto armado en Colombia antes del 1 de diciembre del 1996, basado en el Universo de personas dadas por desaparecidas que conforma la Unidad de Búsqueda de Personas dadas por Desaparecidas -UBPD-.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📌 Alcance del análisis")
    st.markdown("""
    - Periodo de análisis: hasta 2016  
    - Fuente: UBPD  
    - Universo: Personas dadas por desaparecidas  
    - Enfoque: caracterización sociodemográfica de mujeres  
    """)

with col2:
    st.markdown("### 🎯 Enfoque")
    st.markdown("""
    - Violencia basada en género  
    - Análisis territorial  
    - Perspectiva interseccional  
    - Soporte a la búsqueda humanitaria  
    """)


st.markdown("""
### 🔄 Actualización de la información

La información presentada en este visor corresponde al **último corte oficial del Universo de Personas dadas por Desaparecidas**, con fecha de actualización al **15 de marzo de 2026**.

Este corte incorpora procesos de integración, depuración y validación de registros provenientes de múltiples fuentes, garantizando consistencia y calidad en la información utilizada para el análisis.
""")
st.markdown("---")

st.markdown("""
La desaparición de mujeres en Colombia constituye una de las expresiones más profundas y silenciosas de las violencias asociadas al conflicto armado. 
Este visor presenta una caracterización sociodemográfica desde un enfoque territorial e interseccional, con el propósito de aportar evidencia para la comprensión del fenómeno y el fortalecimiento de acciones de **búsqueda, de reparación y no repetición**.

El análisis se basa en el **Universo de Personas dadas por Desaparecidas (PDD)** consolidado por la Unidad de Búsqueda de Personas dadas por Desaparecidas (UBPD), el cual integra múltiples fuentes de información y procesos de validación.

Para esta caracterización se utilizaron variables específicas autorizadas, entre ellas:
- Fecha de nacimiento  
- Sexo al nacer  
- Lugar de nacimiento  
- Lugar de ocurrencia de la desaparición  
- Fecha de desaparición  
- Edad al momento de la desaparición  

Es importante señalar que, si bien el universo contiene un conjunto más amplio de variables, el uso de la información está sujeto a principios de **reserva estadística y protección de la investigación humanitaria**, por lo cual esta visualización se limita a variables que no comprometen procesos en curso ni la seguridad de las personas involucradas.
""")

st.markdown("### 🏛️ Sobre la Unidad de Búsqueda")

st.markdown("""
La **Unidad de Búsqueda de Personas dadas por Desaparecidas (UBPD)** es un mecanismo humanitario, extrajudicial e independiente creado en el marco del Acuerdo Final de Paz en Colombia.

Su misión es dirigir, coordinar y contribuir a la implementación de acciones humanitarias de búsqueda y localización de personas dadas por desaparecidas en el contexto y en razón del conflicto armado, garantizando el derecho de las familias a conocer la verdad.

La UBPD orienta su labor bajo principios de centralidad de las víctimas, enfoque territorial, diferencial y de género, articulando información proveniente de diversas fuentes para apoyar procesos de búsqueda efectivos.
""")

st.markdown("### 🌐 Más información")

st.markdown("""
Para conocer más sobre la labor de la Unidad de Búsqueda, visite:

👉 https://www.unidadbusqueda.gov.co  

Este visor busca aportar a la comprensión pública del fenómeno, promoviendo el uso responsable de la información y el reconocimiento de las personas dadas por desaparecidas y las mujeres buscadoras.
""")


st.markdown("""
<br>

<h3 style='text-align: center; color:#6A1B9A;'>
Cada dato representa una vida.  
Cada análisis, una oportunidad para encontrar.
</h3>
""", unsafe_allow_html=True)
