"""
Este módulo prepara todo lo que el dashboard web necesita:
- Lectura/consistencia datos vía analysis.cargar_datos
- Cálculos de métricas (KPI / stats)
- Generación gráficas con Matplotlib
- Conversión cada figura PNG -> cadena Base64 embebida (data URI HTML)
- Texto único conclusion armado combinando estadísticas

¿Por backend Matplotlib 'Agg'?
En servidor no siempre existe ventana gráfica. Agg dibuja "sin pantalla" y permite
guardar PNG a bytes en memoria (BytesIO).

Nota importante: Mantener Agg sólo aquí evita interferir si en analysis.py
otra persona ejecuta plt.show() en escritorio usando otro backend.
"""

from __future__ import annotations

import base64
import io
from datetime import datetime

import matplotlib

# Debe ejecutarse antes de importar pyplot cuando usamos Agg como backend útil servidor.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402 — orden intencional respecto matplotlib.use(...)
import pandas as pd

from analysis import cargar_datos

# Colores alineados aproximados a Bootstrap (--bs-primary típico 5.x ≈ #0d6efd)
# Esto ayuda visualmente a que barras/gráficas "parezcan del mismo equipo" que navbar/UI.
COLOR_PRIMARY = "#0d6efd"
COLOR_SECONDARY = "#6610f2"
COLOR_SUCCESS = "#198754"
COLOR_INFO = "#0dcaf0"
COLOR_MUTED = "#6c757d"


def _fig_to_base64_uri(fig: plt.Figure) -> str:
    """
    Transforma una figura Matplotlib a string usable en HTML:<img src="data:image/png;base64,...">.

    Pasos conceptuales:
    1) Guardar PNG en memoria buffers BytesIO en vez de archivo disco.
    2) Codificar binario PNG a texto Base64 (seguro dentro atributos largos ascii).
    3) anteponer prefijo MIME que HTML entienda como embedded image.
    4) plt.close(fig) libera RAM backend interno servidor (buena práctica web).
    """
    buffer = io.BytesIO()

    # dpi y bbox_inches afectan tamaño/precisión apariencia navegador
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=120)

    plt.close(fig)

    buffer.seek(0)  # volver lectura desde inicio antes leer todos bytes PNG

    encoded = base64.b64encode(buffer.read()).decode("ascii")

    # Data URI formato estándar: tipo + codificación textual embebido
    return f"data:image/png;base64,{encoded}"


def _prep_edad(df: pd.DataFrame) -> pd.Series:
    """
    Estima edad simple reste año_actual - año_nacimiento para cada fecha válida.

    Limitación conscientemente académica: ignoramos mes/día para no complicar cálculos;
    dataset grande típico aceptación curso suficientemente ilustrativo.
    Sin fecha NaT produce None eventualmente ignorado estadísticos.
    """
    hoy = datetime.now()

    # copy() aisla mutaciones accidental futuras cuando operamos intermedios
    df = df.copy()

    edad = df["fecha_nacimiento"].apply(
        lambda x: hoy.year - x.year if pd.notnull(x) else None,
    )
    return edad


def grafica_top_nacionalidades(df: pd.DataFrame) -> str:
    """
    Barras horizontal/columnas típicas TOP categorías repetidas nacionalidad registrada más.
    value_counts cuenta frecuencia; head(5) recorta sólo primeras importantes comunicación ejecutiva rápido.
    """
    resultado = df["nacionalidad"].value_counts().head(5)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    colores = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_INFO, COLOR_MUTED]
    # color list recortamos longitud igual categorías efectivas graficadas dinámicamente
    resultado.plot(kind="bar", ax=ax, color=colores[: len(resultado)])

    ax.set_title("Top 5 nacionalidades con más solicitudes", fontsize=13, pad=12)
    ax.set_xlabel("Nacionalidad")
    ax.set_ylabel("Cantidad de solicitudes")

    # rotación texto eje evita etiquetas superpuestas algunas nacionalidades strings largos
    ax.tick_params(axis="x", rotation=35)

    fig.tight_layout()  # ajusta espaciados márgenes evita etiquetas cortadas algunos tamaños navegadores

    return _fig_to_base64_uri(fig)


