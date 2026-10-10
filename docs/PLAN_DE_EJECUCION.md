# Plan de Ejecución — Proyecto Final: Página Web de un Hotel

**Curso:** Programación 3 · **Valor:** 40 % de la nota final · **Hoy:** semana 5 · **Entrega:** semana 15 (≈ 10 semanas de trabajo) vía **GitHub** + presentación de 15–20 min
**Equipo (4):** Dorian · Denisse · Ashley · Yojan

> Estado: **borrador v0.2**. Los roles son una propuesta para discutir en la reunión de esta semana.

---

## 1. Resumen de lo que pide el PDF

| Tema | Requisito |
|---|---|
| Tecnologías obligatorias | HTML5 semántico, CSS3 (box model + Flexbox/Grid), Bootstrap (grid + componentes), JavaScript (eventos, validaciones, elementos dinámicos), AJAX con jQuery (simular envío/recepción de datos) |
| Opcional en el PDF | PHP (formulario de contacto funcional). **Nosotros sí lo vamos a hacer** |
| Dashboard | **AdminLTE** visto en clase, con gráficos (**ChartJS**) o tablas interactivas (**DataTables**). El botón de *login* debe llevar al dashboard |
| Páginas obligatorias | Inicio · Servicios · Habitaciones · Reserva/Contacto · Ubicación · Dashboard |
| Entrega según el PDF | `.zip` con estructura organizada + breve documentación del propósito de cada archivo/sección |
| Presentación | 15–20 min: funcionalidades implementadas y **retos superados** |
| Reglas | Participación **equitativa** de todos en desarrollo y presentación. Plagio o requisitos mínimos incumplidos = descalificación automática |

### Rúbrica (guía de prioridades)

| Criterio | Peso |
|---|---|
| Diseño general (estética, colores, fuentes, disposición) | 20 % |
| Interactividad con JavaScript | 20 % |
| Estructura HTML5 semántica | 15 % |
| Estilización CSS3 (Flexbox/Grid) | 15 % |
| Uso de Bootstrap (componentes, rejilla, responsivo) | 15 % |
| Formulario funcional y conexión básica (PHP opcional) | 10 % |
| Creatividad y originalidad | 5 % |

### Decisiones del equipo

| Tema | Decisión |
|---|---|
| Reuniones | 1 por semana |
| Cronograma | Hoy es la semana 5; entrega en la semana 15 |
| Entrega | Repositorio de **GitHub** |
| Colaboración | **GitHub** (repositorio, ramas, Pull Requests, Projects) |
| Repositorio | https://github.com/AshleyAvilaV/pagina_web_hotel (cuenta de Ashley) |
| Entorno local | **XAMPP** (Apache + PHP); todos lo instalan esta semana |
| Temática del hotel | **Por definir** — se decide esta semana (ver sección 11) |

### ⚠️ Pendiente de confirmar con el profesor/profesora
- El PDF pide grupos de **5** y somos **4**.
- El PDF habla de entregar un **.zip**; nosotros queremos entregar por **GitHub**. Hay que confirmar que se acepta el enlace al repositorio (y si debe ser público o privado con acceso para el profesor/profesora). Como respaldo, el ZIP se descarga del propio repositorio (*Code → Download ZIP*).

---

## 2. Equipo y reparto de responsabilidades (propuesta)

Cada integrante tiene **una o dos páginas propias + un área transversal + un bloque de la presentación**, para que la participación sea equitativa y todos puedan explicar su parte.

| Integrante | Páginas propias | Área transversal | Bloque en la presentación |
|---|---|---|---|
| **Dorian** | `login.html` + **Dashboard** (AdminLTE, ChartJS, DataTables) | Repositorio y flujo de Git, estructura de carpetas, integración final y versión `v1.0` | Introducción, arquitectura del proyecto y dashboard |
| **Denisse** | **Inicio** + **Servicios** | Identidad visual (paleta, tipografías, logo), CSS global y consistencia de diseño; diapositivas | Concepto del hotel, diseño y páginas Inicio/Servicios |
| **Ashley** | **Habitaciones** + **Ubicación** | Documentación (README + propósito de cada archivo) y control de calidad responsivo | Habitaciones, galería, mapa y documentación |
| **Yojan** | **Reserva/Contacto** | JavaScript de validaciones, AJAX con jQuery y PHP (`contacto.php`) | Formulario, validaciones, AJAX/PHP y retos superados |

