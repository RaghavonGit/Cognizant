# Hands-On 3 — Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### 17. Five criteria for deciding whether a test case should be automated

Applied to: *"Test that `POST /api/courses/` returns 201 with the correct course data when valid input is provided."*

1. **Repeatability** — Will this test run many times (every commit, every regression cycle)? Yes — course creation is core CRUD functionality exercised on every build. → Automate.
2. **Stability of the feature** — Is the feature's behavior/UI settled, not actively churning? The `POST /api/courses/` contract (required fields, response shape) is stable. → Automate.
3. **Determinism** — Does the test produce the same result every run given the same input, with no reliance on human judgement? A JSON status/body assertion is fully deterministic. → Automate.
4. **Cost of manual execution vs automation** — Manual execution means opening Postman and checking a response by eye every time; automation lets this run in seconds as part of CI with zero human time after the initial investment. → Automate.
5. **Risk/criticality of the feature** — Course creation is a critical path (nothing downstream — enrollment, scheduling — works without it). High-risk-if-broken features are prioritized for automation. → Automate.

All five criteria point the same direction here — this is a textbook case for automation (it's why Hands-On 4-7 in this exercise book target exactly this kind of scenario, just against the Playground instead of this API).

### 18. Automate or Manual — Course Management API test cases

| # | Test Case | Decision | Justification |
|---|---|---|---|
| a | Regression test for all CRUD endpoints after every code change | **Automate** | Repetitive, runs on every change, deterministic pass/fail — the single best automation candidate. |
| b | Exploratory testing of a new search feature | **Manual** | Exploratory testing is inherently unscripted human investigation looking for the unexpected; automating it defeats the purpose. |
| c | Performance test: 100 concurrent users calling `GET /api/courses/` | **Automate** (with a dedicated tool, e.g., Locust/JMeter, not Selenium) | Impossible to generate reliable concurrent load manually; needs to run repeatedly across builds to catch regressions. |
| d | UI test for the login form | **Automate** | Stable, repetitive, high-value regression coverage — canonical Selenium use case. |
| e | Verify the API documentation (Swagger) is accurate | **Manual** (or a lightweight automated schema-diff check, but human judgement is needed to assess "accurate") | Judging whether prose/descriptions are accurate and clear requires human review; automation can only check schema shape, not clarity. |
| f | Smoke test: verify the API is reachable after deployment | **Automate** | Must run on every single deployment, fast, deterministic — a perfect low-effort automation candidate (and a CI/CD gate). |

### 19. Test Automation ROI

**Definition:** Test automation ROI measures whether the upfront (and ongoing maintenance) cost of automating a test is recovered by the time saved over its repeated manual executions — i.e., automation "pays for itself" once cumulative time saved exceeds the time invested in building and maintaining it.

**Given:**
- Automation build cost: 4 hours = 240 minutes
- Manual execution cost: 30 minutes/run
- Maintenance overhead: 20% of automated-run time, applied *after* the 10th run

**Calculation (break-even = cumulative automated cost < cumulative manual cost):**

Assume each automated run itself takes ~1 minute of machine time (negligible vs. the 30-minute manual run) — the real cost being compared is the 240-minute build investment against manual runs saved.

- After **n** runs without maintenance overhead: automation saves `30n − 240` minutes (ignoring negligible automated execution time).
- Break-even (before maintenance kicks in): `30n = 240` → `n = 8` runs.
- Since maintenance overhead only applies **after the 10th run**, runs 1–10 accrue savings at the full 30 min/run rate with no penalty. By run 8, cumulative savings already reach `30×8 = 240` minutes — matching the 240-minute build cost.

**→ Automation pays for itself after the 8th run**, comfortably before the 20% maintenance overhead even begins (which only applies from run 11 onward). From run 11 onward, add 20% overhead per run — e.g., treat each subsequent run as effectively costing `0.2 × 30 = 6` minutes of upkeep, still far cheaper than the 30-minute manual alternative, so automation remains net-positive indefinitely for a test that runs regularly.

### 20. Flaky tests

**Definition:** A flaky test is a test that produces inconsistent results (sometimes pass, sometimes fail) *without any change to the code under test* — the failure is caused by the test's own instability, not a real regression.

**Example:** `test_dropdown_selection` sometimes fails with `NoSuchElementException` because the script tries to interact with the `<select>` element before the LambdaTest Playground page has fully finished rendering — it's a timing issue, not an actual bug in dropdown selection.

**Three strategies to prevent/fix flaky tests:**

1. **Replace `time.sleep()` and implicit waits with explicit `WebDriverWait` + `ExpectedConditions`** — wait for the actual condition (element visible/clickable) instead of a fixed guess at timing (see Hands-On 5).
2. **Isolate test state** — use `scope='function'` fixtures so each test gets a fresh browser/session instead of sharing state across tests, eliminating order-dependent failures.
3. **Quarantine and retry-with-investigation, not blind retry** — when a flaky test is identified, tag it and investigate the root cause (race condition, animation, network latency) rather than papering over it with automatic retries, which hide real instability and erode trust in the suite.

---

## Task 2: Compare Automation Framework Types

### 21. The five framework types

**Linear (Record & Playback)**
- *Description:* Tests are recorded/written as flat, standalone scripts with no reusable functions — each script does everything from opening the browser to asserting results in one sequence.
- *Advantage:* Fastest to create — no design overhead, good for one-off exploratory scripts.
- *Disadvantage:* Zero reuse — the same "open browser and log in" code is duplicated in every script, so a UI change means fixing dozens of files.
- *Example use:* A one-time smoke check that `GET /api/courses/` doesn't 500 after a hotfix deploy — write it, run it once, throw it away.

**Modular**
- *Description:* Breaks the application into logical modules (login, course-creation, enrollment) with reusable functions per module that tests call into, reducing duplication.
- *Advantage:* Reusable functions mean a UI/API change is fixed in one place instead of many scripts.
- *Disadvantage:* Still requires programming skill to write/maintain; test data is often still hardcoded inside the functions.
- *Example use:* A `create_course_via_api(name, code, credits, dept_id)` helper reused across "create course," "duplicate course," and "enrollment" test modules.

**Data-Driven**
- *Description:* Separates test logic from test data — the same test script runs repeatedly against different input sets pulled from a CSV/JSON/Excel file or parametrize decorator.
- *Advantage:* One script covers many input combinations (valid, missing field, duplicate code, boundary credits) without duplicating test code.
- *Disadvantage:* Doesn't solve UI-locator duplication by itself — usually needs to be combined with Modular for full reuse.
- *Example use:* One `test_create_course(payload, expected_status)` test parametrized with 10 rows covering every field-validation edge case for `POST /api/courses/`.

**Keyword-Driven**
- *Description:* Test steps are expressed as keywords (e.g., `OpenBrowser`, `EnterCourseName`, `ClickSubmit`) in a table/spreadsheet, interpreted by an underlying engine — largely decoupling "what to test" from code.
- *Advantage:* Non-technical team members (e.g., a QA analyst who knows the domain but not Python) can write and read test cases.
- *Disadvantage:* Significant upfront investment to build the keyword engine/library; can obscure what's actually happening under the hood, complicating debugging.
- *Example use:* A QA analyst defines a new course-creation test as a row of keywords (`NavigateTo | CourseForm`, `EnterField | code | CS999`, `ClickButton | Submit`) without touching Python.

**Hybrid**
- *Description:* Combines Modular's reusable functions, Data-Driven's external parameterisation, and optionally Keyword-Driven's abstraction — the pragmatic, most commonly used real-world approach.
- *Advantage:* Gets the benefits of all three (reuse + data coverage + accessibility) without over-committing to any single rigid structure.
- *Disadvantage:* More design upfront — deciding what goes in page objects vs. data files vs. test files requires discipline, or the codebase drifts back toward Linear chaos.
- *Example use:* The POM-based suite built in Hands-On 7 — `pages/` = Modular reuse, `@pytest.mark.parametrize` = Data-Driven coverage, readable `page.enter_message(...)` calls = keyword-like clarity for less technical reviewers.

### 22. Recommended framework for the Course Management frontend Selenium suite

**Requirements:** login with 50 user/password combos, reuse login steps across 20 test cases, support both technical and non-technical contributors.

**Recommendation: Hybrid (Modular + Data-Driven), with light Keyword-Driven elements.**

- **Modular** gives a `LoginPage` class with `login(username, password)` reused across all 20 dependent test cases — one place to fix if the login form changes.
- **Data-Driven** (`@pytest.mark.parametrize` over a CSV/JSON of the 50 credential pairs) covers all combinations without writing 50 near-identical test functions.
- A thin **Keyword-Driven** layer (well-named, English-readable Page Object methods like `page.login_with_invalid_password()`) lets non-technical team members read and reason about test intent even if they can't write the underlying Python, and — with a small additional layer — could contribute new data rows (new credential pairs) without touching code at all.

Pure Linear would duplicate the login flow 20 times; pure Keyword-Driven alone is overkill engineering effort for a team that already has developers who can write Python. Hybrid is the standard real-world answer, and it's exactly the structure Hands-On 6–7 build.

### 23. Hybrid framework folder structure — Course Management frontend tests

```
course_management_tests/
├── conftest.py                  # shared fixtures: driver, base_url, login helper
├── pytest.ini / pyproject.toml  # pytest configuration
├── requirements.txt             # selenium, pytest, webdriver-manager, pytest-html
├── config/
│   └── settings.py              # environment URLs, timeouts, browser choice
├── data/
│   ├── login_credentials.csv    # 50 user/password rows for data-driven login tests
│   └── course_payloads.json     # valid/invalid course-creation payloads
├── pages/                       # Page Object files — locators + actions, no asserts
│   ├── base_page.py
│   ├── login_page.py
│   ├── course_form_page.py
│   └── course_list_page.py
├── utils/                       # shared helpers
│   ├── wait_helpers.py          # wrapper functions around WebDriverWait
│   └── data_loader.py           # reads CSV/JSON into parametrize-ready lists
├── tests/                       # test files — assertions only, call into pages/
│   ├── test_login.py
│   ├── test_course_creation.py
│   └── test_course_list.py
└── reports/
    └── report.html              # pytest-html output (gitignored, generated per run)
```

- `data/` holds the Data-Driven parameterisation source.
- `pages/` holds the Modular, reusable interaction layer (also where Keyword-Driven-style readable method names live).
- `utils/` holds cross-cutting helpers (waits, data loading) shared by every test.
- `tests/` stays thin — pure `page.method()` calls plus `assert` statements, per the POM golden rule from Hands-On 7.
