from typing import cast

from wabbi.model import Assignment, Name, Node, Program, Variable, VariableDecl
from wabbi.walker import Visitor, Walker


class DeinitVisitor(Visitor):
    def __init__(self, to_visit: list[type[Node]]) -> None:
        super().__init__(to_visit)
        self._vars = set()

    def visit_variable(self, node: Variable) -> list[VariableDecl | Assignment]:
        if node.name in self._vars:
            raise SyntaxError(f"Redeclaration of existing variable {node.name}")
        self._vars.add(node.name)
        return [
            VariableDecl(name=node.name, loc=node.loc),
            Assignment(
                lhs=Name(value=node.name, loc=node.loc), rhs=node.expr, loc=node.loc
            ),
        ]


def deinit_variables(program: Program) -> Program:
    walker = Walker(DeinitVisitor([Variable]))
    return cast(Program, walker.traverse(program))
