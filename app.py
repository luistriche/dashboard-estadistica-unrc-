import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la Página
st.set_page_config(page_title="Dashboard Estadístico - UNRC", layout="wide")

# 2. Encabezado Institucional con Integrantes
st.title("📊 Análisis de Frecuencias y Gráficos Estadísticos")
st.markdown("### Licenciatura en Ciencia de Datos para Negocios | Grupo: 201")
st.write("**Integrantes:** Luis Armando Triche Ramírez & Chrissier Magdiel Quintero Jacobo")
st.divider()

# 3. Datos de la Investigación (Edades de 20 clientes en Tijuana)
edades = [22, 24, 25, 28, 29, 31, 32, 34, 35, 36, 38, 39, 41, 42, 45, 46, 48, 50, 52, 55]
df_edades = pd.DataFrame({'Edad': edades})

# 4. Cálculo de la Tabla de Frecuencias (Regla de Sturges)
bins = [22, 29, 36, 43, 50, 57]
labels = ["[22-29)", "[29-36)", "[36-43)", "[43-50)", "[50-57]"]
df_edades['Clase'] = pd.cut(df_edades['Edad'], bins=bins, labels=labels, right=False)

tabla = df_edades['Clase'].value_counts().sort_index().reset_index()
tabla.columns = ['Intervalo', 'fi (Absoluta)']
tabla['hi% (Relativa)'] = (tabla['fi (Absoluta)'] / len(edades) * 100).round(2)
tabla['Fi (Acumulada)'] = tabla['fi (Absoluta)'].cumsum()

# 5. Interfaz de Exposición (Pestañas)
tab_inicio, tab_cuant, tab_cual = st.tabs(["🗂️ Tabla de Frecuencias", "📈 Gráficos Cuantitativos", "📊 Gráficos Cualitativos"])

with tab_inicio:
    st.header("Construcción de Tabla (Regla de Sturges)")
    st.write("La estadística descriptiva organiza datos crudos para hacerlos comprensibles en los negocios.")
    st.table(tabla)
    st.info("fi: conteo de repeticiones | hi%: proporción del total | Fi: suma progresiva.")

with tab_cuant:
    st.header("Gráficos Cuantitativos")
    
    st.subheader("1. Histograma")
    st.write("**Uso:** Datos continuos y agrupados. Barras pegadas.")
    fig1 = px.histogram(df_edades, x="Edad", nbins=5, title="Histograma de Edades", color_discrete_sequence=['#800000'])
    fig1.update_layout(bargap=0)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("2. Polígono de Frecuencias")
    st.write("**Uso:** Ver la tendencia uniendo puntos medios (marcas de clase).")
    marcas_clase = [25.5, 32.5, 39.5, 46.5, 53.5]
    fig2 = px.line(x=marcas_clase, y=tabla['fi (Absoluta)'], markers=True, title="Polígono de Frecuencias", color_discrete_sequence=['#D4AF37'])
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("3. Ojiva")
    st.write("**Uso:** Ver cuántos datos están por debajo de un valor (Frecuencia Acumulada).")
    limites_sup = [29, 36, 43, 50, 57]
    fig3 = px.line(x=limites_sup, y=tabla['Fi (Acumulada)'], markers=True, title="Ojiva Ascendente")
    st.plotly_chart(fig3, use_container_width=True)

with tab_cual:
    st.header("Gráficos Cualitativos")

    st.subheader("4. Diagrama de Barras")
    st.write("**Uso:** Comparar categorías. Barras SEPARADAS.")
    fig4 = px.bar(tabla, x='Intervalo', y='fi (Absoluta)', title="Comparativa por Categoría", color='Intervalo')
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("5. Gráfica de Pastel")
    st.write("**Uso:** Ver el porcentaje que representa cada parte del total.")
    fig5 = px.pie(tabla, values='fi (Absoluta)', names='Intervalo', title="Distribución Porcentual")
    st.plotly_chart(fig5, use_container_width=True)