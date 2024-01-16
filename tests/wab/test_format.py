from wab.format import format_program
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


def test_formats_program_1():
    program = Program(
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
    assert format_program(program) == (
        """var x = 10;
x = x + 1;
print (23 * 45) + x;"""
    )


def test_formats_program_2():
    program = Program(
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
    assert format_program(program) == (
        """var n = 0;
while n < 10 {
    if n == 10 {
        var x = n * 100;
        print x;
    } else {
        print n;
    }
    n = n + 1;
}"""
    )


def test_formats_program_3():
    program = Program(
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
    assert format_program(program) == (
        """func square(x) {
    var r = x * x;
    return r;
}
var result = square(4);
print result;"""
    )
