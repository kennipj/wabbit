from wab.fold_constants import fold_constants
from wab.model import (
    Assignment,
    BinOp,
    Integer,
    Name,
    Parenthesis,
    Print,
    Program,
    Variable,
)


def test_folds_program_1():
    program = Program(
        statements=[
            Variable(name="x", expr=Integer(10)),
            Assignment(Name(value="x"), BinOp(op="+", lhs=Name("x"), rhs=Integer(1))),
            Print(
                BinOp(
                    op="+",
                    lhs=Parenthesis(BinOp(op="*", lhs=Integer(23), rhs=Integer(45))),
                    rhs=Name("x"),
                )
            ),
        ]
    )
    assert fold_constants(program) == Program(
        statements=[
            Variable(name="x", expr=Integer(10)),
            Assignment(Name(value="x"), BinOp(op="+", lhs=Name("x"), rhs=Integer(1))),
            Print(
                BinOp(
                    op="+",
                    lhs=Integer(1035),
                    rhs=Name("x"),
                )
            ),
        ]
    )


def test_folds_print_constant():
    program = Program(
        statements=[
            Print(
                expr=BinOp(
                    op="*",
                    lhs=Parenthesis(
                        BinOp(op="+", lhs=Integer(value=2), rhs=Integer(value=3))
                    ),
                    rhs=Integer(4),
                )
            )
        ]
    )
    assert fold_constants(program) == Program(statements=[Print(expr=Integer(20))])
