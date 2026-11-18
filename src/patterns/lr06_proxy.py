"""ЛР6: Заместитель (Proxy) — контроль доступа и ленивая загрузка хранилища."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from src.patterns.lr05_facade_flyweight import GraphicalPasswordFacade
from src.patterns.lr01_builder import PatternProfile


class PasswordBackend(Protocol):
    def unlock(self, points: list[int]) -> tuple[bool, str]: ...


class PasswordFacadeProxy:
    def __init__(self, profile: PatternProfile, max_attempts: int = 3) -> None:
        self._facade: GraphicalPasswordFacade | None = None
        self._profile = profile
        self._attempts = 0
        self._max = max_attempts
        self._locked = False

    def _service(self) -> GraphicalPasswordFacade:
        if self._facade is None:
            self._facade = GraphicalPasswordFacade(self._profile)
            path = self._profile.storage_path
            if path.is_file():
                data = json.loads(path.read_text(encoding="utf-8"))
                self._facade._hash = data.get("hash")
        return self._facade

    def unlock(self, points: list[int]) -> tuple[bool, str]:
        if self._locked:
            return False, "Заместитель: доступ заблокирован"
        ok, msg = self._service().unlock(points)
        if not ok:
            self._attempts += 1
            if self._attempts >= self._max:
                self._locked = True
                return False, "Заместитель: слишком много попыток"
        else:
            self._attempts = 0
        return ok, msg

    def setup(self, points: list[int]) -> tuple[bool, str]:
        self._locked = False
        self._attempts = 0
        return self._service().setup(points)