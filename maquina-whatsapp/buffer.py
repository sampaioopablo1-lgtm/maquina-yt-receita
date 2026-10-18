"""Debounce por contato: junta as mensagens que chegam em sequência num turno só."""
import os, threading

BUFFER_SECONDS = float(os.environ.get("BUFFER_SECONDS", "8"))
_buf: dict[str, list[str]] = {}
_timers: dict[str, threading.Timer] = {}
_lock = threading.Lock()


def push(user: str, text: str, on_flush) -> None:
    with _lock:
        _buf.setdefault(user, []).append(text)
        if user in _timers:
            _timers[user].cancel()
        t = threading.Timer(BUFFER_SECONDS, _flush, args=(user, on_flush))
        t.daemon = True
        _timers[user] = t
        t.start()


def _flush(user: str, on_flush) -> None:
    with _lock:
        msgs = _buf.pop(user, [])
        _timers.pop(user, None)
    if msgs:
        on_flush(user, "\n".join(msgs))
