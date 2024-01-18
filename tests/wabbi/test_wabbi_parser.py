from utils import read_source

from wabbi.model import (
    Assignment,
    BinOp,
    Boolean,
    Branch,
    Break,
    Call,
    ExprAsStatement,
    Function,
    Integer,
    LogicalOp,
    Name,
    Negation,
    Parenthesis,
    Print,
    Program,
    RelationalOp,
    Return,
    UnaryOp,
    Variable,
    VariableDecl,
    While,
)
from wabbi.parser import Parser
from wabbi.tokenizer import tokenize


def test_passes_operator_test():
    source = read_source("test_operators.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            Variable(name="x", expr=Integer(value=2)),
            Variable(name="y", expr=Integer(value=5)),
            Print(expr=BinOp(op="+", lhs=Name(value="x"), rhs=Name(value="y"))),
            Print(expr=BinOp(op="-", lhs=Name(value="x"), rhs=Name(value="y"))),
            Print(expr=BinOp(op="*", lhs=Name(value="x"), rhs=Name(value="y"))),
            Print(expr=BinOp(op="/", lhs=Name(value="x"), rhs=Name(value="y"))),
            Print(expr=BinOp(op="/", lhs=Name(value="y"), rhs=Name(value="x"))),
            Print(expr=UnaryOp(op="-", expr=Name(value="x"))),
            Branch(
                condition=RelationalOp(
                    op="<", lhs=Name(value="x"), rhs=Name(value="y")
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=RelationalOp(
                    op="<=", lhs=Name(value="x"), rhs=Name(value="y")
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=RelationalOp(
                    op=">", lhs=Name(value="y"), rhs=Name(value="x")
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=RelationalOp(
                    op=">=", lhs=Name(value="y"), rhs=Name(value="x")
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=RelationalOp(
                    op="==", lhs=Name(value="x"), rhs=Name(value="y")
                ),
                body=[Print(expr=Integer(value=0))],
                else_=[Print(expr=Integer(value=1))],
            ),
            Branch(
                condition=RelationalOp(
                    op="!=", lhs=Name(value="x"), rhs=Name(value="y")
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
        ]
    )


def test_optional_else():
    source = read_source("test_else.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            Function(
                name="abs",
                args=["x"],
                body=[
                    Branch(
                        condition=RelationalOp(
                            op="<", lhs=Name(value="x"), rhs=Integer(value=0)
                        ),
                        body=[Return(expr=UnaryOp(op="-", expr=Name(value="x")))],
                        else_=[],
                    ),
                    Return(expr=Name(value="x")),
                ],
            ),
            Print(expr=Call(name="abs", args=[Integer(value=2)])),
            Print(expr=Call(name="abs", args=[UnaryOp(op="-", expr=Integer(value=2))])),
        ]
    )


def test_optional_value():
    source = read_source("test_optvalue.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            VariableDecl(name="x"),
            Function(
                name="setx",
                args=["v"],
                body=[Assignment(lhs=Name(value="x"), rhs=Name(value="v"))],
            ),
            ExprAsStatement(expr=Call(name="setx", args=[Integer(value=123)])),
            Print(expr=Name(value="x")),
        ]
    )


def test_multiple_args():
    source = read_source("test_multiple.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            Function(
                name="f",
                args=["x", "y", "z"],
                body=[
                    Return(
                        expr=BinOp(
                            op="*",
                            lhs=Parenthesis(
                                expr=BinOp(
                                    op="+", lhs=Name(value="x"), rhs=Name(value="y")
                                )
                            ),
                            rhs=Name(value="z"),
                        )
                    )
                ],
            ),
            Print(
                expr=Call(
                    name="f",
                    args=[Integer(value=1), Integer(value=2), Integer(value=3)],
                )
            ),
            Function(name="g", args=[], body=[Return(expr=Integer(value=42))]),
            Print(expr=Call(name="g", args=[])),
        ]
    )


def test_passes_logical_op_test():
    source = read_source("test_logical.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            Variable(name="x", expr=Integer(value=3)),
            Variable(name="y", expr=Integer(value=10)),
            Variable(name="z", expr=Integer(value=20)),
            Branch(
                condition=Boolean(value="true"),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=Boolean(value="false"),
                body=[Print(expr=Integer(value=0))],
                else_=[Print(expr=Integer(value=1))],
            ),
            Branch(
                condition=LogicalOp(
                    op="and",
                    lhs=RelationalOp(op="<", lhs=Name(value="x"), rhs=Name(value="y")),
                    rhs=RelationalOp(op="<", lhs=Name(value="y"), rhs=Name(value="z")),
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=LogicalOp(
                    op="or",
                    lhs=Negation(
                        op="not",
                        expr=RelationalOp(
                            op="<", lhs=Name(value="x"), rhs=Name(value="y")
                        ),
                    ),
                    rhs=Negation(
                        op="not",
                        expr=RelationalOp(
                            op="<", lhs=Name(value="y"), rhs=Name(value="z")
                        ),
                    ),
                ),
                body=[Print(expr=Integer(value=0))],
                else_=[Print(expr=Integer(value=1))],
            ),
            Branch(
                condition=LogicalOp(
                    op="or",
                    lhs=RelationalOp(op="<", lhs=Name(value="x"), rhs=Integer(value=0)),
                    rhs=RelationalOp(
                        op=">", lhs=Name(value="z"), rhs=Integer(value=30)
                    ),
                ),
                body=[Print(expr=Integer(value=0))],
                else_=[Print(expr=Integer(value=1))],
            ),
            Branch(
                condition=LogicalOp(
                    op="or",
                    lhs=Negation(
                        op="not",
                        expr=RelationalOp(
                            op="<", lhs=Name(value="x"), rhs=Integer(value=0)
                        ),
                    ),
                    rhs=RelationalOp(
                        op=">", lhs=Name(value="z"), rhs=Integer(value=30)
                    ),
                ),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
        ]
    )


def test_break():
    source = read_source("test_break.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        statements=[
            Variable(name="n", expr=Integer(value=0)),
            While(
                condition=RelationalOp(
                    op="==", lhs=Integer(value=0), rhs=Integer(value=0)
                ),
                body=[
                    Print(expr=Name(value="n")),
                    Assignment(
                        lhs=Name(value="n"),
                        rhs=BinOp(op="+", lhs=Name(value="n"), rhs=Integer(value=1)),
                    ),
                    Branch(
                        condition=RelationalOp(
                            op="==", lhs=Name(value="n"), rhs=Integer(value=10)
                        ),
                        body=[Break()],
                        else_=[],
                    ),
                ],
            ),
        ]
    )
