from format import format_program
from model import (
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


def print_source(program: Program):
    print(format_program(program))


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

print("\n---- PROGRAM 1  ----\n")
print_source(program_1)
print("\n---- PROGRAM 2  ----\n")
print_source(program_2)
print("\n---- PROGRAM 3  ----\n")
print_source(program_3)
