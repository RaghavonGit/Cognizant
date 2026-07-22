# Hands-On 1 — QA Concepts, Functional Testing & Defect Lifecycle

System under test: **Course Management API** (Flask + SQLAlchemy, blueprint `courses_bp`, base path `/api/courses/`). Models: `Department`, `Course`, `Student`, `Enrollment`. Endpoints: `GET /`, `POST /`, `GET /<id>/`, `PUT /<id>/`, `DELETE /<id>/`, `GET /<id>/students/`.

## Task 1: Map Testing Types to a Real System

### 1. One test case per test level

**Unit Testing** — test a single function in isolation.
- Test: `Course.to_dict()` returns a dict with keys `id, name, code, credits, department_id` and that `credits` is serialized as an `int`, not a string.
- No Flask app, no DB required — construct a `Course` object in memory and assert on the returned dict.

**Integration Testing** — test two components working together (API endpoint + database).
- Test: Calling `create_course()` with a valid payload actually persists a row via SQLAlchemy — after the call, `Course.query.filter_by(code='CS101').first()` returns a row matching the request payload.
- This exercises the route handler *and* the ORM/DB layer together, but not the HTTP stack.

**System Testing** — full end-to-end flow from API request to database response.
- Test: Send a real HTTP `POST /api/courses/` request (via `requests` or Flask test client) with `{"name": "Data Structures", "code": "CS201", "credits": 4, "department_id": 1}`, assert `201` status and JSON body `{"status": "success", "data": {...}}`, then send `GET /api/courses/<id>/` and confirm the same values come back.
- This exercises routing, request parsing, validation, DB commit, and serialization together — the whole stack.

**User Acceptance Testing (UAT)** — from the perspective of an actual college admin.
- Test: A college admin uses the admin UI (or Postman collection) to add "Advanced Databases" under the Computer Science department, then confirms the course appears in the course list students see when enrolling. Success is judged against the admin's real workflow, not internal correctness.

### 2. Functional vs Non-Functional classification

| Test case | Classification |
|---|---|
| Unit: `to_dict()` shape | Functional |
| Integration: `create_course()` persists row | Functional |
| System: POST → GET round trip | Functional |
| UAT: admin adds a course | Functional |

**Non-functional example:** Performance test — `POST /api/courses/` must respond in under 300ms at p95 under 50 concurrent requests. This doesn't ask "does it create the course correctly?" (functional) but "does it do so fast enough under load?" (non-functional).

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing** — the tester has no knowledge of the internal code; they only know the documented inputs and outputs (e.g., "POST valid JSON to `/api/courses/`, expect 201"). They cannot see that `create_course()` checks `required = ['name', 'code', 'credits', 'department_id']` — they discover missing-field behavior only by probing it.
- **White-Box Testing** — the tester (usually the developer) has full visibility into `routes.py` and writes tests that specifically target each `if field not in data` branch, the `get_or_404` 404 path, and the `IntegrityError` that would fire from the `UniqueConstraint` on `code`.
- A **QA tester** typically performs black-box testing (validates behavior against requirements/spec). A **developer** typically performs white-box testing (unit tests written with knowledge of branches and edge cases in their own code).

### 4. Three formal test cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-COURSE-001 | Create course with valid data returns 201 | Department with `id=1` exists in DB | 1. Send `POST /api/courses/` with body `{"name":"Operating Systems","code":"CS301","credits":4,"department_id":1}`<br>2. Inspect response | Status `201`; JSON `status="success"`; `data.code == "CS301"`; a row exists in `courses` table with this code | | |
| TC-COURSE-002 | Create course missing required field returns 400 | None | 1. Send `POST /api/courses/` with body `{"name":"Operating Systems","credits":4,"department_id":1}` (no `code`)<br>2. Inspect response | Status `400`; JSON `{"error": "Missing field: code"}`; no row inserted | | |
| TC-COURSE-003 | Create course with duplicate course code returns error | A course with `code="CS301"` already exists | 1. Send `POST /api/courses/` with body `{"name":"OS Redux","code":"CS301","credits":3,"department_id":1}`<br>2. Inspect response | Request fails due to the `unique=True` constraint on `Course.code` (currently surfaces as an unhandled `IntegrityError` → 500; **should** be a `409 Conflict` with a clear message — flagged as a defect, see Hands-On 1 Task 2 note) | | |

