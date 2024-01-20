from typing import cast

from wabbit.model import BinOp, Integer, Parenthesis, Program, UnaryOp
from wabbit.walker import Visitor, Walker


class FoldConstants(Visitor):
    def visit_binop(self, node: BinOp) -> Integer | BinOp:
        if node.op not in {"+", "*", "/", "-"}:
            return node

        lhs_val = None
        rhs_val = None
        if isinstance(node.lhs, Integer):
            lhs_val = node.lhs.value
        if isinstance(node.lhs, UnaryOp) and isinstance(node.lhs.expr, Integer):
            lhs_val = -node.lhs.expr.value

        if isinstance(node.rhs, UnaryOp) and isinstance(node.rhs.expr, Integer):
            rhs_val = -node.rhs.expr.value
        if isinstance(node.rhs, Integer):
            rhs_val = node.rhs.value

        if lhs_val is not None and rhs_val is not None:
            return Integer(value=eval(f"{lhs_val} {node.op} {rhs_val}"), loc=node.loc)
        return node

    def visit_parenthesis(self, node: Parenthesis) -> Integer | Parenthesis:
        if isinstance(node.expr, Integer):
            return Integer(value=node.expr.value, loc=node.loc)
        return node


def fold_constants(program: Program) -> Program:
    visitor = FoldConstants(
        to_visit=[BinOp, Parenthesis],
        pre_visit=[],
        source=program.source,
        fname=program.fname,
    )
    walker = Walker(visitor)
    return cast(Program, walker.traverse(program))
