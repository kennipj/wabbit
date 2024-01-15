from contextlib import contextmanager

from model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    Expression,
    Function,
    Integer,
    Name,
    Parenthesis,
    Print,
    Program,
    Return,
    Statement,
    Variable,
    While,
)


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


def fmt_expr(node: Expression) -> str:
    match node:
        case Name():
            return node.value
        case Integer():
            return str(node.value)
        case BinOp():
            return f"{fmt_expr(node.lhs)} {node.op} {fmt_expr(node.rhs)}"
        case Parenthesis():
            return f"({fmt_expr(node.expr)})"
        case Call():
            args = ", ".join(fmt_expr(arg) for arg in node.args)
            return f"{fmt_expr(node.name)}({args})"
        case _:
            raise ValueError(f"Unexpected expression: {node}")


def fmt_stmt(node: Statement, lines: Lines) -> None:
    match node:
        case Assignment():
            lines.append(f"{fmt_expr(node.lhs)} = {fmt_expr(node.rhs)};")
        case Variable():
            lines.append(f"var {fmt_expr(node.name)} = {fmt_expr(node.expr)};")
        case Print():
            lines.append(f"print {fmt_expr(node.expr)};")
        case While():
            lines.append(f"while {fmt_expr(node.condition)} {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in node.body)
            lines.append("}")
        case Branch():
            lines.append(f"if {fmt_expr(node.condition)} {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in node.body)

            if node.else_:
                lines.append("} else {")
                with lines.indent():
                    any(fmt_stmt(stmt, lines) for stmt in node.else_)

            lines.append("}")
        case Function():
            args = ", ".join(fmt_expr(arg) for arg in node.args)
            lines.append(f"func {fmt_expr(node.name)}({args}) {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in node.body)
            lines.append("}")
        case Return():
            lines.append(f"return {fmt_expr(node.expr)};")
        case _:
            raise ValueError(f"Unexpected statement: {node}")


def format_program(program: Program) -> str:
    lines = Lines()
    for stmt in program.statements:
        fmt_stmt(stmt, lines)
    return "\n".join(lines)
