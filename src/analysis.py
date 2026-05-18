import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# =============================
# CARGA Y LIMPIEZA DE DATOS
# =============================
def cargar_datos(ruta):
    df = pd.read_excel(ruta)

    # Renombrar columnas (más limpias)
    df.columns = [
        "anio",
        "nacionalidad",
        "sexo",
        "fecha_nacimiento",
        "vocacion",
        "numero"
    ]

    # Convertir fechas
    df["fecha_nacimiento"] = pd.to_datetime(
        df["fecha_nacimiento"], errors="coerce", dayfirst=True
    )

    return df


# =============================
# ANÁLISIS 1: TOP NACIONALIDADES
# =============================
def top_nacionalidades(df):
    resultado = df["nacionalidad"].value_counts().head(5)

    print("\nTOP 5 NACIONALIDADES:")
    print(resultado)

    resultado.plot(kind='bar')
    plt.title("Top 5 Nacionalidades")
    plt.xlabel("Nacionalidad")
    plt.ylabel("Cantidad de solicitudes")
    plt.show()


# =============================
# ANÁLISIS 2: SOLICITUDES POR AÑO
# =============================
def solicitudes_por_anio(df):
    resultado = df["anio"].value_counts().sort_index()

    print("\nSOLICITUDES POR AÑO:")
    print(resultado)

    resultado.plot(kind='line', marker='o')
    plt.title("Solicitudes por Año")
    plt.ylabel("Cantidad")
    plt.show()


# =============================
# ANÁLISIS 3: DISTRIBUCIÓN POR SEXO
# =============================
def distribucion_sexo(df):
    resultado = df["sexo"].value_counts()

    print("\nDISTRIBUCIÓN POR SEXO:")
    print(resultado)

    resultado.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribución por Sexo")
    plt.ylabel("")
    plt.show()


# =============================
# ANÁLISIS 4: EDAD PROMEDIO
# =============================
def edad_promedio(df):
    hoy = datetime.now()

    df["edad"] = df["fecha_nacimiento"].apply(
        lambda x: hoy.year - x.year if pd.notnull(x) else None
    )

    promedio = df["edad"].mean()

    print("\nEDAD PROMEDIO DE SOLICITANTES:")
    print(round(promedio, 2))

    df["edad"].plot(kind='hist', bins=20)
    plt.title("Distribución de Edades")
    plt.xlabel("Edad")
    plt.show()


# =============================
# MENÚ INTERACTIVO
# =============================
def menu(df):
    while True:
        print("\n====== MENÚ DE ANÁLISIS ======")
        print("1. Top 5 nacionalidades")
        print("2. Solicitudes por año")
        print("3. Distribución por sexo")
        print("4. Edad promedio")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            top_nacionalidades(df)
        elif opcion == "2":
            solicitudes_por_anio(df)
        elif opcion == "3":
            distribucion_sexo(df)
        elif opcion == "4":
            edad_promedio(df)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    ruta = "../data/Visa_Applications_Colombia_2017_20250217.xlsx"  # Ajustar según ubicación
    df = cargar_datos(ruta)
    menu(df)