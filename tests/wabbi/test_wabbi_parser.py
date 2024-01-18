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
    SourceLoc,
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
        loc=SourceLoc(lineno=0, start=0, end=520),
        statements=[
            Variable(
                loc=SourceLoc(lineno=3, start=1, end=10),
                name="x",
                expr=Integer(loc=SourceLoc(lineno=3, start=9, end=10), value=2),
            ),
            Variable(
                loc=SourceLoc(lineno=4, start=1, end=10),
                name="y",
                expr=Integer(loc=SourceLoc(lineno=4, start=9, end=10), value=5),
            ),
            Print(
                loc=SourceLoc(lineno=6, start=1, end=12),
                expr=BinOp(
                    loc=SourceLoc(lineno=6, start=7, end=12),
                    op="+",
                    lhs=Name(loc=SourceLoc(lineno=6, start=7, end=8), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=6, start=11, end=12), value="y"),
                ),
            ),
            Print(
                loc=SourceLoc(lineno=7, start=1, end=12),
                expr=BinOp(
                    loc=SourceLoc(lineno=7, start=7, end=12),
                    op="-",
                    lhs=Name(loc=SourceLoc(lineno=7, start=7, end=8), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=7, start=11, end=12), value="y"),
                ),
            ),
            Print(
                loc=SourceLoc(lineno=8, start=1, end=12),
                expr=BinOp(
                    loc=SourceLoc(lineno=8, start=7, end=12),
                    op="*",
                    lhs=Name(loc=SourceLoc(lineno=8, start=7, end=8), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=8, start=11, end=12), value="y"),
                ),
            ),
            Print(
                loc=SourceLoc(lineno=9, start=1, end=12),
                expr=BinOp(
                    loc=SourceLoc(lineno=9, start=7, end=12),
                    op="/",
                    lhs=Name(loc=SourceLoc(lineno=9, start=7, end=8), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=9, start=11, end=12), value="y"),
                ),
            ),
            Print(
                loc=SourceLoc(lineno=10, start=1, end=12),
                expr=BinOp(
                    loc=SourceLoc(lineno=10, start=7, end=12),
                    op="/",
                    lhs=Name(loc=SourceLoc(lineno=10, start=7, end=8), value="y"),
                    rhs=Name(loc=SourceLoc(lineno=10, start=11, end=12), value="x"),
                ),
            ),
            Print(
                loc=SourceLoc(lineno=11, start=1, end=9),
                expr=UnaryOp(
                    loc=SourceLoc(lineno=11, start=7, end=9),
                    op="-",
                    expr=Name(loc=SourceLoc(lineno=11, start=8, end=9), value="x"),
                ),
            ),
            Branch(
                loc=SourceLoc(lineno=14, start=14, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=14, start=4, end=9),
                    op="<",
                    lhs=Name(loc=SourceLoc(lineno=14, start=4, end=5), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=14, start=8, end=9), value="y"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=15, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=15, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=17, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=17, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=20, start=20, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=20, start=4, end=10),
                    op="<=",
                    lhs=Name(loc=SourceLoc(lineno=20, start=4, end=5), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=20, start=9, end=10), value="y"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=21, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=21, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=23, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=23, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=26, start=26, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=26, start=4, end=9),
                    op=">",
                    lhs=Name(loc=SourceLoc(lineno=26, start=4, end=5), value="y"),
                    rhs=Name(loc=SourceLoc(lineno=26, start=8, end=9), value="x"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=27, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=27, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=29, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=29, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=32, start=32, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=32, start=4, end=10),
                    op=">=",
                    lhs=Name(loc=SourceLoc(lineno=32, start=4, end=5), value="y"),
                    rhs=Name(loc=SourceLoc(lineno=32, start=9, end=10), value="x"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=33, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=33, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=35, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=35, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=38, start=38, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=38, start=4, end=10),
                    op="==",
                    lhs=Name(loc=SourceLoc(lineno=38, start=4, end=5), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=38, start=9, end=10), value="y"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=39, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=39, start=10, end=11), value=0
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=41, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=41, start=10, end=11), value=1
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=44, start=44, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=44, start=4, end=10),
                    op="!=",
                    lhs=Name(loc=SourceLoc(lineno=44, start=4, end=5), value="x"),
                    rhs=Name(loc=SourceLoc(lineno=44, start=9, end=10), value="y"),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=45, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=45, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=47, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=47, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
        ],
    )


