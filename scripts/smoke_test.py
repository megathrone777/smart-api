"""Smoke test: boots the API and exercises endpoints against the shared Supabase.

Read-only checks plus auth/validation error shapes. No data is mutated.
Run: .venv\\Scripts\\python.exe scripts\\smoke_test.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import httpx

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PORT = 8901
BASE = f"http://127.0.0.1:{PORT}"

FAILURES: list[str] = []


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"')
    return values


def wait_ready(client: httpx.Client) -> None:
    for _ in range(60):
        try:
            response = client.get(f"{BASE}/health")
            if response.status_code == 200:
                return
        except httpx.TransportError:
            time.sleep(0.5)
    raise RuntimeError("server did not become ready")


def check(
    client: httpx.Client,
    method: str,
    url: str,
    headers: dict[str, str],
    expected: int,
    label: str,
    body: dict | None = None,
) -> None:
    response = client.request(method, f"{BASE}{url}", headers=headers, json=body)
    snippet = response.text[:140].replace("\n", " ")
    status = "OK " if response.status_code == expected else "FAIL"
    print(f"[{status}] {label}: {response.status_code} (expected {expected}) {snippet}")
    if response.status_code != expected:
        FAILURES.append(label)


def run_checks(client: httpx.Client, bypass: dict[str, str]) -> None:
    # Public routes
    check(client, "GET", "/health", {}, 200, "health (public)")

    # Auth required
    check(client, "GET", "/overview/report", {}, 401, "no auth -> 401 shape")
    check(
        client, "POST", "/devicemanagement/devices", {}, 401,
        "write without auth -> 401", body={"deviceName": "x"},
    )

    # Bypass header reads
    check(client, "GET", "/overview/report", bypass, 200, "report via bypass")
    check(client, "GET", "/tags/list?limit=2", bypass, 200, "tags/list")
    check(client, "GET", "/tags/recent", bypass, 200, "tags/recent")
    check(client, "GET", "/user/list?limit=2", bypass, 200, "user/list")
    check(client, "GET", "/devicemanagement/list?limit=2", bypass, 200, "devices/list")
    check(client, "GET", "/devicemanagement/producttypes", bypass, 200, "producttypes")
    check(client, "GET", "/devicemanagement/connectionqualities", bypass, 200, "connectionqualities")
    check(client, "GET", "/devicemanagement/lastpayload", bypass, 200, "lastpayload")
    check(
        client, "GET", "/devicemanagement/device/lookup-unused?identifier=AABBCCDD",
        bypass, 200, "lookup-unused",
    )
    check(client, "GET", "/meters/list", bypass, 200, "meters/list")
    check(client, "GET", "/meters/1/consumption/info", bypass, 200, "consumption/info")
    check(client, "GET", "/chart/meters/consumption", bypass, 200, "meter chart")
    check(client, "GET", "/chart/weather/temperatures", bypass, 200, "weather chart")
    check(client, "GET", "/chart/room-temperature/1", bypass, 200, "room temp chart")
    check(client, "GET", "/heatingschedule/list", bypass, 200, "heatingschedule/list")
    check(client, "GET", "/heatingschedule/1/details", bypass, 200, "heatingschedule details")
    check(client, "GET", "/locations", bypass, 200, "locations tree")
    check(client, "GET", "/export/rooms-data", bypass, 200, "export rooms-data")
    check(client, "GET", "/summer-mode", bypass, 200, "summer-mode")
    check(client, "GET", "/summer-mode/test/dwd?postcode=10115", bypass, 200, "summer-mode test dwd")
    check(client, "GET", "/notifications/rules", bypass, 200, "notification rules")
    check(client, "GET", "/notifications/system-activations", bypass, 200, "system activations")
    check(client, "GET", "/notifications/activations?limit=2", bypass, 200, "user activations")
    check(
        client, "GET", "/heatingschedule/occupancy/settings/list?limit=2",
        bypass, 200, "occupancy settings list",
    )
    check(
        client, "GET", "/heatingschedule/occupancy/presence/rooms?limit=2",
        bypass, 200, "presence rooms",
    )
    check(
        client, "GET", "/heatingschedule/occupancy/upcoming/list?limit=2",
        bypass, 200, "upcoming list",
    )
    check(
        client, "GET", "/heatingschedule/occupancy/uploads/list?limit=2",
        bypass, 200, "uploads list",
    )
    check(client, "POST", "/heatingschedule/occupancy/check", bypass, 200, "occupancy check")
    check(client, "GET", "/operationaloverview/list", bypass, 200, "operational list")
    check(
        client, "GET", "/operationaloverview/tech/list?limit=2",
        bypass, 200, "tech rooms list",
    )
    check(client, "GET", "/overview/list?limit=2", bypass, 200, "overview logs list")
    check(client, "GET", "/overview/list-devices-offline?limit=2", bypass, 200, "devices offline")
    check(
        client, "GET", "/overview/list-unassigned-rooms?limit=2",
        bypass, 200, "unassigned rooms",
    )

    # Login with definitely-invalid credentials -> 401 {"error": ...}
    check(
        client, "POST", "/auth/login", {}, 401, "login invalid creds",
        body={"email": "no-such-user@invalid.test", "password": "wrong"},
    )

    # Validation error -> Fastify-style 400
    check(client, "POST", "/auth/login", {}, 400, "login missing fields -> 400", body={})


def main() -> int:
    env = load_env()
    bypass = {"Pass": env["APP_BYPASS_PASS"]}

    process = subprocess.Popen(
        [
            str(ROOT / ".venv" / "Scripts" / "python.exe"),
            "-m",
            "uvicorn",
            "app.main:app",
            "--port",
            str(PORT),
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        with httpx.Client(timeout=30) as client:
            wait_ready(client)
            run_checks(client, bypass)

            schema = client.get(f"{BASE}/openapi.json").json()
            paths = len(schema.get("paths", {}))
            print(f"[INFO] openapi paths: {paths}")
            if paths < 60:
                FAILURES.append("openapi path count")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

    if FAILURES:
        print(f"\nFAILED: {FAILURES}")
        return 1

    print("\nAll smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
