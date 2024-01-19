from typing import cast

from wabbit.exceptions import WabbitSyntaxError
from wabbit.model import (
    Assignment,
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
    def __init__(self, to_visit: list[type[Node]], source: str, fname: str) -> None:
        super().__init__(to_visit, source, fname)
        self._vars = set()

    def visit_intvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        self._maybe_err(node)
        return [
            VariableDecl(
                name=node.name, loc=node.loc, type_=Type(value="int", loc=node.loc)
            ),
            Assignment(
                lhs=IntName(value=node.name, loc=node.loc), rhs=node.expr, loc=node.loc
            ),
        ]

    def visit_floatvariable(self, node: Variable) -> list[VariableDecl | Assignment]:
        self._maybe_err(node)
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

    def _maybe_err(self, node: Variable) -> None:
        if node.name in self._vars:
            self.errors.append(
                WabbitSyntaxError(
                    msg=f"Redeclaration of existing variable `{node.name}`.",
                    fname=self.fname,
                    source=self.source,
                    lineno=node.loc.lineno,
                    start=node.loc.start,
                    end=node.loc.end,
                )
            )
        else:
            self._vars.add(node.name)


def deinit_variables(program: Program) -> Program:
    visitor = DeinitVisitor([IntVariable, FloatVariable], program.source, program.fname)
    program = cast(Program, Walker(visitor).traverse(program))
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return program
