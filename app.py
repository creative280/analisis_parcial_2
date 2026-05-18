"""
Aplicación Flask: dashboard de visualizaciones del proyecto de análisis de visas.

¿Qué hace este archivo?
- Arranca la app web Flask.
- Expone una ruta "/" que renderiza templates/dashboard.html.
- Llama al módulo src/dashboard_service.py para preparar gráficas (Base64),
  métricas (stats) y el texto de conclusión antes de pintar HTML.

Ejecutar desde la raíz del repositorio:

    pip install -r requirements.txt
    python app.py

Luego abrir en el navegador: http://127.0.0.1:5000/
"""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, render_template

# ---------------------------------------------------------------------------
# Ruta base del proyecto (carpeta donde está este archivo app.py)
# ---------------------------------------------------------------------------
# Path(__file__) apunta al path real de este .py en disco.
# .parent sube un nivel para obtener la carpeta raíz del proyecto.
ROOT = Path(__file__).resolve().parent

# Carpeta donde vive dashboard_service.py y analysis.py
SRC = ROOT / "src"

# Python debe poder importar desde "src" al hacer: from dashboard_service import ...
# sys.path lista rutas donde busca módulos; si falta SRC, la agregamos al inicio (0).
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# noqa: E402 — el linter se quejaría porque el import viene "tarde"; es intencional
# (necesitamos modificar sys.path antes de importar módulos de src/).
from dashboard_service import construir_contexto_dashboard  # noqa: E402

# Instancia principal de Flask. El parámetro __name__ le dice cómo ubicar carpeta templates/.
app = Flask(__name__)

# Ruta absoluta al Excel: mejor que rutas relativas frágiles "dependiendo desde dónde ejecutes".
DATA_PATH = ROOT / "data" / "Visa_Applications_Colombia_2017_20250217.xlsx"


@app.route("/")
def dashboard():
    """
    Se ejecuta cuando el usuario entra en http://host:puerto/

    Flask recibe GET / y llama a esta función para construir la respuesta HTML.
    """
    # Sin datos no hay dashboard: mensaje corto útil durante desarrollo.
    # Código HTTP 500 indica fallo servidor; aquí equivale a configuración incompleta.
    if not DATA_PATH.is_file():
        return (
            f"No se encontró el archivo de datos esperado:\n{DATA_PATH}\n"
            "Coloca el Excel en la carpeta data/ y recarga.",
            500,
        )

    # ctx (contexto): diccionario con todo lo que la plantilla Jinja espera usar.
    # Incluye: stats, conclusion, img_nacionalidades, img_anios, img_sexo, img_edades.
    ctx = construir_contexto_dashboard(str(DATA_PATH))

    # **ctx expande llaves como argumentos con nombre para render_template.
    # Equivale conceptualmente a:
    #   render_template("dashboard.html",
    #       stats=ctx["stats"],
    #       conclusion=ctx["conclusion"],
    #       ...)
    return render_template("dashboard.html", **ctx)


if __name__ == "__main__":
    # Solo arranca el servidor cuando ejecutamos "python app.py" directamente.
    # Si importaras app desde otro archivo, típicamente NO querrías lanzar servidor solo.
    # debug=True: mensajes de error más legibles útiles en clase; no usar público así.
    app.run(debug=True, host="127.0.0.1", port=5000)
