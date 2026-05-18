# Guía ampliada: Flask, Bootstrap y el dashboard del Parcial 3  
**Audiencia:** estudiantes de **VIII semestre** (Ingeniería de Software — Inteligencia Artificial)  
**Proyecto de referencia:** `flask_parcial_3` (visa en Colombia, Excel en `data/`, servidor en `app.py`)

Este documento explica **qué es Flask**, **qué es Bootstrap**, cómo dialogan entre sí y **qué construyeron exactamente** en este proyecto, con **ejemplos aplicados al código actual** para poder estudiarlo o exponerlo con seguridad técnica.

---

## Primero: ¿qué problema resolvemos?

Necesitaban cumplir (entre otras cosas):

- Una **dashboard en Flask** donde se **vean todas las gráficas** definidas para el proyecto.
- **Debajo**, una **conclusión general** del análisis.
- Una **presentación ordenada visualmente**.

La solución en este repositorio es:

1. **Python + Pandas** leen el Excel y preparan datos.
2. **Matplotlib** dibuja gráficas **en el servidor**.
3. Cada imagen se convierte en un **dato embebido** (`data:image/png;base64,...`) para enviarla al HTML sin guardar `.png` en disco.
4. **Flask** arma la página y la entrega al navegador.
5. **Bootstrap** da la rejilla responsive, navbar, tarjetas y tipografía profesional sin escribir mucho CSS a mano.

---

# Parte 1 — ¿Qué es Flask y cómo pensarlo?

## 1.1 Definición en términos de carrera “Software”

**Flask** es un **microframework web** para Python.

- Es **servidor HTTP de desarrollo**: escucha puertos (por defecto algo como **5000**), recibe solicitudes (**request**) y contesta (**response**) con texto HTML, JSON, archivos, etc.
- Promueve un **orden claro**: *rutas URL → función en Python → plantilla HTML*.

No es necesario conocer Django completo solo para Flask: Flask **no impone una estructura enorme**. Aquí decidieron tener:

```
flask_parcial_3/
├── app.py                 → Entrada Flask, rutas HTTP
├── templates/
│   └── dashboard.html      → Vista (HTML “con huecos” rellenos por servidor)
├── data/
│   └── ...xlsx             → Fuente de datos
└── src/
    ├── analysis.py         → Carga desde Excel + análisis de consola (anterior)
    └── dashboard_service.py → Gráficas + métricas + conclusión (para web)
```

Eso coincide con una idea habitual en web: separar lo que **computa datos** (`src`) de lo que **pinta páginas** (`templates`), aun cuando todo sea relativamente compacto como en este parcial.

## 1.2 Cliente ↔ servidor en una línea mental

Imagine el ciclo cuando usted escribe **http://127.0.0.1:5000/**:

1. **Navegador** hace solicitud GET a esa URL (**cliente HTTP**).
2. **Python** ejecuta **Flask**.
3. Flask ve la ruta `/` registrada (`@app.route("/")`).
4. Se ejecuta la función `dashboard()`.
5. Esa función **prepara un diccionario de variables para la vista** (`contexto`).
6. `render_template` **mezcla datos + HTML**.
7. El navegador recibe HTML finalizado y muestra página.

Este modelito es suficientemente completo como concepto técnico de **aplicación dinámica** para el nivel del curso.

## 1.3 Los cuatro elementos imprescindibles de Flask aplicados aquí

### (A) `from flask import Flask, render_template`

- Importa clase `Flask` y la herramienta `render_template` que busca carpetas llamadas **`templates`** al lado de `app.py`.

### (B) `app = Flask(__name__)`

- **`__name__`** indica cómo debe nombrarse el paquete interno cuando Flask busca recursos relacionados (`templates`, `static` si hubiera carpeta así). En esencia: *“Este archivo principal es donde vive mi app.”*

### (C) Rutas `@app.route("/")`

