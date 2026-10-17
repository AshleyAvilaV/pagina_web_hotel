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
├── assets/             # css, js, img, vendor
├── data/               # JSON simulados
├── php/                # contacto.php
└── docs/               # plan de ejecución y material de apoyo
```

### Propósito de cada archivo

| Archivo / carpeta | Propósito |
|---|---|
| `index.html` | Página de inicio. Por ahora es un "Hola, mundo" para comprobar que el sitio se sirve desde XAMPP. |
| `servicios.html` | Servicios del hotel (restaurante, spa, tours…). Por ahora es un marcador de posición. |
| `habitaciones.html` | Tipos de habitación, galería y precios simulados. Por ahora es un marcador de posición. |
| `reserva.html` | Formulario de reserva y contacto. Por ahora es un marcador de posición. |
| `ubicacion.html` | Mapa interactivo y cómo llegar. Por ahora es un marcador de posición. |
| `login.html` | Login simulado que redirige al dashboard. Por ahora es un marcador de posición. |
| `dashboard/index.html` | Panel de administración con AdminLTE, ChartJS y DataTables. Por ahora es un marcador de posición. |
| `assets/css/` | Hojas de estilo propias (`estilos.css` con variables en `:root`, Flexbox y Grid). |
| `assets/js/` | Scripts propios (`main.js`, `validaciones.js`, `ajax.js`, `dashboard.js`). |
| `assets/img/` | Imágenes optimizadas, organizadas por sección. |
| `assets/vendor/` | Librerías externas (Bootstrap, jQuery, ChartJS, DataTables) si se usan en local en lugar de CDN. |
| `data/` | Archivos JSON simulados (habitaciones, servicios, estadísticas) y reservas guardadas por PHP. |
| `php/` | Scripts de servidor; aquí irá `contacto.php`. |
| `docs/` | Plan de ejecución y material de apoyo. |
| `.gitignore` | Excluye archivos del sistema, de editores y los datos generados por el formulario (`data/reservas.json`). |
| `.gitkeep` | Archivo vacío para que Git guarde las carpetas que todavía no tienen contenido; se borra cuando la carpeta tenga archivos reales. |
| `CLAUDE.md` | Instrucciones del proyecto para el asistente Claude Code. |

## Créditos

> Por completar: fuentes y licencias de imágenes, y librerías utilizadas.

| Recurso | Uso | Fuente | Licencia |
|---|---|---|---|
| Playfair Display y Lato (provisionales) | Tipografías de títulos y texto | [Google Fonts](https://fonts.google.com/) | SIL Open Font License 1.1 |
| Material Symbols Outlined | Íconos | [Google Fonts — Icons](https://fonts.google.com/icons) | Apache 2.0 |
