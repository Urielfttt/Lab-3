import pandas as pd
import os
import matplotlib.pyplot as plt

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


def explorar(datos):
    print("\n--- EXPLORACIÓN ---")

    for nombre, df in datos.items():
        print(f"\nDATASET: {nombre.upper()}")
        print("Dimensiones:", df.shape)
        print("Columnas:", list(df.columns))
        print(df.head(6))
        print(df.describe())
def limpiar(datos):
    if "netflix" in datos:
        df = datos["netflix"]
        df["duration_num"] = df["duration"].astype(str).str.extract(r'(\d+)')
        df["duration_num"] = pd.to_numeric(df["duration_num"], errors='coerce')
    return datos

def ingreso(datos):

    # Gym
    if "gym" in datos:
        print("\nNuevo registro Gym")
        nuevo = {
            "Age": 25,
            "Gender": "Male",
            "Workout_Type": "Cardio",
            "Session_Duration": 1.0,
            "Calories_Burned": float(input("Calories Burned: ")),
            "Experience_Level": 2,
            "BMI": 22.0,
            "Fat_Percentage": float(input("Fat %: "))
        }
        datos["gym"] = pd.concat([datos["gym"], pd.DataFrame([nuevo])], ignore_index=True)

    if "steam" in datos:
        print("\nNuevo juego Steam")
        nuevo = {
            "price": float(input("Precio: ")),
            "discount_percent": float(input("Descuento: "))
        }
        datos["steam"] = pd.concat([datos["steam"], pd.DataFrame([nuevo])], ignore_index=True)

    return datos

def filtros(datos):
    if "ev" in datos:
        df = datos["ev"]
        col_year = [c for c in df.columns if "year" in c.lower()][0]
        col_price = [c for c in df.columns if "price" in c.lower() or "msrp" in c.lower()][0]

        year = int(input("Año máximo EV: "))
        price = float(input("Precio máximo EV: "))

        print(df[df[col_year] < year])
        print(df[df[col_price] < price])
    if "gym" in datos:
        df = datos["gym"]
        cal = float(input("Min calorías: "))
        fat = float(input("Max grasa: "))

        print(df[df["Calories_Burned"] >= cal])
        print(df[df["Fat_Percentage"] <= fat])

    if "steam" in datos:
        df = datos["steam"]
        if "price" in df.columns:
            price = float(input("Precio mínimo Steam: "))
            disc = float(input("Descuento máximo Steam: "))

            print(df[df["price"] > price])
            print(df[df["discount_percent"] < disc])

    if "netflix" in datos:
        df = datos["netflix"]
        dur = int(input("Duración mínima: "))
        year = int(input("Año máximo Netflix: "))

        print(df[df["duration_num"] > dur])
        print(df[df["release_year"] < year])

def categorias(datos):

    if "ev" in datos:
        df = datos["ev"]
        col_range = [c for c in df.columns if "range" in c.lower()][0]

        df["RangoCategoria"] = df[col_range].apply(
            lambda x: "Bajo" if x < 100 else "Medio" if x <= 250 else "Alto"
        )

    if "gym" in datos:
        df = datos["gym"]
        df["NivelFrecuencia"] = df["Workout_Frequency"].apply(
            lambda x: "Baja" if x < 3 else "Moderada" if x <= 5 else "Alta"
        )

    if "steam" in datos:
        df = datos["steam"]
        if "price" in df.columns:
            df["GamaJuego"] = df["price"].apply(
                lambda x: "Baja" if x < 10 else "Media" if x <= 24 else "Alta"
            )

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

def analisis(datos):

    def grafico(df, col, titulo):
        df[col].value_counts().plot(kind="bar")
        plt.title(titulo)
        plt.xlabel("Categoría")
        plt.ylabel("Cantidad")
        plt.show()

    print("\n--- CONTEOS ---")

    if "ev" in datos:
        print(datos["ev"]["RangoCategoria"].value_counts())
        grafico(datos["ev"], "RangoCategoria", "Vehículos")

    if "gym" in datos:
        print(datos["gym"]["NivelFrecuencia"].value_counts())
        grafico(datos["gym"], "NivelFrecuencia", "Gym")

    if "steam" in datos and "GamaJuego" in datos["steam"]:
        print(datos["steam"]["GamaJuego"].value_counts())
        grafico(datos["steam"], "GamaJuego", "Steam")

    if "netflix" in datos:
        print(datos["netflix"]["TipoAudiencia"].value_counts())
        grafico(datos["netflix"], "TipoAudiencia", "Netflix")

    print("\n--- AGRUPACIONES ---")

    if "ev" in datos:
        print(datos["ev"].groupby("RangoCategoria").agg({
            "Base MSRP": "mean",
            "Model Year": "mean",
            "Electric Range": "std"
        }))

    if "gym" in datos:
        print(datos["gym"].groupby("NivelFrecuencia").agg({
            "Session_Duration": "mean",
            "Experience_Level": "mean",
            "BMI": "std"
        }))

    if "steam" in datos and "GamaJuego" in datos["steam"]:
        print(datos["steam"].groupby("GamaJuego").agg({
            "price": ["mean", "std"],
            "discount_percent": "mean"
        }))

    if "netflix" in datos:
        print(datos["netflix"].groupby("TipoAudiencia").agg({
            "duration_num": "mean",
            "type": lambda x: x.mode()[0]
        }))

def guardar(datos):

    if "ev" in datos:
        datos["ev"].to_csv("Electric_Vehicle_Population_Actualizado.csv", index=False)

    if "gym" in datos:
        datos["gym"].to_csv("GymExerciseTracking_Actualizado.csv", index=False)

    if "steam" in datos:
        datos["steam"].to_csv("steam_store_data_2024_Actualizado.csv", index=False)

    if "netflix" in datos:
        datos["netflix"].to_csv("netflix_titles_Actualizado.csv", index=False)

    print("\nArchivos guardados correctamente")