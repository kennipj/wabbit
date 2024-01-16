from typing import cast

from wab.model import (
    Branch,
    Function,
    GlobalName,
    GlobalVar,
    LocalName,
    LocalVar,
    Name,
    Node,
    Program,
    VariableDecl,
    While,
)
from wab.walker import Visitor, Walker


class ResolveScopes(Visitor):
    def __init__(self, to_visit: list[type[Node]]) -> None:
        self._visit_status: dict[int, bool] = {}
        self._globals = set()
        self._varnames = set()
        self._scope_level = 0
        super().__init__(to_visit)

    def visit_function(self, node: Function) -> Function:
        self._varnames.update({arg for arg in node.args})
        self._visit_status[id(node)] = not self._visit_status.get(id(node), True)
        self._scope_level += -1 if self._visit_status[id(node)] else 1
        return node

    def visit_branch(self, node: Branch) -> Branch:
        self._visit_status[id(node)] = not self._visit_status.get(id(node), True)
        self._scope_level += -1 if self._visit_status[id(node)] else 1
        return node

    def visit_while(self, node: While) -> While:
        self._visit_status[id(node)] = not self._visit_status.get(id(node), True)
        self._scope_level += -1 if self._visit_status[id(node)] else 1
        return node

    def visit_variabledecl(self, node: VariableDecl) -> VariableDecl:
        self._varnames.add(node.name)
        if self._scope_level > 0:
            return LocalVar(node.name)
        self._globals.add(node.name)
        return GlobalVar(node.name)

    def visit_name(self, node: Name) -> Name:
        if node.value not in self._varnames:
            raise SyntaxError(f"Encountered undeclared variable {node.value}.")

        if node.value in self._globals:
            return GlobalName(value=node.value)
        if self._scope_level > 0:
            return LocalName(value=node.value)
        return GlobalName(value=node.value)


def resolve_scopes(program: Program) -> Program:
    walker = Walker(ResolveScopes([VariableDecl, Branch, While, Function, Name]))
    return cast(Program, walker.traverse(program, direction="both"))
