"""
Aplicación Flask: dashboard de visualizaciones del proyecto de análisis de visas.

Ejecutar desde la raíz del repositorio:

    pip install -r requirements.txt
    python app.py

Luego abrir en el navegador: http://127.0.0.1:5000/
"""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, render_template

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dashboard_service import construir_contexto_dashboard  # noqa: E402

app = Flask(__name__)

DATA_PATH = ROOT / "data" / "Visa_Applications_Colombia_2017_20250217.xlsx"


@app.route("/")
def dashboard():
    if not DATA_PATH.is_file():
        return (
            f"No se encontró el archivo de datos esperado:\n{DATA_PATH}\n"
            "Coloca el Excel en la carpeta data/ y recarga.",
            500,
        )
    ctx = construir_contexto_dashboard(str(DATA_PATH))
    return render_template("dashboard.html", **ctx)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
