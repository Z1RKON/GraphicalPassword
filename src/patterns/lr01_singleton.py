"""ЛР1: Singleton — единый реестр настроек безопасности."""

from __future__ import annotations


class SecuritySettingsRegistry:
    """Одиночка: один экземпляр настроек графического пароля."""

    _instance: SecuritySettingsRegistry | None = None

    def __new__(cls) -> SecuritySettingsRegistry:
        if cls._instance is None:
            inst = super().__new__(cls)
            inst.min_pattern_length = 4
            inst.grid_size = 3
            inst.hash_salt = "skfu-v8"
            cls._instance = inst
        return cls._instance

    @classmethod
    def reset_for_tests(cls) -> None:
        cls._instance = None