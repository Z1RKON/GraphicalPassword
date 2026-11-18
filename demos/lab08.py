from src.patterns.lr08_chain import ValidationContext, build_validation_chain

chain = build_validation_chain()
for pts in [[], [0, 9], [0, 1, 2], [0, 1, 2, 5]]:
    r = chain.handle(ValidationContext(list(pts)))
    print(pts, "->", r.ok, r.message)