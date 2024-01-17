import pytest

from wab.deinit import deinit_variables
from wab.model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    Function,
    GlobalName,
    GlobalVar,
    Integer,
    LocalName,
    LocalVar,
    Name,
    Print,
    Program,
    Return,
    Variable,
    While,
)
from wab.resolve import resolve_scopes


def test_scopes_nested_while_program():
    program = Program(
        statements=[
            Variable(name="x", expr=Integer(42)),
            While(
                condition=BinOp(op="<", lhs=Name(value="x"), rhs=Integer(50)),
                body=[
                    Variable(name="y", expr=Integer(42)),
                    While(
                        condition=BinOp(op="<", lhs=Name(value="x"), rhs=Integer(50)),
                        body=[
                            Variable(name="z", expr=Integer(42)),
                            While(
                                condition=BinOp(
                                    op="<", lhs=Name(value="x"), rhs=Integer(50)
                                ),
                                body=[],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
    assert resolve_scopes(deinit_variables(program)) == Program(
        statements=[
            GlobalVar(name="x"),
            Assignment(lhs=GlobalName(value="x"), rhs=Integer(value=42)),
            While(
                condition=BinOp(
                    op="<", lhs=GlobalName(value="x"), rhs=Integer(value=50)
                ),
                body=[
                    LocalVar(name="y"),
                    Assignment(lhs=LocalName(value="y"), rhs=Integer(value=42)),
                    While(
                        condition=BinOp(
                            op="<", lhs=GlobalName(value="x"), rhs=Integer(value=50)
                        ),
                        body=[
                            LocalVar(name="z"),
                            Assignment(lhs=LocalName(value="z"), rhs=Integer(value=42)),
                            While(
                                condition=BinOp(
                                    op="<",
                                    lhs=GlobalName(value="x"),
                                    rhs=Integer(value=50),
                                ),
                                body=[],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )


def test_scopes_program_2():
    program = Program(
        statements=[
            Variable(name="n", expr=Integer(value=0)),
            While(
                BinOp(op="<", lhs=Name(value="n"), rhs=Integer(10)),
                body=[
                    Branch(
                        condition=BinOp(op="==", lhs=Name("n"), rhs=Integer(10)),
                        body=[
                            Variable(
                                name="x",
                                expr=BinOp(op="*", lhs=Name("n"), rhs=Integer(100)),
                            ),
                            Print(expr=Name("x")),
                        ],
                        else_=[
                            Print(expr=Name("n")),
                        ],
                    ),
                    Assignment(
                        lhs=Name("n"), rhs=BinOp(op="+", lhs=Name("n"), rhs=Integer(1))
                    ),
                ],
            ),
        ]
    )
    assert resolve_scopes(deinit_variables(program)) == Program(
        statements=[
            GlobalVar(name="n"),
            Assignment(lhs=GlobalName(value="n"), rhs=Integer(value=0)),
            While(
                condition=BinOp(
                    op="<", lhs=GlobalName(value="n"), rhs=Integer(value=10)
                ),
                body=[
                    Branch(
                        condition=BinOp(
                            op="==", lhs=GlobalName(value="n"), rhs=Integer(value=10)
                        ),
                        body=[
                            LocalVar(name="x"),
                            Assignment(
                                lhs=LocalName(value="x"),
                                rhs=BinOp(
                                    op="*",
                                    lhs=GlobalName(value="n"),
                                    rhs=Integer(value=100),
                                ),
                            ),
                            Print(expr=LocalName(value="x")),
                        ],
                        else_=[Print(expr=GlobalName(value="n"))],
                    ),
                    Assignment(
                        lhs=GlobalName(value="n"),
                        rhs=BinOp(
                            op="+", lhs=GlobalName(value="n"), rhs=Integer(value=1)
                        ),
                    ),
                ],
            ),
        ]
    )


def test_scopes_program_3():
    program = Program(
        statements=[
            Function(
                name="square",
                args=["x"],
                body=[
                    Variable(
                        name="r", expr=BinOp(op="*", lhs=Name("x"), rhs=Name("x"))
                    ),
                    Return(Name("r")),
                ],
            ),
            Variable(name="result", expr=Call(name="square", args=[Integer(4)])),
            Print(expr=Name("result")),
        ]
    )
    assert resolve_scopes(deinit_variables(program)) == Program(
        statements=[
            Function(
                name="square",
                args=["x"],
                body=[
                    LocalVar(name="r"),
                    Assignment(
                        lhs=LocalName(value="r"),
                        rhs=BinOp(
                            op="*", lhs=LocalName(value="x"), rhs=LocalName(value="x")
                        ),
                    ),
                    Return(expr=LocalName(value="r")),
                ],
            ),
            GlobalVar(name="result"),
            Assignment(
                lhs=GlobalName(value="result"),
                rhs=Call(name="square", args=[Integer(value=4)]),
            ),
            Print(expr=GlobalName(value="result")),
        ]
    )


def test_raises_syntax_error_on_undeclared_variable():
    program = Program(
        statements=[
            Assignment(
                lhs=Name("y"), rhs=BinOp(op="+", lhs=Name("x"), rhs=Integer(value=1))
            ),
        ]
    )
    with pytest.raises(SyntaxError):
        resolve_scopes(deinit_variables(program))
