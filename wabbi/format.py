from wabbi.model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    Expression,
    Function,
    GlobalName,
    GlobalVar,
    Integer,
    LocalName,
    LocalVar,
    Name,
    Parenthesis,
    Print,
    Program,
    Return,
    Statement,
    Variable,
    VariableDecl,
    While,
)
from wabbi.utils import Lines


def format_program(program: Program) -> str:
    lines = Lines()
    for stmt in program.statements:
        fmt_stmt(stmt, lines)
    return "\n".join(lines)


def fmt_expr(node: Expression) -> str:
    match node:
        case LocalName(value):
            return f"local[{value}]"

        case GlobalName(value):
            return f"global[{value}]"

        case Name(value):
            return value

        case Integer(value):
            return str(value)

        case BinOp(op, lhs, rhs):
            return f"{fmt_expr(lhs)} {op} {fmt_expr(rhs)}"

        case Parenthesis(expr):
            return f"({fmt_expr(expr)})"

        case Call(name, args):
            formatted_args = ", ".join(fmt_expr(arg) for arg in args)
            return f"{name}({formatted_args})"

        case _:
            raise ValueError(f"Unexpected expression: {node}")


def fmt_stmt(node: Statement, lines: Lines) -> None:
    match node:
        case Assignment(lhs, rhs):
            lines.append(f"{fmt_expr(lhs)} = {fmt_expr(rhs)};")

        case Variable(name, expr):
            lines.append(f"var {name} = {fmt_expr(expr)};")

        case GlobalVar(name):
            lines.append(f"global {name};")

        case LocalVar(name):
            lines.append(f"local {name};")

        case VariableDecl(name):
            lines.append(f"var {name};")

        case Print(expr):
            lines.append(f"print {fmt_expr(expr)};")

        case While(condition, body):
            lines.append(f"while {fmt_expr(condition)} {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in body)
            lines.append("}")

        case Branch(condition, body, else_):
            lines.append(f"if {fmt_expr(condition)} {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in body)

            if else_:
                lines.append("} else {")
                with lines.indent():
                    any(fmt_stmt(stmt, lines) for stmt in else_)

            lines.append("}")

        case Function(name, args):
            formatted_args = ", ".join(arg for arg in args)
            lines.append(f"func {name}({formatted_args}) {{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in node.body)
            lines.append("}")

        case Return(expr):
            lines.append(f"return {fmt_expr(expr)};")

        case _:
            raise ValueError(f"Unexpected statement: {node}")