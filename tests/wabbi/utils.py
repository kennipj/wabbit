def read_source(program: str) -> str:
    with open(f"wabbi/tests/{program}") as f:
        return f.read()
