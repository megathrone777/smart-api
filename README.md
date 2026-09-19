# smart-api

FastAPI + Supabase API — полный порт Fastify-приложения `smartheating-api`
(оба работают с одной и той же базой Supabase).

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

## Project structure

The API mirrors the layering of the reference Fastify app 1:1:

```
app/
├── main.py                 # FastAPI app, auth hook + CORS middleware, routers
├── dependencies.py         # Depends()-функции (пагинация, текущий JWT-пользователь)
├── core/
│   ├── config.py           # настройки (env, pydantic-settings)
│   ├── errors.py           # Fastify-совместимые форматы ошибок (401/400/500)
│   └── supabase_client.py  # подключение к Supabase (service-role key)
├── globals/                # коллекции Supabase, id-поля, productTypes, weekdays
├── helpers/                # get_all / get_by_id / paginate / patch / put /
│                           # put_many / remove / remove_many / edges / get_collections
├── store/                  # meta-флаги, дерево зданий/этажей/комнат
├── utils/                  # seeded random, series, make_dwd, room_to_tech_room ...
├── schemas/                # Pydantic-схемы запросов (validation)
├── services/               # бизнес-логика, вынесенная из роутеров
└── routers/                # APIRouter на каждую группу эндпоинтов
    (auth, health, locations, devices, tags, users, heating, energy,
     season, occupancy, overview, notifications, operations)
```

## Route groups (parity with the Fastify app)

| Group | Prefix | Endpoints |
|---|---|---|
| auth | `/auth` | login, register |
| health | `/health` | public health probe |
| locations | `/locations`, `/export` | tree CRUD, floor rooms, rooms-data export |
| devices | `/devicemanagement`, `/settings` | list/create/assign/rename, product types |
| tags | `/tags` | CRUD + recent + room assign/unassign |
| users | `/user` | profile, list, create, update, delete, reset-password |
| heating | `/heatingschedule` | program CRUD + details + assignrooms |
| energy | `/meters`, `/chart` | meters, consumption, weather/room charts |
| season | `/summer-mode` | locations, dwd, toggle, postcode, settings |
| occupancy | `/heatingschedule/occupancy` | settings/presence/upcoming/uploads, timeslots |
| overview | `/overview` | report, logs, offline devices, unassigned rooms |
| notifications | `/notifications` | rules CRUD, activations, system activations, toggle |
| operations | `/operationaloverview` | buildings, floor details, tech rooms |

Auth works exactly like the Fastify app: everything is protected by a JWT
(`Authorization: Bearer <token>`), except `/auth/*`, `/docs*`, `/health`,
and requests carrying the `Pass: <APP_BYPASS_PASS>` header.

## Notes

- `.env` is git-ignored; commit the `.env.example` template only.
- The `.env` file is resolved relative to `app/core/config.py`,
  so the app can be started from any working directory.
- Code convention: your application code is a single top-level package
  named `app`, so internal imports are prefixed with `app.`
  (`from app.routers import tags`) — making third-party/vendor imports
  (`from fastapi import ...`, `from supabase import ...`) easy to
  distinguish from your own code.
- Smoke test (read-only, boots the server and checks all route groups):

  ```
  .venv\Scripts\python.exe scripts\smoke_test.py
  ```
