# Module 2 — Frontend Development — Submission

Digital Nurture 5.0, Python Full Stack Engineer Track. All 10 hands-on exercises
build one running project — a **Student Portal** — progressively across HTML/CSS,
JavaScript, React, Angular, and Vue.js.

## Folder map

| Hands-On | Topic | Folder |
|---|---|---|
| 1 | HTML5 semantic structure & CSS3 foundations | `handson_01/` |
| 2 | Flexbox, Grid & responsive design | `handson_02/` |
| 3 | JavaScript ES6+ & DOM manipulation | `handson_03/` |
| 4 | Async JS, Fetch API & Axios | `handson_04/` |
| 5 | React fundamentals (components, props, state, hooks) | `student-portal-react/` |
| 6 | React Router, Context API & Redux Toolkit | `student-portal-react/` (same project, extended) |
| 7 | Angular — components, services, DI, routing, forms | `student-portal-angular/` |
| 8 | Vue.js — Composition API, Vue Router & Pinia | `student-portal-vue/` |
| 9 | Accessibility & cross-browser compatibility | `handson_09/` (audits the Hands-On 1–3 HTML/CSS/JS portal) |
| 10 | Centralised API layer & advanced Redux (framework chosen: **React**) | `student-portal-react/` (same project, extended) |

Hands-On 5, 6, and 10 share a single `student-portal-react/` project because they are
designed to build on each other (per the exercise book's "single running project" note).
Each hands-on's specific screenshots are still separated inside
`student-portal-react/screenshots/` with a `handson5_`, `handson6_`, or `handson10_`
filename prefix.

## Running each part

- **Hands-On 1–4, 9** (plain HTML/CSS/JS): open `index.html` directly in a browser, or
  serve the folder with any static server (e.g. `python -m http.server`) since Hands-On
  3, 4, and 9 use ES modules (`<script type="module">`), which some browsers block on
  `file://` — a local server avoids that.
- **student-portal-react/**: `npm install && npm run dev` → http://localhost:5173
- **student-portal-angular/**: `npm install && npx ng serve` → http://localhost:4200
- **student-portal-vue/**: `npm install && npm run dev` → http://localhost:5174 (or
  whatever port Vite prints)

`node_modules/` is excluded from this submission per the exercise book's guidelines —
reinstall with `npm install` in each framework folder before running.

## Screenshots

Every folder has its own `screenshots/` subfolder with numbered PNGs (and a couple of
`.txt`/`.md` evidence files for console output, W3C/Lighthouse results, and the
accessibility/cross-browser report) captured at each task's "Expected Outcome"
checkpoint.
