from dataclasses import dataclass
from typing import Literal

from wabbit.exceptions import WabbitSyntaxError


class IntTyped:
    ...


class FloatTyped:
    ...


class Numeric:
    value: int | float


@dataclass
class SourceLoc:
    lineno: int
    start: int
    end: int


@dataclass
class Node:
    loc: SourceLoc


@dataclass
class Statement(Node):
    ...


@dataclass
class Expression(Node):
    ...


@dataclass
class Type(Node):
    value: Literal["int", "float"]


@dataclass
class Name(Expression):
    value: str


@dataclass
class IntName(Name, IntTyped):
    ...


@dataclass
class FloatName(Name, FloatTyped):
    ...


@dataclass
class Integer(Expression, IntTyped, Numeric):
    value: int


@dataclass
class Float(Expression, FloatTyped, Numeric):
    value: float


@dataclass
class BooleanExpression(Expression):
    ...


@dataclass
class BinOp(Expression):
    op: Literal["+", "*", "-", "/"]
    lhs: Expression
    rhs: Expression


@dataclass
class IntBinOp(BinOp, IntTyped):
    ...


@dataclass
class FloatBinOp(BinOp, FloatTyped):
    ...


@dataclass
class RelationalOp(BooleanExpression):
    op: Literal["==", "<", ">", "<=", ">=", "!="]
    lhs: Expression
    rhs: Expression


@dataclass
class IntRelOp(RelationalOp, IntTyped):
    ...


@dataclass
class FloatRelOp(RelationalOp, FloatTyped):
    ...


@dataclass
class Assignment(Statement):
    lhs: Name
    rhs: Expression


@dataclass
class Variable(Statement):
    name: str
    expr: Expression


@dataclass
class IntVariable(Variable, IntTyped):
    name: str


@dataclass
class FloatVariable(Variable, FloatTyped):
    name: str


@dataclass
class VariableDecl(Statement):
    name: str
    type_: Type


@dataclass
class Print(Statement):
    expr: Expression


@dataclass
class IntPrint(Print, IntTyped):
    ...


@dataclass
class FloatPrint(Print, FloatTyped):
    ...


@dataclass
class Parenthesis(Expression):
    expr: Expression


@dataclass
class IntParen(Parenthesis, IntTyped):
    ...


@dataclass
class FloatParen(Parenthesis, FloatTyped):
    ...


@dataclass
class While(Statement):
    condition: Expression
    body: list[Statement]


@dataclass
class Branch(Statement):
    condition: Expression
    body: list[Statement]
    else_: list[Statement]


@dataclass
class FunctionArg(Name):
    type_: Type


@dataclass
class FloatFunctionArg(FunctionArg, FloatTyped):
    ...


@dataclass
class IntFunctionArg(FunctionArg, IntTyped):
    ...


@dataclass
class Function(Statement):
    name: str
    args: list[FunctionArg]
    body: list[Statement]
    ret_type_: Type


@dataclass
class Return(Statement):
    expr: Expression


@dataclass
class Call(Expression):
    name: str
    args: list[Expression]


@dataclass
class IntCall(Call, IntTyped):
    ...


@dataclass
class FloatCall(Call, FloatTyped):
    ...


@dataclass
class LocalVar(VariableDecl):
    ...


@dataclass
class GlobalVar(VariableDecl):
    ...


@dataclass
class LocalName(Name):
    ...


@dataclass
class IntLocalName(LocalName, IntTyped):
    ...


@dataclass
class FloatLocalName(LocalName, FloatTyped):
    ...


@dataclass
class GlobalName(Name):
    ...


@dataclass
class IntGlobalName(GlobalName, IntTyped):
    ...


@dataclass
class FloatGlobalName(GlobalName, FloatTyped):
    ...


@dataclass
class UnaryOp(Expression):
    op: Literal["-"]
    expr: Expression


@dataclass
class IntUnaryOp(UnaryOp, IntTyped):
    ...


@dataclass
class FloatUnaryOp(UnaryOp, FloatTyped):
    ...


@dataclass
class ExprAsStatement(Statement):
    expr: Expression


@dataclass
class Boolean(BooleanExpression):
    value: Literal["true", "false"]


@dataclass
class LogicalOp(BooleanExpression):
    op: Literal["and", "or"]
    lhs: BooleanExpression
    rhs: BooleanExpression


@dataclass
class Negation(BooleanExpression):
    op: Literal["not"]
    expr: BooleanExpression


@dataclass
class Break(Statement):
    ...


@dataclass
class ErrorExpr(Expression):
    err: WabbitSyntaxError


@dataclass
class Program(Node):
    statements: list[Statement]
    source: str
    fname: str = "file.wb"
