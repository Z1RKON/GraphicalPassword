from concurrent.futures import wait
from pathlib import Path
import tempfile

from src.patterns.lr06_proxy import PasswordFacadeProxy
from src.patterns.lr07_command_iterator import GridIterator, PatternPathIterator, SetupPasswordCommand
from src.patterns.lr08_chain import ValidationContext, build_validation_chain
from src.patterns.lr09_mediator_memento import PatternInputMediator
from src.patterns.lr10_observer_state import AuditLogObserver, LockContext, SetupState
from src.patterns.lr11_strategy_template import Sha256Strategy, StrictLengthTemplate
from src.patterns.lr12_mvc import PatternController, PatternModel, PatternView
from src.patterns.lr13_circuit_breaker import BreakerState, UnlockCircuitBreaker
from src.patterns.lr14_repository import JsonFilePasswordRepository
from src.patterns.lr15_future import PatternVerifyPromise
from src.patterns.lr01_builder import PatternProfileBuilder
from src.patterns.lr05_facade_flyweight import GraphicalPasswordFacade


def test_lr06_proxy():
    with tempfile.TemporaryDirectory() as d:
        p = PatternProfileBuilder().with_storage(Path(d) / "x.json").build()
        proxy = PasswordFacadeProxy(p, max_attempts=1)
        proxy.setup([0, 1, 2, 5])
        assert not proxy.unlock([1, 2, 3, 4])[0]
        assert "заблокирован" in proxy.unlock([0, 1, 2, 5])[1].lower()


def test_lr07_command_iterator():
    with tempfile.TemporaryDirectory() as d:
        f = GraphicalPasswordFacade(PatternProfileBuilder().with_storage(Path(d) / "a.json").build())
        assert "SETUP" in SetupPasswordCommand(f, [0, 1, 2, 5]).execute()
        assert list(GridIterator()) == list(range(9))
        assert list(PatternPathIterator([0, 1, 2])) == [0, 1, 2]


def test_lr08_chain():
    chain = build_validation_chain()
    assert not chain.handle(ValidationContext([])).ok
    assert chain.handle(ValidationContext([0, 1, 2, 5])).ok


def test_lr09_mediator_memento():
    m = PatternInputMediator()
    for p in [0, 1, 2, 5]:
        m.dot_selected(p)
    snap = m.save()
    m.clear()
    m.restore(snap)
    assert m.points == [0, 1, 2, 5]


def test_lr10_observer_state():
    with tempfile.TemporaryDirectory() as d:
        f = GraphicalPasswordFacade(PatternProfileBuilder().with_storage(Path(d) / "a.json").build())
        ctx = LockContext(f)
        log = AuditLogObserver()
        ctx.subject.attach(log)
        assert isinstance(ctx.state, SetupState)
        ctx.state.on_setup(ctx)
        assert "password_configured" in log.events


def test_lr11_strategy_template():
    h = Sha256Strategy().hash_pattern((0, 1, 2, 5), "s")
    assert len(h) == 64
    assert StrictLengthTemplate().validate([0, 1, 2, 5]).ok


def test_lr12_mvc():
    ctrl = PatternController(PatternModel(), PatternView())
    out = ctrl.action_setup([0, 1, 2, 5])
    assert "VIEW" in out


def test_lr13_circuit_breaker():
    br = UnlockCircuitBreaker(2)
    assert br.state == BreakerState.CLOSED
    br.call_unlock(lambda p: (False, "x"), [0, 1, 2, 3])
    br.call_unlock(lambda p: (False, "x"), [0, 1, 2, 3])
    assert br.state == BreakerState.OPEN


def test_lr14_repository():
    with tempfile.TemporaryDirectory() as d:
        repo = JsonFilePasswordRepository(Path(d) / "db.json")
        repo.save("abc")
        assert repo.load().pattern_hash == "abc"
        repo.delete()
        assert repo.load().pattern_hash is None


def test_lr15_future():
    with tempfile.TemporaryDirectory() as d:
        f = GraphicalPasswordFacade(PatternProfileBuilder().with_storage(Path(d) / "a.json").build())
        f.setup([0, 1, 2, 5])
        promise = PatternVerifyPromise()
        fut = promise.submit_verify(f.unlock, [0, 1, 2, 5])
        wait([fut])
        assert fut.result()[0]
        promise.shutdown()