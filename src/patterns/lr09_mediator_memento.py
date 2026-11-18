"""ЛР9: Посредник + Снимок."""

from __future__ import annotations

from dataclasses import dataclass

from src.domain.pattern import normalize_raw_points


@dataclass
class PatternMemento:
    raw_points: list[int]


class PatternInputMediator:
    """Посредник между «точками» и валидатором без прямой связи компонентов."""

    def __init__(self) -> None:
        self._points: list[int] = []
        self._last_message: str = ""

    def dot_selected(self, index: int) -> None:
        if self._points and self._points[-1] == index:
            return
        self._points.append(index)

    def commit(self) -> bool:
        r = normalize_raw_points(self._points)
        self._last_message = r.message
        return r.ok

    def save(self) -> PatternMemento:
        return PatternMemento(list(self._points))

    def restore(self, memento: PatternMemento) -> None:
        self._points = list(memento.raw_points)

    def clear(self) -> None:
        self._points.clear()

    @property
    def points(self) -> list[int]:
        return list(self._points)