def test_optional_else():
    source = read_source("test_else.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=128),
        statements=[
            Function(
                loc=SourceLoc(lineno=3, start=1, end=1),
                name="abs",
                args=["x"],
                body=[
                    Branch(
                        loc=SourceLoc(lineno=4, start=4, end=4),
                        condition=RelationalOp(
                            loc=SourceLoc(lineno=4, start=7, end=12),
                            op="<",
                            lhs=Name(
                                loc=SourceLoc(lineno=4, start=7, end=8), value="x"
                            ),
                            rhs=Integer(
                                loc=SourceLoc(lineno=4, start=11, end=12), value=0
                            ),
                        ),
                        body=[
                            Return(
                                loc=SourceLoc(lineno=5, start=7, end=16),
                                expr=UnaryOp(
                                    loc=SourceLoc(lineno=5, start=14, end=16),
                                    op="-",
                                    expr=Name(
                                        loc=SourceLoc(lineno=5, start=15, end=16),
                                        value="x",
                                    ),
                                ),
                            )
                        ],
                        else_=[],
                    ),
                    Return(
                        loc=SourceLoc(lineno=7, start=4, end=12),
                        expr=Name(loc=SourceLoc(lineno=7, start=11, end=12), value="x"),
                    ),
                ],
            ),
            Print(
                loc=SourceLoc(lineno=10, start=1, end=13),
                expr=Call(
                    loc=SourceLoc(lineno=10, start=7, end=12),
                    name="abs",
                    args=[Integer(loc=SourceLoc(lineno=10, start=11, end=12), value=2)],
                ),
            ),
            Print(
                loc=SourceLoc(lineno=11, start=1, end=14),
                expr=Call(
                    loc=SourceLoc(lineno=11, start=7, end=13),
                    name="abs",
                    args=[
                        UnaryOp(
                            loc=SourceLoc(lineno=11, start=11, end=13),
                            op="-",
                            expr=Integer(
                                loc=SourceLoc(lineno=11, start=12, end=13), value=2
                            ),
                        )
                    ],
                ),
            ),
        ],
    )


def test_optional_value():
    source = read_source("test_optvalue.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=138),
        statements=[
            VariableDecl(loc=SourceLoc(lineno=2, start=1, end=6), name="x"),
            Function(
                loc=SourceLoc(lineno=4, start=1, end=1),
                name="setx",
                args=["v"],
                body=[
                    Assignment(
                        loc=SourceLoc(lineno=5, start=5, end=10),
                        lhs=Name(loc=SourceLoc(lineno=5, start=5, end=6), value="x"),
                        rhs=Name(loc=SourceLoc(lineno=5, start=9, end=10), value="v"),
                    )
                ],
            ),
            ExprAsStatement(
                loc=SourceLoc(lineno=1, start=1, end=10),
                expr=Call(
                    loc=SourceLoc(lineno=8, start=1, end=9),
                    name="setx",
                    args=[Integer(loc=SourceLoc(lineno=8, start=6, end=9), value=123)],
                ),
            ),
            Print(
                loc=SourceLoc(lineno=9, start=1, end=8),
                expr=Name(loc=SourceLoc(lineno=9, start=7, end=8), value="x"),
            ),
        ],
    )


def test_multiple_args():
    source = read_source("test_multiple.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=171),
        statements=[
            Function(
                loc=SourceLoc(lineno=2, start=1, end=1),
                name="f",
                args=["x", "y", "z"],
                body=[
                    Return(
                        loc=SourceLoc(lineno=3, start=5, end=23),
                        expr=BinOp(
                            loc=SourceLoc(lineno=3, start=12, end=23),
                            op="*",
                            lhs=Parenthesis(
                                loc=SourceLoc(lineno=3, start=12, end=18),
                                expr=BinOp(
                                    loc=SourceLoc(lineno=3, start=13, end=18),
                                    op="+",
                                    lhs=Name(
                                        loc=SourceLoc(lineno=3, start=13, end=14),
                                        value="x",
                                    ),
                                    rhs=Name(
                                        loc=SourceLoc(lineno=3, start=17, end=18),
                                        value="y",
                                    ),
                                ),
                            ),
                            rhs=Name(
                                loc=SourceLoc(lineno=3, start=22, end=23), value="z"
                            ),
                        ),
                    )
                ],
            ),
            Print(
                loc=SourceLoc(lineno=5, start=1, end=15),
                expr=Call(
                    loc=SourceLoc(lineno=5, start=7, end=14),
                    name="f",
                    args=[
                        Integer(loc=SourceLoc(lineno=5, start=9, end=10), value=1),
                        Integer(loc=SourceLoc(lineno=5, start=11, end=12), value=2),
                        Integer(loc=SourceLoc(lineno=5, start=13, end=14), value=3),
                    ],
                ),
            ),
            Function(
                loc=SourceLoc(lineno=8, start=1, end=1),
                name="g",
                args=[],
                body=[
                    Return(
                        loc=SourceLoc(lineno=9, start=4, end=13),
                        expr=Integer(
                            loc=SourceLoc(lineno=9, start=11, end=13), value=42
                        ),
                    )
                ],
            ),
            Print(
                loc=SourceLoc(lineno=12, start=1, end=10),
                expr=Call(loc=SourceLoc(lineno=12, start=7, end=9), name="g", args=[]),
            ),
        ],
    )


