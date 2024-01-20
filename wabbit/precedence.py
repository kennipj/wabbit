from typing import TypeVar, cast

from wabbit.model import BinOp, Expression, LogicalOp, Node, Program, RelationalOp
from wabbit.walker import Visitor, Walker

OP_PRECEDENCE = {
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2,
    "<": 1,
    "<=": 1,
    "==": 1,
    ">": 1,
    ">=": 1,
    "!=": 1,
    "and": 0,
    "or": 0,
}
T = TypeVar("T", bound=Node)


class Precedence(Visitor):
    """Set operator precedence with shunting yard algorithm."""

    def __init__(
        self,
        to_visit: list[type[Node]],
        pre_visit: list[type[Node]],
        source: str,
        fname: str,
    ) -> None:
        super().__init__(to_visit, pre_visit, source, fname)
        self._output = []
        self._operators: list[BinOp | RelationalOp | LogicalOp] = []
        self._visited = set()
        self._in_op = False
        self._top_op = 0

    def visit_relationalop(self, node: RelationalOp) -> Expression:
        return self._process_op(node)

    def visit_binop(self, node: RelationalOp) -> Expression:
        return self._process_op(node)

    def visit_logicalop(self, node: LogicalOp) -> Expression:
        return self._process_op(node)

    def _add_output(self, node: T) -> T:
        if self._in_op:
            self._output.append(node)
        return node

    def _create_op(self) -> Expression:
        while self._operators:
            self._output.append(self._operators.pop())

        stack = []
        for item in self._output:
            if not isinstance(item, (BinOp, RelationalOp, LogicalOp)):
                stack.append(item)
            else:
                rhs = stack.pop()
                lhs = stack.pop()
                if isinstance(item, BinOp):
                    new_node = BinOp(op=item.op, lhs=lhs, rhs=rhs, loc=item.loc)
                elif isinstance(item, LogicalOp):
                    new_node = LogicalOp(op=item.op, lhs=lhs, rhs=rhs, loc=item.loc)
                elif isinstance(item, RelationalOp):
                    new_node = RelationalOp(op=item.op, lhs=lhs, rhs=rhs, loc=item.loc)
                else:
                    raise ValueError("Unknown operator type")
                stack.append(new_node)
        return stack[0]

    def _add_op(self, op: BinOp | RelationalOp | LogicalOp) -> None:
        while self._operators:
            top_op = self._operators[-1]
            if OP_PRECEDENCE[top_op.op] >= OP_PRECEDENCE[op.op]:
                self._output.append(self._operators.pop())
            else:
                break
        self._operators.append(op)

    def _process_op(self, node: RelationalOp | BinOp | LogicalOp) -> Expression:
        if id(node) in self._visited:
            return node
        if self._in_op:
            if not isinstance(node.lhs, (RelationalOp, BinOp, LogicalOp)):
                self._output.append(node.lhs)

            self._add_op(node)

            if not isinstance(node.rhs, (RelationalOp, BinOp, LogicalOp)):
                self._output.append(node.rhs)

            if id(self._top_op) == id(node):
                new_node = self._create_op()
                self._in_op = False
                self._operators = []
                self._output = []
                return new_node

            self._visited.add(id(node))
            return node

        self._in_op = True
        self._top_op = node
        return node


def set_precedence(ast: Program) -> Program:
    visitor = Precedence(
        to_visit=[
            LogicalOp,
            BinOp,
            RelationalOp,
        ],
        pre_visit=[BinOp, RelationalOp, LogicalOp],
        source=ast.source,
        fname=ast.fname,
    )
    ast = cast(Program, Walker(visitor).traverse(ast))
    return ast
