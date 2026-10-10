# Proyecto Final — Página Web de un Hotel (Programación 3)

University final project: a website for a fictitious hotel, built by a team of 4 (Dorian, Denisse, Ashley, Yojan). It is 40 % of the course grade, delivered through GitHub in **week 15** and presented to the class (15–20 min). The team is currently in week 5 (as of 2026-10-09); the hotel's theme and name are **not decided yet**.

## Source of truth

Read [docs/PLAN_DE_EJECUCION.md](docs/PLAN_DE_EJECUCION.md) before planning or building anything. It holds the assignment requirements and grading rubric (section 1), who owns what (2), architecture and Git workflow (3), the week-by-week schedule (4), the requirement → deliverable matrix (5), the definition of done per page (6) and the open questions (12).

- Don't duplicate the plan here. When a decision changes (theme, dates, owners, scope), update the plan.
- If the plan and a request conflict, say so instead of silently diverging.

## Stack — stay inside what the course covers

HTML5 (semantic), CSS3 (our own Flexbox/Grid, not only Bootstrap), Bootstrap, JavaScript, AJAX with jQuery, PHP (run through XAMPP) and AdminLTE with ChartJS / DataTables for the dashboard.

- Don't introduce frameworks or build tooling (React, Vue, Tailwind, npm bundlers, etc.): the grade depends on showing the listed technologies.
- Pages must work served from XAMPP (`http://localhost/...`). `$.getJSON` / AJAX does not work from `file://`.
- Login is simulated (demo credentials checked in JS, then redirect to `dashboard/`). Do not build real authentication.
- `php/contacto.php` validates on the server and stores submissions in a file under `data/`; it does not send email (`mail()` doesn't work on XAMPP by default). Generated data files are gitignored; commit only a sample with fake data.

## Conventions

- Site content, comments and documentation are in **Spanish**. File and folder names follow the structure in the plan (`servicios.html`, `assets/js/validaciones.js`, …).
- Shared navbar, footer, colour palette and typography live in the base template and in CSS variables (`:root`). New pages reuse them, with no inline styles.
- Every page must meet the definition of done in section 6 of the plan: semantic HTML, Bootstrap grid plus a component, responsive at ~375 / 768 / 1200 px, images with `alt` and a recorded source/licence, no console errors.
- When adding or renaming a file, update the file-by-file description in `README.md`; the assignment requires documenting the purpose of each file.

## Git workflow

- One branch per task (`feat/habitaciones`, `feat/dashboard`, …). Never commit directly to `main`; changes go through a Pull Request reviewed by another teammate (Dorian ↔ Yojan, Denisse ↔ Ashley).
- Small, frequent commits: the commit history is evidence of equal participation.
- The remote is `origin` → https://github.com/AshleyAvilaV/pagina_web_hotel (branch `main`). Don't commit, push or open PRs unless the user asks.

## Academic integrity

Plagiarised projects are disqualified automatically. Use images with a free licence and record their source in `README.md`; don't copy full hotel templates. AdminLTE and the course libraries are fine to use.

## Working with the team

- Ownership follows section 2 of the plan: Dorian — login and dashboard; Denisse — home and services; Ashley — rooms and location; Yojan — booking/contact form, JS validations, AJAX and PHP. Keep the work evenly shared and don't build a teammate's page without checking first.
- Reply in the language the user writes in.