**Revisión cruzada de código** (cada Pull Request lo aprueba otra persona): Dorian ↔ Yojan · Denisse ↔ Ashley.

> Si alguien prefiere otra área, se intercambia en la reunión. Lo importante es que la carga quede pareja.

---

## 3. Arquitectura, entorno y entrega

### Estructura de carpetas

```
hotel/
├── index.html              # Inicio
├── servicios.html
├── habitaciones.html
├── reserva.html            # Reserva / Contacto
├── ubicacion.html
├── login.html              # Botón de login → dashboard
├── dashboard/              # AdminLTE (index.html + páginas de estadísticas)
├── assets/
│   ├── css/                # estilos.css (variables, Flexbox/Grid propios)
│   ├── js/                 # main.js, validaciones.js, ajax.js, dashboard.js
│   ├── img/                # imágenes optimizadas por sección
│   └── vendor/             # Bootstrap, jQuery, ChartJS, DataTables (o CDN)
├── data/                   # JSON simulados (habitaciones, servicios, estadísticas)
├── php/
│   └── contacto.php        # procesa el formulario
├── docs/                   # este plan, diapositivas y material de apoyo
├── .gitignore
└── README.md               # propósito, cómo ejecutar y descripción de cada archivo
```

### Decisiones técnicas
- Navbar y footer idénticos en todas las páginas (Bootstrap), con paleta y tipografías en variables CSS (`:root`).
- Datos de habitaciones, servicios y estadísticas en JSON cargados con `$.getJSON` / `$.ajax`. Esto cumple "simulación de envío y recepción de datos".
- Login **simulado** (credenciales de demostración validadas en JS que redirigen a `dashboard/`). No se maneja autenticación real.
- **PHP con XAMPP:** `contacto.php` valida en el servidor y guarda la reserva/consulta en un archivo (por ejemplo `data/reservas.json`) en lugar de enviar correo, porque `mail()` no funciona en XAMPP sin configuración extra. El dashboard puede leer esas reservas en la tabla DataTables, y así el formulario y el dashboard quedan conectados.
- Los archivos generados al usar el formulario van en `.gitignore`; se sube solo un archivo de ejemplo con datos ficticios.
- **Entorno:** cada quien clona el repositorio dentro de la carpeta `htdocs` de XAMPP (o usa un enlace simbólico a ella) y abre `http://localhost/hotel/`. Todos con PHP 8.x (`php -v`).
- Las páginas estáticas deben verse bien si alguien abre el repo sin XAMPP. Ojo: `$.getJSON` **no funciona abriendo el HTML con doble clic** (`file://`). Por eso el README debe explicar cómo ejecutarlo (XAMPP o `php -S localhost:8000`).

### Flujo de trabajo en GitHub
- Un repositorio, con las 4 personas como colaboradoras. Rama `main` protegida, una rama por tarea (`feat/habitaciones`, `feat/dashboard`, …) y Pull Requests con revisión cruzada.
- Si el repositorio es privado y la cuenta es gratuita, GitHub puede no ofrecer la protección de ramas; en ese caso se acuerda por convención no hacer *push* directo a `main` (salvo el arranque inicial).
- Commits frecuentes y pequeños. Como se entrega por GitHub, el historial es la evidencia de **participación equitativa**.
- Cada integrante configura su nombre y correo en Git (`git config user.name` / `user.email`) para que sus commits queden a su nombre.
- **GitHub Projects** como tablero (*Por hacer / En curso / En revisión / Hecho*).

### Qué se entrega en GitHub
- `main` con la versión final y una etiqueta **`v1.0`** creada antes de la fecha límite (ya no se toca después).
- `README.md` con: propósito, integrantes y responsabilidades, **cómo ejecutarlo con XAMPP**, estructura de carpetas, propósito de cada archivo y créditos (imágenes y librerías).
- Sin contraseñas ni archivos pesados innecesarios.
- Respaldo: ZIP descargado de la etiqueta `v1.0` por si piden el `.zip`.

---

## 4. Cronograma (semana 5 → 15)

