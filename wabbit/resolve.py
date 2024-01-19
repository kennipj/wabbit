from typing import cast

from wabbit.exceptions import WabbitSyntaxError
from wabbit.model import (
    Branch,
    CharGlobalName,
    CharLocalName,
    CharName,
    FloatGlobalName,
    FloatLocalName,
    FloatName,
    Function,
    GlobalVar,
    IntGlobalName,
    IntLocalName,
    IntName,
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
        self._varnames.update({arg.value for arg in node.args})
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
            return LocalVar(name=node.name, loc=node.loc, type_=node.type_)
        self._globals.add(node.name)
        return GlobalVar(name=node.name, loc=node.loc, type_=node.type_)

    def visit_intname(self, node: IntName) -> IntLocalName | IntGlobalName:
        self._maybe_error(node)
        if node.value in self._globals:
            return IntGlobalName(value=node.value, loc=node.loc)
        if self._scope_level > 0:
            return IntLocalName(value=node.value, loc=node.loc)
        return IntGlobalName(value=node.value, loc=node.loc)

    def visit_floatname(self, node: FloatName) -> FloatLocalName | FloatGlobalName:
        self._maybe_error(node)
        if node.value in self._globals:
            return FloatGlobalName(value=node.value, loc=node.loc)
        if self._scope_level > 0:
            return FloatLocalName(value=node.value, loc=node.loc)
        return FloatGlobalName(value=node.value, loc=node.loc)

    def visit_charname(self, node: CharName) -> CharLocalName | CharGlobalName:
        self._maybe_error(node)
        if node.value in self._globals:
            return CharGlobalName(value=node.value, loc=node.loc)
        if self._scope_level > 0:
            return CharLocalName(value=node.value, loc=node.loc)
        return CharGlobalName(value=node.value, loc=node.loc)

    def _maybe_error(self, node: Name) -> None:
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


def resolve_scopes(program: Program) -> Program:
    visitor = ResolveScopes(
        [VariableDecl, Branch, While, Function, IntName, FloatName, CharName],
        program.source,
        program.fname,
    )
    walker = Walker(visitor)
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return cast(Program, walker.traverse(program, direction="both"))