def grafica_solicitudes_por_anio(df: pd.DataFrame) -> str:
    """
    Serie temporal simple: conteo solicitudes año columna discrete entera anio ascendente tiempo.
    markers 'o' hacen visible cada año discreto mejor que línea continua sola perceptual clase.
    """
    resultado = df["anio"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    resultado.plot(kind="line", marker="o", ax=ax, color=COLOR_PRIMARY, linewidth=2)

    ax.set_title("Solicitudes de visa por año", fontsize=13, pad=12)
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de solicitudes")

    # grid alfpha bajo sutileza no estorba lectura valores aprox visual estimación rápido
    ax.grid(True, alpha=0.25)

    fig.tight_layout()

    return _fig_to_base64_uri(fig)


def grafica_distribucion_sexo(df: pd.DataFrame) -> str:
    """
    Pastel proporcional categorías sexo conocidas archivo (asumimos pocas etiquetas nivel curso típico).
    autopct inserta texto porcentajes relativo masa total clase visual comparación proporciones rápida oral exposición estudiantil.
    """
    resultado = df["sexo"].value_counts()

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    resultado.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax,
        startangle=90,
        # recortamos colores igual número segmentos efectivos resultado longitud cambiante
        colors=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS][: len(resultado)],
    )

    ax.set_title("Distribución por sexo", fontsize=13, pad=12)
    ax.set_ylabel("")  # limpiar texto vertical automático evita ocupar espacio inútil

    fig.tight_layout()

    return _fig_to_base64_uri(fig)


def grafica_distribucion_edades(df: pd.DataFrame) -> str:
    """
    Histograma muestra forma distribución edades solicitantes después transformación fecha nacimiento.
    bins controla granularidad perceptual clase 20 habitual equilibrio ruido / suavización visual rápido.
    """
    edad = _prep_edad(df)

    serie = edad.dropna()  # sin NaN para que hist no degrade silenciosa incoherencias

    fig, ax = plt.subplots(figsize=(9, 4.8))

    serie.plot(kind="hist", bins=20, ax=ax, color=COLOR_SECONDARY, edgecolor="white", alpha=0.9)

    ax.set_title("Distribución de edades de los solicitantes", fontsize=13, pad=12)
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Frecuencia")

    ax.grid(True, alpha=0.25, axis="y")  # guías sólo ejes valores verticales frecuencia

    fig.tight_layout()

    return _fig_to_base64_uri(fig)


def estadisticas_resumen(df: pd.DataFrame) -> dict:
    """
    Calcula KPI mostrados arriba imágenes en dashboard:
    totals, año pico nacionalidad destacada proporción sexo etc.

    Algunos campos tienen formato _fmt porque Jinja muestra mejor miles con coma humanos lectura,
    otros bruto número python útil formato internos textos concatenación estadística siguiente función.
    """
    edad = _prep_edad(df)

    # mean None si todas sin edad válida protege divisiones inconsistencias muestra vacía estadística sensible
    edad_prom = float(round(edad.mean(), 2)) if edad.notna().any() else None

    # value_counts año -> cuántas solicitudes por año orden temporal idxmax para detectar año máximo masa
    por_anio = df["anio"].value_counts().sort_index()
    anio_max = int(por_anio.idxmax()) if not por_anio.empty else None

    # head(1) extrae mejor categoría frecuente absolutamente hablando nacionalidades
    nacionalidad_top = df["nacionalidad"].value_counts().head(1)
    nombre_top = str(nacionalidad_top.index[0]) if len(nacionalidad_top) else None
    cant_top = int(nacionalidad_top.iloc[0]) if len(nacionalidad_top) else None

    # normalize=True produce proporciones relativas entre 0-1 antes multiplicamos 100 => porcentaje simple clase
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
    """
    FUNCIÓN ORQUESTADORA usada desde app.py

    Una sola entrada de datos + retorno dict coincide expectativas render_template (**ctx expansión Flask).
    Reutiliza cargar_datos centraliza limpieza nombres columnas igual consola proyecto original.
    """
    df = cargar_datos(ruta_excel)
    stats = estadisticas_resumen(df)

    conclusion = texto_conclusion(stats)

    # Cada función grafica_* regresa URIs independientes llamadas pueden costar algo CPU porque render cada visita página.
    # Aceptación académica curso tamaño medio dataset habitual laptop estudiantil sin caching avanzado requerimiento parcial típico.
    return {
        "stats": stats,
        "conclusion": conclusion,
        "img_nacionalidades": grafica_top_nacionalidades(df),
        "img_anios": grafica_solicitudes_por_anio(df),
        "img_sexo": grafica_distribucion_sexo(df),
        "img_edades": grafica_distribucion_edades(df),
    }


def texto_conclusion(stats: dict) -> str:
    """
    Concatena frases condicionadas evitando afirmaciones vacías ejemplo si nacionalidad_top None después limpiezas agresivas.
    placeholders {campo:,} formateadores miles clase visual lectura rápido docente cuando imprime estadística combinada texto largo párrafo final dashboard.
    """
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

    # join filtra strings falsy vacíos dejando espacio uniforme párrafos combinados clase exposición textual fluida estudiantil
    return " ".join(p for p in partes if p)