Ejemplo aplicado (**`app.py` real**):

```python
@app.route("/")
def dashboard():
    ctx = construir_contexto_dashboard(str(DATA_PATH))
    return render_template("dashboard.html", **ctx)
```

- **`@`** = **decorador** en Python que “envuelve” la función siguiente.
- Flask le dice: *Cuando llegue petición a `/`, ejecuta lo que viene debajo.*

**Analogía rápida para exponer:**

> Un URL es como el **nombre de un botón físico**. El decorador registra ese botón contra una **función** que hace trabajo.

Aquí sólo tienen **`/`**. Si después quieren otra página pública tipo `/informe`, agregarían sólo otro `@app.route("/informe")` con otra plantilla sin reescribir todo.

### (D) Ejecución

```python
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
```

Por qué importa (**enseñanza de laboratorio**, no prod real):

| Fragmento             | ¿Qué hace prácticamente? |
|-----------------------|---------------------------|
| `if __name__ == "__main__"` | Solo arranca servidor si ejecutan `python app.py` como script. Si desde otro módulo hicieron `import app`, no se lanzaría servidor implícito. |
| `debug=True`               | Mensajes más claros y recarga rápida mientras desarrollan. Para **internet público** sería grave dejar así: expone errores sensibles conceptuales si no están filtrados. |
| `host="127.0.0.1"`         | En escuela solemos estar “local”. Si quieren prueba rápida en red local de laboratorio pueden cambiar a `0.0.0.0` (con conocimiento docente/red). |

## 1.4 `render_template` y el operador `**ctx`

Este fragmento (**también en `app.py`**) muestra algo didácticamente muy útil para VIII sem:

```python
ctx = construir_contexto_dashboard(str(DATA_PATH))
return render_template("dashboard.html", **ctx)
```

- `ctx` es un **dict** con claves `stats`, `conclusion`, `img_nacionalidades`, etc.

**El `**` en Python**:

```python
d = {"nombre": "Ana", "edad": 22}
some_func(**d)       # Equivalente conceptual a some_func(nombre="Ana", edad=22)
```

Aquí permite que la plantilla `dashboard.html` reciba todas las llaves individuales **sin tener que llamar**:

```python
render_template(..., stats=..., conclusion=..., img_nacionalidades=..., ...)
```

Conclusión práctica aplicada para estudiar: **centralizan la preparación de datos** en Python y **delegan formato visual** mayormente en HTML/CSS.

---

# Parte 2 — ¿Qué es Jinja2 (las `{{ }}` y `{% %}`?

Flask viene con motor de plantillas **Jinja2** que extienden HTML estándar.

## 2.1 Doble llave imprime variable

Ejemplo (**`templates/dashboard.html` real**):

```html
<img src="{{ img_nacionalidades }}" alt="..." />
```

`img_nacionalidades` **no existe en el archivo estático antes de correr servidor**: será reemplazado por contenido producido cuando renderizan esa plantilla tras visitar `/`.

**Nota importante:** ese valor llega ya como texto completo `data:image/png;base64,...` listo para atributo `src`.

## 2.2 Llave-porciento lógicas

Ejemplo del mismo proyecto:

```jinja
{% if stats.edad_promedio is not none %}
  {{ stats.edad_promedio }}
{% else %}
  —
{% endif %}
```

Aquí muestran un **valor alternativo (“—”)** si no pueden calcular promedio (por ejemplo todas las edades perdidas después de errores fuertes de datos).

**Para exposición:** dígan que no es sintaxis nuevo lenguaje, es **DSL de plantillas** que evita tener que hacer `print` manual de etiquetas desde Python línea línea incómodamente.

---

# Parte 3 — ¿Qué es Bootstrap y cómo lo usamos aquí?

## 3.1 Definición directa sin marketing

Bootstrap es una **colección prefabricada** de CSS (y algo de JS opcional) que:

