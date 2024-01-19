from wabbit.model import (
    Assignment,
    Boolean,
    Branch,
    Break,
    Char,
    CharGlobalName,
    CharLocalName,
    CharPrint,
    CharTyped,
    ExprAsStatement,
    Expression,
    Float,
    FloatBinOp,
    FloatCall,
    FloatGlobalName,
    FloatLocalName,
    FloatPrint,
    FloatRelOp,
    FloatTyped,
    FloatUnaryOp,
    Function,
    GlobalName,
    GlobalVar,
    IntBinOp,
    IntCall,
    Integer,
    IntGlobalName,
    IntLocalName,
    IntPrint,
    IntRelOp,
    IntTyped,
    IntUnaryOp,
    LocalName,
    LocalVar,
    LogicalOp,
    Name,
    Negation,
    Parenthesis,
    Program,
    Return,
    Statement,
    While,
)
from wabbit.utils import Lines

# Generate a unique name like ".1", ".2", ".3", etc.
_n = 0


types = {
    "int": "i32",
    "float": "double",
}


def gensym() -> str:
    global _n
    _n += 1
    return f".{_n}"


def generate_llvm(program: Program) -> str:
    lines = Lines()
    lines.append("declare i32 @_print_int(i32 %x)")
    lines.append("declare double @_print_float(double %x)")
    lines.append("declare i32 @_print_char(i32 %x)")
    for stmt in program.statements:
        out_stmt(stmt, lines)
    return "\n".join(lines)


def out_name(node: Name) -> str:
    match node:
        case GlobalName():
            return f"@{node.value}"
        case LocalName():
            return f"%{node.value}"
        case _:
            raise ValueError(f"Unexpected name: {node}")


def res_expr(node: Expression, lines: Lines) -> str:
    literals = {Integer, Name, LocalName, GlobalName}
    match node:
        case LogicalOp():
            lhs_res = res_expr(node.lhs, lines)
            rhs_res = res_expr(node.rhs, lines)
            id_ = gensym()
            lines.append(f"%{id_} = {node.op} i1 {lhs_res}, {rhs_res}")
            return f"%{id_}"

        case Negation():
            res = res_expr(node.expr, lines)
            id_ = gensym()
            lines.append(f"%{id_} = xor i1 1, {res}")
            return f"%{id_}"

        case IntBinOp() | IntRelOp():
            lhs_res = (
                res_expr(node.lhs, lines) if type(node) not in literals else node.lhs
            )
            rhs_res = (
                res_expr(node.rhs, lines) if type(node) not in literals else node.rhs
            )
            id_ = gensym()
            match node.op:
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
                case ">":
                    lines.append(f"%{id_} = icmp sgt i32 {lhs_res}, {rhs_res}")
                case "<=":
                    lines.append(f"%{id_} = icmp sle i32 {lhs_res}, {rhs_res}")
                case ">=":
                    lines.append(f"%{id_} = icmp sge i32 {lhs_res}, {rhs_res}")
                case "==":
                    lines.append(f"%{id_} = icmp eq i32 {lhs_res}, {rhs_res}")
                case "!=":
                    lines.append(f"%{id_} = icmp ne i32 {lhs_res}, {rhs_res}")
            return f"%{id_}"

        case FloatBinOp() | FloatRelOp():
            lhs_res = (
                res_expr(node.lhs, lines) if type(node) not in literals else node.lhs
            )
            rhs_res = (
                res_expr(node.rhs, lines) if type(node) not in literals else node.rhs
            )
            id_ = gensym()
            match node.op:
                case "+":
                    lines.append(f"%{id_} = fadd double {lhs_res}, {rhs_res}")
                case "*":
                    lines.append(f"%{id_} = fmul double {lhs_res}, {rhs_res}")
                case "-":
                    lines.append(f"%{id_} = fsub double {lhs_res}, {rhs_res}")
                case "/":
                    lines.append(f"%{id_} = fdiv double {lhs_res}, {rhs_res}")
                case "<":
                    lines.append(f"%{id_} = fcmp olt double {lhs_res}, {rhs_res}")
                case ">":
                    lines.append(f"%{id_} = fcmp ogt double {lhs_res}, {rhs_res}")
                case "<=":
                    lines.append(f"%{id_} = fcmp ole double {lhs_res}, {rhs_res}")
                case ">=":
                    lines.append(f"%{id_} = fcmp oge double {lhs_res}, {rhs_res}")
                case "==":
                    lines.append(f"%{id_} = fcmp oeq double {lhs_res}, {rhs_res}")
                case "!=":
                    lines.append(f"%{id_} = fcmp one double {lhs_res}, {rhs_res}")
            return f"%{id_}"

        case Boolean():
            return "1" if node.value == "true" else "0"

        case IntUnaryOp():
            res = res_expr(node.expr, lines)
            id_ = gensym()
            lines.append(f"%{id_} = sub i32 0, {res}")
            return f"%{id_}"

        case FloatUnaryOp():
            res = res_expr(node.expr, lines)
            id_ = gensym()
            lines.append(f"%{id_} = fsub double 0.0, {res}")
            return f"%{id_}"

        case Parenthesis():
            return res_expr(node.expr, lines)

        case IntCall():
            args_res = ", ".join([f"i32 {res_expr(arg, lines)}" for arg in node.args])
            arg_types = ", ".join("i32" for _ in range(len(node.args)))
            id_ = gensym()

            lines.append(f"%{id_} = call i32 ({arg_types}) @{node.name}({args_res})")
            return f"%{id_}"

        case FloatCall():
            args_res = ", ".join(
                [f"double {res_expr(arg, lines)}" for arg in node.args]
            )
            arg_types = ", ".join("double" for _ in range(len(node.args)))
            id_ = gensym()

            lines.append(f"%{id_} = call double ({arg_types}) @{node.name}({args_res})")
            return f"%{id_}"

        case IntLocalName() | CharLocalName():
            id_ = gensym()
            lines.append(f"%{id_} = load i32, i32* %{node.value}")
            return f"%{id_}"

        case FloatLocalName():
            id_ = gensym()
            lines.append(f"%{id_} = load double, double* %{node.value}")
            return f"%{id_}"

        case IntGlobalName() | CharGlobalName():
            id_ = gensym()
            lines.append(f"%{id_} = load i32, i32* @{node.value}")
            return f"%{id_}"

        case FloatGlobalName():
            id_ = gensym()
            lines.append(f"%{id_} = load double, double* @{node.value}")
            return f"%{id_}"

        case Integer():
            return str(node.value)

        case Float():
            return str(node.value)

        case Char():
            return str(ord(node.value))

        case _:
            raise ValueError(f"Unexpected expression: {node}")


