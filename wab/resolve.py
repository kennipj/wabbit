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
        self._visited_function = False
        self._visited_branch = False
        self._visited_loop = False
        self._globals = set()
        self._scope_level = 0
        super().__init__(to_visit)

    def visit_function(self, node: Function) -> Function:
        self._scope_level += -1 if self._visited_function else 1
        self._visited_function = not self._visited_function
        return node

    def visit_branch(self, node: Branch) -> Branch:
        self._scope_level += -1 if self._visited_branch else 1
        self._visited_branch = not self._visited_branch
        return node

    def visit_while(self, node: While) -> While:
        self._scope_level += -1 if self._visited_loop else 1
        self._visited_loop = not self._visited_loop
        return node

    def visit_variabledecl(self, node: VariableDecl) -> VariableDecl:
        if self._scope_level > 0:
            return LocalVar(node.name)
        self._globals.add(node.name)
        return GlobalVar(node.name)

    def visit_name(self, node: Name) -> Name:
        if node.value in self._globals:
            return GlobalName(value=node.value)
        if self._scope_level > 0:
            return LocalName(value=node.value)
        return GlobalName(value=node.value)


def resolve_scopes(program: Program) -> Program:
    walker = Walker(ResolveScopes([VariableDecl, Branch, While, Function, Name]))
    return cast(Program, walker.traverse(program, direction="both"))
