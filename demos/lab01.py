"""Демо ЛР1: Singleton + Builder."""

from src.patterns.lr01_builder import PatternProfileBuilder
from src.patterns.lr01_singleton import SecuritySettingsRegistry


def main() -> None:
    a = SecuritySettingsRegistry()
    b = SecuritySettingsRegistry()
    print("Singleton:", a is b, "min_length=", a.min_pattern_length)

    profile = (
        PatternProfileBuilder()
        .with_theme("dark")
        .with_min_length(4)
        .build()
    )
    print("Builder profile:", profile)


if __name__ == "__main__":
    main()