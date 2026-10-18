"""Debounce por usuário: cada mensagem nova reinicia a espera; no fim, tudo vira um turno só."""
import threading
from typing import Callable


class MessageBuffer:
    def __init__(self, wait_seconds: float, on_flush: Callable[[str, list[str]], None]):
        self.wait = wait_seconds
        self.on_flush = on_flush
        self._pending: dict[str, list[str]] = {}
        self._timers: dict[str, threading.Timer] = {}
        self._lock = threading.Lock()

    def add(self, user: str, text: str) -> None:
        with self._lock:
            self._pending.setdefault(user, []).append(text)
            if user in self._timers:
                self._timers[user].cancel()
            t = threading.Timer(self.wait, self._flush, [user])
            t.daemon = True
            self._timers[user] = t
            t.start()

    def _flush(self, user: str) -> None:
        with self._lock:
            texts = self._pending.pop(user, [])
            self._timers.pop(user, None)
        if texts:
            print(f"[buffer] flush user={user} msgs={len(texts)}")
            self.on_flush(user, texts)
