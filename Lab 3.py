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

        nuevo = pd.DataFrame([{
            "price": price,
            "discount_percent": disc
        }])

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