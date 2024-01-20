from typing import Literal, cast

from wabbit.exceptions import WabbitTypeError
from wabbit.model import (
    BinOp,
    BoolCall,
    BoolName,
    BoolParen,
    BoolPrint,
    BoolRelOp,
    BoolTyped,
    BoolVariable,
    Call,
    CharCall,
    CharName,
    CharPrint,
    CharTyped,
    CharVariable,
    ErrorExpr,
    Expression,
    FloatBinOp,
    FloatCall,
    FloatName,
    FloatParen,
    FloatPrint,
    FloatRelOp,
    FloatTyped,
    FloatUnaryOp,
    FloatVariable,
    Function,
    FunctionArg,
    IntBinOp,
    IntCall,
    IntName,
    IntParen,
    IntPrint,
    IntRelOp,
    IntTyped,
    IntUnaryOp,
    IntVariable,
    Name,
    Node,
    Parenthesis,
    Print,
    Program,
    RelationalOp,
    SourceLoc,
    UnaryOp,
    Variable,
    VariableDecl,
)
from wabbit.walker import Visitor, Walker


class AddTypes(Visitor):
    def __init__(
        self,
        to_visit: list[type[Node]],
        pre_visit: list[type[Node]],
        source: str,
        fname: str,
    ) -> None:
        super().__init__(to_visit, pre_visit, source, fname)
        self._globals: dict[str, Literal["float", "int", "char", "bool"]] = {}
        self._funcs: dict[str, dict] = {}
        self._locals: dict[str, Literal["float", "int", "char", "bool"]] = {}
        self._in_scope = False

    def visit_binop(self, node: BinOp) -> Expression:
        match (node.lhs, node.rhs):
            case (IntTyped(), IntTyped()):
                return IntBinOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
            case (FloatTyped(), FloatTyped()):
                return FloatBinOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
            case _:
                return ErrorExpr(
                    loc=node.loc,
                    err=WabbitTypeError(
                        msg=(
                            f"Operator {node.op} not supported for types "
                            f'"{_type(node.lhs)}" and "{_type(node.rhs)}"'
                        ),
                        fname=self.fname,
                        source=self.source,
                        loc=node.loc,
                    ),
                )

    def visit_relationalop(self, node: RelationalOp) -> Expression:
        match (node.lhs, node.rhs):
            case (IntTyped(), IntTyped()):
                return IntRelOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
            case (FloatTyped(), FloatTyped()):
                return FloatRelOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
            case (BoolTyped(), BoolTyped()):
                return BoolRelOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
            case _:
                return ErrorExpr(
                    loc=node.loc,
                    err=WabbitTypeError(
                        msg=(
                            f"Operator {node.op} not supported for types "
                            f'"{_type(node.lhs)}" and "{_type(node.rhs)}"'
                        ),
                        fname=self.fname,
                        source=self.source,
                        loc=node.loc,
                    ),
                )

    def visit_unaryop(self, node: UnaryOp) -> Expression:
        if isinstance(node.expr, IntTyped):
            return IntUnaryOp(op=node.op, expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatUnaryOp(op=node.op, expr=node.expr, loc=node.loc)

        return ErrorExpr(
            loc=node.loc,
            err=WabbitTypeError(
                msg=f'Operator {node.op} not supported for type "{_type(node.expr)}".',
                fname=self.fname,
                source=self.source,
                loc=node.loc,
            ),
        )

    def visit_print(self, node: Print) -> Print:
        if isinstance(node.expr, IntTyped):
            return IntPrint(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatPrint(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, CharTyped):
            return CharPrint(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, BoolTyped):
            return BoolPrint(expr=node.expr, loc=node.loc)
        return node

    def visit_parenthesis(self, node: Parenthesis) -> Expression:
        if isinstance(node.expr, IntTyped):
            return IntParen(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatParen(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, BoolTyped):
            return BoolParen(expr=node.expr, loc=node.loc)

        return ErrorExpr(
            loc=node.loc,
            err=WabbitTypeError(
                msg=f'Parenthesis not supported for type"{_type(node.expr)}".',
                fname=self.fname,
                source=self.source,
                loc=node.loc,
            ),
        )

    def visit_variable(self, node: Variable) -> Variable:
        name = node.name
        if name in self._locals or name in self._globals:
            expr = ErrorExpr(
                loc=node.loc,
                err=WabbitTypeError(
                    msg=f"Redeclaration of existing variable `{node.name}`.",
                    fname=self.fname,
                    source=self.source,
                    loc=node.loc,
                ),
            )
        else:
            expr = node.expr

        to_update = self._locals if self._in_scope else self._globals
        if isinstance(node.expr, IntTyped):
            to_update[node.name] = "int"
            return IntVariable(name=node.name, expr=expr, loc=node.loc)

        elif isinstance(node.expr, FloatTyped):
            to_update[node.name] = "float"
            return FloatVariable(name=node.name, expr=expr, loc=node.loc)

        elif isinstance(node.expr, CharTyped):
            to_update[node.name] = "char"
            return CharVariable(name=node.name, expr=expr, loc=node.loc)

        elif isinstance(node.expr, BoolTyped):
            to_update[node.name] = "bool"
            return BoolVariable(name=node.name, expr=expr, loc=node.loc)

        return node

    def visit_variabledecl(self, node: VariableDecl) -> VariableDecl:
        if self._in_scope:
            self._locals[node.name] = node.type_.value
        else:
            self._globals[node.name] = node.type_.value
        return node
        # if node.type_.value == "int":
        #     self._vars[node.name] = "int"
        #     return node

        # elif node.type_.value == "float":
        #     self._vars[node.name] = "float"
        #     return node

        # elif node.type_.value == "char":
        #     self._vars[node.name] = "char"
        #     return node

        # elif node.type_.value == "char":
        #     self._vars[node.name] = "char"
        #     return node

        # raise TypeError(f"Unexpected type {node.type_}")

    def visit_call(self, node: Call) -> Expression:
        func = self._funcs.get(node.name)
        if not func:
            return ErrorExpr(
                err=WabbitTypeError(
                    msg=f'"{node.name}" is not defined.',
                    fname=self.fname,
                    source=self.source,
                    loc=node.loc,
                ),
                loc=node.loc,
            )

        ret_type_ = func["ret"]
        args = self._funcs[node.name]["args"]
        if len(args) != len(node.args):
            return ErrorExpr(
                err=WabbitTypeError(
                    msg=(
                        f'"{node.name}" expects {len(args)} arguments, but '
                        f"received {len(node.args)} arguments."
                    ),
                    fname=self.fname,
                    source=self.source,
                    loc=SourceLoc(
                        lineno=node.args[0].loc.lineno,
                        start=node.args[0].loc.start,
                        end=node.args[-1].loc.end,
                    )
                    if len(node.args) > 0
                    else node.loc,
                ),
                loc=node.loc,
            )
        new_args = []
        for idx, arg in enumerate(node.args):
            param_type = args[idx].type_.value
            param_name = args[idx].value

            if not (type_ := _type(arg)) == param_type:
                new_args.append(
                    ErrorExpr(
                        loc=node.loc,
                        err=WabbitTypeError(
                            msg=(
                                f'Argument of type "{type_}" cannot be assigned '
                                f'to parameter "{param_name}" of type "{param_type}"'
                                f' in function "{node.name}"'
                            ),
                            fname=self.fname,
                            source=self.source,
                            loc=arg.loc,
                        ),
                    )
                )
            else:
                new_args.append(arg)
        if ret_type_ == "int":
            return IntCall(name=node.name, args=new_args, loc=node.loc)
        elif ret_type_ == "float":
            return FloatCall(name=node.name, args=new_args, loc=node.loc)
        elif ret_type_ == "bool":
            return BoolCall(name=node.name, args=new_args, loc=node.loc)
        else:
            return CharCall(name=node.name, args=new_args, loc=node.loc)

    def visit_name(self, node: Name) -> Expression:
        if self._in_scope:
            type_ = self._locals.get(node.value)
            if not type_:
                type_ = self._globals.get(node.value)
        else:
            type_ = self._globals.get(node.value)
        if not type_:
            return ErrorExpr(
                err=WabbitTypeError(
                    msg=f'"{node.value}" is not defined.',
                    fname=self.fname,
                    source=self.source,
                    loc=node.loc,
                ),
                loc=node.loc,
            )
        if type_ == "int":
            return IntName(value=node.value, loc=node.loc)
        elif type_ == "float":
            return FloatName(value=node.value, loc=node.loc)
        elif type_ == "bool":
            return BoolName(value=node.value, loc=node.loc)
        else:
            return CharName(value=node.value, loc=node.loc)

    def visit_functionarg(self, node: FunctionArg) -> FunctionArg:
        self._locals[node.value] = node.type_.value
        return node

    def visit_function(self, node: Function) -> Function:
        arg_types = [arg for arg in node.args]
        self._funcs[node.name] = {"args": arg_types, "ret": node.ret_type_.value}
        if self._in_scope:
            self._locals = {}
        self._in_scope = not self._in_scope
        return node


def add_types(program: Program) -> Program:
    visitor = AddTypes(
        to_visit=[
            BinOp,
            RelationalOp,
            Name,
            Call,
            VariableDecl,
            Variable,
            Parenthesis,
            FunctionArg,
            Function,
            Print,
            UnaryOp,
        ],
        pre_visit=[
            Function,
        ],
        source=program.source,
        fname=program.fname,
    )
    return cast(Program, Walker(visitor).traverse(program))


def _type(node) -> Literal["int", "float", "char", "bool", "unknown"]:
    if isinstance(node, IntTyped):
        return "int"
    elif isinstance(node, FloatTyped):
        return "float"
    elif isinstance(node, CharTyped):
        return "char"
    elif isinstance(node, BoolTyped):
        return "char"
    else:
        return "unknown"
