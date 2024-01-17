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
    UnaryOp,
    Variable,
    While,
)
from wabbi.utils import Lines

# Generate a unique name like ".1", ".2", ".3", etc.
_n = 0


def gensym() -> str:
    global _n
    _n += 1
    return f".{_n}"


def generate_llvm(program: Program) -> str:
    lines = Lines()
    lines.append("declare i32 @_print_int(i32 %x)")
    for stmt in program.statements:
        out_stmt(stmt, lines)
    return "\n".join(lines)


def out_name(node: Name) -> str:
    match node:
        case GlobalName(name):
            return f"@{name}"
        case LocalName(name):
            return f"%{name}"
        case _:
            raise ValueError(f"Unexpected name: {node}")


def res_expr(node: Expression, lines: Lines) -> str:
    literals = {Integer, Name, LocalName, GlobalName}
    match node:
        case BinOp(op, lhs, rhs):
            lhs_res = res_expr(lhs, lines) if type(node) not in literals else lhs
            rhs_res = res_expr(rhs, lines) if type(node) not in literals else rhs
            id_ = gensym()
            match op:
                case "+":
                    lines.append(f"%{id_} = add i32 {lhs_res}, {rhs_res}")
                case "*":
                    lines.append(f"%{id_} = mul i32 {lhs_res}, {rhs_res}")
                case "-":
                    lines.append(f"%{id_} = sub i32 {lhs_res}, {rhs_res}")
                case "/":
                    lines.append(f"%{id_} = sdiv i32 {lhs_res}, {rhs_res}")
                case "<":
                    lines.append(f"%{id_} = icmp slt i32 {lhs_res}, {rhs_res}")
                case "==":
                    lines.append(f"%{id_} = icmp eq i32 {lhs_res}, {rhs_res}")
            return f"%{id_}"

        case UnaryOp(op, expr):
            res = res_expr(expr, lines)
            id_ = gensym()
            lines.append(f"%{id_} = sub i32 0, {res}")
            return f"%{id_}"

        case Parenthesis(expr):
            return res_expr(expr, lines)

        case Call(name, args):
            args_res = ", i32 ".join([res_expr(arg, lines) for arg in args])
            arg_types = ", ".join("i32" for _ in range(len(args)))
            id_ = gensym()

            lines.append(f"%{id_} = call i32 ({arg_types}) @{name}(i32 {args_res})")
            return f"%{id_}"

        case Integer(value):
            return str(value)

        case LocalName(value):
            id_ = gensym()
            lines.append(f"%{id_} = load i32, i32* %{value}")
            return f"%{id_}"

        case GlobalName(value):
            id_ = gensym()
            lines.append(f"%{id_} = load i32, i32* @{value}")
            return f"%{id_}"

        case _:
            raise ValueError(f"Unexpected expression: {node}")


def out_stmt(node: Statement, lines: Lines) -> None:
    match node:
        case Assignment(lhs, rhs):
            res_rhs = res_expr(rhs, lines)
            lines.append(f"store i32 {res_rhs}, i32* {out_name(lhs)}")

        case Variable(name, expr):
            raise ValueError("Unexpected Variable - AST not full compiled.")

        case GlobalVar(name):
            lines.append(f"@{name} = global i32 0")

        case LocalVar(name):
            lines.append(f"%{name} = alloca i32")

        case Print(expr):
            lines.append(f"call i32 (i32) @_print_int(i32 {res_expr(expr, lines)})")

        case While(condition, body):
            lt = gensym()
            lb = gensym()
            le = gensym()
            lines.append(f"br label %{lt}")

            lines.extend([f"{lt}:"])
            with lines.indent():
                test = res_expr(condition, lines)
                lines.append(f"br i1 {test}, label %{lb}, label %{le}")

            lines.extend([f"{lb}:"])
            with lines.indent():
                any(out_stmt(stmt, lines) for stmt in body)
                lines.append(f"br label %{lt}")

            lines.extend([f"{le}:"])

        case Branch(condition, body, else_):
            test = res_expr(condition, lines)
            lc = gensym()
            la = gensym()
            lm = gensym()

            lines.append(f"br i1 {test}, label %{lc}, label %{la}")
            lines.extend([f"{lc}:"])
            with lines.indent():
                any(out_stmt(stmt, lines) for stmt in body)
                lines.append(f"br label %{lm}")
            lines.extend([f"{la}:"])
            with lines.indent():
                any(out_stmt(stmt, lines) for stmt in else_)
                lines.append(f"br label %{lm}")
            lines.extend([f"{lm}:"])

        case Function(name, args, body):
            res_args = ", i32 %.a".join(str(n) for n in range(len(args)))
            lines.append(f"define i32 @{name}(i32 %.a{res_args}) {{")
            with lines.indent():
                for idx, arg in enumerate(args):
                    lines.append(f"%{arg} = alloca i32")
                    lines.append(f"store i32 %.a{idx}, i32* %{arg}")
                any(out_stmt(stmt, lines) for stmt in body)

            lines.append("}")

        case Return(expr):
            res = res_expr(expr, lines)
            lines.append(f"ret i32 {res}")

        case _:
            raise ValueError(f"Unexpected statement: {node}")
