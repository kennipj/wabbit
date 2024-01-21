from dataclasses import dataclass
from typing import Literal

from wabbit.exceptions import WabbitError


class UnknownType:
    ...


class IntTyped:
    ...


class BoolTyped:
    ...


class FloatTyped:
    ...


class CharTyped:
    ...


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
    value: Literal["int", "float", "char", "bool"]


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
class CharName(Name, CharTyped):
    ...


@dataclass
class BoolName(Name, BoolTyped):
    ...


@dataclass
class Integer(Expression, IntTyped):
    value: int


@dataclass
class Float(Expression, FloatTyped):
    value: str


@dataclass
class Char(Expression, CharTyped):
    value: str


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
class RelationalOp(Expression):
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
class BoolRelOp(RelationalOp, BoolTyped):
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
    ...


@dataclass
class FloatVariable(Variable, FloatTyped):
    ...


@dataclass
class CharVariable(Variable, FloatTyped):
    ...


@dataclass
class BoolVariable(Variable, BoolTyped):
    ...


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
class CharPrint(Print, CharTyped):
    ...


@dataclass
class BoolPrint(Print, BoolTyped):
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
class BoolParen(Parenthesis, BoolTyped):
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
class CharCall(Call, CharTyped):
    ...


@dataclass
class BoolCall(Call, BoolTyped):
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
class CharLocalName(LocalName, CharTyped):
    ...


@dataclass
class BoolLocalName(LocalName, BoolTyped):
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
class CharGlobalName(GlobalName, CharTyped):
    ...


@dataclass
class BoolGlobalName(GlobalName, BoolTyped):
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
class Boolean(Expression, BoolTyped):
    value: Literal["true", "false"]


@dataclass
class LogicalOp(Expression, BoolTyped):
    op: Literal["and", "or"]
    lhs: Expression
    rhs: Expression


@dataclass
class Negation(Expression, BoolTyped):
    op: Literal["not"]
    expr: Expression


@dataclass
class Break(Statement):
    ...


@dataclass
class ErrorExpr(Expression, UnknownType):
    err: WabbitError


@dataclass
class Program(Node):
    statements: list[Statement]
    source: str
    fname: str = "file.wb"
