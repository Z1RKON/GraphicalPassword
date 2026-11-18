from src.patterns.lr02_factory_prototype import PatternTemplate, RelaxedValidatorCreator, StrictValidatorCreator


def main() -> None:
    strict = StrictValidatorCreator().create_validator()
    relaxed = RelaxedValidatorCreator().create_validator()
    print("Factory strict:", strict.validate([0, 1, 2, 5]))
    print("Factory relaxed:", relaxed.validate([0, 1, 2]))

    tpl = PatternTemplate("home", [0, 1, 2, 5])
    clone = tpl.clone()
    clone.points.append(8)
    print("Prototype clone diff:", tpl.points, clone.points)


if __name__ == "__main__":
    main()