- Uniformiza tamaños fuentes, paddings (`espaciados`), grids responsivos (“**12 columnas** mágicas que se reorganizan en móvil”).
- Reduce tiempo de desarrollo visual.

En este proyecto se integra mediante **CDN** (red de distribución) en lugar de npm/composer — perfecto nivel parcial porque no configuraron bundlers.

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet" .../>
```

¿Qué CDN trae prácticamente? **Clases** listas tipo:

| Clase ejemplo | ¿Qué hace intuitivamente aquí en UI? |
|---------------|--------------------------------------|
| `container`       | Centro contenido máximo ancho razonable, márgenes laterales auto. |
| `row`, `col-*`    | Cuadrícula adaptable: ejemplo `col-lg-6`, mitad página en escritorio grande, apilamiento en móvil. |
| `navbar`..., `bg-primary` | Barra superior típico color corporativo institucional. |
| `card`, `shadow-sm`       | Cajas agrupadas con sombra corta profesional sin CSS manual grande. |

## 3.2 Bootstrap Grid aplicado específico a tus gráficas

En `dashboard.html` hay **rejilla**:

```html
<div class="row g-4 mb-4">
  <div class="col-lg-6">
    <!-- tarjeta gráfico 1 -->
  </div>
  <div class="col-lg-6">
    <!-- tarjeta gráfico 2 -->
  </div>
...
</div>
```

**Traducción al lenguaje de exposición**:

- Dos columnas lado a lado **si la pantalla es grande** (`lg` ≈ breakpoints ≥992px típico en BS5 histórico; ver doc oficial cuando profundice).
- En pantalla estrecha, columnas probablemente ocupen todo ancho porque **automáticamente apilan**.
- **`g-4`** aumenta gutters (espacio hueco horizontal/vertical moderado tarjetas adyacentes) → sensación menos amontonada sin medir pixeles uno a uno.

Por eso se verá profesional rápido incluso antes de pintar algo personalizado.

## 3.3 CSS extra que no es Bootstrap

Al final tienen etiqueta `<style>...</style>` con selectores específicos (`.hero`, `.chart-card`, `.metric`). Eso muestra nivel maduro VIII sem:

- **Bootstrap arma el esqueleto global** (rejilla/navbar/cards estándares).
- **CSS propio muy acotado** refina marca visual (radios grandes, degradado subtíl fondo, sombras temáticas con color primario institucional de Bootstrap `#0d6efd` relacionado tonalmente manualmente usando transparencias en `rgba`).

Ejemplo pedagogico rápido (no aparece igual literal en archivo, solo ilustrativo):

```css
body {
  background: linear-gradient(...);
}
```

Aquí están **mezclando**:

1. Diseño rápido (Bootstrap).
2. Personalización superficial (su propio degradado página completa para que no se ve plano monocromático base).

Buen argumento ante docente diferenciando niveles trabajo “plantilla sólo” versus “adaptación marca curso”.

## 3.4 Script Bootstrap JS cargado sí o sí

Hay:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" ... ></script>
```

En este proyecto concreto el HTML **usa** apenas componentes estáticos; no hay menús colapsibles accionados que *insistan* tener JS inicializado.

**Propósito habitual docente**:

- Futuro cercano pueden agregar un **Navbar toggler**, **Carousel**, **Collapse** necesitante JS inicial Bootstrap.
- Cargarlo ya marca buena práctica académica: “traigo stack completa aun cuando no todas piezas están activadas aún”. No hay gran costo en ambiente clase.

---

# Parte 4 — Lo que REALMENTE hicieron técnicos a nivel código

## 4.1 Carga inicial del Excel (`src/analysis.py`)

```python
def cargar_datos(ruta):
    df = pd.read_excel(ruta)
    df.columns = ["anio","nacionalidad","sexo","fecha_nacimiento","vocacion","numero"]
    df["fecha_nacimiento"] = pd.to_datetime(..., errors="coerce", dayfirst=True)
    return df
