# Student Portal — React

Built across Hands-On 5, 6, and 10 of the Digital Nurture 5.0 Frontend Development
exercise book. Vite + React, React Router, Redux Toolkit (with `createAsyncThunk`), a
centralised Axios API layer, and a top-level Error Boundary.

## Running

```
npm install
npm run dev
```

## State management comparison — React+Redux vs Angular+NgRx vs Vue+Pinia

| | React + Redux Toolkit | Angular + NgRx (concept) | Vue + Pinia |
|---|---|---|---|
| **Boilerplate** | Low — `createSlice` generates action creators + reducer in one call; `createAsyncThunk` removes manual pending/fulfilled/rejected wiring. | Highest — separate files for actions, reducers, effects, and selectors are the idiomatic pattern, even for simple state. | Lowest — a Pinia store is a single `defineStore` call; the Composition API "setup store" style reads like a Vue component (`ref`, `computed`, plain functions). |
| **Learning curve** | Moderate — need to understand the Flux loop (dispatch → reducer → store → selector) plus React hooks (`useSelector`/`useDispatch`). | Steepest — requires understanding RxJS Observables, Effects as a separate side-effect layer, and Angular DI, on top of the Flux loop. | Gentlest — if you know Vue's `ref`/`computed`, a store is just those same primitives shared across components; no new mental model. |
| **Built-in tooling** | Redux DevTools (time-travel debugging, action log) works out of the box via `configureStore`. | Redux DevTools also supports NgRx via `@ngrx/store-devtools`; Angular DI makes services easy to mock in tests. | Vue DevTools has a dedicated Pinia tab showing every store's state and the actions that mutated it — comparable to Redux DevTools. |
| **Async handling** | `createAsyncThunk` + `extraReducers` (this project: `fetchAllCourses` in `enrollmentSlice.js`). | NgRx Effects (`@Effect`) intercept an action, call a service, and dispatch a new action on success/failure — side effects are explicitly kept out of reducers. | Plain `async` actions inside the store (`fetchAndEnroll` in the Vue project's `enrollment.js`) — no separate side-effect layer needed. |
| **Selectors** | Plain functions (`selectCourses`, `selectCoursesLoading` in `enrollmentSlice.js`) passed to `useSelector`. | NgRx selectors (`createSelector`) are memoized and composable, similar in spirit to Reselect. | Not usually needed — Pinia getters (`computed`) already serve this role, and `storeToRefs` extracts reactive references directly. |

**Takeaway:** Redux Toolkit meaningfully closes the ergonomics gap with Pinia for small
apps, but NgRx's stricter separation (actions/reducers/effects/selectors as distinct
files) pays off mainly at large-team scale where explicitness prevents accidental
side effects in reducers — for a project this size, Pinia's simplicity wins on raw
developer experience.
