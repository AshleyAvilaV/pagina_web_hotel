# Proyecto Final — Página Web de un Hotel

Proyecto final del curso **Programación 3**: diseño y desarrollo de la página web de un hotel ficticio que integra HTML5, CSS3, Bootstrap, JavaScript, AJAX con jQuery, PHP y un dashboard con AdminLTE.

> **Estado:** en planificación (semana 5). La temática y el nombre del hotel se definen esta semana.

## Equipo

| Integrante | Páginas propias | Área transversal |
|---|---|---|
| Dorian | Login y Dashboard | Repositorio, integración y versión final |
| Denisse | Inicio y Servicios | Identidad visual y CSS global |
| Ashley | Habitaciones y Ubicación | Documentación y control de calidad responsivo |
| Yojan | Reserva/Contacto | Validaciones JS, AJAX y PHP |

El reparto es una propuesta y se detalla en el plan de ejecución.

## Documentación

- 📋 [**Plan de ejecución**](docs/PLAN_DE_EJECUCION.md): requisitos del proyecto, reparto de responsabilidades, cronograma de la semana 5 a la 15, flujo de trabajo en GitHub, riesgos y próximos pasos.
- 📌 [**Tablero de tareas**](https://github.com/users/dorianprogrammer/projects/1): quién hace qué y en qué estado va cada tarea (Por hacer, En curso, En revisión, Hecho). Cada tarea es un [issue](https://github.com/AshleyAvilaV/pagina_web_hotel/issues) de este repositorio.

## Cómo ejecutarlo

> Por completar cuando exista la primera versión del sitio.

El proyecto usa PHP y AJAX, por lo que **no se debe abrir el HTML con doble clic**; hay que servirlo desde un servidor local:

1. Instalar [XAMPP](https://www.apachefriends.org/) e iniciar **Apache**.
2. Clonar este repositorio dentro de la carpeta `htdocs` de XAMPP.
3. Abrir `http://localhost/<nombre-de-la-carpeta>/` en el navegador.

Alternativa sin XAMPP: `php -S localhost:8000` desde la raíz del proyecto.

### Credenciales de demostración

El login es simulado (no hay autenticación real). Para entrar al dashboard:

| Correo | Contraseña |
|---|---|
| `admin@paraisotico.cr` | `Paraiso2026` |

## Estructura del proyecto

> Estructura planeada; se irá completando con el propósito de cada archivo.

```
├── index.html          # Inicio
├── servicios.html
├── habitaciones.html
├── reserva.html        # Reserva / Contacto
├── ubicacion.html
├── login.html          # Login → dashboard
├── dashboard/          # AdminLTE
├── componentes/        # piezas HTML compartidas (header) que se cargan por AJAX
├── assets/             # css, js, img, vendor
├── data/               # JSON simulados
├── php/                # contacto.php
└── docs/               # plan de ejecución y material de apoyo
```

### Propósito de cada archivo

| Archivo / carpeta | Propósito |
|---|---|
| `index.html` | Página de inicio. Por ahora solo tiene el header compartido. |
| `servicios.html` | Servicios del hotel (restaurante, spa, tours…). Por ahora es un marcador de posición. |
| `habitaciones.html` | Tipos de habitación, galería y precios simulados. Por ahora es un marcador de posición. |
| `reserva.html` | Formulario de reserva y contacto. Por ahora es un marcador de posición. |
| `ubicacion.html` | Mapa interactivo y cómo llegar. Por ahora es un marcador de posición. |
| `login.html` | Login simulado según el Figma: valida los campos con JavaScript, compara con las credenciales de demostración y redirige al dashboard. |
| `dashboard/index.html` | Panel de administración con AdminLTE, ChartJS y DataTables. Por ahora es un marcador de posición. |
| `componentes/header.html` | Header compartido (navbar de Bootstrap y menú lateral en móvil). Se edita solo aquí: `main.js` lo inserta en todas las páginas excepto login y dashboard. |
| `assets/css/` | Hojas de estilo propias (`estilos.css` con variables en `:root`, Flexbox y Grid). |
| `assets/css/estilos.css` | Estilos globales que cargan todas las páginas: paleta y tipografías en variables (`:root`), base tipográfica y el header compartido (navbar + menú lateral). |
| `assets/css/inicio.css` | Estilos propios de la página de Inicio. |
| `assets/css/login.css` | Estilos del login: panel con foto, formulario, estados de los campos (válido, error, foco) y versión móvil. |
| `assets/img/hojas-decorativas.png` | Hojas decorativas de las esquinas del header. |
| `assets/img/login-panel.jpg` | Foto del panel izquierdo del login (volcán y piscina). |
| `assets/js/` | Scripts propios (`main.js`, `validaciones.js`, `ajax.js`, `dashboard.js`). |
| `assets/js/login.js` | Login simulado: validación de correo y contraseña, mostrar/ocultar contraseña, "Recordarme" (guarda el correo en `localStorage`), aviso de funciones no disponibles y redirección al dashboard. |
| `assets/js/main.js` | Carga los componentes compartidos con jQuery (`$.load`) en los elementos con `data-component` y marca en el menú la página actual. |
| `assets/img/` | Imágenes optimizadas, organizadas por sección. |
| `assets/vendor/` | Librerías externas (Bootstrap, jQuery, ChartJS, DataTables) si se usan en local en lugar de CDN. |
| `assets/vendor/bootstrap/` | Bootstrap 5.3.8 en local: `css/bootstrap.min.css` (estilos y rejilla) y `js/bootstrap.bundle.min.js` (componentes interactivos, incluye Popper). Los `.map` solo sirven para depurar en el navegador. |
| `assets/vendor/jquery/` | jQuery 3.7.1 en local (AJAX y manipulación del DOM). |
| `data/` | Archivos JSON simulados (habitaciones, servicios, estadísticas) y reservas guardadas por PHP. |
| `php/` | Scripts de servidor; aquí irá `contacto.php`. |
| `docs/` | Plan de ejecución y material de apoyo. |
| `.github/workflows/revision-ia.yml` | Pipeline de GitHub Actions: en cada Pull Request ejecuta `revision_ia.py` y publica el resultado como comentario del PR. Los umbrales se cambian con `UMBRAL_ALTO` y `UMBRAL_AMBIGUO`; con `FALLAR_SI_ALTO: "true"` el check falla si el índice es alto. |
| `.github/scripts/revision_ia.py` | Calcula un índice (0–100 %) de posible código generado con IA a partir de señales en las líneas añadidas y en los commits del PR. Es un indicador para el revisor, no una prueba. Se puede probar en local con `python3 .github/scripts/revision_ia.py --base origin/main`. |
| `.gitignore` | Excluye archivos del sistema, de editores y los datos generados por el formulario (`data/reservas.json`). |
| `.gitkeep` | Archivo vacío para que Git guarde las carpetas que todavía no tienen contenido; se borra cuando la carpeta tenga archivos reales. |
| `CLAUDE.md` | Instrucciones del proyecto para el asistente Claude Code. |

## Créditos

> Por completar: fuentes y licencias de imágenes, y librerías utilizadas.

| Recurso | Uso | Fuente | Licencia |
|---|---|---|---|
| Lilita One y Linden Hill | Tipografías de títulos y texto | [Google Fonts](https://fonts.google.com/) | SIL Open Font License 1.1 |
| Material Symbols Rounded | Íconos | [Google Fonts — Icons](https://fonts.google.com/icons) | Apache 2.0 |
| Bootstrap 5.3.8 | Rejilla y componentes | [getbootstrap.com](https://getbootstrap.com/) | MIT |
| jQuery 3.7.1 | AJAX y DOM | [jquery.com](https://jquery.com/) | MIT |
| Bootstrap Icons (Instagram, Facebook, WhatsApp) | Íconos de redes en el header, como SVG en línea | [icons.getbootstrap.com](https://icons.getbootstrap.com/) | MIT |
| Hojas decorativas (`hojas-decorativas.png`) | Adorno del header | Exportada del Figma del equipo — **pendiente: confirmar el origen de la imagen** | Por confirmar |
| Foto del login (`login-panel.jpg`) | Panel izquierdo del login | Exportada del Figma del equipo — **pendiente: confirmar el origen de la imagen** | Por confirmar |