> Si el orden de las clases difiere (por ejemplo, cuándo ven AJAX, PHP o AdminLTE), se reacomodan las semanas 9–11 para trabajar cada tema cuando ya se haya visto.

| Semana | Objetivo | Dorian | Denisse | Ashley | Yojan |
|---|---|---|---|---|---|
| **5** (hoy) | Kickoff. **Todos:** instalar XAMPP y clonar el repo | Crear repo en GitHub, invitar al equipo, estructura de carpetas, `.gitignore`, README inicial y guía de Git | Liderar la elección de **tema y nombre** del hotel (2–3 propuestas para votar) | Reunir referencias de habitaciones y de la ubicación según el tema | Probar PHP en XAMPP (`info.php`); definir campos y reglas del formulario |
| **6** | Diseño y base | Plantilla base Bootstrap (head, navbar, footer) en `main` | Paleta, tipografías, logo y variables CSS; wireframes de Inicio y Servicios; banco de imágenes | Wireframes de Habitaciones y Ubicación; tipos de habitación y precios simulados (`habitaciones.json`) | Wireframe de Reserva; esquema de datos de reservas |
| **7–8** | Páginas estáticas | `login.html` + instalar AdminLTE y esqueleto del dashboard | **Inicio** y **Servicios** completos (HTML5 + Bootstrap + CSS) | **Habitaciones** (cards, galería) + **Ubicación** (iframe de Google Maps + cómo llegar) | `reserva.html` maquetado con formularios Bootstrap |
| **9–10** | Interactividad con JavaScript | Login simulado → dashboard; gráficos ChartJS (ocupación mensual, tipos de reserva) | Interacciones en Inicio/Servicios (animaciones, tabs/acordeón, scroll); pulido de CSS global | Filtro por tipo/precio, modal de galería, selector de fechas | Validación JS de campos, fechas y huéspedes; cálculo de total simulado |
| **11** | AJAX + PHP + datos | DataTables de reservas con datos vía AJAX | Servicios cargados desde JSON con AJAX | Habitaciones desde JSON con AJAX; "Reservar" precarga la habitación | `contacto.php` (validación en servidor, guarda en archivo) + envío con jQuery y mensajes de éxito/error |
| **12** | Integración y colchón | Dashboard muestra las reservas reales del formulario; pruebas de punta a punta | Revisión de diseño; optimizar imágenes | Revisión responsiva (móvil/tablet/escritorio) | Pruebas del formulario (casos válidos e inválidos). **Congelar funcionalidades al final de la semana** |
| **13** | QA y documentación | Enlaces rotos, consola sin errores; probar el repo **clonado desde cero** en XAMPP | Diseño final; empezar diapositivas | README (cómo ejecutar + propósito de cada archivo) y validación W3C HTML/CSS | Revisión básica de seguridad en PHP (sanitizar entradas); lista de **retos superados** |
| **14** | Ensayos y cierre | Etiqueta `v1.0` y ZIP de respaldo; solo se corrigen errores | Diapositivas finales | Revisión final del README | Preparar demo del formulario |
| **15** | Entrega y presentación | Verificar que el repo esté entregado como se acordó | Presentar | Presentar | Presentar |

En la semana 14 se agregan **2 ensayos cronometrados** (sesiones extra a la reunión semanal).

**Hitos**
- 🏁 Fin de semana 6: tema, diseño y plantilla base aprobados.
- 🏁 Fin de semana 8: las 6 páginas existen (aunque sin toda la interactividad).
- 🏁 Fin de semana 11: todas las funcionalidades obligatorias terminadas (versión mínima completa).
- 🏁 Fin de semana 12: **congelamiento de funcionalidades**.
- 🏁 Fin de semana 14: `v1.0` creada, documentación lista y ensayos hechos.

---

## 5. Matriz de requisitos → entregable → responsable

