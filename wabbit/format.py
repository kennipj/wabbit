from wabbit.model import (
    Assignment,
    BinOp,
    Boolean,
    Branch,
    Break,
    Call,
    ExprAsStatement,
    Expression,
    Float,
    Function,
    FunctionArg,
    GlobalName,
    GlobalVar,
    Integer,
    LocalName,
    LocalVar,
    LogicalOp,
    Name,
    Negation,
    Parenthesis,
    Print,
    Program,
    RelationalOp,
    Return,
    Statement,
    UnaryOp,
    Variable,
    VariableDecl,
    While,
)
from wabbit.utils import Lines


def format_program(program: Program) -> str:
    lines = Lines()
    for stmt in program.statements:
        fmt_stmt(stmt, lines)
    return "\n".join(lines)


def fmt_expr(node: Expression) -> str:
    match node:
        case LocalName():
            return f"local[{node.value}]"

        case GlobalName():
            return f"global[{node.value}]"

        case FunctionArg():
            return f"{node.value} {node.type_.value}"

        case Name():
            return node.value

        case Integer():
            return str(node.value)

        case Float():
            return str(node.value)

        case BinOp() | RelationalOp() | LogicalOp():
            return f"{fmt_expr(node.lhs)} {node.op} {fmt_expr(node.rhs)}"

        case UnaryOp():
            return f"{node.op}{fmt_expr(node.expr)}"

        case Parenthesis():
            return f"({fmt_expr(node.expr)})"

        case Call():
            formatted_args = ", ".join(fmt_expr(arg) for arg in node.args)
            return f"{node.name}({formatted_args})"

        case Boolean():
            return node.value

        case Negation():
            return f"{node.op} {fmt_expr(node.expr)}"

        case _:
            raise ValueError(f"Unexpected expression: {node}")


def fmt_stmt(node: Statement, lines: Lines) -> None:
    match node:
        case Assignment():
            lines.append(f"{fmt_expr(node.lhs)} = {fmt_expr(node.rhs)};")

        case Variable():
            lines.append(f"var {node.name} = {fmt_expr(node.expr)};")

        case GlobalVar():
            lines.append(f"global {node.name};")

        case LocalVar():
            lines.append(f"local {node.name};")

        case VariableDecl():
            lines.append(f"var {node.name} {node.type_.value};")

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
            formatted_args = ", ".join(fmt_expr(arg) for arg in node.args)
            lines.append(f"func {node.name}({formatted_args}) {node.ret_type_.value}{{")
            with lines.indent():
                any(fmt_stmt(stmt, lines) for stmt in node.body)
            lines.append("}")

        case Return():
            lines.append(f"return {fmt_expr(node.expr)};")

        case Break():
            lines.append("break;")

        case ExprAsStatement():
            lines.append(f"{node.expr};")

        case _:
            raise ValueError(f"Unexpected statement: {node}")
