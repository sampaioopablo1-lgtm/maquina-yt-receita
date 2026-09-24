"""Idempotent, time-gated G-03 promotion runner for the official GHL API."""

from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python versions without zoneinfo
    ZoneInfo = None


BASE_URL = "https://services.leadconnectorhq.com"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
PIPELINE_ID = "0Fo2xbeayE4EP6yuSUtq"
NOVO_LEAD = "7ae9c950-9bcf-4e60-8bc5-cb7388c87b7d"
CONNECTAR = "deb60542-a5cd-43ae-b875-b467b120a72c"
VERSION = "2021-07-28"
# The task is configured with StartWhenAvailable/WakeToRun. If Windows starts
# it late after sleep or a power-off, allow the delayed run through Sep 30.
WINDOW_START = datetime(2026, 9, 29, 8, 0)
WINDOW_END = datetime(2026, 9, 30, 8, 0)

if ZoneInfo is not None:
    SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")
else:  # pragma: no cover - fallback for old Python on the local PC
    SAO_PAULO_TZ = timezone(timedelta(hours=-3), name="UTC-03:00")

WINDOW_START = WINDOW_START.replace(tzinfo=SAO_PAULO_TZ)
WINDOW_END = WINDOW_END.replace(tzinfo=SAO_PAULO_TZ)

ROOT = Path(__file__).resolve().parent.parent
PIT_FILE = ROOT / ".local" / "_ghl_pit.txt"
MARKER_FILE = ROOT / ".local" / "g03-run.json"


def local_now():
    """Return timezone-aware Sao Paulo wall time."""
    return datetime.now(SAO_PAULO_TZ)


def read_token():
    # Deliberately never log or include this value in an exception/report.
    token = os.environ.get("GHL_PIT", "").strip()
    if token:
        return token
    return PIT_FILE.read_text(encoding="utf-8").strip()


def request(method, path, token, body=None):
    payload = None if body is None else json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + token,
        "Version": VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        with urlopen(Request(BASE_URL + path, data=payload, headers=headers,
                             method=method), timeout=30) as response:
            raw = response.read()
            return response.status, (json.loads(raw.decode("utf-8")) if raw else {})
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:300]
        if error.code == 401:
            raise RuntimeError("GHL API 401 Unauthorized: PIT is invalid or expired") from None
        if error.code == 429:
            raise RuntimeError("GHL API 429 Too Many Requests: retry later") from None
        if 400 <= error.code < 500:
            raise RuntimeError("GHL API %d client error: %s" % (error.code, detail)) from None
        raise RuntimeError("GHL API %d server error" % error.code) from None
    except URLError as error:
        raise RuntimeError("GHL API network error: %s" % error.reason) from None


def opportunity_items(data):
    if isinstance(data, list):
        return data
    for key in ("opportunities", "opportunity", "data", "results"):
        value = data.get(key) if isinstance(data, dict) else None
        if isinstance(value, list):
            return value
    return []


def count_overdue_tasks(token, now):
    """Report-only task probe; task mutation is intentionally not implemented."""
    body = {"locationId": LOCATION_ID, "status": "open"}
    try:
        _, data = request("POST", "/locations/%s/tasks/search" % LOCATION_ID,
                          token, body)
    except RuntimeError as error:
        # Endpoint availability varies; do not make a report-only probe block G-03.
        print("task report unavailable: " + str(error))
        return None
    tasks = data if isinstance(data, list) else data.get("tasks", [])
    overdue = 0
    for task in tasks if isinstance(tasks, list) else []:
        due = task.get("dueDate") or task.get("due_date")
        if isinstance(due, str) and due[:10] < now.strftime("%Y-%m-%d"):
            overdue += 1
    return overdue


def main():
    now = local_now()
    if MARKER_FILE.exists():
        try:
            if json.loads(MARKER_FILE.read_text(encoding="utf-8")).get("completed"):
                print("G-03 already completed; no CRM writes")
                return
        except (OSError, ValueError):
            pass
    if not WINDOW_START <= now <= WINDOW_END:
        print("outside scheduled window; no CRM writes")
        return

    token = read_token()
    report = {
        "completed": False,
        "run_timestamp": now.isoformat(timespec="seconds"),
        "window": "2026-09-29T08:00 to 2026-09-30T08:00 America/Sao_Paulo",
        "queried": 0,
        "promoted": 0,
        "skipped_non_open": 0,
        "overdue_tasks": None,
    }
    report["overdue_tasks"] = count_overdue_tasks(token, now)
    query = urlencode({"locationId": LOCATION_ID, "pipelineId": PIPELINE_ID,
                       "pipelineStageId": NOVO_LEAD, "status": "open",
                       "limit": "100"})
    _, data = request("GET", "/opportunities/search?" + query, token)
    opportunities = opportunity_items(data)
    report["queried"] = len(opportunities)
    for opportunity in opportunities:
        opportunity_id = opportunity.get("id") or opportunity.get("opportunityId")
        if not opportunity_id or opportunity.get("status", "open") != "open":
            report["skipped_non_open"] += 1
            continue
        body = {"pipelineStageId": CONNECTAR, "pipelineId": PIPELINE_ID,
                "status": "open"}
        request("PUT", "/opportunities/" + str(opportunity_id), token, body)
        report["promoted"] += 1
        time.sleep(0.05)
    report["completed"] = True
    MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    MARKER_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print("G-03 completed: queried=%d promoted=%d overdue_tasks=%s" %
          (report["queried"], report["promoted"], report["overdue_tasks"]))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("G-03 stopped without completing: " + str(error))
        raise SystemExit(1)
