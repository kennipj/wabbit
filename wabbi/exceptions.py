from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wabbi.tokenizer import Token


class WabbitSyntaxError(Exception):
    def __init__(
        self, msg: str, fname: str, source: str, lineno: int, column: int, length: int
    ) -> None:
        self._msg = msg
        self._err_msg = self._make_err_msg(fname, source, lineno, column, length)

    @classmethod
    def from_token(cls, msg: str, fname: str, source: str, token: "Token"):
        return WabbitSyntaxError(
            msg, fname, source, token.lineno, token.column, len(token)
        )

    def _make_err_msg(
        self, fname: str, source: str, lineno: int, column: int, length: int
    ) -> str:
        line = "  " + source.splitlines()[lineno - 1]
        point_msg = (
            "  "
            + "".join(" " for _ in range(column - 1))
            + "".join("^" for _ in range(length))
        )
        return f'File "{fname}" line {lineno} \n' + line + "\n" + point_msg + "\n"

    def __repr__(self) -> str:
        return f"WabbitSyntaxError({self._msg})"

    def __str__(self) -> str:
        return self._err_msg + f"WabbitSyntaxError: {self._msg}"
