def read_source(program: str) -> str:
    with open(f"wab/tests/{program}") as f:
        return f.read()
