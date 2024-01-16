from typing import cast

from wab.model import Assignment, Program, Variable, VariableDecl
from wab.walker import Visitor, Walker


class DeinitVisitor(Visitor):
    def visit_variable(self, node: Variable) -> list[VariableDecl | Assignment]:
        return [VariableDecl(name=node.name), Assignment(lhs=node.name, rhs=node.expr)]


def deinit_variables(program: Program) -> Program:
    walker = Walker(DeinitVisitor([Variable]))
    return cast(Program, walker.traverse(program))
