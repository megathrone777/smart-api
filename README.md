# smart-api

FastAPI + Supabase API.

## Setup

1. Create your environment file from the template:

   ```
   copy .env.example .env
   ```

2. Fill in real values in `.env`.
   - Supabase values: Dashboard -> Project Settings -> API
   - The variable names **must** match exactly:
     `APP_BYPASS_PASS`, `APP_JWT_SECRET`, `SUPABASE_JWT_SECRET`,
     `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL`.

3. Run the API (from the project root — the entry point is configured
   in `pyproject.toml` via `[tool.fastapi] entrypoint = "app.main:app"`):

   ```
   uv run fastapi dev
   ```

   Opens at http://127.0.0.1:8000 (docs at http://127.0.0.1:8000/docs).

## Deploy to FastAPI Cloud

The entry point is configured in `pyproject.toml`:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

so FastAPI Cloud automatically imports `app` from `app/main.py` — no
Application Directory setting or file path needed at deploy time. Two
things to remember:

1. **Environment variables** — `.env` is **never** uploaded to the cloud.
   Set every variable from `.env` in FastAPI Cloud (Dashboard -> App ->
   Environment Variables), or via the CLI:

   ```
   fastapi cloud env set APP_BYPASS_PASS          "<value>" --secret
   fastapi cloud env set APP_JWT_SECRET           "<value>" --secret
   fastapi cloud env set SUPABASE_JWT_SECRET      "<value>" --secret
   fastapi cloud env set SUPABASE_URL             "<value>" --secret
   fastapi cloud env set SUPABASE_PUBLISHABLE_KEY "<value>" --secret
   fastapi cloud env set SUPABASE_SERVICE_ROLE_KEY "<value>" --secret
   ```

2. Deploy:

   ```
   fastapi deploy
   ```

   > Quick sanity check: `uv run fastapi dev` should start the app from the
   > project root without passing a file path. If that works, the cloud
   > config is right.

## Notes

- `.env` is git-ignored; commit the `.env.example` template only.
- The `.env` file is resolved relative to `app/core/config.py`,
  so the app can be started from any working directory.
- Code convention: your application code is a single top-level package
  named `app`, so internal imports are prefixed with `app.`
  (`from app.routers import tags`) — making third-party/vendor imports
  (`from fastapi import ...`, `from supabase import ...`) easy to
  distinguish from your own code.
- No `__pycache__/` folders ever appear inside `app/`: bytecode is
  redirected to a central cache via the user-level env var
  `PYTHONPYCACHEPREFIX` (set with
  `setx PYTHONPYCACHEPREFIX "%LOCALAPPDATA%\Python\pycache"`).
  Restart the terminal after setting it.
