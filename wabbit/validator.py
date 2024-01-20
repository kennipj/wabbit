from wabbit.model import ErrorExpr, Program
from wabbit.walker import Visitor, Walker


class Validator(Visitor):
    def visit_errorexpr(self, node: ErrorExpr) -> ErrorExpr:
        self.errors.append(node.err)
        return node


def validate_ast(ast: Program):
    visitor = Validator(
        to_visit=[ErrorExpr], pre_visit=[], source=ast.source, fname=ast.fname
    )
    Walker(visitor).traverse(ast)
    if visitor.errors:
        for err in visitor.errors:
            print(err)
        exit()
    return ast
