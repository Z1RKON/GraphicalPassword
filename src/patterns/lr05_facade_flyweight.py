"""ЛР5: Facade + Flyweight."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from src.domain.pattern import PatternValidationResult, normalize_raw_points
from src.patterns.lr01_builder import PatternProfile, PatternProfileBuilder


@dataclass(frozen=True)
class DotGlyph:
    """Приспособленец: внутреннее неизменяемое состояние точки сетки."""

    index: int
    x: int
    y: int
    label: str


class DotFlyweightFactory:
    _pool: dict[int, DotGlyph] = {}

    @classmethod
    def get_dot(cls, index: int) -> DotGlyph:
        if index not in cls._pool:
            row, col = divmod(index, 3)
            cls._pool[index] = DotGlyph(index=index, x=col, y=row, label=f"D{index}")
        return cls._pool[index]

    @classmethod
    def pool_size(cls) -> int:
        return len(cls._pool)


class GraphicalPasswordFacade:
    """Фасад: простой API поверх валидатора и хранилища."""

    def __init__(self, profile: PatternProfile | None = None) -> None:
        self.profile = profile or PatternProfileBuilder().build()
        self._hash: str | None = None

    def setup(self, points: list[int]) -> tuple[bool, str]:
        r = normalize_raw_points(points, min_length=self.profile.min_length)
        if not r.ok:
            return False, r.message
        self._hash = self._make_hash(r.normalized)
        self._save()
        return True, "Пароль сохранён"

    def unlock(self, points: list[int]) -> tuple[bool, str]:
        if not self._hash:
            return False, "Пароль не задан"
        r = normalize_raw_points(points, min_length=self.profile.min_length)
        if not r.ok:
            return False, r.message
        if self._make_hash(r.normalized) == self._hash:
            return True, "Разблокировано"
        return False, "Неверный шаблон"

    def describe_grid(self) -> list[str]:
        return [DotFlyweightFactory.get_dot(i).label for i in range(9)]

    def _make_hash(self, pattern: tuple[int, ...]) -> str:
        s = "-".join(map(str, pattern))
        return hashlib.sha256(f"{s}:{self.profile.storage_path.name}".encode()).hexdigest()

    def _save(self) -> None:
        path = self.profile.storage_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"hash": self._hash}), encoding="utf-8")