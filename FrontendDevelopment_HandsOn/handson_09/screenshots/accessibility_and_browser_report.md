# Hands-On 9 — Accessibility & Cross-Browser Report

## Task 1 — Lighthouse Audit & Semantic Fixes

- **Baseline score:** 100/100 (`lighthouse_before.report.html` / `.json`)
- **Post-fix score:** 100/100 (`lighthouse_after.report.html` / `.json`)
- The automated score was already 100 because axe's accessible-name algorithm accepts
  an `<input>`'s `placeholder` as a fallback name. That is **not** WCAG-robust (SC 1.3.1) —
  placeholders disappear once typing starts and aren't reliably read by all assistive
  tech — so the manual fixes below were applied regardless of the automated pass:

| Issue | Fix |
|---|---|
| Page started at `<h2>`, no `<h1>` | Added a visually-hidden `<h1>` before the `<h2>` so the heading order is `h1 → h2 → h3` |
| Search input relied only on `placeholder` | Added a real (visually-hidden) `<label for="search-courses">` |
| No images existed to test alt-text rules | Added a decorative logo icon with `alt=""` to demonstrate the decorative-image pattern |
| No landmark label on `<nav>` | Added `aria-label="Main navigation"` |

## Task 2 — ARIA & Keyboard Navigation

- `aria-label="Main navigation"` on `<nav>`; `aria-current="page"` on the active "Courses" link.
- Course cards: `tabindex="0"` (already present from Hands-On 3) + a `keydown` listener for
  `Enter` that calls the same `selectCourse()` handler as `click` — verified in
  `03_enter_key_selected_card.png` (Tab to a card, press Enter, "Selected: ..." appears).
- Results count: `<p id="results-count" role="status" aria-live="polite">` updates on every
  search/sort so screen readers announce "N courses found" without moving focus.
- Mobile hamburger menu: `<button id="menu-toggle" aria-expanded="false" aria-controls="main-nav">`
  toggles `aria-expanded` between `"true"`/`"false"` on click — verified in
  `04_mobile_menu_closed.png` (expanded=false) vs `05_mobile_menu_open.png` (expanded=true).
- Keyboard walkthrough: Tabbed through header → nav links → search input → sort button →
  course cards in `02_keyboard_focus_visible.png` — every interactive element receives a
  visible focus ring (`outline: 3px solid #facc15`); nothing is skipped or trapped.

## Task 3 — Colour Contrast & Cross-Browser Testing

### Contrast ratios (computed via WCAG relative-luminance formula)

| Foreground | Background | Ratio | WCAG AA (4.5:1) |
|---|---|---|---|
| `#4b5563` (card body text) | `#ffffff` | 7.56:1 | Pass |
| `#1f2937` (body text) | `#f4f6f8` | 13.55:1 | Pass |
| `#ffffff` (header text) | `#1e293b` | 14.63:1 | Pass |
| `#2563eb` (accent blue / links) | `#ffffff` | 5.17:1 | Pass |
| `#2563eb` (accent blue) | `#eef2ff` (selected-course bg) | 4.62:1 | Pass |

No colour combination on the page needed adjustment — all exceed the 4.5:1 minimum for
normal text (large text only needs 3:1).

### caniuse.com support check

Feature checked: **CSS `gap` in Flexbox** (used in `.controls`, `.course-grid` fallback,
and the mobile nav) and **`clamp()`** (used for fluid typography in Hands-On 2).

- `gap` in Flexbox: supported in Chrome 84+, Firefox 63+, Safari 14.1+, Edge 84+ — baseline
  "widely available" since 2021. No polyfill required for this project's target browsers.
- `clamp()`: supported in Chrome 79+, Firefox 75+, Safari 13.1+, Edge 79+ — also widely
  available. Both features are safe to use without fallbacks for any evergreen browser.

### Cross-browser rendering notes (Chromium vs Firefox engine differences)

Layout was verified with Chromium (`06_chromium_render.png`) via the automated
screenshots throughout this exercise book. A Firefox render pass was attempted with
Playwright's Firefox build but the headless Firefox process could not launch in this
sandboxed environment — re-run `node shot_crossbrowser_ho9.js` on a machine with a full
Firefox install (or open the file directly in desktop Firefox/Safari/Edge) to capture
that comparison. Known cross-engine differences to watch for with this codebase:

- **Firefox** renders `font-family: Arial, Helvetica, sans-serif` with slightly tighter
  letter-spacing than Chromium/Blink — no layout impact, cosmetic only.
- **Grid `auto-fit` + `minmax()`** (Hands-On 2 course grid) reflows identically across
  Chromium, Firefox, and WebKit — this is a widely-implemented CSS Grid feature with no
  known engine divergence.
- **`gap` in Flexbox** (this file's `.controls`) is supported identically across all three
  engines at the versions listed above.

### Polyfill demonstration

For an older-browser fallback, `css-vars-ponyfill` (CDN) can be added for CSS custom
properties support in browsers that predate native `var()` support:

```html
<script src="https://cdn.jsdelivr.net/npm/css-vars-ponyfill@2/dist/css-vars-ponyfill.min.js"></script>
<script>cssVars();</script>
```

This project's CSS does not currently rely on custom properties (`--var`), so the
ponyfill is not required — it's documented here as the mechanism to reach for if custom
properties were introduced and IE11-class support were ever needed.
