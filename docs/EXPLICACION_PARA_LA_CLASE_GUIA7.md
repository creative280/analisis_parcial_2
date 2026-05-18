# Explicación del proyecto Flask (alineado con la Guía 7)

Este documento sirve para **estudiar y exponer** en clase cómo está armada la práctica frente a lo que dice la **Guía 7 (Flask)** de Inteligencia Artificial.

---

## 1. ¿Qué pide la Guía 7 y cómo lo cumple este código?

| Tema en la Guía 7 | Cómo aparece aquí |
|-------------------|-------------------|
| Instalar Flask (`pip install flask`) | Hazlo en tu entorno antes de ejecutar (`pip install flask pandas matplotlib`). |
| Crear `app.py` como punto de entrada | Archivo **`app.py`** en la carpeta del proyecto. |
| `from flask import Flask` y `app = Flask(__name__)` | Líneas iniciales: se crea la **instancia de la aplicación**. |
| Rutas con `@app.route(...)` | Ruta **`/`** (principal) con las gráficas y ruta **`/acerca`** (segunda página, como ejemplo de “más de una funcionalidad”). |
| Ejecutar con `if __name__ == '__main__':` y `app.run(debug=True)` | Final del archivo `app.py`; el servidor solo arranca si ejecutas ese archivo directamente. |
| Carpetas **`templates`** y `render_template` | Carpeta **`templates/`** con `grafica.html` y `acerca.html`; Flask **renderiza HTML** desde ahí. |
| Enviar variables a la plantilla | Se envían **`grafica1`** y **`grafica2`** (cadenas Base64) a `grafica.html` para mostrar las imágenes. |

Las secciones de la guía sobre **lista en plantilla** o **calculadora con POST** son ejercicios aparte para aprender métodos GET/POST; **no tienen por qué** repetirse en un proyecto de gráficas, siempre que el núcleo (Flask + rutas + templates + variables) esté cubierto, como ocurre aquí.

---

## 2. Estructura de carpetas (qué archivo hace qué)

```
prueba_fl/
├── app.py                 # Servidor Flask, carga datos, genera gráficas en memoria
├── data/
│   └── ventas.csv         # Datos fuente (ventas)
└── templates/
    ├── grafica.html       # Página principal: muestra las dos imágenes
    └── acerca.html        # Página “Acerca” (segunda ruta)
```

Ejecutar **siempre desde la carpeta donde está `app.py`** (`prueba_fl`), para que Excel/CSV encuentre bien la ruta `data/ventas.csv`.

---

## 3. `app.py` — bloques explicados (para exponer línea conceptual)

### 3.1 Configuración de Matplotlib antes de cargar pyplot

- Se usa **`matplotlib.use('Agg')`** antes de `import matplotlib.pyplot as plt`.
- **Motivo:** el backend **Agg** dibuja en memoria/pixel buffer, sin abrir ventana en el servidor. Así Flask puede guardar cada figura como PNG en bytes y mandarlas al navegador.

### 3.2 Lectura y limpieza del CSV (`ventas.csv`)

- **`open("data/ventas.csv", "rb")`:** se leen bytes crudos porque el archivo tenía líneas donde la codificación UTF-8 llegaba incompleta.
- **`raw.replace(...)`:** parches muy concretos a secuencias corruptas antes de **decodificar** a texto con `.decode("utf-8", errors="ignore")`.
- **`pd.read_csv(StringIO(text), sep=",")`:** Pandas necesita archivo o stream de texto; `StringIO` convierte ese texto en algo “como archivo” para `read_csv`.
- **Strip y formato de texto:** `.str.strip()`, `.str.title()` en columnas texto para valores uniformes (“Cliente ” vs “cliente”).
- **Fechas y números:** `pd.to_datetime` para `fecha`, `pd.to_numeric` para cantidad y precio, con **`errors="coerce"`** por si viene basura → se vuelven `NaT`/`NaN` y después se corrigen/filtran.
- **Nulos:** rellenos en cantidad/precio a 0, y **eliminar filas** sin fecha válida (`dropna` en `fecha`).
- **Columna calculada:** `total_venta = cantidad * precio_unitario` para graficar totales económicos.

