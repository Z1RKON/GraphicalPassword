"""ЛР1: Builder — пошаговая сборка профиля блокировки."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.patterns.lr01_singleton import SecuritySettingsRegistry


@dataclass
class PatternProfile:
    theme: str
    min_length: int
    storage_path: Path
    allow_jump: bool = True


class PatternProfileBuilder:
    def __init__(self) -> None:
        reg = SecuritySettingsRegistry()
        self._theme = "dark"
        self._min_length = reg.min_pattern_length
        self._path = Path.home() / ".graphical_password_patterns.json"
        self._allow_jump = True

    def with_theme(self, theme: str) -> PatternProfileBuilder:
        self._theme = theme
        return self

    def with_min_length(self, n: int) -> PatternProfileBuilder:
        self._min_length = n
        return self

    def with_storage(self, path: Path) -> PatternProfileBuilder:
        self._path = path
        return self

    def with_jump_rules(self, allowed: bool) -> PatternProfileBuilder:
        self._allow_jump = allowed
        return self

    def build(self) -> PatternProfile:
        return PatternProfile(
            theme=self._theme,
            min_length=self._min_length,
            storage_path=self._path,
            allow_jump=self._allow_jump,
        )