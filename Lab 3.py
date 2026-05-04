<<<<<<< HEAD
# =======================================================================
# LABORATORIO 4: SISTEMA DE ANALISIS MULTI-DATASET
# Curso: CC2005
# =======================================================================

import pandas as pd
import os

# -----------------------------------------------------------------------
# PARTE 1: CARGA DE DATOS
# -----------------------------------------------------------------------

def cargar_datos():
    archivos = {
        "ev": "Electric_Vehicle_Population.csv",
        "gym": "GymExerciseTracking.csv",
        "steam": "steam_store_data_2024.csv",
        "netflix": "netflix_titles.csv"
    }

    datos = {}

    print("\n--- CARGANDO DATOS ---")

    for nombre, ruta in archivos.items():
        if os.path.exists(ruta):
            df = pd.read_csv(ruta)
            df.columns = df.columns.str.strip()
            datos[nombre] = df
            print(f"[OK] {nombre} cargado ({df.shape[0]} filas)")
        else:
            print(f"[ERROR] No se encontró {ruta}")

    return datos


# -----------------------------------------------------------------------
# PARTE 2: EXPLORACIÓN
# -----------------------------------------------------------------------

def explorar_datos(datos):
    print("\n--- EXPLORACION ---")

    for nombre, df in datos.items():
        print(f"\nDataset: {nombre.upper()}")
        print("Dimensiones:", df.shape)
        print("Columnas:", list(df.columns))
        print("Primeras filas:")
        print(df.head(5))
        print("Estadísticas:")
        print(df.describe(include='all'))


# -----------------------------------------------------------------------
# PARTE 3: LIMPIEZA
# -----------------------------------------------------------------------

def limpiar_datos(datos):

    # Netflix duración
    if "netflix" in datos:
        df = datos["netflix"]
        df["duration_num"] = df["duration"].astype(str).str.extract(r'(\d+)')
        df["duration_num"] = pd.to_numeric(df["duration_num"], errors='coerce')

    return datos


# -----------------------------------------------------------------------
# PARTE 4: INGRESO DE DATOS
# -----------------------------------------------------------------------

def ingresar_datos(datos):
    print("\n--- INGRESO DE DATOS ---")

    # Gym
    if "gym" in datos:
        print("\nNuevo registro Gym")
        cal = float(input("Calories Burned: "))
        fat = float(input("Fat %: "))

        nuevo = pd.DataFrame([{
            "Calories_Burned": cal,
            "Fat_Percentage": fat
        }])

        datos["gym"] = pd.concat([datos["gym"], nuevo], ignore_index=True)

    # Steam
    if "steam" in datos:
        print("\nNuevo juego Steam")
        price = float(input("Precio: "))
        disc = float(input("Descuento: "))

=======
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
>>>>>>> 59fcc856917930868d1a870400992a7d8c594c10
        nuevo = pd.DataFrame([{
            "price": price,
            "discount_percent": disc
        }])
<<<<<<< HEAD

        datos["steam"] = pd.concat([datos["steam"], nuevo], ignore_index=True)

    return datos


# -----------------------------------------------------------------------
# PARTE 5: FILTROS
# -----------------------------------------------------------------------

def filtros(datos):
    print("\n--- FILTROS ---")

    # EV
    if "ev" in datos:
        df = datos["ev"]
        col_year = [c for c in df.columns if "year" in c.lower()][0]
        col_price = [c for c in df.columns if "price" in c.lower() or "msrp" in c.lower()][0]

        year = int(input("Año máximo EV: "))
        price = float(input("Precio máximo EV: "))

        print(df[df[col_year] < year])
        print(df[df[col_price] < price])

    # Gym
    if "gym" in datos:
        df = datos["gym"]
        cal = float(input("Min calorías: "))
        fat = float(input("Max grasa: "))

        print(df[df["Calories_Burned"] >= cal])
        print(df[df["Fat_Percentage"] <= fat])

    # Steam
    if "steam" in datos:
        df = datos["steam"]
        if "price" in df.columns:
            price = float(input("Precio mínimo Steam: "))
            print(df[df["price"] > price])

    # Netflix
    if "netflix" in datos:
        df = datos["netflix"]
        dur = int(input("Duración mínima: "))
        year = int(input("Año máximo Netflix: "))

        print(df[df["duration_num"] > dur])
        print(df[df["release_year"] < year])


# -----------------------------------------------------------------------
# PARTE 6: VARIABLES CATEGÓRICAS
# -----------------------------------------------------------------------

def categorias(datos):

    # EV
    if "ev" in datos:
        df = datos["ev"]
        col_range = [c for c in df.columns if "range" in c.lower()][0]

        df["RangoCategoria"] = df[col_range].apply(
            lambda x: "Bajo" if x < 100 else "Medio" if x <= 250 else "Alto"
        )

    # Gym
    if "gym" in datos:
        df = datos["gym"]
        df["NivelFrecuencia"] = df["Workout_Frequency"].apply(
            lambda x: "Baja" if x < 3 else "Moderada" if x <= 5 else "Alta"
        )

    # Steam
    if "steam" in datos:
        df = datos["steam"]
        if "price" in df.columns:
            df["GamaJuego"] = df["price"].apply(
                lambda x: "Baja" if x < 10 else "Media" if x <= 24 else "Alta"
            )

    # Netflix
    if "netflix" in datos:
        df = datos["netflix"]

        def audiencia(x):
            if x in ["G","TV-Y","TV-G","TV-Y7","TV-Y7-FV"]:
                return "Niños"
            elif x in ["PG","TV-PG"]:
                return "Adolescentes"
            elif x in ["PG-13","TV-14"]:
                return "Adultos Jóvenes"
            else:
                return "Adultos"

        df["TipoAudiencia"] = df["rating"].apply(audiencia)

    return datos


