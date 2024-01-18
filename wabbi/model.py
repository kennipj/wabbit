from dataclasses import dataclass
from typing import Literal

from wabbi.exceptions import WabbitSyntaxError


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
class Name(Expression):
    value: str


@dataclass
class Integer(Expression):
    value: int


@dataclass
class BooleanExpression(Expression):
    ...


@dataclass
class BinOp(Expression):
    op: Literal["+", "*", "-", "/"]
    lhs: Expression
    rhs: Expression


@dataclass
class RelationalOp(BooleanExpression):
    op: Literal["==", "<", ">", "<=", ">=", "!="]
    lhs: Expression
    rhs: Expression


@dataclass
class Assignment(Statement):
    lhs: Name
    rhs: Expression


@dataclass
class Variable(Statement):
    name: str
    expr: Expression


@dataclass
class VariableDecl(Statement):
    name: str


@dataclass
class Print(Statement):
    expr: Expression


@dataclass
class Parenthesis(Expression):
    expr: Expression


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
class Function(Statement):
    name: str
    args: list[str]
    body: list[Statement]


@dataclass
class Return(Statement):
    expr: Expression


@dataclass
class Call(Expression):
    name: str
    args: list[Expression]


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
class GlobalName(Name):
    ...


@dataclass
class UnaryOp(Expression):
    op: Literal["-"]
    expr: Expression


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