### 3.3 Agregaciones antes de graficar (fuera de la función de ruta)

- **`ventas_por_ciudad`:** agrupa por `ciudad`, suma `total_venta`, ordena de mayor a menor (para la primera gráfica de barras).
- **`ventas_producto`:** agrupa por `producto`, suma `cantidad` (para la segunda gráfica de líneas).

Esto está **fuera del `@app.route`** para ejecutarse **una vez** al arrancar la app y no repetir trabajo en cada visita.

### 3.4 Ruta principal `/`

- **`@app.route('/')`** + **`def grafica():`:** cuando visitas **`http://127.0.0.1:5000/`**, Flask ejecuta esta función.

**Gráfica 1**

1. **`fig1, ax1 = plt.subplots()`** — figura nueva.
2. **`ventas_por_ciudad.plot(kind="bar", ...)`** — diagrama de barras en ese eje.
3. **`plt.tight_layout()`** — ajusta márgenes.
4. **`io.BytesIO()`** — buffer en memoria; **`savefig`** en formato PNG dentro del buffer.
5. **`base64.b64encode(...).decode()`** — la imagen pasa a **texto Base64** para embeber en HTML (`<img src="data:image/png;base64,...">`).
6. **`plt.close(fig1)`** — libera memoria del backend de matplotlib (buena práctica en servidor).

**Gráfica 2:** mismo patrón con `fig2`, línea sobre `ventas_producto`.

**Plantilla:**

- **`return render_template('grafica.html', grafica1=..., grafica2=...)`** — equivale al tema **“Mostrar página HTML”** + **“Enviar variables”** de la Guía 7.

### 3.5 Segunda ruta `/acerca`

- **`@app.route("/acerca")`** + función **`acerca`** que solo hace **`return render_template("acerca.html")`**.
- Demuestra el concepto guía **“segunda URL / otra vista”**. En el navegador: **`http://127.0.0.1:5000/acerca`**.

### 3.6 Punto de entrada

- **`if __name__ == '__main__':`** — si importas `app.py` desde otro módulo **no** se levanta el servidor solo.
- **`app.run(debug=True)`** — modo desarrollo: mensajes de error útiles (**no usar en internet público así** para producción).

---

## 4. `templates/grafica.html` — qué muestra y cómo usa las variables

- Es **plantilla HTML** que Flask procesa antes de responder al navegador.
- **`{{ grafica1 }}`** y **`{{ grafica2 }}`** — sintaxis **Jinja2**, igual espíritu que la guía con `{{ nombre_usuario }}`.
- **`src="data:image/png;base64,{{ grafica1 }}"`** — formato **data URI**: el navegador interpreta ese texto como imagen PNG sin necesidad de un archivo `.png` aparte.

---

## 5. `templates/acerca.html`

- Vista estática complementaria enlazando de vuelta a **`/`**, para relacionar bien con **“Agregar una segunda ruta”** de la Guía 7.

---

## 6. Cómo correr la demo antes de exponer

1. Abrir terminal en la carpeta del proyecto (donde está `app.py`).
2. Activar tu entorno virtual si usas uno.
3. **`pip install flask pandas matplotlib`** (primera vez o si falta algo).
4. **`python app.py`**
5. Navegador: **`http://127.0.0.1:5000/`** (gráficas) y **`http://127.0.0.1:5000/acerca`** (segunda página).
6. Comprobar instalación Flask (opcional como en la guía): **`python -m pip show flask`**.

---

## 7. Ideas para una exposición corta (2–3 minutos)

1. **Qué es Flask** en una frase: microframework para web en Python.
2. **`app`** y rutas **`/`** vs **`/acerca`** — misma app, diferentes URLs.
3. **`render_template` + variables** — separas **lógica** (Python) de **presentación** (HTML).
4. Datos desde CSV → Pandas → gráficas en memoria → **Base64 → HTML**.
5. Cierre: por qué `Agg`, por qué `plt.close`.

Con esto tienes ordenado el guion técnico alineado a la **Guía 7** y al código tal como está pensado para la clase.
