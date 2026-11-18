"""ЛР8: Цепочка обязанностей — поэтапная валидация шаблона."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.pattern import PatternValidationResult, normalize_raw_points, MAX_PATTERN_LENGTH


@dataclass
class ValidationContext:
    points: list[int]
    message: str = ""


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler
        return handler

    def handle(self, ctx: ValidationContext) -> PatternValidationResult:
        if not self._check(ctx):
            return PatternValidationResult(False, (), ctx.message)
        if self._next:
            return self._next.handle(ctx)
        return normalize_raw_points(ctx.points)

    @abstractmethod
    def _check(self, ctx: ValidationContext) -> bool: ...


class EmptyHandler(Handler):
    def _check(self, ctx: ValidationContext) -> bool:
        if not ctx.points:
            ctx.message = "Пустой шаблон"
            return False
        return True


class RangeHandler(Handler):
    def _check(self, ctx: ValidationContext) -> bool:
        if any(p < 0 or p >= MAX_PATTERN_LENGTH for p in ctx.points):
            ctx.message = "Точка вне сетки"
            return False
        return True


class LengthHandler(Handler):
    def __init__(self, min_len: int = 4) -> None:
        super().__init__()
        self._min = min_len

    def _check(self, ctx: ValidationContext) -> bool:
        if len(ctx.points) < self._min:
            ctx.message = f"Меньше {self._min} точек"
            return False
        return True


def build_validation_chain(min_len: int = 4) -> Handler:
    head = EmptyHandler()
    head.set_next(RangeHandler()).set_next(LengthHandler(min_len))
    return head