from wab.model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    Function,
    Integer,
    Name,
    Parenthesis,
    Print,
    Program,
    Return,
    Variable,
    While,
)

program_1 = Program(
    statements=[
        Variable(name=Name("x"), expr=Integer(10)),
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

program_2 = Program(
    statements=[
        Variable(name=Name("n"), expr=Integer(value=0)),
        While(
            BinOp(op="<", lhs=Name(value="n"), rhs=Integer(10)),
            body=[
                Branch(
                    condition=BinOp(op="==", lhs=Name("n"), rhs=Integer(10)),
                    body=[
                        Variable(
                            name=Name("x"),
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

program_3 = Program(
    statements=[
        Function(
            name=Name("square"),
            args=[Name("x")],
            body=[
                Variable(
                    name=Name("r"), expr=BinOp(op="*", lhs=Name("x"), rhs=Name("x"))
                ),
                Return(Name("r")),
            ],
        ),
        Variable(
            name=Name("result"), expr=Call(name=Name("square"), args=[Integer(4)])
        ),
        Print(expr=Name("result")),
    ]
)


program_4 = Program(
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

program_5 = Program(
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
