from pathlib import Path
import tempfile

import pytest

from src.patterns.lr01_builder import PatternProfileBuilder
from src.patterns.lr01_singleton import SecuritySettingsRegistry
from src.patterns.lr02_factory_prototype import PatternTemplate, StrictValidatorCreator
from src.patterns.lr03_bridge_adapter import LegacyPatternAdapter, LegacyPatternAPI, PatternView, JsonRenderer
from src.patterns.lr04_composite_decorator import DotLeaf, LoggingValidatorDecorator, PatternComposite, BasePatternValidator
from src.patterns.lr05_facade_flyweight import DotFlyweightFactory, GraphicalPasswordFacade


@pytest.fixture(autouse=True)
def _reset_singleton():
    SecuritySettingsRegistry.reset_for_tests()
    yield
    SecuritySettingsRegistry.reset_for_tests()


def test_lr01_singleton_and_builder():
    assert SecuritySettingsRegistry() is SecuritySettingsRegistry()
    p = PatternProfileBuilder().with_min_length(4).build()
    assert p.min_length == 4


def test_lr02_factory_and_prototype():
    v = StrictValidatorCreator().create_validator()
    assert v.validate([0, 1, 2, 5]).ok
    t = PatternTemplate("a", [1, 2, 3])
    c = t.clone()
    assert c.points == t.points and c is not t


def test_lr03_bridge_and_adapter():
    assert "points" in PatternView(JsonRenderer()).show_validation([0, 1, 2, 5])
    assert LegacyPatternAdapter(LegacyPatternAPI()).validate_csv("0,1,2,5").ok


def test_lr04_composite_decorator():
    comp = PatternComposite()
    for i in (0, 1, 2, 5):
        d = DotLeaf(i)
        d.activate()
        comp.add(d)
    assert comp.validate().ok
    log: list[str] = []
    assert LoggingValidatorDecorator(BasePatternValidator(), log).validate([0, 1, 2, 5]).ok
    assert len(log) == 2


def test_lr05_facade_flyweight():
    with tempfile.TemporaryDirectory() as d:
        profile = PatternProfileBuilder().with_storage(Path(d) / "x.json").build()
        f = GraphicalPasswordFacade(profile)
        DotFlyweightFactory.get_dot(0)
        DotFlyweightFactory.get_dot(0)
        assert DotFlyweightFactory.pool_size() == 1
        assert f.setup([0, 1, 2, 5])[0]
        assert f.unlock([0, 1, 2, 5])[0]