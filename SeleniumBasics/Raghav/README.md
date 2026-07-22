# SeleniumBasics — Raghav

Submission for the Digital Nurture 5.0 "QA Concepts & Selenium Basics" hands-on exercise book (7 exercises). Target application for all coding exercises: [LambdaTest Selenium Playground](https://www.lambdatest.com/selenium-playground/) (now redirects to `testmuai.com` — LambdaTest rebranded to TestMu AI; the `/selenium-playground/` pages and their markup are unchanged, only the domain differs).

Course Management API referenced throughout Hands-On 1–3 is the Flask project at `d:\Cognizant\Python(Django)\flask_coursemanager`.

## Structure

```
SeleniumBasics/Raghav/
├── requirements.txt              # pip-installable deps (per submission guidelines)
├── pyproject.toml / uv.lock       # actual project env, managed with uv (uv run ...)
├── written_exercises/
│   ├── qa_concepts.md            # Hands-On 1
│   ├── v_model_analysis.md       # Hands-On 2
│   └── automation_strategy.md    # Hands-On 3
└── automation_scripts/
    ├── hands_on_4/                # WebDriver setup, navigation, windows, screenshots
    │   ├── setup_test.py          #   (also holds the shared build_driver/open_page helpers)
    │   └── navigation_test.py
    ├── hands_on_5/                # Locators (all 6 strategies) + explicit/fluent waits
    │   ├── locators_test.py
    │   └── waits_test.py
    ├── hands_on_6/                # pytest: fixtures, parametrize, HTML report, screenshot-on-failure
    │   ├── conftest.py
    │   └── test_playground.py
    └── hands_on_7/                # Page Object Model refactor of Hands-On 6
        ├── pages/
        │   ├── base_page.py
        │   ├── simple_form_page.py
        │   ├── checkbox_page.py
        │   ├── dropdown_page.py
        │   └── input_form_page.py
        └── tests/
            ├── conftest.py
            └── test_playground.py
```

## Outcome screenshots

[`outcome_screenshots/`](outcome_screenshots/) contains 8 real screenshots captured by re-running the automation against the live Playground, as visual evidence each hands-on's automation actually works end to end (not just "tests passed" in a terminal):

| # | File | Shows |
|---|---|---|
| 1 | `01_handson4_playground_homepage_loaded.png` | Hands-On 4 — Playground loaded via WebDriver setup |
| 2 | `02_handson4_second_tab_google_opened.png` | Hands-On 4 — second tab opened and switched to |
| 3 | `03_handson5_locators_message_input_filled.png` | Hands-On 5 — message input located and filled |
| 4 | `04_handson5_explicit_wait_alert_visible.png` | Hands-On 5 — Bootstrap alert surfaced via `WebDriverWait` |
| 5 | `05_handson6_pytest_simple_form_result.png` | Hands-On 6 — simple form message echoed back |
| 6 | `06_handson6_pytest_checkbox_checked.png` | Hands-On 6 — checkbox checked state |
| 7 | `07_handson7_pom_dropdown_wednesday_selected.png` | Hands-On 7 (POM) — dropdown selection |
| 8 | `08_handson7_pom_input_form_success.png` | Hands-On 7 (POM) — input form success message |

## Setup

```bash
uv sync                      # installs selenium, pytest, webdriver-manager, pytest-html
# or, without uv:
pip install -r requirements.txt
```

Requires Google Chrome installed locally; `webdriver-manager` auto-downloads the matching ChromeDriver on first run.

## Running

```bash
# Hands-On 4
uv run python automation_scripts/hands_on_4/setup_test.py
uv run python automation_scripts/hands_on_4/navigation_test.py

# Hands-On 5
uv run python automation_scripts/hands_on_5/locators_test.py
uv run python automation_scripts/hands_on_5/waits_test.py

# Hands-On 6 (pytest suite, flat driver calls)
uv run pytest automation_scripts/hands_on_6/ -v --html=automation_scripts/hands_on_6/report.html --self-contained-html

# Hands-On 7 (POM-refactored suite)
uv run pytest automation_scripts/hands_on_7/tests/ -v --html=automation_scripts/hands_on_7/report.html --self-contained-html
```

All scripts run headless by default and have been executed end-to-end against the live site as part of building this submission — every listed test passes.

## Notable deviations from the task sheet (and why)

The task sheet was written against an earlier version of the Playground; a few real-DOM details differ from what the steps assume. Each is called out in a comment at its exact location in code, but summarized here:

- **LambdaTest → TestMu AI rebrand.** `lambdatest.com/selenium-playground/` 302-redirects to `testmuai.com/selenium-playground/`. Scripts still `.get()` the original PDF URL; Selenium follows the redirect transparently.
- **Simple Form Demo message input has no `name` attribute.** `By.NAME` is demonstrated on the Checkbox Demo's `input[name='option1']` instead (Hands-On 5, `locators_test.py`).
- **`By.TAG_NAME` on `<input>` does not resolve to the message box** — it resolves to an unrelated hidden marketing-widget field that happens to be the first `<input>` in the DOM. Kept in the script and called out explicitly, since it's a real, useful lesson about why bare tag-name locators are unreliable.
- **Checkbox Demo has 8 "Option N" labels, not 4** — two separate checkbox widgets on the same page both use that label text.
- **Bootstrap Alerts success text reads "…success message…", not "…successfully…"** — assertions match the live copy.
- **The Playground is a JS-hydrated (Next.js) app** — clicking a button immediately after `driver.get()` can race the page's own click-handler attachment and silently no-op. Fixed once, centrally, via `open_page()` / `BasePage.navigate_to()`, which waits for `document.readyState == 'complete'` before returning control to the test.
- **Input Form Submit has no phone field and requires 11 fields (not 4) before it will submit successfully** — `InputFormPage.fill_form()` keeps the 4 task-relevant parameters (`name`, `email`, `password`, `address`) and fills the remaining required-but-untested fields with fixed defaults internally.
