from wab.deinit import deinit_variables
from wab.model import (
    Assignment,
    BinOp,
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
)
from wab.resolve import resolve_scopes
from wab.unscript import unscript_toplevel


def test_unscripts_program_7():
    program = Program(
        statements=[
            Variable(name="v", expr=Integer(4)),
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
    assert unscript_toplevel(resolve_scopes(deinit_variables(program))) == Program(
        statements=[
            GlobalVar(name="v"),
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
            Function(
                name="main",
                args=["_"],
                body=[
                    Assignment(lhs=GlobalName(value="v"), rhs=Integer(value=4)),
                    Assignment(
                        lhs=GlobalName(value="result"),
                        rhs=Call(name="square", args=[Integer(value=4)]),
                    ),
                    Print(expr=GlobalName(value="result")),
                    Return(expr=Integer(value=0)),
                ],
            ),
        ]
    )
