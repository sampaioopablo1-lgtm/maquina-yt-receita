"""Read-only report of open overdue GHL tasks for the WeSales location.

The endpoint is a read-only search even though GHL exposes it as POST.
This module intentionally contains no mutation endpoint or task/tag update.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None


BASE_URL = "https://services.leadconnectorhq.com"
LOCATION_ID = "1D53YTI9C7oIMBavcQxV"
VERSION = "2021-07-28"
ROOT = Path(__file__).resolve().parent.parent
PIT_FILE = ROOT / ".local" / "_ghl_pit.txt"
PAGE_SIZE = 100
MAX_PAGES = 1000

if ZoneInfo is not None:
    SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")
else:  # pragma: no cover
    SAO_PAULO_TZ = timezone(timedelta(hours=-3), name="UTC-03:00")


def read_token() -> str:
    """Read the PIT without ever including it in output or exceptions."""
    token = os.environ.get("GHL_PIT", "").strip()
    if token:
        return token
    return PIT_FILE.read_text(encoding="utf-8").strip()


def _items(data: object) -> list[dict]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("tasks", "data", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _request_page(token: str, page: int, limit: int) -> list[dict]:
    body = json.dumps({
        "locationId": LOCATION_ID,
        "status": "open",
        "page": page,
        "limit": limit,
    }).encode("utf-8")
    request = Request(
        BASE_URL + "/locations/%s/tasks/search" % LOCATION_ID,
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Version": VERSION,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read()
    except HTTPError as error:
        if error.code == 401:
            raise RuntimeError("GHL API 401 Unauthorized") from None
        raise RuntimeError("GHL API returned HTTP %d" % error.code) from None
    except URLError:
        raise RuntimeError("GHL API network error") from None
    try:
        return _items(json.loads(raw.decode("utf-8")) if raw else {})
    except (UnicodeDecodeError, ValueError):
        raise RuntimeError("GHL API returned invalid JSON") from None


def _sanitized(task: dict) -> dict:
    """Keep report output to stable, non-sensitive task metadata."""
    return {
        "id": task.get("id") or task.get("taskId"),
        "title": task.get("title") or task.get("name"),
        "due_date": task.get("dueDate") or task.get("due_date"),
        "contact_id": task.get("contactId") or task.get("contact_id"),
        "assigned_to": task.get("assignedTo") or task.get("assigned_to"),
        "status": task.get("status"),
    }


def collect_overdue(token: str, today: str, limit: int = PAGE_SIZE) -> dict:
    """Fetch every open task page and return a sanitized report."""
    if not 1 <= limit <= PAGE_SIZE:
        raise ValueError("limit must be between 1 and %d" % PAGE_SIZE)
    overdue = []
    pages = 0
    while pages < MAX_PAGES:
        pages += 1
        tasks = _request_page(token, pages, limit)
        for task in tasks:
            due = task.get("dueDate") or task.get("due_date")
            if isinstance(due, str) and due[:10] < today:
                overdue.append(_sanitized(task))
        if len(tasks) < limit:
            break
    else:
        raise RuntimeError("pagination safety limit reached")
    return {
        "location_id": LOCATION_ID,
        "as_of_date": today,
        "pages_read": pages,
        "open_overdue_tasks": len(overdue),
        "tasks": overdue,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=PAGE_SIZE,
                        help="page size (1-%d)" % PAGE_SIZE)
    args = parser.parse_args()
    today = datetime.now(SAO_PAULO_TZ).date().isoformat()
    report = collect_overdue(read_token(), today, args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError) as error:
        print("G-03 task report stopped: " + str(error))
        raise SystemExit(1)
