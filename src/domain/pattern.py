"""Доменная логика графического пароля (вариант 8)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

GRID_SIZE = 3
MIN_PATTERN_LENGTH = 4
MAX_PATTERN_LENGTH = GRID_SIZE * GRID_SIZE

_JUMP_MIDDLE: dict[tuple[int, int], int] = {
    (0, 2): 1, (2, 0): 1, (0, 6): 3, (6, 0): 3,
    (2, 8): 5, (8, 2): 5, (6, 8): 7, (8, 6): 7,
    (1, 7): 4, (7, 1): 4, (3, 5): 4, (5, 3): 4,
}


def expand_step(current: int, nxt: int, visited: set[int]) -> list[int]:
    if current == nxt or nxt in visited:
        return []
    key = (current, nxt)
    if key in _JUMP_MIDDLE and _JUMP_MIDDLE[key] not in visited:
        return [_JUMP_MIDDLE[key], nxt]
    dr, dc = abs(current // 3 - nxt // 3), abs(current % 3 - nxt % 3)
    if dr <= 1 and dc <= 1 and (dr + dc > 0):
        return [nxt]
    return []


@dataclass(frozen=True)
class PatternValidationResult:
    ok: bool
    normalized: tuple[int, ...]
    message: str = ""


def normalize_raw_points(points: Iterable[int], min_length: int = MIN_PATTERN_LENGTH) -> PatternValidationResult:
    seq = list(points)
    if not seq:
        return PatternValidationResult(False, (), "Пустой шаблон")
    if any(not (0 <= p < MAX_PATTERN_LENGTH) for p in seq):
        return PatternValidationResult(False, (), "Индекс вне сетки 0–8")

    visited: set[int] = set()
    normalized: list[int] = []
    for i, p in enumerate(seq):
        if i == 0:
            visited.add(p)
            normalized.append(p)
            continue
        added = expand_step(normalized[-1], p, visited)
        if not added:
            return PatternValidationResult(False, (), f"Недопустимый переход {normalized[-1]} -> {p}")
        for cell in added:
            if cell in visited:
                return PatternValidationResult(False, (), "Повтор точки")
            visited.add(cell)
            normalized.append(cell)

    if len(normalized) < min_length:
        return PatternValidationResult(False, tuple(normalized), f"Минимальная длина — {min_length}")
    return PatternValidationResult(True, tuple(normalized), "")