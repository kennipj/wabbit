from typing import cast

from wabbi.model import BinOp, Integer, Parenthesis, Program
from wabbi.walker import Visitor, Walker


class FoldConstants(Visitor):
    def visit_binop(self, node: BinOp) -> Integer | BinOp:
        if node.op not in {"+", "*"}:
            return node
        if not isinstance(node.lhs, Integer) or not isinstance(node.rhs, Integer):
            return node
        return Integer(
            value=eval(
                f"{cast(Integer, node.lhs).value} {node.op} {cast(Integer, node.rhs).value}"
            )
        )

    def visit_parenthesis(self, node: Parenthesis) -> Integer | Parenthesis:
        if isinstance(node.expr, Integer):
            return Integer(node.expr.value)
        return node


def fold_constants(program: Program) -> Program:
    visitor = FoldConstants([BinOp, Parenthesis])
    walker = Walker(visitor)
    return cast(Program, walker.traverse(program))
