from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wabbit.model import SourceLoc
    from wabbit.tokenizer import Token


class WabbitError:
    def __init__(
        self, msg: str, fname: str, source: str, lineno: int, start: int, end: int
    ) -> None:
        self.lineno = lineno
        self.start = start
        self.end = end
        self._msg = msg
        self._err_msg = self._make_err_msg(fname, source)

    def _make_err_msg(self, fname: str, source: str) -> str:
        line = "  " + source.splitlines()[self.lineno - 1]
        point_msg = (
            "  "
            + "".join(" " for _ in range(self.start - 1))
            + "".join("^" for _ in range(self.end - self.start))
        )
        return f'File "{fname}" line {self.lineno} \n' + line + "\n" + point_msg + "\n"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._msg})"

    def __str__(self) -> str:
        return self._err_msg + f"{self.__class__.__name__}: {self._msg}\n"


class WabbitTypeError(WabbitError):
    def __init__(self, msg: str, fname: str, source: str, loc: "SourceLoc") -> None:
        self.lineno = loc.lineno
        self.start = loc.start
        self.end = loc.end
        self._msg = msg
        self._err_msg = self._make_err_msg(fname, source)


class WabbitSyntaxError(WabbitError):
    @classmethod
    def from_token(cls, msg: str, fname: str, source: str, token: "Token"):
        return WabbitSyntaxError(
            msg, fname, source, token.lineno, token.column, token.column + len(token)
        )

    @classmethod
    def from_loc(cls, msg: str, fname: str, source: str, loc: "SourceLoc"):
        return WabbitSyntaxError(msg, fname, source, loc.lineno, loc.start, loc.end)
