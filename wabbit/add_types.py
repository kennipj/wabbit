from typing import Literal, cast

from wabbit.model import (
    BinOp,
    Call,
    FloatBinOp,
    FloatCall,
    FloatFunctionArg,
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
    IntFunctionArg,
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
    UnaryOp,
    Variable,
    VariableDecl,
)
from wabbit.walker import Visitor, Walker


class AddTypes(Visitor):
    def __init__(self, to_visit: list[type[Node]], source: str, fname: str) -> None:
        super().__init__(to_visit, source, fname)
        self._vars: dict[str, Literal["float", "int"]] = {}
        self._funcs: dict[str, Literal["float", "int"]] = {}

    def visit_binop(self, node: BinOp) -> IntBinOp | FloatBinOp:
        if isinstance(node.lhs, IntTyped):
            return IntBinOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
        elif isinstance(node.lhs, FloatTyped):
            return FloatBinOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_relationalop(self, node: RelationalOp) -> IntRelOp | FloatRelOp:
        if isinstance(node.lhs, IntTyped):
            return IntRelOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)
        elif isinstance(node.lhs, FloatTyped):
            return FloatRelOp(op=node.op, lhs=node.lhs, rhs=node.rhs, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_unaryop(self, node: UnaryOp) -> IntUnaryOp | FloatUnaryOp:
        if isinstance(node.expr, IntTyped):
            return IntUnaryOp(op=node.op, expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatUnaryOp(op=node.op, expr=node.expr, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_print(self, node: Print) -> IntPrint | FloatPrint:
        if isinstance(node.expr, IntTyped):
            return IntPrint(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatPrint(expr=node.expr, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_parenthesis(self, node: Parenthesis) -> IntParen | FloatParen:
        if isinstance(node.expr, IntTyped):
            return IntParen(expr=node.expr, loc=node.loc)
        elif isinstance(node.expr, FloatTyped):
            return FloatParen(expr=node.expr, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_variable(self, node: Variable) -> IntVariable | FloatVariable:
        if isinstance(node.expr, IntTyped):
            self._vars[node.name] = "int"
            return IntVariable(name=node.name, expr=node.expr, loc=node.loc)

        elif isinstance(node.expr, FloatTyped):
            self._vars[node.name] = "float"
            return FloatVariable(name=node.name, expr=node.expr, loc=node.loc)

        raise TypeError(f"Expected typed node. Got untyped {node}")

    def visit_variabledecl(self, node: VariableDecl) -> VariableDecl:
        if node.type_.value == "int":
            self._vars[node.name] = "int"
            return node

        elif node.type_.value == "float":
            self._vars[node.name] = "float"
            return node

        raise TypeError(f"Unexpected type {node.type_}")

    def visit_call(self, node: Call) -> IntCall | FloatCall:
        type_ = self._funcs[node.name]
        if type_ == "int":
            return IntCall(name=node.name, args=node.args, loc=node.loc)
        elif type_ == "float":
            return FloatCall(name=node.name, args=node.args, loc=node.loc)

        raise TypeError(f"Unexpected type {type_}")

    def visit_name(self, node: Name) -> IntName | FloatName:
        type_ = self._vars[node.value]
        if type_ == "int":
            return IntName(value=node.value, loc=node.loc)
        elif type_ == "float":
            return FloatName(value=node.value, loc=node.loc)

        raise TypeError(f"Unexpected type {type_}")

    def visit_functionarg(
        self, node: FunctionArg
    ) -> FunctionArg:  # IntFunctionArg | FloatFunctionArg:
        if node.type_.value == "int":
            self._vars[node.value] = "int"
            return node

        elif node.type_.value == "float":
            self._vars[node.value] = "float"
            return node

        raise TypeError(f"Unexpected type {node.type_}")

    def visit_function(self, node: Function) -> Function:
        if node.ret_type_.value == "int":
            self._funcs[node.name] = "int"
            return node

        elif node.ret_type_.value == "float":
            self._funcs[node.name] = "float"
            return node

        raise TypeError(f"Unexpected type {node.ret_type_}")


def add_types(program: Program) -> Program:
    visitor = AddTypes(
        [
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
        program.source,
        program.fname,
    )
    return cast(Program, Walker(visitor).traverse(program))
