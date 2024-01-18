from typing import cast

from wabbi.exceptions import WabbitSyntaxError
from wabbi.model import Assignment, Name, Node, Program, Variable, VariableDecl
from wabbi.walker import Visitor, Walker


class DeinitVisitor(Visitor):
    def __init__(self, to_visit: list[type[Node]], source: str, fname: str) -> None:
        super().__init__(to_visit, source, fname)
        self._vars = set()

    def visit_variable(self, node: Variable) -> list[VariableDecl | Assignment]:
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
        return [
            VariableDecl(name=node.name, loc=node.loc),
            Assignment(
                lhs=Name(value=node.name, loc=node.loc), rhs=node.expr, loc=node.loc
            ),
        ]


def deinit_variables(program: Program) -> Program:
    visitor = DeinitVisitor([Variable], program.source, program.fname)
    program = cast(Program, Walker(visitor).traverse(program))
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return program
