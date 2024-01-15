from dataclasses import dataclass


@dataclass
class Statement:
    ...


@dataclass
class Expression:
    ...


@dataclass
class Name(Expression):
    value: str


@dataclass
class Integer(Expression):
    value: int


@dataclass
class Assignment(Statement):
    lhs: Name
    rhs: Expression


@dataclass
class Variable(Statement):
    name: Name
    expr: Expression


@dataclass
class Print(Statement):
    expr: Expression


@dataclass
class Add(Expression):
    lhs: Expression
    rhs: Expression


@dataclass
class Mul(Expression):
    lhs: Expression
    rhs: Expression


@dataclass
class Parenthesis(Expression):
    expr: Expression


@dataclass
class LessThan(Expression):
    lhs: Expression
    rhs: Expression


@dataclass
class Equal(Expression):
    lhs: Expression
    rhs: Expression


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
    name: Name
    args: list[Name]
    body: list[Statement]


@dataclass
class Return(Statement):
    expr: Expression


@dataclass
class Call(Expression):
    name: Name
    args: list[Expression]


@dataclass
class Program:
    statements: list[Statement]
