from utils import read_source

from wabbi.model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    ExprAsStatement,
    Function,
    Integer,
    Name,
    Print,
    Program,
    Return,
    UnaryOp,
    Variable,
    VariableDecl,
)
from wabbi.parser import Parser
from wabbi.tokenizer import tokenize


def test_passes_operator_test():
    source = read_source("test_operators.wb")
    ast = Parser(tokenize(source)).parse()
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
                condition=BinOp(op="<", lhs=Name(value="x"), rhs=Name(value="y")),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=BinOp(op="<=", lhs=Name(value="x"), rhs=Name(value="y")),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=BinOp(op=">", lhs=Name(value="y"), rhs=Name(value="x")),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=BinOp(op=">=", lhs=Name(value="y"), rhs=Name(value="x")),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
            Branch(
                condition=BinOp(op="==", lhs=Name(value="x"), rhs=Name(value="y")),
                body=[Print(expr=Integer(value=0))],
                else_=[Print(expr=Integer(value=1))],
            ),
            Branch(
                condition=BinOp(op="!=", lhs=Name(value="x"), rhs=Name(value="y")),
                body=[Print(expr=Integer(value=1))],
                else_=[Print(expr=Integer(value=0))],
            ),
        ]
    )


def test_optional_else():
    source = read_source("test_else.wb")
    ast = Parser(tokenize(source)).parse()
    assert ast == Program(
        statements=[
            Function(
                name="abs",
                args=["x"],
                body=[
                    Branch(
                        condition=BinOp(
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
    ast = Parser(tokenize(source)).parse()
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
