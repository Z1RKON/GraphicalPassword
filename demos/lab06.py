from pathlib import Path
import tempfile
from src.patterns.lr01_builder import PatternProfileBuilder
from src.patterns.lr06_proxy import PasswordFacadeProxy

with tempfile.TemporaryDirectory() as d:
    p = PatternProfileBuilder().with_storage(Path(d) / "x.json").build()
    proxy = PasswordFacadeProxy(p, max_attempts=2)
    proxy.setup([0, 1, 2, 5])
    print(proxy.unlock([0, 3, 6, 7]))
    print(proxy.unlock([0, 3, 6, 7]))
    print(proxy.unlock([0, 1, 2, 5]))