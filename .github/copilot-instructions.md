## Purpose

Concise, actionable guidance for AI coding agents working in this repository. It focuses on how to run the app, the important structural patterns, and repository-specific quirks that affect imports and runtime behavior.

## Quick facts

- Language: Python (src/ layout)
- Web framework: Flask (app created in `src/tgmp/main.py`, uses Blueprints)
- Key package namespace: `tgmp` (located under `src/`)

## How to run (PowerShell)

1) Create a venv, activate it, and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Recommended safe start (avoids importing `src/tgmp/__init__.py` which currently imports a `db` module that may be missing):

```powershell
Set-Location -Path .\src\tgmp
python .\main.py
```

Why this is recommended: importing the `tgmp` package (for example via `FLASK_APP=tgmp:app` or `python -m tgmp.main`) executes `src/tgmp/__init__.py`. That file imports `.db` and calls `app.teardown_appcontext(close_connection)` which will raise ImportError if `db.py` is not present. Running `main.py` from `src/tgmp` executes the module as a script and avoids the package import side-effect.

Other options (use with caution):
- You can set `PYTHONPATH=src` and then run `python -m tgmp.main`, but importing the `tgmp` package will still execute `__init__.py` and can fail until `db.py` is fixed or the import is guarded.
- `debug_env.py` (repo root) is handy to inspect `PYTHONPATH`, `FLASK_APP` and how imports are resolved.

## Key files to consult

- `src/tgmp/main.py` — Flask `app` definition, blueprint registration and `main()` that runs `app.run(debug=True)`.
- `src/tgmp/__init__.py` — re-exports `app` and wires `teardown_appcontext(close_connection)`. Be aware of the `from .db import close_connection` import.
- `src/tgmp/controllers/` — route handlers and blueprint definitions (HTTP layer). Example: `controllers/main_controller.py`.
- `src/tgmp/services/` — lightweight business logic functions (e.g. `services/media_service.py` defines `get_video()`).
- `src/tgmp/entities/` — domain objects; `media_entity.py` implements `Media` which uses `pathlib.Path` to find files and raises FileNotFound/NotADirectory errors.
- `debug_env.py` — prints env and import resolution info (useful for debugging run issues).
- `requirements.txt` / `pyproject.toml` — dependencies and packaging hints.

## Patterns & repo-specific conventions

- src/ layout (source under `src/`): tests or tools should either set `PYTHONPATH=src` or run from a directory that makes imports resolve correctly.
- Top-level (non-package) imports appear in many modules (e.g. `from controllers.main_controller import main_bp`) — modules were written to run in the `src/tgmp` context and not necessarily as an installed package.
- Controller -> Service -> Entity flow: controllers call functions in `services/` which instantiate or call methods on objects in `entities/`. Example: `controllers` → `services/media_service.get_video()` → `entities.Media`.
- Side-effecting package `__init__.py`: currently performs imports with side effects (wiring teardown). Until `db.py` is present or this import is made lazy, importing `tgmp` will fail. Be cautious when authoring code that imports `tgmp` directly.

## Troubleshooting tips for agents

- If `ImportError` occurs when importing `tgmp`, run `python .\main.py` from `src/tgmp` instead of using the Flask CLI or package import.
- Use `debug_env.py` to dump `PYTHONPATH` and `FLASK_APP` resolution.
- If you need to use the Flask CLI during development, either fix `src/tgmp/__init__.py` (wrap `from .db import close_connection` in try/except or make it lazy) or temporarily set FLASK_APP to a module that does not require package-level imports (and ensure imports do not re-run `__init__`).

## Small, safe fixes an agent can propose

- Guard the `db` import in `src/tgmp/__init__.py` with a try/except and a clear TODO comment so local imports do not break exploration.
- Add a short README section (or update existing README) with the recommended run command shown above (cd into `src/tgmp` + `python main.py`) so contributors don't get tripped by package import side effects.

## Example references (copy-paste lines to open files)
- `src/tgmp/main.py` — Flask app + `main()`
- `src/tgmp/__init__.py` — package exports and `close_connection` import
- `src/tgmp/services/media_service.py` — `get_video()` demonstrating controller→service→entity flow
- `src/tgmp/entities/media_entity.py` — `Media` class that uses `Path.glob`

---
If anything in this guidance looks incomplete or you want the AI instructions angled toward a particular task (tests, refactor, CI), tell me which focus and I will iterate.
