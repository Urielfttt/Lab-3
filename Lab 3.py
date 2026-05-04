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
