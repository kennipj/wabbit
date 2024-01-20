from typing import Literal, cast

from wabbit.exceptions import WabbitSyntaxError, WabbitTypeError
from wabbit.model import (
    Break,
    CharTyped,
    ErrorExpr,
    FloatTyped,
    Function,
    IntTyped,
    Node,
    Program,
    Return,
    While,
)
from wabbit.walker import Visitor, Walker


class TypeCheck(Visitor):
    def __init__(
        self,
        to_visit: list[type[Node]],
        pre_visit: list[type[Node]],
        source: str,
        fname: str,
    ) -> None:
        self._in_func = False
        self._ret_type = ""
        self._in_loop = False
        self._visited = set()
        super().__init__(to_visit, pre_visit, source, fname)

    def visit_errorexpr(self, node: ErrorExpr) -> ErrorExpr:
        if id(node) not in self._visited:
            self.errors.append(node.err)
        self._visited.add(id(node))
        return node

    def visit_function(self, node: Function) -> Function:
        self._in_func = not self._in_func
        self._ret_type = node.ret_type_.value
        return node

    def visit_return(self, node: Return) -> Return:
        if not self._in_func:
            self.errors.append(
                WabbitSyntaxError.from_loc(
                    msg='"return" can be used only within a function.',
                    fname=self.fname,
                    source=self.source,
                    loc=node.loc,
                )
            )
        elif (type_ := _type(node.expr)) != self._ret_type:
            if id(node) not in self._visited:
                self.errors.append(
                    WabbitTypeError(
                        msg=(
                            f'Expression of type "{type_}" cannot be '
                            f'assigned to return type "{self._ret_type}".'
                        ),
                        fname=self.fname,
                        source=self.source,
                        loc=node.expr.loc,
                    )
                )
        self._visited.add(id(node))
        return node

    def visit_while(self, node: While) -> While:
        self._in_loop = not self._in_loop
        return node

    def visit_break(self, node: Break) -> Break:
        if not self._in_loop:
            if id(node) not in self._visited:
                self.errors.append(
                    WabbitTypeError(
                        msg='"break" can only be used within a loop',
                        fname=self.fname,
                        source=self.source,
                        loc=node.loc,
                    )
                )
        self._visited.add(id(node))
        return node


def check_types(ast: Program) -> Program:
    visitor = TypeCheck(
        to_visit=[ErrorExpr, Function, Return, While, Break],
        pre_visit=[Function, While],
        source=ast.source,
        fname=ast.fname,
    )
    ast = cast(Program, Walker(visitor=visitor).traverse(ast))
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return ast


def _type(node) -> Literal["int", "float", "char", "unknown"]:
    if isinstance(node, IntTyped):
        return "int"
    elif isinstance(node, FloatTyped):
        return "float"
    elif isinstance(node, CharTyped):
        return "char"
    else:
        return "unknown"