| # | Requisito del PDF | Entregable concreto | Responsable | Rúbrica |
|---|---|---|---|---|
| 1 | Home atractivo, descripción e imágenes, enlaces a secciones | `index.html` con hero, carrusel, resumen y botones a cada página | Denisse | Diseño 20 %, Bootstrap 15 % |
| 2 | Servicios con imagen y descripción | `servicios.html` con cards (habitaciones, restaurante, spa, tours) | Denisse | Diseño, HTML5 |
| 3 | Habitaciones con detalle, galería y precios simulados | `habitaciones.html` + `habitaciones.json` + galería | Ashley | JS 20 %, Bootstrap |
| 4 | Formulario funcional con validación en JS | `reserva.html` + `validaciones.js` | Yojan | JS 20 %, Formulario 10 % |
| 5 | Mapa interactivo y cómo llegar | `ubicacion.html` con iframe de Google Maps | Ashley | HTML5, Diseño |
| 6 | Dashboard con gráficos/tablas; login → dashboard | `login.html` + `dashboard/` (AdminLTE + ChartJS + DataTables) | Dorian | JS, Bootstrap |
| 7 | AJAX con jQuery | `ajax.js` (JSON de habitaciones/servicios/estadísticas y envío del formulario) | Yojan / Ashley / Dorian / Denisse | JS 20 % |
| 8 | PHP (opcional en el PDF, lo haremos) | `php/contacto.php` | Yojan | Formulario 10 % |
| 9 | CSS3: box model + Flexbox/Grid | `estilos.css` con variables y layouts propios (no solo Bootstrap) | Denisse (todos aportan) | CSS3 15 % |
| 10 | HTML5 semántico | `header`, `nav`, `main`, `section`, `article`, `footer`, `figure`, `label` | Todos | HTML5 15 % |
| 11 | Documentación del propósito de cada archivo | `README.md` | Ashley (todos aportan) | Entrega |
| 12 | Entrega organizada | Repo en GitHub con `v1.0` (+ ZIP de respaldo) | Dorian | Entrega |
| 13 | Presentación 15–20 min | Diapositivas + guion con bloques por persona | Denisse (todos aportan) | Presentación |

---

## 6. Definición de "terminado" por página

Una página se considera terminada cuando cumple **todo** lo siguiente:

- [ ] HTML5 semántico y sin errores en el validador W3C.
- [ ] Navbar y footer comunes; estilos de `estilos.css` aplicados (sin estilos inline).
- [ ] Uso de rejilla Bootstrap y al menos un componente (card, carrusel, modal, accordion, formulario…).
- [ ] Al menos una sección con Flexbox o Grid **escrito en nuestro CSS**.
- [ ] Se ve bien en móvil (~375 px), tablet (~768 px) y escritorio (≥1200 px).
- [ ] Imágenes optimizadas, con `alt` y con fuente/licencia registrada.
- [ ] Sin errores en la consola del navegador.
- [ ] Funciona servida desde XAMPP.
- [ ] Revisada y aprobada por otra persona del equipo (Pull Request).
- [ ] Sus archivos están descritos en el README.

---

## 7. Interactividad (para el 20 % de JavaScript)

**Versión mínima (semanas 9–11)**
- **Reserva:** validar campos obligatorios, formato de correo, `check-in < check-out`, número de huéspedes; calcular el total según noches y tipo de habitación; mensajes de error/éxito sin recargar.
- **Habitaciones:** filtro por tipo y rango de precio; modal con galería; botón "Reservar" que lleva al formulario con la habitación preseleccionada.
- **Servicios / Inicio:** tabs o acordeón, animaciones al hacer scroll, contador animado (habitaciones, huéspedes, años).
- **Login:** validación de campos y redirección al dashboard.
- **Dashboard:** gráficos (ocupación mensual, tipos de reserva, ingresos) con ChartJS y tabla de reservas con DataTables (búsqueda, orden, paginación), cargados vía AJAX.

**Extras opcionales** (solo después del congelamiento de la versión mínima, para el 5 % de creatividad)
- Modo oscuro, selector de idioma ES/EN, calendario de disponibilidad, reseñas de huéspedes, animaciones más elaboradas.

> Prioridad: **todo lo que se muestre en la presentación debe funcionar**. Mejor menos funciones bien terminadas que muchas a medias.

---

## 8. Presentación (15–20 min)

| Min | Quién | Contenido |
|---|---|---|
| 0–3 | Dorian | Objetivo, concepto del hotel, arquitectura y tecnologías |
| 3–8 | Denisse | Identidad visual, Inicio y Servicios (demostración en vivo) |
| 8–13 | Ashley | Habitaciones (filtro, galería), Ubicación y documentación |
| 13–18 | Yojan | Reserva: validaciones, AJAX/PHP |
| 18–20 | Dorian (dashboard) + todos | Login → dashboard, **retos superados** y cierre |

