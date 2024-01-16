from wab.deinit import deinit_variables
from wab.model import (
    Assignment,
    BinOp,
    Integer,
    Name,
    Parenthesis,
    Program,
    Variable,
    VariableDecl,
)


def test_folds_multi_var_program():
    program = Program(
        statements=[
            Variable(name=Name("x"), expr=Integer(42)),
            Variable(name=Name("y"), expr=BinOp("+", lhs=Integer(2), rhs=Name("x"))),
            Variable(
                name=Name("z"),
                expr=BinOp(
                    op="*",
                    lhs=Parenthesis(expr=BinOp("+", lhs=Integer(3), rhs=Name("y"))),
                    rhs=Name("x"),
                ),
            ),
        ]
    )
    assert deinit_variables(program) == Program(
        statements=[
            VariableDecl(name=Name("x")),
            Assignment(lhs=Name("x"), rhs=Integer(42)),
            VariableDecl(name=Name("y")),
            Assignment(lhs=Name("y"), rhs=BinOp("+", lhs=Integer(2), rhs=Name("x"))),
            VariableDecl(name=Name("z")),
            Assignment(
                lhs=Name("z"),
                rhs=BinOp(
                    op="*",
                    lhs=Parenthesis(expr=BinOp("+", lhs=Integer(3), rhs=Name("y"))),
                    rhs=Name("x"),
                ),
            ),
        ]
    )
