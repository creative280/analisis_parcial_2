# Cómo funciona Bootstrap: guía práctica con ejemplos aplicados  
**Proyecto:** `flask_parcial_3` — plantilla principal `templates/dashboard.html` · **Bootstrap 5.3.3**

La documentación oficial (inglés) sirve como referencia detallada: [Bootstrap 5 — Layout](https://getbootstrap.com/docs/5.3/layout/grid/), [Navbar](https://getbootstrap.com/docs/5.3/components/navbar/), [Cards](https://getbootstrap.com/docs/5.3/components/card/), [Utilities](https://getbootstrap.com/docs/5.3/utilities/spacing/).

---

## 1. ¿Qué es Bootstrap y qué “hace” en tu página?

Bootstrap es un **framework de CSS (y un poco de JavaScript)** que define **clases** con nombres fijos. Al poner esas clases en tu HTML, el navegador aplica estilos predefinidos (márgenes, colores, rejillas, tipografía) **sin que tengas que escribir todo el CSS a mano**.

En tu dashboard pasa esto:

1. En el `<head>` enlazás el CSS de Bootstrap por **CDN** (un archivo remino comprimido).
2. En el `<body>` usás clases como `container`, `row`, `col-md-3`, `navbar`, `card`.
3. Bootstrap “lee” esas clases y pinta la página de forma coherente y **responsive** (se adapta al ancho de pantalla).

**Ejemplo mínimo (solo concepto):**

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
<div class="container">
  <p class="text-primary fw-bold">Hola Bootstrap</p>
</div>
```

**Aplicado en tu proyecto** (`dashboard.html`): el `<link>` al CSS de Bootstrap está en las líneas que cargan `bootstrap@5.3.3` desde `cdn.jsdelivr.net`. Sin esa línea, la mayoría de las clases del dashboard **no tendrían efecto**.

---

## 2. Meta `viewport` y por qué importa en móviles

Bootstrap asume que la página declara ancho de pantalla correcto en móviles:

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

**Qué hace:** le dice al navegador del celular que use el ancho real del dispositivo, no un “ancho falso” de escritorio. Así las columnas `col-*` pueden apilarse bien.

**Aplicado en tu proyecto:** está en `dashboard.html` justo después de `charset`. Si lo quitás, en algunos móviles la página puede verse “miniaturizada” o con zoom raro.

---

## 3. Contenedores: `container` vs `container-fluid`

| Clase | Comportamiento típico |
|--------|------------------------|
| `container` | Centra el contenido y deja **márgenes laterales**; en pantallas muy anchas no estira el texto infinito (más legible). |
| `container-fluid` | Ocupa **casi todo el ancho** siempre (útil dashboards full-bleed). |

**Ejemplo mínimo:**

```html
<div class="container">
  <p>Contenido centrado con márgenes automáticos.</p>
</div>
```

**Aplicado en tu proyecto:**

- La **barra superior** (`<nav>`) tiene un `<div class="container">` dentro: el texto del título no toca los bordes del monitor.
- El **contenido principal** usa `<main class="container pb-5">`: mismo ancho legible y `pb-5` = **padding bottom** grande (espacio antes del pie).

`pb-5` es una **utilidad de espaciado** de Bootstrap (lo verás en la sección 7).

---

## 4. Sistema de rejilla (Grid): filas y columnas

Bootstrap divide el ancho en **12 columnas virtuales**. Sumás `col-*` dentro de un `row` y el motor reparte el espacio.

**Reglas útiles para VIII semestre:**

- Siempre: **padre** `row`, **hijos** `col-...`.
- `col-6` ≈ mitad del ancho (6/12).
- `col-12` ≈ ancho completo.
- Puedes combinar **prefijos de breakpoint**: `col-6 col-md-3` significa “en pantallas **≥ md** comportate como 3/12; en más chicas, aplica la regla de `col-6`”.

**Breakpoints comunes en BS5 (memorizar el orden de tamaño):**

| Prefijo | Ancho mínimo aproximado |
|---------|-------------------------|
| (sin prefijo, solo `col-*`) | Extra small, base |
| `sm` | ≥576px |
| `md` | ≥768px |
| `lg` | ≥992px |
| `xl` | ≥1200px |
| `xxl` | ≥1400px |

**Ejemplo mínimo (dos columnas en pantalla grande, una columna en chica):**

```html
<div class="row">
  <div class="col-12 col-lg-6">Izquierda</div>
  <div class="col-12 col-lg-6">Derecha</div>
</div>
```

**Aplicado en tu proyecto — KPI (indicadores):**

```html
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">...</div>
  ...
</div>
```

- `col-6`: en móvil, **2 tarjetas por fila** (6+6=12).
- `col-md-3`: desde **md** en adelante, **4 tarjetas por fila** (3+3+3+3=12).

**Aplicado en tu proyecto — gráficas:**

```html
<div class="row g-4 mb-4">
  <div class="col-lg-6">...</div>
  ...
</div>
```

- En pantallas **grandes** (`lg`), **2 gráficas por fila**.
- En pantallas **más angostas**, cada `col-lg-6` pasa a ocupar el 100% (comportamiento por defecto si no forzás `col-12` explícito: el `col-lg-6` solo aplica desde `lg`; abajo de eso las columnas se apilan).

**`g-3` y `g-4`:** son **gutters** (hueco entre columnas). `g-4` deja más aire entre tarjetas de gráficas que `g-3` entre KPI.

---

## 5. Navbar (barra de navegación)

Componente típico con muchas clases juntas; cada una aporta un detalle:

**Ejemplo mínimo:**

```html
<nav class="navbar navbar-dark bg-primary">
  <div class="container">
    <span class="navbar-brand">Mi app</span>
  </div>
</nav>
```

| Clase (resumen) | Rol |
|-----------------|-----|
| `navbar` | Activa estilos base de barra. |
| `navbar-expand-lg` | En pantallas ≥ `lg` los ítems se muestran en línea; en móvil prepara colapso (si tuvieras botón). |
| `navbar-dark` | Texto/iconos claros sobre fondo oscuro. |
| `bg-primary` | Color de fondo **primario** del tema (en BS5 por defecto es un azul `#0d6efd`). |
| `mb-4` | Margen inferior. |
| `shadow-sm` | Sombra suave. |
| `navbar-brand` | Estilo de “marca” / título. |
| `navbar-text` | Texto secundario en la barra. |
| `ms-lg-auto` | Margen **start** automático desde breakpoint `lg` (empuja el texto a la derecha en escritorio). |
| `text-white-50` | Blanco con transparencia. |
| `fw-semibold` | Peso de fuente semi-negrita (utility tipográfica). |

**Aplicado en tu proyecto:** revisá el bloque `<nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4 shadow-sm">` en `dashboard.html`. Ahí combinás branding del parcial + subtítulo técnico alineado a la derecha en pantallas grandes.

---

## 6. Cards (tarjetas)

Las **cards** agrupan borde, padding y opcionalmente cabecera/cuerpo.

**Ejemplo mínimo:**

```html
<div class="card">
  <div class="card-header">Título arriba</div>
  <div class="card-body">
    Contenido
  </div>
</div>
```

**Variantes útiles:**

- `bg-white` fuerza fondo blanco útil cuando el contexto tiene gradientes.
- `h-100` hace que la tarjeta **stretch** a la misma altura que vecinas dentro de una fila (se ve ordenado cuando una gráfica es más alta que otra sin `h-100`).

**Aplicado en tu proyecto:**

1. **Tarjeta “hero”** (encabezado del panel):  
   `class="card hero mb-4 text-white bg-primary bg-gradient"`  
   - Usa Bootstrap (`card`, colores `bg-*`, texto `text-white`, utilidad tipográfica/spacing como `mb-4`).  
   - La clase `hero` es **tuya**, definida en el `<style>` del mismo archivo para bordes y sombra más personalizados.

2. **KPI**: `card metric` + `card-body` → caja compacta números/indicadores.

3. **Gráficas**: `card chart-card h-100` + `card-header` + `card-body text-center`.  
   - `chart-card` amplía tus estilos (borde azul muy suave, sombra ligera).  
   - `img` con `max-width: 100%` en tu CSS clase `.chart-card img` evita que el PNG desborde el ancho disponible dentro de Bootstrap.

---

## 7. Utilidades de espaciado: `m-*`, `p-*`, “tamaños”

Bootstrap usa una escala aproximada **0–5** (a veces más en utilidades extendidas):

| Prefijo | Significado |
|---------|-------------|
| `m` | **margin** (margen exterior) |
| `p` | **padding** (relleno interior) |
| Sufijos direccionales | `t` top, `b` bottom, `s` start (izq en LTR), `e` end (der), `x` horizontal, `y` vertical |

**Ejemplos:**

- `mb-2` → margin-bottom pequeño (separar título de lo que sigue).
- `mb-4` → margin-bottom más grande (separar secciones).
- `py-4` → padding vertical dentro de `card-body` (aire arriba/abajo del texto del hero).
- `pb-5` en `<main>` → padding bottom grande para no pegar el pie de página al borde inferior.

**Aplicado en tu proyecto:** buscá `mb-2`, `mb-4`, `py-4`, `pb-5`, `g-3`, `g-4` en `dashboard.html` y probá **cambiar un número** (por ejemplo `g-3` → `g-2`) y recargar: verás cómo afloja o aprieta el layout sin tocar CSS personalizado.

---

## 8. Tipografía y utilidades de texto / color

| Clase | Efecto |
|-------|--------|
| `h1`, `h2`, … o `h3` “de utilidad” | Tamaños de encabezado semánticos / visuales. |
| `h3` en un `<h1>` | Truco común: **semánticamente** es un título principal (`<h1>`) pero **visualmente** se ve como `h3` (`class="h3"`). |
| `small` | Texto secundario más chico. |
| `text-muted` | Color apagado (gris del tema). |
| `fs-4`, `fs-6` | **Font size** responsive del sistema de utilidades. |
| `fw-semibold` | Negrita intermedia. |
| `lead` | Párrafo un poco más grande (énfasis suave). |
| `text-secondary` | Color secundario del tema. |
| `opacity-75` | Transparencia del texto (sobre fondos de color). |

**Aplicado en tu proyecto:**

- KPI: `text-muted small` para etiquetas (“Registros”, “Periodo”), `fs-4 fw-semibold` para el número grande.
- Conclusión: `lead fs-6 text-secondary` combina legibilidad con jerarquía visual.
- La clase propia `.section-title` imita un “overline” gris (no es de Bootstrap, pero **coexiste** con utilidades como `mb-2`).

---

## 9. Bordes, sombras y utilidades rápidas

| Clase | Efecto |
|-------|--------|
| `border-top` | Línea superior (usada en el `<footer>`). |
| `text-center` | Centrar contenido inline/flex hijos según contexto. |
| `shadow-sm` | Sombra pequeña (navbar). |
| `bg-gradient` | Degradado sobre utilidades `bg-primary` (hero). |

**Aplicado en tu proyecto:** `footer` con `border-top pt-3` separa visualmente el cierre de la página (`pt-3` = padding-top).

---

## 10. JavaScript de Bootstrap (`bootstrap.bundle.min.js`)

Al final de `dashboard.html` cargás:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" ...></script>
```

Incluye **Popper** (posicionamiento) para cosas como **dropdowns, tooltips, popovers** y comportamiento de algunos componentes dinámicos.

**En tu dashboard actual:** no es imprescindible para lo que muestrás (principalmente grid + cards + navbar estática). Sí es **costumbre recomendada** porque si después agregan menú colapsable o modal, ya tienen la base cargada.

---

## 11. Dónde entra tu CSS propio (`<style>` del dashboard)

Bootstrap resuelve el **80 % del layout**.

Tu bloque `:root`, `.hero`, `.chart-card`, `.metric`, etc. sirve para:

- Bordes redondeados uniformes (`--dash-radius`).
- Sombras con un tinte ligero azul institucional.
- Fondo con **gradient** suave para que la página no se vea “plana Bootstrap default”.
- Resaltar bloque conclusion con `--bs-primary`-like `#0d6efd` borde lateral.

**Ejercicio práctico para clase:** cambiá sólo `--dash-shadow` en `:root` y observá efecto sobre `.hero` y `.chart-card` sin romper rejilla Bootstrap.

---

## 12. Checklist rápido para exponer (“cómo explicarlo en 1 minuto”)

1. **Bootstrap define clases**, el navegador aplica CSS prearmado al HTML.
2. **Grid:** `container` → `row` → `col-*` (siempre hasta 12 unidades virtuales por fila).
3. **Responsive:** combinás `col-6 col-md-3` para móvil vs escritorio como en tus KPI.
4. **Componentes:** `navbar`, `card` + utilidades (`mb-4`, `text-muted`, `fs-4`).
5. **CDN:** Bootstrap vive fuera del repo pero se enlaza rápido; tu CSS corto complementa marca visual equipo.

Si querés experimentar sin romper dashboard, creá **`templates/playground.html`** aparte copiando un `row/col` minimal y tocando clases hasta que visualmente “haga clic” cómo funcionan breakpoints y gutters.