```

¿Por qué importa para clase?

- **`read_excel`**: formato propietario tabla negocio.
- **`errors='coerce'`**: evita crashes por fecha inválidas raras (se tornan NaT permitiendo filtro posterior eventual sin caer proceso completo servidor).
- **`dayfirst=True`**: formato dd/mm habitual regiones español LATAM cuando ambigüidades.

Este análisis se reutiliza vía **`from analysis import cargar_datos`** en `dashboard_service.py`: **single source sobre limpieza mínima** evita inconsistencias repetidas.

### Breve paralelo consola `/` web original

Las funciones tipo `top_nacionalidades(df)` muestran con `plt.show()` **interfaz escritorio estudiante ejecutando desde IDE**.

Versión nueva web **replaza `show()` por export renderizable HTML**: misma estadística pero presentación servidor.

Esta distinción **es muy pedagógica**:

> Una misma función intelectual (contar valores) lleva DOS formas físicas de resultado (ventana escritorio VS bytes imagen servidor).

---

## 4.2 Generación servidor imágenes `dashboard_service.py`

### ¿Por backend `matplotlib.use("Agg")`?

En escritorio estudiante ejecutan consola donde ventana aparece físicamente cuando `plt.show()`.

En servidor no hay escritorio garantizado detrás proceso Python en producción típico.

Agg es **solo raster sin GUI**: produce buffer imagen suficientemente para web.

¿Qué problema evita clase?

Sin eso algunos estudiantes en Windows lanzan servidor y obtienen error backend intentando abrir UI no disponible proceso servicio segundo plan.

### ¿Qué hace `_fig_to_base64_uri`?

Pasos ordenados (**versión textual resumida lógico**):

1. `savefig(... format='png', bbox_inches='tight')` ⇒ bytes PNG en memoria.
2. Encode base64 ⇒ ASCII seguro dentro URL larga embebido.
3. antepondrán prefijo oficial `data:image/png;base64,` para HTML entienda formato.

Ejemplo sintético mínimo (no es igual literal proyecto, sólo muestra técnico):

```
data:image/png;base64,iVBORw0KGgoAAAANSUhEU...
```

Ventaja parcial clase:

- Sin escribir permisos disco extra ruta producción clase.
- Un solo ciclo servidor -> cliente.

Desventaja aprendido honesto:

Si dataset enorme repetir graficaciones pesadas cada request `/` cargaría CPU. Aquí tamaño proyecto académico lo toleran. En industria usarían caching, pre-render o framework chart front-end.

Es buen argumento nivel VIII sem ante docente mencionándolo conscientemente muestra conocimiento infra.

### Paleta colores alineados Bootstrap `#0d6efd` etc.

Elegir colores cercanos marca UI **produce cohesión perceptual**:

- Navbar `bg-primary` azul institucional.
- Barras usan tonalidades derivadas cercanas perceptualmente aun si no hexadecimal idénticas linea pixel perfecto marca Apple.

Sirve ejemplo **comunicación visión equipo diseño ingeniería** pequeños detalles.

---

## 4.3 KPI + conclusión `estadisticas_resumen()` + `texto_conclusion()`

**Por qué hay KPI antes gráficas?**

En comunicación ejecutiva clase:

Primero numero guía rápido luego soporte evidencia grafica segundo.

Aquí muestran `total_filas_fmt`, año pico número solicitudes formato miles `,`.

**Construcción conclusión con strings condicionadas:**

```python
if stats["top_nacionalidad"]:
    texto_parte(...)
```

Evita frases triviales cuando data vacía degenerada.

**Ejemplo mental examen rápido docente**:

Si eliminan accidentalmente todas filas por error script carga excel falso, KPI mostrarían inconsistencias perceptibles rápido desarrolladores debug.

---

## 4.4 `dashboard()` seguridad archivo inexistente

