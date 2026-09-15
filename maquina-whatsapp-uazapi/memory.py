"""Histórico por usuário no formato nativo do Gemini. Dict + lock. Perde no restart, e tudo bem."""
import os, threading

MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "20"))
_hist: dict[str, list] = {}
_paused: set[str] = set()
_lock = threading.Lock()


def append(user: str, role: str, text: str) -> None:
    with _lock:
        h = _hist.setdefault(user, [])
        h.append({"role": role, "parts": [{"text": text}]})
        del h[:-MAX_HISTORY]
        while h and h[0]["role"] != "user":
            h.pop(0)


def get(user: str) -> list:
    with _lock:
        return list(_hist.get(user, []))


def reset(user: str) -> None:
    with _lock:
        _hist.pop(user, None)


def pause(user: str) -> None:
    with _lock:
        _paused.add(user)


def is_paused(user: str) -> bool:
    with _lock:
        return user in _paused
