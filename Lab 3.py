

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lab 4", layout="wide")

st.title("📊 Laboratorio 4 - Análisis de Datos")

@st.cache_data
def cargar_datos():
    ev = pd.read_csv("Electric_Vehicle_Population.csv")
    gym = pd.read_csv("GymExerciseTracking.csv")
    steam = pd.read_csv("steam_store_data_2024.csv")
    netflix = pd.read_csv("netflix_titles.csv")

    ev.columns = ev.columns.str.strip()
    gym.columns = gym.columns.str.strip()
    steam.columns = steam.columns.str.strip()
    netflix.columns = netflix.columns.str.strip()

    # limpiar duración Netflix
    netflix["duration_num"] = netflix["duration"].astype(str).str.extract(r'(\d+)')
    netflix["duration_num"] = pd.to_numeric(netflix["duration_num"], errors='coerce')

    return ev, gym, steam, netflix

ev, gym, steam, netflix = cargar_datos()


opcion = st.sidebar.selectbox("Sección", [
    "Exploración",
    "Ingreso",
    "Filtros",
    "Categorías",
    "Análisis",
    "Preguntas",
    "Guardar"
])

if opcion == "Exploración":
    st.header("Exploración")

    for nombre, df in zip(
        ["Vehículos", "Gym", "Steam", "Netflix"],
        [ev, gym, steam, netflix]
    ):
        st.subheader(nombre)
        st.write("Dimensiones:", df.shape)
        st.write("Columnas:", df.columns.tolist())
        st.dataframe(df.head(6))
        st.write(df.describe())