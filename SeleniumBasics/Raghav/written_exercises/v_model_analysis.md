# Hands-On 2 — SDLC vs TDLC: V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 9. The V-Model

```
Requirements               Acceptance Testing
      \                           /
       \                         /
    System Design          System Testing
         \                     /
          \                   /
     Architecture Design  Integration Testing
              \               /
               \             /
          Module Design   Unit Testing
                    \         /
                     \       /
                      Coding
                    (bottom vertex)
```

The left side (development, descending) mirrors the right side (testing, ascending) — each development phase has a matching test phase that validates the decisions made at that level.

### 10. SDLC ↔ TDLC phase pairs and test artifacts produced

| SDLC Phase | TDLC Phase | Test Artifact Produced During Dev Phase |
|---|---|---|
| Requirements | Acceptance Testing | **Acceptance Test plan** — e.g., "Admin can create/update/delete courses" scenarios, drafted from the requirements doc for the Course Management API. |
| System Design | System Testing | **System Test plan** — end-to-end scenarios covering the API + DB + any frontend, derived from the high-level architecture diagram. |
| Architecture Design | Integration Testing | **Integration Test plan** — which component pairs need testing together, e.g., `courses_bp` routes + SQLAlchemy models, or Course Management API + a future Student Portal frontend. |
| Module Design | Unit Testing | **Unit Test plan / test case matrix** — one entry per function, e.g., `create_course()`, `Course.to_dict()`, derived from each module's design spec. |
| Coding | (bottom vertex — code is written, then both directions converge) | The implementation itself, plus **unit tests written alongside** the code (TDD-style). |

### 11. Entry & Exit criteria per TDLC phase

**Unit Testing**
- *Entry:* Module code compiles/runs; unit test cases are written against the module design spec (e.g., for `Course.to_dict()`).
- *Exit:* All unit tests pass; code coverage meets the agreed threshold (e.g., 80%); no known critical logic errors in the module.

**Integration Testing**
- *Entry:* All required unit tests pass; the components to be integrated (e.g., `courses_bp` + `extensions.db`) are individually stable and deployed to a test environment.
- *Exit:* All integration test cases pass; interfaces between components (route → ORM → DB) behave per the architecture spec; no open critical/high defects on component interaction.

**System Testing**
- *Entry:* Integration testing is complete and signed off; the full application (API + DB) is deployed to a system-test environment resembling production.
- *Exit:* All system test cases (full request→response→DB round trips) pass; non-functional criteria (performance, security basics) are met; defect count is below the release threshold.

**Acceptance Testing (UAT)**
- *Entry:* System testing is complete and exit criteria met; a UAT environment with realistic data is available; UAT test cases derived from requirements are ready.
- *Exit:* The college admin (or their representative) signs off that the Course Management workflows meet their real-world needs; no open critical/high defects; stakeholder formal approval to release.

### 12. Two early QA engagement points (not just testing phases)

1. **Requirements review** — QA reviews the Course Management API requirements doc *before* any design or coding starts, flagging ambiguities such as "what happens when a course code is duplicated?" or "is `credits` required to be a positive integer?" This is far cheaper to fix on paper than after `POST /api/courses/` ships without that validation.
2. **Architecture/Module design review** — QA reviews the proposed schema (`Department`/`Course`/`Student`/`Enrollment` and their foreign keys/unique constraints) to identify testability gaps early, e.g., noticing the `Course.code` unique constraint has no corresponding error-handling path in `create_course()`, before a single line of the route handler is written.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three problems with Waterfall testing-after-development (Course Management API)

1. **Defects are found late and are expensive to fix.** If the missing-`IntegrityError`-handling bug on duplicate course codes is only found during system testing (after the whole app is "done"), fixing it means re-opening code that was considered finished, re-running full regression, and delaying the release — versus catching it in a design review.
2. **Requirements ambiguity compounds.** If nobody testable-reviews "credits" and "department_id" constraints upfront, developers make silent assumptions (e.g., `credits` can be negative) that only surface as bugs once QA finally gets the finished API — by which point the DB schema and dozens of dependent tests may need rework.
3. **No early feedback loop for the team.** Waterfall testing-after-development means the admin/registrar (real users) don't see or use the Course Management workflows until the very end — if the UX is wrong (e.g., "students" endpoint returns raw IDs instead of names), that's discovered too late to cheaply redesign.

### 14. QA's role in Agile ceremonies

- **Sprint Planning** — QA helps define testable **acceptance criteria** for each story (e.g., for "Add course creation endpoint," QA clarifies: valid input → 201, missing field → 400, duplicate code → 409) *before* estimation, so testability is baked into the story's definition of done.
- **Daily Standup** — QA reports **blocking issues**: environments down, a flaky test blocking the pipeline, or a defect blocking further testing of a story (e.g., "can't test enrollment because course creation 500s").
- **Sprint Review** — QA supports **demo testing**: verifying the demoed features actually work as claimed in front of stakeholders, and flags anything not production-ready before it's shown as "done."
- **Retrospective** — QA contributes to **process improvement**: e.g., proposing that flaky Selenium tests be quarantined, or that a recurring class of bugs (missing input validation) become a mandatory code-review checklist item.

### 15. Four Shift-Left practices applied to the Course Management API

(a) **Reviewing requirements for testability** — Before coding `POST /api/courses/`, QA asks "what's the expected status code and body for a duplicate `code`?" This forces the team to define behavior (409 + error message) instead of discovering an unhandled 500 later.

(b) **Writing test cases before code (TDD/BDD)** — Write `test_create_course_missing_field_returns_400()` *before* implementing the required-field check in `create_course()`; the test drives the implementation and guarantees the check exists.

(c) **Static code analysis** — Run a linter/type checker (e.g., ruff, mypy/ty) on `courses/routes.py` and `courses/models.py` on every commit to catch issues like an unguarded `db.session.commit()` without exception handling, before the code ever reaches a test environment.

(d) **API contract testing before integration** — Define the `/api/courses/` request/response schema (e.g., via an OpenAPI spec) and validate the route handler against it automatically, so a future frontend team can build against a stable, agreed contract instead of discovering mismatches during integration.

### 16. Acceptance Criteria — Given-When-Then

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

```gherkin
Scenario: Happy path — course created successfully
  Given I am an authenticated college admin
  And no course with code "CS401" exists
  When I submit a POST request to /api/courses/ with
    | name    | Machine Learning |
    | code    | CS401            |
    | credits | 4                |
    | department_id | 1          |
  Then the response status should be 201
  And the response body should contain the created course with code "CS401"
  And a new row should exist in the courses table with code "CS401"

Scenario: Duplicate course code
  Given a course with code "CS401" already exists
  When I submit a POST request to /api/courses/ with code "CS401" and otherwise valid data
  Then the response status should be 409
  And the response body should contain an error message indicating the course code already exists
  And no duplicate row should be created in the courses table

Scenario: Missing required fields
  Given I am an authenticated college admin
  When I submit a POST request to /api/courses/ with body { "name": "Machine Learning" }
  Then the response status should be 400
  And the response body should contain an error message naming the first missing required field
  And no row should be created in the courses table
```