```python
if not DATA_PATH.is_file():
    return (mensaje texto explicativo, 500)
```

**500** código HTTP servidor error — no es UX perfecto producto cliente final, sí es feedback explícito **desarrollo** laboratorio rápido: “falta colocación dataset”.

Versión clase podrían mejorar usando plantilla errores friendly luego opcional nivel extra.

---

# Parte 5 — Mapa rápido de EXAMEN/ORAL recomendaciones

## Cinco bullets memorizar salida sala

1. **Flask = microframework servidor HTTP rutas función plantilla**.
2. **Plantilla ≠ HTML estático.** Se llena servidor con Jinja antes enviar navegador.
3. **Bootstrap = CSS grid rápido + componentes** vía CDN; personalizamos poco pero significativo degrade fondo radios sombras marca curso integración.
4. **Matplotlib Agg + Base64 = patrón común clase convertir estadística servidor → imagen embebido sin archivos físicos externos dinámicos temporales clase Windows permisos alumnos dispersos escritorios instituciones.
5. **Separación `analysis`** (limpia datos reproducible tanto consola servidor) demuestra reutilización abstracciones software decente nivel académico.

## Oración “elevator pitch” equipo

> Cargamos un Excel institucional, limpiamos datos con pandas, generamos estadísticas reproducibles igual que proyecto consola inicial, después convertimos gráficas Matplotlib servidor memoria formato embebido y servimos página única usando Flask enrutador raíz combinando layout responsive Bootstrap KPI textual conclusión pedagógica final.

Si dominan ese párrafo oral fluido seguridad aumenta perceptible ante jurado rápido.

---

# Parte 6 — Cómo correr proyecto y verificar rápido (checklist equipo)

Desde carpeta proyecto raíz donde está `requirements.txt`:

1. `pip install -r requirements.txt`
2. Aseguren Excel presente **`data/`** mismo nombre esperado `Visa_Applications_Colombia_2017_20250217.xlsx` configurado rutas dentro `app.py` actual.
3. `python app.py`
4. navegador `http://127.0.0.1:5000/`
5. Visuales debe mostrar KPI + 4 graficas correspondientes proyecto + conclusión abajo ordenada dentro card borde destacado tema primario institucional.

Si algo falló:

| Síntoma | Posible causa académica |
|---------|--------------------------|
| 500 archivo no encontrado | Excel mal nombre / mal carpeta /
| página vacío gráfica rota lugar imagen sin decode | problema Matplotlib errores servidor log consola lanzamiento server |
| gráficas sin estilo esperado navegador | CDN bloqueado red instituciones – probar tethering hotspot docente permite |

(Estas líneas muestran **mentalidad soporte equipo** clase superior semestral.)

---

## Cierre

Este proyecto combina conocimientos VIII sem (**datos**, **servidor web conceptual**, **separación lógicas**, **interfaces responsivas rápidos prototipado**) dentro alcance tiempo parcial típico: no es infra despliegue industria nivel AWS completo pero es **fundamento suficientemente sólido** para explicar capas servidor-cliente usando stack Python popular académico.

Si después quieren mejorar siguiente iteración pueden considerar (**sin obligación parcial cerrado**) cosas pedagogía avanzadas:

- segunda ruta `/metodología` texto estático científicos procedimento limpieza,
- archivo `requirements` versionado pinning exactitudes reproducibilidad equipo,
- caché imágenes precomputadas,
- mover gráficas front-end usando Plotly pero eso aumenta Javascript curva aprendizaje.

---

**Última nota práctica.** Si reproducen contenido textual oral casi verbatim en diapositiva, sugieren **diagrama simple flechas** `(Excel→Pandas→Matplotlib→Base64→Jinja/Bootstrap HTML→Cliente)` para memorización visual rápida compañeros.

---

*Documento pensado complementario a entregables técnicos; no sustituye rúbrica docente institucional exacta.*