> Note: TC-COURSE-003 doubles as evidence for a real defect — `create_course()` does not catch `IntegrityError` from the unique constraint on `code`, so a duplicate code currently produces an unhandled 500 instead of a clean 409/400. This is exactly the kind of bug black-box system testing surfaces.

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
                    │
                    ├──> Rejected   (not reproducible / not a bug / working as intended)
                    └──> Deferred   (valid bug, fix postponed to a later release)
```

- **New** — QA logs the defect (e.g., "duplicate course code causes 500").
- **Assigned** — Lead/triager assigns it to a developer.
- **Open** — Developer accepts and starts investigating/fixing.
- **Fixed** — Developer commits a fix (e.g., catches `IntegrityError`, returns 409) and moves it to Retest.
- **Retest** — QA re-runs the original failing test case (TC-COURSE-003) against the fix.
- **Verified** — QA confirms the fix resolves the issue with no regression.
- **Closed** — Defect is closed out, tracked in the release notes.
- **Rejected path** — if the developer/triager determines the reported behavior is correct, not reproducible, or a duplicate report, it moves straight to Rejected instead of Assigned/Open.
- **Deferred path** — if the bug is real but low-impact and fixing it now isn't worth delaying the release (e.g., a typo in Swagger docs), it's marked Deferred and revisited in a future sprint/release.

### 6. Severity & Priority classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) `POST /api/courses/` returns 500 for **all** requests | **Critical** | **P1** | Core create-course functionality is completely broken for every user — total feature outage, blocks all downstream workflows (enrollment depends on courses existing). |
| (b) Course names >150 chars silently truncated, no error | **Medium** | **P3** | Data is corrupted but the app doesn't crash and most real course names are well under 150 chars — low likelihood, moderate impact when it does happen, no user-facing error to trigger urgency. |
| (c) Typo in `/docs` Swagger description | **Low** | **P4** | Purely cosmetic, no functional impact, doesn't block any workflow. Fix whenever convenient. |
| (d) Login intermittently returns 401 with correct credentials | **High** | **P1** | Intermittent auth failures are hard to reproduce and erode trust in the whole system; even though it "sometimes works," an unreliable login gate is a severe and urgent problem — every intermittent failure is a real user locked out. |

### 7. Defect report — bug (a)

- **Defect ID:** DEF-2026-0142
- **Title:** `POST /api/courses/` returns 500 Internal Server Error for all requests
- **Environment:** Staging, Python 3.12, Flask 3.x, SQLite (`instance/coursemanager.db`)
- **Build Version:** course-management-api v0.3.1
- **Severity:** Critical
- **Priority:** P1
- **Steps to Reproduce:**
  1. Start the API (`python app.py`) against a fresh DB.
  2. Send `POST /api/courses/` with a valid JSON body: `{"name": "Databases", "code": "CS210", "credits": 3, "department_id": 1}`.
  3. Observe the response.
- **Expected Result:** `201 Created` with `{"status": "success", "data": {"id": ..., "name": "Databases", "code": "CS210", "credits": 3, "department_id": 1}}`.
- **Actual Result:** `500 Internal Server Error`, body `{"error": "Internal server error"}` for every request regardless of payload validity.
- **Attachments:** screenshot of 500 error

### 8. Severity vs Priority

- **Severity** measures the *technical impact* of the defect on the system — how badly it breaks functionality, regardless of who notices it.
- **Priority** measures *business urgency* — how soon it needs to be fixed, based on who is affected and how visible it is.
- **Example where High Severity ≠ High Priority:** if the Course Management API's bulk CSV-import feature (used once a year by one registrar) crashes with a 500, that's High Severity (a feature is completely broken) but Low/Medium Priority (almost nobody hits it and it's not needed until next year's import). Conversely, a cosmetic misalignment on the CEO's dashboard is Low Severity (nothing is broken) but can be High Priority (visible to leadership, needs fixing before the next demo).
