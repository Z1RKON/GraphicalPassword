"""Демо ЛР5: Facade + Flyweight."""

from pathlib import Path
import tempfile

from src.patterns.lr01_builder import PatternProfileBuilder
from src.patterns.lr05_facade_flyweight import DotFlyweightFactory, GraphicalPasswordFacade


def main() -> None:
    with tempfile.TemporaryDirectory() as d:
        profile = PatternProfileBuilder().with_storage(Path(d) / "p.json").build()
        app = GraphicalPasswordFacade(profile)
        print("Flyweight pool:", app.describe_grid(), "size=", DotFlyweightFactory.pool_size())
        print(app.setup([0, 1, 2, 5]))
        print(app.unlock([0, 1, 2, 5]))
        print(app.unlock([0, 3, 6, 7]))


if __name__ == "__main__":
    main()