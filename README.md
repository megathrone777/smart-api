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

3. Run the API:

   ```
   cd src
   uv run uvicorn main:app --reload
   ```

   Opens at http://127.0.0.1:8000 (docs at http://127.0.0.1:8000/docs).

## Deploy to FastAPI Cloud

This project uses a `src/` layout, so the FastAPI Cloud default of
"app at the repository root" does not apply. Two required settings:

1. **Application Directory** — set it to `src`:

   - Dashboard: App -> Settings -> Application Directory -> `src` -> Update
   - or CLI: `fastapi cloud apps update --directory src`

2. **Environment variables** — `.env` is **never** uploaded to the cloud.
   Set every variable from `.env` in FastAPI Cloud (Dashboard -> App ->
   Environment Variables), or via the CLI:

   ```
   fastapi cloud env set APP_BYPASS_PASS        "<value>" --secret
   fastapi cloud env set APP_JWT_SECRET         "<value>" --secret
   fastapi cloud env set SUPABASE_JWT_SECRET    "<value>" --secret
   fastapi cloud env set SUPABASE_URL           "<value>" --secret
   fastapi cloud env set SUPABASE_PUBLISHABLE_KEY "<value>" --secret
   fastapi cloud env set SUPABASE_SERVICE_ROLE_KEY "<value>" --secret
   ```

3. Deploy:

   ```
   fastapi deploy
   ```

   > Quick sanity check: `cd src` then `fastapi dev` should start the app
   > without passing a file path. If that works, the cloud config is right.

## Notes

- `.env` is git-ignored; commit the `.env.example` template only.
- The `.env` file is resolved relative to `src/core/config.py`,
  so the app can be started from any working directory.
