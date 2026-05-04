

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
<<<<<<< HEAD


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

=======

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

>>>>>>> d8a78adde008e9270c02c00c3c9f6ab333fa8aaa
    for nombre, df in zip(
        ["Vehículos", "Gym", "Steam", "Netflix"],
        [ev, gym, steam, netflix]
    ):
        st.subheader(nombre)
        st.write("Dimensiones:", df.shape)
        st.write("Columnas:", df.columns.tolist())
        st.dataframe(df.head(6))
<<<<<<< HEAD
        st.write(df.describe())

if opcion == "Ingreso":
    st.header("Ingreso de Datos")

    
    st.subheader("Nuevo Gym")
    cal = st.number_input("Calories Burned", 0.0)
    fat = st.number_input("Fat %", 0.0, 100.0)

    if st.button("Agregar Gym"):
        nuevo = pd.DataFrame([{
            "Age": 25,
            "Gender": "Male",
            "Workout_Type": "Cardio",
            "Session_Duration": 1.0,
            "Calories_Burned": cal,
            "Experience_Level": 2,
            "BMI": 22.0,
            "Fat_Percentage": fat
        }])
        gym = pd.concat([gym, nuevo], ignore_index=True)
        st.success("Registro agregado")

    
    st.subheader("Nuevo Steam")
    price = st.number_input("Precio")
    disc = st.number_input("Descuento")

    if st.button("Agregar Steam"):
        nuevo = pd.DataFrame([{
            "price": price,
            "discount_percent": disc
        }])
        steam = pd.concat([steam, nuevo], ignore_index=True)
        st.success("Juego agregado")


if opcion == "Filtros":
    st.header("Filtros")


    st.subheader("Vehículos")
    year = st.slider("Año máximo", 2000, 2025)
    price = st.number_input("Precio máximo")
    st.dataframe(ev[ev["Model Year"] < year])
    st.dataframe(ev[ev["Base MSRP"] < price])

    
    st.subheader("Gym")
    cal = st.number_input("Min calorías")
    fat = st.number_input("Max grasa")
    st.dataframe(gym[gym["Calories_Burned"] >= cal])
    st.dataframe(gym[gym["Fat_Percentage"] <= fat])

    
    st.subheader("Steam")
    price = st.number_input("Precio mínimo Steam")
    disc = st.number_input("Descuento máximo")
    st.dataframe(steam[steam["price"] > price])
    st.dataframe(steam[steam["discount_percent"] < disc])

    st.subheader("Netflix")
    dur = st.number_input("Duración mínima")
    year = st.number_input("Año máximo Netflix")
    st.dataframe(netflix[netflix["duration_num"] > dur])
    st.dataframe(netflix[netflix["release_year"] < year])


if opcion == "Categorías":
    st.header("Categorías")

    # EV
    ev["RangoCategoria"] = ev["Electric Range"].apply(
        lambda x: "Bajo" if x < 100 else "Medio" if x <= 250 else "Alto"
    )

    # Gym
    gym["NivelFrecuencia"] = gym["Workout_Frequency"].apply(
        lambda x: "Baja" if x < 3 else "Moderada" if x <= 5 else "Alta"
    )

    # Steam
    steam["GamaJuego"] = steam["price"].apply(
        lambda x: "Baja" if x < 10 else "Media" if x <= 24 else "Alta"
    )

    def audiencia(x):
        if x in ["G","TV-Y","TV-G","TV-Y7","TV-Y7-FV"]:
            return "Niños"
        elif x in ["PG","TV-PG"]:
            return "Adolescentes"
        elif x in ["PG-13","TV-14"]:
            return "Adultos Jóvenes"
        else:
            return "Adultos"

    netflix["TipoAudiencia"] = netflix["rating"].apply(audiencia)

    st.subheader("Conteos")
    st.write(ev["RangoCategoria"].value_counts())
    st.write(gym["NivelFrecuencia"].value_counts())
    st.write(steam["GamaJuego"].value_counts())
    st.write(netflix["TipoAudiencia"].value_counts())
=======
        st.write(df.describe())
>>>>>>> d8a78adde008e9270c02c00c3c9f6ab333fa8aaa
