"""ЛР4: Composite + Decorator."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.pattern import PatternValidationResult, normalize_raw_points


class GridComponent(ABC):
    @abstractmethod
    def index(self) -> int: ...

    @abstractmethod
    def collect_points(self) -> list[int]: ...


class DotLeaf(GridComponent):
    def __init__(self, index: int, active: bool = False) -> None:
        self._index = index
        self._active = active

    def index(self) -> int:
        return self._index

    def activate(self) -> None:
        self._active = True

    def collect_points(self) -> list[int]:
        return [self._index] if self._active else []


class PatternComposite(GridComponent):
    """Компоновщик: последовательность точек как дерево."""

    def __init__(self) -> None:
        self._children: list[GridComponent] = []

    def add(self, component: GridComponent) -> None:
        self._children.append(component)

    def index(self) -> int:
        return self._children[0].index() if self._children else -1

    def collect_points(self) -> list[int]:
        out: list[int] = []
        for ch in self._children:
            out.extend(ch.collect_points())
        return out

    def validate(self) -> PatternValidationResult:
        return normalize_raw_points(self.collect_points())


class ValidatorBase(ABC):
    @abstractmethod
    def validate(self, points: list[int]) -> PatternValidationResult: ...


class BasePatternValidator(ValidatorBase):
    def validate(self, points: list[int]) -> PatternValidationResult:
        return normalize_raw_points(points)


class LoggingValidatorDecorator(ValidatorBase):
    """Декоратор: логирование поверх валидатора."""

    def __init__(self, wrapped: ValidatorBase, log: list[str] | None = None) -> None:
        self._wrapped = wrapped
        self._log = log if log is not None else []

    def validate(self, points: list[int]) -> PatternValidationResult:
        self._log.append(f"validate input={points}")
        result = self._wrapped.validate(points)
        self._log.append(f"result ok={result.ok} msg={result.message}")
        return result