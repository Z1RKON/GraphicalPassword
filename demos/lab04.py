from src.patterns.lr04_composite_decorator import BasePatternValidator, DotLeaf, LoggingValidatorDecorator, PatternComposite


def main() -> None:
    comp = PatternComposite()
    for i in [0, 1, 2, 5]:
        leaf = DotLeaf(i)
        leaf.activate()
        comp.add(leaf)
    print("Composite validate:", comp.validate())

    logs: list[str] = []
    dec = LoggingValidatorDecorator(BasePatternValidator(), logs)
    print(dec.validate([0, 1, 2, 5]))
    print("Decorator log:", logs)


if __name__ == "__main__":
    main()