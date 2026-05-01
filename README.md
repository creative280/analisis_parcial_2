# 📊 Análisis de Solicitudes de Visa en Colombia

## 👥 Integrantes
Ana María Camacho Castaño
Fabian Alberto Bedoya
Maicol Smith Bueno
Jorge Iván Marín Cifuentes
Alejandro Taborda Sepúlveda

---

## 🎯 Objetivo

Analizar el comportamiento de las solicitudes de visa en Colombia usando Python y Pandas, con el fin de identificar patrones, tendencias y conclusiones relevantes.

---

## ✅ Requerimientos del parcial (cómo se cumple)

- **Carga en Pandas**: el script carga el dataset desde `data/` (o por parámetro) y lo convierte en un `DataFrame`.
- **4 análisis propuestos** (cada uno imprime resultados por consola y genera una gráfica):
  - **Análisis 1**: Top 10 países con más solicitudes.
  - **Análisis 2**: Evolución de solicitudes por mes (según fecha de aplicación).
  - **Análisis 3**: Distribución de estados de la solicitud (aprobada/denegada/etc.).
  - **Análisis 4**: Tipos de visa más solicitados.
- **Salida**:
  - Resultados: consola + Graficas tipo Modal


---

## 🧰 Tecnologías utilizadas

- Python
- Pandas
- Matplotlib

---

## 📁 Estructura del proyecto

- data/: contiene el dataset
- src/: código principal

---

## ▶️ Cómo ejecutar el proyecto

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Colocar el dataset (Visa_Applications_Colombia_2017_20250217.xlsx) en `data/` (recomendado) y ejecutar:

```bash
cd src
python analysis.py
```
