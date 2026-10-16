# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Conciliador de Facturas y Retenciones: a monthly reconciliation tool that cross-checks a supplier invoicing file (`data/facturas.csv`) against accounting records (`data/contabilidad.csv`), flagging monetary/tax discrepancies, duplicates, missing accounting entries, and empty required fields. Two-tier architecture: Angular 17 frontend + FastAPI/Pandas backend. Spanish is the language of the domain, code identifiers, and UI — keep new code consistent with this (variable/function names, docstrings, error messages, and inconsistency labels are all in Spanish).

## Commands

### Backend (from `backend/`)
```bash
python3.12 -m venv venv && source venv/bin/activate   # first-time setup; must be Python 3.11–3.13 (3.14 can't install pinned pandas)
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000   # run dev server (http://localhost:8000, docs at /docs)
python -m pytest tests -v                              # run all tests
python -m pytest tests/test_conciliacion.py -v          # run a single test file
python -m pytest tests/test_conciliacion.py::test_name -v  # run a single test
```
`pytest.ini` sets `pythonpath = .` and `testpaths = tests`, so pytest must be run from inside `backend/`.

### Frontend (from `frontend/`)
```bash
npm install
npx ng serve --open   # dev server at http://localhost:4200
npx ng build                                      # production build to dist/
npx ng test --watch=false --browsers=ChromeHeadless  # Karma/Jasmine unit tests (needs Chrome)
npx ng test --watch=false --browsers=ChromeHeadless --include='**/tabla-resultados/*.spec.ts'  # single spec
```
Component SCSS imports shared tokens/mixins with `@use 'variables' as *;` — resolved from `src/styles/` via `stylePreprocessorOptions.includePaths` in `angular.json`.

Both servers must run concurrently for the app to work end-to-end (frontend calls backend via CORS at `environment.apiUrl`, default `http://localhost:8000`).

## Architecture

**Backend data flow** (`backend/app/`): `api/routes.py` receives two uploaded CSV files → `services/lector_csv.py` decodes bytes (tries `utf-8-sig`, `utf-8`, `latin-1`, `cp1252` in order) and validates required columns, returning a pandas DataFrame of all-string dtype → `services/conciliacion.py::procesar_conciliacion` runs the actual reconciliation rules row-by-row → result is validated against `schemas/conciliacion.py` Pydantic models and returned as JSON.

**Reconciliation rules** (`services/conciliacion.py`), all monetary math uses `Decimal` (never `float`) quantized to 2 decimals with `ROUND_HALF_UP`:
- `iva_esperado = base_gravable * tarifa_iva`; mismatch vs. reported `valor_iva` → `"Diferencia en IVA"`.
- `total_esperado = base_gravable + iva_esperado - valor_retencion` — deliberately uses the *expected* IVA (not the reported one) so a bad reported IVA can't mask/compensate a total mismatch. Mismatch → `"Diferencia en total"`.
- Duplicate `id_factura` within `facturas.csv` → every occurrence marked `"Factura duplicada"` (rows are never dropped).
- `id_factura` not present in `contabilidad.csv` → `"Factura sin registro contable"`.
- Empty `id_factura`, `base_gravable`, `nit_proveedor`, `fecha_factura`, or `concepto` → `"Campo obligatorio vacío: <campo>"`.
- A row is `"Correcta"` iff its inconsistencia list is empty, else `"Con inconsistencia"`.
- `id_factura` values are normalized via `normalize_id` (stripped) before duplicate/cross-reference checks, so incidental whitespace doesn't cause false negatives.

Changes to these rules must stay in sync with the worked examples and expected counts documented in `README.md` (section 9 "Reglas de Negocio" and section 11 "Resultados Obtenidos") — update both if behavior changes.

**Frontend** (`frontend/src/app/`): standalone components, no routing/NgModules, Angular 17 control flow (`@if`/`@for`). `AppComponent` is the container: it owns `cargando`/`mensajeError`/`resultados`, calls `ConciliacionService.procesarArchivos` (multipart `FormData` POST to `/api/conciliacion`), and maps `HttpErrorResponse` to user messages (only a string `detail` is shown verbatim; FastAPI 422s have a list `detail`). Presentational children in `components/`: `carga-archivos` (holds selected files, validates `.csv`, emits `procesar` / `archivosCambiados`), `resumen-conciliacion`, and `tabla-resultados` (owns the estado filter; resets it whenever a new `resultados` input arrives). `models/conciliacion.model.ts` mirrors the backend Pydantic schemas exactly; keep them in sync when changing the API response shape. All monetary fields arrive as 2-decimal strings — compared as strings for highlighting, formatted for display only via `MonedaCopPipe`.

## Configuration

Backend env vars (see `backend/.env.example`): `BACKEND_HOST`, `BACKEND_PORT`, `ALLOWED_ORIGINS` (comma-separated CORS origins, read in `app/core/config.py`). Frontend API URL is set per-environment in `frontend/src/environments/environment*.ts`.