# -----------------------------------------------------------------------
# PARTE 7: ANÁLISIS
# -----------------------------------------------------------------------

def analisis(datos):

    print("\n--- CONTEOS ---")

    if "ev" in datos:
        print(datos["ev"]["RangoCategoria"].value_counts())

    if "gym" in datos:
        print(datos["gym"]["NivelFrecuencia"].value_counts())

    if "steam" in datos and "GamaJuego" in datos["steam"]:
        print(datos["steam"]["GamaJuego"].value_counts())

    if "netflix" in datos:
        print(datos["netflix"]["TipoAudiencia"].value_counts())

    print("\n--- AGRUPACIONES ---")

    if "ev" in datos:
        print(datos["ev"].groupby("RangoCategoria").mean(numeric_only=True))

    if "gym" in datos:
        print(datos["gym"].groupby("NivelFrecuencia").mean(numeric_only=True))


# -----------------------------------------------------------------------
# PARTE 8: PREGUNTAS
# -----------------------------------------------------------------------

def preguntas(datos):

    print("\n--- RESPUESTAS ---")

    if "ev" in datos:
        print("EV correlación:")
        print(datos["ev"].select_dtypes(include='number').corr())

    if "gym" in datos:
        print("Gym correlación:")
        print(datos["gym"].select_dtypes(include='number').corr())

    if "netflix" in datos:
        print("\nTop recientes:")
        print(datos["netflix"].sort_values("release_year", ascending=False).head(10))

        if "country" in datos["netflix"]:
            print("\nPaíses:")
            print(datos["netflix"]["country"].value_counts().head(10))


# -----------------------------------------------------------------------
# PARTE 9: GUARDAR
# -----------------------------------------------------------------------

def guardar(datos):

    if "ev" in datos:
        datos["ev"].to_csv("EV_actualizado.csv", index=False)

    if "gym" in datos:
        datos["gym"].to_csv("Gym_actualizado.csv", index=False)

    if "steam" in datos:
        datos["steam"].to_csv("Steam_actualizado.csv", index=False)

    if "netflix" in datos:
        datos["netflix"].to_csv("Netflix_actualizado.csv", index=False)

    print("\nArchivos guardados correctamente")


# -----------------------------------------------------------------------
# MENU PRINCIPAL
# -----------------------------------------------------------------------

def main():

    datos = cargar_datos()

    if len(datos) == 0:
        print("No hay datos. Fin.")
        return

    datos = limpiar_datos(datos)

    activo = True

    while activo:
        print("\n===== MENU =====")
        print("1. Exploración")
        print("2. Ingreso datos")
        print("3. Filtros")
        print("4. Crear categorías")
        print("5. Análisis")
        print("6. Preguntas")
        print("7. Guardar")
        print("8. Salir")

        op = input("Seleccione opción: ")

        if op == "1":
            explorar_datos(datos)
        elif op == "2":
            datos = ingresar_datos(datos)
        elif op == "3":
            filtros(datos)
        elif op == "4":
            datos = categorias(datos)
        elif op == "5":
            analisis(datos)
        elif op == "6":
            preguntas(datos)
        elif op == "7":
            guardar(datos)
        elif op == "8":
            activo = False
        else:
            print("Opción inválida")


# -----------------------------------------------------------------------
# EJECUCIÓN
# -----------------------------------------------------------------------

if __name__ == "__main__":
    main()
=======
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


    ev["RangoCategoria"] = ev["Electric Range"].apply(
        lambda x: "Bajo" if x < 100 else "Medio" if x <= 250 else "Alto"
    )

    gym["NivelFrecuencia"] = gym["Workout_Frequency"].apply(
        lambda x: "Baja" if x < 3 else "Moderada" if x <= 5 else "Alta"
    )

    
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

if opcion == "Análisis":
    st.header("Análisis Agrupado")

    st.subheader("Vehículos")
    st.dataframe(ev.groupby("RangoCategoria").agg({
        "Base MSRP": "mean",
        "Model Year": "mean",
        "Electric Range": "std"
    }))

    st.subheader("Gym")
    st.dataframe(gym.groupby("NivelFrecuencia").agg({
        "Session_Duration": "mean",
        "Experience_Level": "mean",
        "BMI": "std"
    }))

    st.subheader("Steam")
    st.dataframe(steam.groupby("GamaJuego").agg({
        "price": ["mean", "std"],
        "discount_percent": "mean"
    }))

    st.subheader("Netflix")
    st.dataframe(netflix.groupby("TipoAudiencia").agg({
        "duration_num": "mean",
        "type": lambda x: x.mode()[0]
    }))

if opcion == "Preguntas":
    st.header("Preguntas")

    st.subheader("Vehículos")
    st.dataframe(ev[["Electric Range","Model Year"]].corr())
    st.dataframe(ev[["Base MSRP","Electric Range"]].corr())

    st.subheader("Gym")
    st.dataframe(gym[["Calories_Burned","Session_Duration"]].corr())
    st.dataframe(gym[["Fat_Percentage","Experience_Level"]].corr())

    st.subheader("Netflix")
    st.dataframe(netflix.sort_values("release_year", ascending=False).head(10))
    st.dataframe(netflix["country"].value_counts().head(10))

if opcion == "Guardar":
    ev.to_csv("Electric_Vehicle_Population_Actualizado.csv", index=False)
    gym.to_csv("GymExerciseTracking_Actualizado.csv", index=False)
    steam.to_csv("steam_store_data_2024_Actualizado.csv", index=False)
    netflix.to_csv("netflix_titles_Actualizado.csv", index=False)

    st.success("Archivos guardados correctamente")
>>>>>>> 59fcc856917930868d1a870400992a7d8c594c10
