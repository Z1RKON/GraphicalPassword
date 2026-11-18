from src.patterns.lr03_bridge_adapter import ConsoleRenderer, JsonRenderer, LegacyPatternAdapter, LegacyPatternAPI, PatternView


def main() -> None:
    view1 = PatternView(ConsoleRenderer())
    view2 = PatternView(JsonRenderer())
    pts = [0, 1, 2, 5]
    print(view1.show_validation(pts))
    print(view2.show_validation(pts))

    adapter = LegacyPatternAdapter(LegacyPatternAPI())
    print("Adapter:", adapter.validate_csv("0,1,2,5"))


if __name__ == "__main__":
    main()