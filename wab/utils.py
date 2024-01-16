from contextlib import contextmanager


class Lines(list[str]):
    def __init__(self):
        super().__init__()
        self._indentation = 0

    @contextmanager
    def indent(self):
        self._indentation += 4
        try:
            yield
        finally:
            self._indentation -= 4

    def append(self, line: str) -> None:
        indented = f"{self._indentation * ' '}{line}"
        return super().append(indented)