Preparativos: ensayo cronometrado en la semana 14, sitio corriendo en XAMPP con una copia de respaldo, capturas de pantalla por si falla algo en vivo, y que cada persona sepa explicar también el código de las demás.

---

## 9. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| Reparto desigual del trabajo (el PDF lo penaliza) | Commits y PR por persona; revisar el tablero en la reunión semanal |
| Acusación de plagio | Usar imágenes libres (Unsplash/Pexels u otras con licencia), registrar fuentes y no copiar plantillas completas de hoteles; AdminLTE y las librerías del curso sí se pueden usar |
| El profesor no acepta la entrega por GitHub | Confirmarlo esta semana; tener listo el ZIP de la etiqueta `v1.0` |
| XAMPP da problemas (puerto 80 ocupado, permisos en `htdocs`) | Instalarlo esta semana y probar `localhost`; si el puerto está ocupado, cambiar Apache a 8080; alternativa `php -S` |
| Conflictos al unir ramas | Integrar a `main` cada semana, no solo al final; PR pequeños |
| Con una sola reunión semanal, los PR se quedan sin revisar | Avisar por WhatsApp al abrir un PR y revisarlo en 1–2 días |
| Dejar la documentación para el último día | Cada quien documenta sus archivos en el mismo Pull Request |
| Estilos inconsistentes entre páginas | Variables CSS y plantilla base compartida desde la semana 6 |
| Retrasar la elección del tema (bloquea diseño e imágenes) | Decidirla en la reunión de esta semana, aunque sea provisional |
| Ser 4 y no 5 (el PDF pide 5) | Confirmar con el profesor/profesora esta semana; mantener un alcance realista |

---

## 10. Comunicación

- Grupo de WhatsApp para dudas rápidas y recordatorios entre reuniones.
- **1 reunión por semana** (30–45 min), con esta agenda fija:
  1. Estado de cada persona (qué terminó, qué sigue, qué la bloquea).
  2. Revisión de los Pull Requests pendientes y prueba conjunta de `main`.
  3. Acuerdo de las tareas de la semana siguiente.
- Como hay una sola reunión, el avance entre semanas se apoya en GitHub Projects y los Pull Requests: cada quien actualiza su tarjeta y avisa por WhatsApp cuando abre un PR.
- En la semana 14 se suman **sesiones extra** para los ensayos de la presentación.

---

## 11. Próximos pasos (semana 5)

- [ ] Escribirle al profesor/profesora: somos 4 (no 5) y queremos entregar por GitHub (¿público o privado con acceso?).
- [ ] **Elegir la temática y el nombre del hotel.** Cada quien lleva 1 idea a la reunión (ejemplos: hotel de playa, ecolodge de montaña, boutique urbano) y se vota. Hay que escoger un lugar **real** en Google Maps que encaje con la temática, para la página de Ubicación.
- [ ] Aprobar o ajustar el reparto de la sección 2.
- [ ] **Todos:** instalar XAMPP, iniciar Apache y comprobar `http://localhost/`.
- [x] Repositorio creado en la cuenta de Ashley, con un primer commit del README.
- [ ] Dar acceso de escritura (colaboradores) a las 4 personas y confirmar que todas pueden hacer *push*.
- [ ] Subir al repositorio el plan (`docs/`) y `CLAUDE.md`; agregar la estructura de carpetas y el `.gitignore`.
- [ ] Configurar el tablero de GitHub Projects con las tareas de la semana 6.
- [ ] Acordar versiones de librerías (Bootstrap, jQuery, AdminLTE, ChartJS, DataTables) y si van locales o por CDN.

---

## 12. Preguntas abiertas

1. ¿Cuál es el día exacto de entrega de la semana 15 y a qué hora cierra?
2. ¿El profesor/profesora acepta el enlace al repositorio en lugar del `.zip`? ¿Debe ser público?
3. ¿Qué temática y nombre elegimos?
4. ¿En qué semana se ven AJAX, PHP y AdminLTE en clase? (para ajustar las semanas 9–11)
