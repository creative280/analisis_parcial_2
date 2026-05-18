"""
Módulo de análisis de datos (uso por CONSOLA) + función compartida cargar_datos

¿Por qué conviven dos “mundos”?

1) Si ejecutás este archivo (python analysis.py): aparece menú texto y graficas escritorio matplotlib plt.show().
2) El servidor web (Flask / dashboard_service.py) importa SOLO cargar_datos()
   porque el dashboard genera PNG en memoria y no debe depender plt.show servidor.

Los nombres de columnas están en español “normalizados” para simplificar código analíticos posteriores
al leer archivo Excel instituciones académica original encabezados con tildes o variaciones escritura.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# =============================
# CARGA Y LIMPIEZA DE DATOS
# =============================


def cargar_datos(ruta):
    """
    Lee archivo Excel ubicado disk ruta provista clase docente equipo.

    Parámetro ruta: string POSIX/Windows combinado ejemplo "../data/archivo.xlsx" consola dentro src/
                             o bien path absolutos desde proyecto raíz servidor flask.

    Retorna DataFrame pandas con columnas coherentes proyecto parcial siguiente lista:

    Retorno columnas después renombrar:
      anio, nacionalidad, sexo, fecha_nacimiento, vocacion, numero
    """
    # read_excel requiere openpyxl típicamente engine automático suficientes versiones instalación requirements proyecto.
    df = pd.read_excel(ruta)

    # Excel original llega español instituciones; pandas lee texto exacto archivo.
    # Estandarizamos etiquetas porque facilita trabajo equipos diferentes máquinas (menos errores tipeando 'Fecha_' largo).
    df.columns = [
        "anio",
        "nacionalidad",
        "sexo",
        "fecha_nacimiento",
        "vocacion",
        "numero",
    ]

    # Convertir fecha_nacimiento a tipo temporal datetime64[ns].
    #
    # errors="coerce" -> si llega fecha inválida textual se vuelve NaT (fecha nula tipo pandas)
    # en vez de lanzar crash interrumpiendo menú clase ansiedad desarrolladora principiante.
    #
    # dayfirst=True importante regiones día/mes habitual lectura formato dd/mm/yyyy ambiguo.
    df["fecha_nacimiento"] = pd.to_datetime(
        df["fecha_nacimiento"], errors="coerce", dayfirst=True
    )

    return df


# =============================
# ANÁLISIS 1: TOP NACIONALIDADES
# =============================


def top_nacionalidades(df):
    """
    Cuenta frecuencias columna categorical nacionalidad, quedarse sólo TOP 5.
    Gráfico barras + impresiones consolas narrativas rápidos examen clase demostraciones directas estadística poblacional geografica académica.
    """
    resultado = df["nacionalidad"].value_counts().head(5)

    print("\nTOP 5 NACIONALIDADES:")
    print(resultado)

    resultado.plot(kind="bar")  # gráficas consola habitual notebook estudio proyecto incipiente
    plt.title("Top 5 Nacionalidades")
    plt.xlabel("Nacionalidad")
    plt.ylabel("Cantidad de solicitudes")
    plt.show()  # abre interfaz escritorio estudiante ejecutando locales IDE clase


# =============================
# ANÁLISIS 2: SOLICITUDES POR AÑO
# =============================


def solicitudes_por_anio(df):
    """
    value_counts año entero clasifica masa solicitudes anio columna ascendente chronological sort_index garantiza tiempo izquierda→derecha lectura intuitiva clase exposición rápido.
    """
    resultado = df["anio"].value_counts().sort_index()

    print("\nSOLICITUDES POR AÑO:")
    print(resultado)

    resultado.plot(kind="line", marker="o")  # markers destacan año discreto visualmente
    plt.title("Solicitudes por Año")
    plt.ylabel("Cantidad")
    plt.show()


# =============================
# ANÁLISIS 3: DISTRIBUCIÓN POR SEXO
# =============================


def distribucion_sexo(df):
    """
    pastel autopct muestra proporción suma relativos círculos aprendiendo lectura proporción porcentajes pie chart curso nivel introducción estadística ingenierías carrera instituciones.
    """
    resultado = df["sexo"].value_counts()

    print("\nDISTRIBUCIÓN POR SEXO:")
    print(resultado)

    resultado.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribución por Sexo")
    plt.ylabel("")  # pie visualmente mejor sin label eje fantasía clase académica
    plt.show()


# =============================
# ANÁLISIS 4: EDAD PROMEDIO
# =============================


def edad_promedio(df):
    """
    Estima años edad usando diferencia año calendario simple resta año hoy año nacimiento.
    IMPORTANTE método acotado académico: puede desviarse leve ±1 año respecto cálculos exactos con mes día.
    suficientemente ilustrativo parcial rápido.

    Histograma permite ver dispersión población alrededor promedio aritmetico medio impreso consola clase.
    """
    hoy = datetime.now()

    # apply recorriendo fecha_nacimiento fila fila: si NaT resultado None estadísticos posteriores mean ignora opcional clase
    df["edad"] = df["fecha_nacimiento"].apply(
        lambda x: hoy.year - x.year if pd.notnull(x) else None,
    )

    promedio = df["edad"].mean()

    print("\nEDAD PROMEDIO DE SOLICITANTES:")
    print(round(promedio, 2))

    df["edad"].plot(kind="hist", bins=20)  # distribución agrupamiento clases igual que dashboard servidor coherencia discursiva equipo
    plt.title("Distribución de Edades")
    plt.xlabel("Edad")
    plt.show()


# =============================
# MENÚ INTERACTIVO
# =============================


def menu(df):
    """
    Bucle textual simple while True permite seleccionar análisis interactivamente sin re-ejecutar script completo.
    input(str) clase laboratorio habitual Windows consola cursores docente supervise.

    Opción 5 break sale limpiamente demostraciones control clase evitando CTR-C bruscos inexperimen ados estudiantes incipientes.
    """
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
    # ruta relativa asume ejecución typical 'cd src' antes python analysis.py proyecto parcial equipo original.
    # Si cambió estructura directorios proyecto ajustá según nueva convención académica docente nueva versión cursada.
    ruta = "../data/Visa_Applications_Colombia_2017_20250217.xlsx"

    df = cargar_datos(ruta)

    menu(df)
