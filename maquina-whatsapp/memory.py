"""Histórico por contato, em memória, no formato do Claude. Zero infra."""
import os, threading

MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "30"))
_hist: dict[str, list] = {}
_paused: set[str] = set()
_lock = threading.Lock()


def get(user: str) -> list:
    with _lock:
        return list(_hist.get(user, []))


def append(user: str, role: str, content) -> None:
    with _lock:
        h = _hist.setdefault(user, [])
        h.append({"role": role, "content": content})
        # nunca cortar no meio de um par tool_use/tool_result
        while len(h) > MAX_HISTORY:
            h.pop(0)
            while h and h[0]["role"] != "user":
                h.pop(0)


def pause(user: str) -> None:
    with _lock:
        _paused.add(user)


def is_paused(user: str) -> bool:
    with _lock:
        return user in _paused
