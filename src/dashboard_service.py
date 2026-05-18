"""
Generación de figuras para el dashboard web (matplotlib sin ventana).

Usamos el backend 'Agg' únicamente en este módulo para poder guardar PNG en memoria
sin afectar el script analysis.py cuando se ejecuta por consola con plt.show().
"""

from __future__ import annotations

import base64
import io
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from analysis import cargar_datos

# Paleta coherentes con Bootstrap / UI limpia
COLOR_PRIMARY = "#0d6efd"
COLOR_SECONDARY = "#6610f2"
COLOR_SUCCESS = "#198754"
COLOR_INFO = "#0dcaf0"
COLOR_MUTED = "#6c757d"


def _fig_to_base64_uri(fig: plt.Figure) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=120)
    plt.close(fig)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _prep_edad(df: pd.DataFrame) -> pd.Series:
    hoy = datetime.now()
    df = df.copy()
    edad = df["fecha_nacimiento"].apply(
        lambda x: hoy.year - x.year if pd.notnull(x) else None,
    )
    return edad


def grafica_top_nacionalidades(df: pd.DataFrame) -> str:
    resultado = df["nacionalidad"].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    colores = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_INFO, COLOR_MUTED]
    resultado.plot(kind="bar", ax=ax, color=colores[: len(resultado)])
    ax.set_title("Top 5 nacionalidades con más solicitudes", fontsize=13, pad=12)
    ax.set_xlabel("Nacionalidad")
    ax.set_ylabel("Cantidad de solicitudes")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    return _fig_to_base64_uri(fig)


def grafica_solicitudes_por_anio(df: pd.DataFrame) -> str:
    resultado = df["anio"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    resultado.plot(kind="line", marker="o", ax=ax, color=COLOR_PRIMARY, linewidth=2)
    ax.set_title("Solicitudes de visa por año", fontsize=13, pad=12)
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de solicitudes")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    return _fig_to_base64_uri(fig)


def grafica_distribucion_sexo(df: pd.DataFrame) -> str:
    resultado = df["sexo"].value_counts()
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    resultado.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax,
        startangle=90,
        colors=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS][: len(resultado)],
    )
    ax.set_title("Distribución por sexo", fontsize=13, pad=12)
    ax.set_ylabel("")
    fig.tight_layout()
    return _fig_to_base64_uri(fig)


def grafica_distribucion_edades(df: pd.DataFrame) -> str:
    edad = _prep_edad(df)
    serie = edad.dropna()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    serie.plot(kind="hist", bins=20, ax=ax, color=COLOR_SECONDARY, edgecolor="white", alpha=0.9)
    ax.set_title("Distribución de edades de los solicitantes", fontsize=13, pad=12)
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Frecuencia")
    ax.grid(True, alpha=0.25, axis="y")
    fig.tight_layout()
    return _fig_to_base64_uri(fig)


def estadisticas_resumen(df: pd.DataFrame) -> dict:
    edad = _prep_edad(df)
    edad_prom = float(round(edad.mean(), 2)) if edad.notna().any() else None
    por_anio = df["anio"].value_counts().sort_index()
    anio_max = int(por_anio.idxmax()) if not por_anio.empty else None
    nacionalidad_top = df["nacionalidad"].value_counts().head(1)
    nombre_top = str(nacionalidad_top.index[0]) if len(nacionalidad_top) else None
    cant_top = int(nacionalidad_top.iloc[0]) if len(nacionalidad_top) else None

    sexo_counts = df["sexo"].value_counts(normalize=True) * 100
    dominante_sexo = sexo_counts.idxmax() if len(sexo_counts) else None
    pct_dominante = float(round(sexo_counts.max(), 1)) if len(sexo_counts) else None

    total = int(len(df))
    return {
        "total_filas": total,
        "total_filas_fmt": f"{total:,}",
        "anos_rango": f"{int(df['anio'].min())} – {int(df['anio'].max())}",
        "edad_promedio": edad_prom,
        "anio_pico": anio_max,
        "pico_valor": int(por_anio.max()) if anio_max is not None else None,
        "pico_valor_fmt": (
            f"{int(por_anio.max()):,}" if anio_max is not None else None
        ),
        "top_nacionalidad": nombre_top,
        "top_nacionalidad_cantidad": cant_top,
        "top_nacionalidad_cantidad_fmt": (
            f"{cant_top:,}" if cant_top is not None else None
        ),
        "sexo_predominante": dominante_sexo,
        "sexo_predominante_pct": pct_dominante,
    }


def construir_contexto_dashboard(ruta_excel: str) -> dict:
    df = cargar_datos(ruta_excel)
    stats = estadisticas_resumen(df)
    conclusion = texto_conclusion(stats)

    return {
        "stats": stats,
        "conclusion": conclusion,
        "img_nacionalidades": grafica_top_nacionalidades(df),
        "img_anios": grafica_solicitudes_por_anio(df),
        "img_sexo": grafica_distribucion_sexo(df),
        "img_edades": grafica_distribucion_edades(df),
    }


def texto_conclusion(stats: dict) -> str:
    partes = [
        (
            "Se analizaron {total_filas:,} registros de solicitudes de visa en Colombia "
            "para el período {anos_rango}."
        ).format(**stats),
        (
            "La nacionalidad con mayor número de registros fue {top_nacionalidad} "
            "({top_nacionalidad_cantidad:,} solicitudes)."
        ).format(**stats)
        if stats["top_nacionalidad"]
        else "",
        (
            "El año con mayor volumen registrado fue {anio_pico}, con "
            "{pico_valor:,} solicitudes, lo cual sugiere un punto alto de demanda "
            "en ese periodo temporal."
        ).format(**stats)
        if stats["anio_pico"] is not None
        else "",
        (
            "En cuanto al perfil demográfico, la edad promedio estimada fue de "
            "{edad_promedio} años, útil como referencia del rango típico de "
            "solicitantes; el histograma permite ver si esa media está apoyada en "
            "una distribución concentrada o dispersa."
        ).format(**stats)
        if stats["edad_promedio"] is not None
        else "",
        (
            "La distribución por sexo muestra un predominio de {sexo_predominante} "
            "(aprox. {sexo_predominante_pct} %), información relevante para contexto "
            "demográfico, siempre complementada con otros factores institucionales."
        ).format(**stats)
        if stats["sexo_predominante"] and stats["sexo_predominante_pct"] is not None
        else "",
        (
            "En conjunto, las cuatro visualizaciones permiten combinar dimensión "
            "geográfica (nacionalidad), temporal (año), demográfica (sexo y edad) "
            "y plantear hipótesis sobre picos de demanda y perfiles de quienes "
            "solicitan visa en el dataset analizado."
        ),
    ]
    return " ".join(p for p in partes if p)
