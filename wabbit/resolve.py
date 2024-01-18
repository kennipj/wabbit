from typing import cast

from wabbit.exceptions import WabbitSyntaxError
from wabbit.model import (
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
from wabbit.walker import Visitor, Walker


class ResolveScopes(Visitor):
    def __init__(self, to_visit: list[type[Node]], source: str, fname: str) -> None:
        self.errors = []
        self._visit_status: dict[int, bool] = {}
        self._globals = set()
        self._varnames = set()
        self._scope_level = 0
        super().__init__(to_visit, source, fname)

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
            return LocalVar(name=node.name, loc=node.loc)
        self._globals.add(node.name)
        return GlobalVar(name=node.name, loc=node.loc)

    def visit_name(self, node: Name) -> Name:
        if node.value not in self._varnames:
            self.errors.append(
                WabbitSyntaxError(
                    msg=f"Undeclared variable: `{node.value}`.",
                    source=self.source,
                    fname=self.fname,
                    lineno=node.loc.lineno,
                    start=node.loc.start,
                    end=node.loc.end,
                )
            )

        if node.value in self._globals:
            return GlobalName(value=node.value, loc=node.loc)
        if self._scope_level > 0:
            return LocalName(value=node.value, loc=node.loc)
        return GlobalName(value=node.value, loc=node.loc)


def resolve_scopes(program: Program) -> Program:
    visitor = ResolveScopes(
        [VariableDecl, Branch, While, Function, Name], program.source, program.fname
    )
    walker = Walker(visitor)
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return cast(Program, walker.traverse(program, direction="both"))