def test_passes_logical_op_test():
    source = read_source("test_logical.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=447),
        statements=[
            Variable(
                loc=SourceLoc(lineno=2, start=1, end=10),
                name="x",
                expr=Integer(loc=SourceLoc(lineno=2, start=9, end=10), value=3),
            ),
            Variable(
                loc=SourceLoc(lineno=3, start=1, end=11),
                name="y",
                expr=Integer(loc=SourceLoc(lineno=3, start=9, end=11), value=10),
            ),
            Variable(
                loc=SourceLoc(lineno=4, start=1, end=11),
                name="z",
                expr=Integer(loc=SourceLoc(lineno=4, start=9, end=11), value=20),
            ),
            Branch(
                loc=SourceLoc(lineno=7, start=7, end=1),
                condition=Boolean(
                    loc=SourceLoc(lineno=7, start=4, end=4), value="true"
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=8, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=8, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=10, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=10, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=13, start=13, end=1),
                condition=Boolean(
                    loc=SourceLoc(lineno=13, start=4, end=5), value="false"
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=14, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=14, start=10, end=11), value=0
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=16, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=16, start=10, end=11), value=1
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=19, start=19, end=1),
                condition=LogicalOp(
                    loc=SourceLoc(lineno=19, start=4, end=19),
                    op="and",
                    lhs=RelationalOp(
                        loc=SourceLoc(lineno=19, start=4, end=9),
                        op="<",
                        lhs=Name(loc=SourceLoc(lineno=19, start=4, end=5), value="x"),
                        rhs=Name(loc=SourceLoc(lineno=19, start=8, end=9), value="y"),
                    ),
                    rhs=RelationalOp(
                        loc=SourceLoc(lineno=19, start=14, end=19),
                        op="<",
                        lhs=Name(loc=SourceLoc(lineno=19, start=14, end=15), value="y"),
                        rhs=Name(loc=SourceLoc(lineno=19, start=18, end=19), value="z"),
                    ),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=20, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=20, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=22, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=22, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=25, start=25, end=1),
                condition=LogicalOp(
                    loc=SourceLoc(lineno=25, start=4, end=26),
                    op="or",
                    lhs=Negation(
                        loc=SourceLoc(lineno=25, start=4, end=13),
                        op="not",
                        expr=RelationalOp(
                            loc=SourceLoc(lineno=25, start=8, end=13),
                            op="<",
                            lhs=Name(
                                loc=SourceLoc(lineno=25, start=8, end=9), value="x"
                            ),
                            rhs=Name(
                                loc=SourceLoc(lineno=25, start=12, end=13), value="y"
                            ),
                        ),
                    ),
                    rhs=Negation(
                        loc=SourceLoc(lineno=25, start=17, end=26),
                        op="not",
                        expr=RelationalOp(
                            loc=SourceLoc(lineno=25, start=21, end=26),
                            op="<",
                            lhs=Name(
                                loc=SourceLoc(lineno=25, start=21, end=22), value="y"
                            ),
                            rhs=Name(
                                loc=SourceLoc(lineno=25, start=25, end=26), value="z"
                            ),
                        ),
                    ),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=26, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=26, start=10, end=11), value=0
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=28, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=28, start=10, end=11), value=1
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=31, start=31, end=1),
                condition=LogicalOp(
                    loc=SourceLoc(lineno=31, start=4, end=19),
                    op="or",
                    lhs=RelationalOp(
                        loc=SourceLoc(lineno=31, start=4, end=9),
                        op="<",
                        lhs=Name(loc=SourceLoc(lineno=31, start=4, end=5), value="x"),
                        rhs=Integer(loc=SourceLoc(lineno=31, start=8, end=9), value=0),
                    ),
                    rhs=RelationalOp(
                        loc=SourceLoc(lineno=31, start=13, end=19),
                        op=">",
                        lhs=Name(loc=SourceLoc(lineno=31, start=13, end=14), value="z"),
                        rhs=Integer(
                            loc=SourceLoc(lineno=31, start=17, end=19), value=30
                        ),
                    ),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=32, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=32, start=10, end=11), value=0
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=34, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=34, start=10, end=11), value=1
                        ),
                    )
                ],
            ),
            Branch(
                loc=SourceLoc(lineno=37, start=37, end=1),
                condition=LogicalOp(
                    loc=SourceLoc(lineno=37, start=4, end=23),
                    op="or",
                    lhs=Negation(
                        loc=SourceLoc(lineno=37, start=4, end=13),
                        op="not",
                        expr=RelationalOp(
                            loc=SourceLoc(lineno=37, start=8, end=13),
                            op="<",
                            lhs=Name(
                                loc=SourceLoc(lineno=37, start=8, end=9), value="x"
                            ),
                            rhs=Integer(
                                loc=SourceLoc(lineno=37, start=12, end=13), value=0
                            ),
                        ),
                    ),
                    rhs=RelationalOp(
                        loc=SourceLoc(lineno=37, start=17, end=23),
                        op=">",
                        lhs=Name(loc=SourceLoc(lineno=37, start=17, end=18), value="z"),
                        rhs=Integer(
                            loc=SourceLoc(lineno=37, start=21, end=23), value=30
                        ),
                    ),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=38, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=38, start=10, end=11), value=1
                        ),
                    )
                ],
                else_=[
                    Print(
                        loc=SourceLoc(lineno=40, start=4, end=11),
                        expr=Integer(
                            loc=SourceLoc(lineno=40, start=10, end=11), value=0
                        ),
                    )
                ],
            ),
        ],
    )


