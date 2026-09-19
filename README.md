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

## Notes

- `.env` is git-ignored; commit the `.env.example` template only.
- The `.env` file is resolved relative to `src/core/config.py`,
  so the app can be started from any working directory.
