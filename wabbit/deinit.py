from typing import cast

from wabbit.model import (
    Assignment,
    BoolVariable,
    CharName,
    CharVariable,
    FloatName,
    FloatVariable,
    IntName,
    IntVariable,
    Node,
    Program,
    Type,
    Variable,
    VariableDecl,
)
from wabbit.walker import Visitor, Walker


class DeinitVisitor(Visitor):
    def __init__(
        self,
        to_visit: list[type[Node]],
        pre_visit: list[type[Node]],
        source: str,
        fname: str,
    ) -> None:
        super().__init__(to_visit, pre_visit, source, fname)
        self._vars = set()

    def visit_intvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        return [
            VariableDecl(
                name=node.name, loc=node.loc, type_=Type(value="int", loc=node.loc)
            ),
            Assignment(
                lhs=IntName(value=node.name, loc=node.loc), rhs=node.expr, loc=node.loc
            ),
        ]

    def visit_floatvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        return [
            VariableDecl(
                name=node.name, loc=node.loc, type_=Type(value="float", loc=node.loc)
            ),
            Assignment(
                lhs=FloatName(value=node.name, loc=node.loc),
                rhs=node.expr,
                loc=node.loc,
            ),
        ]

    def visit_charvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        return [
            VariableDecl(
                name=node.name, loc=node.loc, type_=Type(value="char", loc=node.loc)
            ),
            Assignment(
                lhs=CharName(value=node.name, loc=node.loc),
                rhs=node.expr,
                loc=node.loc,
            ),
        ]

    def visit_boolvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        return [
            VariableDecl(
                name=node.name, loc=node.loc, type_=Type(value="bool", loc=node.loc)
            ),
            Assignment(
                lhs=CharName(value=node.name, loc=node.loc),
                rhs=node.expr,
                loc=node.loc,
            ),
        ]


def deinit_variables(program: Program) -> Program:
    visitor = DeinitVisitor(
        to_visit=[IntVariable, FloatVariable, CharVariable, BoolVariable],
        pre_visit=[],
        source=program.source,
        fname=program.fname,
    )
    program = cast(Program, Walker(visitor).traverse(program))
    return program