def test_break():
    source = read_source("test_break.wb")
    ast = Parser(tokenize(source), source).parse()
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=122),
        statements=[
            Variable(
                loc=SourceLoc(lineno=3, start=1, end=10),
                name="n",
                expr=Integer(loc=SourceLoc(lineno=3, start=9, end=10), value=0),
            ),
            While(
                loc=SourceLoc(lineno=4, start=1, end=1),
                condition=RelationalOp(
                    loc=SourceLoc(lineno=4, start=7, end=13),
                    op="==",
                    lhs=Integer(loc=SourceLoc(lineno=4, start=7, end=8), value=0),
                    rhs=Integer(loc=SourceLoc(lineno=4, start=12, end=13), value=0),
                ),
                body=[
                    Print(
                        loc=SourceLoc(lineno=5, start=5, end=12),
                        expr=Name(loc=SourceLoc(lineno=5, start=11, end=12), value="n"),
                    ),
                    Assignment(
                        loc=SourceLoc(lineno=6, start=5, end=14),
                        lhs=Name(loc=SourceLoc(lineno=6, start=5, end=6), value="n"),
                        rhs=BinOp(
                            loc=SourceLoc(lineno=6, start=9, end=14),
                            op="+",
                            lhs=Name(
                                loc=SourceLoc(lineno=6, start=9, end=10), value="n"
                            ),
                            rhs=Integer(
                                loc=SourceLoc(lineno=6, start=13, end=14), value=1
                            ),
                        ),
                    ),
                    Branch(
                        loc=SourceLoc(lineno=7, start=7, end=5),
                        condition=RelationalOp(
                            loc=SourceLoc(lineno=7, start=8, end=15),
                            op="==",
                            lhs=Name(
                                loc=SourceLoc(lineno=7, start=8, end=9), value="n"
                            ),
                            rhs=Integer(
                                loc=SourceLoc(lineno=7, start=13, end=15), value=10
                            ),
                        ),
                        body=[Break(loc=SourceLoc(lineno=8, start=9, end=14))],
                        else_=[],
                    ),
                ],
            ),
        ],
    )