def out_stmt(node: Statement, lines: Lines, break_to: str | None = None) -> None:
    match node:
        case Assignment():
            res_rhs = res_expr(node.rhs, lines)
            if isinstance(node.rhs, (IntTyped, CharTyped)):
                lines.append(f"store i32 {res_rhs}, i32* {out_name(node.lhs)}")
                return

            elif isinstance(node.rhs, FloatTyped):
                lines.append(f"store double {res_rhs}, double* {out_name(node.lhs)}")
                return

            raise ValueError(f"Untyped expression! {node.rhs}")

        case GlobalVar():
            if node.type_.value in {"int", "char"}:
                lines.append(f"@{node.name} = global i32 0")
                return

            elif node.type_.value == "float":
                lines.append(f"@{node.name} = global double 0.0")
                return

            raise ValueError(f"Unknown type: {node.type_.value}")

        case LocalVar():
            if node.type_.value in {"int", "char"}:
                lines.append(f"%{node.name} = alloca i32")
                return
            elif node.type_.value == "float":
                lines.append(f"%{node.name} = alloca double")
                return

            raise ValueError(f"Unknown type: {node.type_.value}")

        case IntPrint():
            lines.append(
                f"call i32 (i32) @_print_int(i32 {res_expr(node.expr, lines)})"
            )

        case FloatPrint():
            lines.append(
                f"call double (double) @_print_float(double {res_expr(node.expr, lines)})"
            )

        case CharPrint():
            lines.append(
                f"call i32 (i32) @_print_char(i32 {res_expr(node.expr, lines)})"
            )

        case While():
            lt = gensym()
            lb = gensym()
            le = gensym()
            lines.append(f"br label %{lt}")

            lines.extend([f"{lt}:"])
            with lines.indent():
                test = res_expr(node.condition, lines)
                lines.append(f"br i1 {test}, label %{lb}, label %{le}")

            lines.extend([f"{lb}:"])
            with lines.indent():
                any(out_stmt(stmt, lines, break_to=le) for stmt in node.body)
                lines.append(f"br label %{lt}")

            lines.extend([f"{le}:"])

        case Branch():
            test = res_expr(node.condition, lines)
            lc = gensym()
            la = gensym()
            lm = gensym()

            lines.append(f"br i1 {test}, label %{lc}, label %{la}")
            lines.extend([f"{lc}:"])
            with lines.indent():
                any(out_stmt(stmt, lines, break_to=break_to) for stmt in node.body)
                lines.append(f"br label %{lm}")
            lines.extend([f"{la}:"])
            with lines.indent():
                any(out_stmt(stmt, lines, break_to=break_to) for stmt in node.else_)
                lines.append(f"br label %{lm}")
            lines.extend([f"{lm}:"])

        case Function():
            res_args = ", ".join(
                f"{types[arg.type_.value]} %.a{idx}"
                for idx, arg in enumerate(node.args)
            )
            ret_type = types[node.ret_type_.value]
            lines.append(f"define {ret_type} @{node.name}({res_args}) {{")
            with lines.indent():
                for idx, arg in enumerate(node.args):
                    t = arg.type_.value
                    lines.append(f"%{arg.value} = alloca {types[t]}")
                    lines.append(f"store {types[t]} %.a{idx}, {types[t]}* %{arg.value}")
                any(out_stmt(stmt, lines) for stmt in node.body)
                lines.append(f"ret {ret_type} {'0' if ret_type == 'i32' else '0.0'}")

            lines.append("}")

        case Break():
            if not break_to:
                raise SyntaxError("Break used outside of loop!")
            lines.append(f"br label %{break_to}")

        case Return():
            res = res_expr(node.expr, lines)
            if isinstance(node.expr, IntTyped):
                lines.append(f"ret i32 {res}")
                return
            elif isinstance(node.expr, FloatTyped):
                lines.append(f"ret double {res}")
                return

            raise ValueError(f"Untyped expression! {node.expr}")

        case ExprAsStatement():
            res_expr(node.expr, lines)

        case _:
            raise ValueError(f"Unexpected statement: {node}")
