from wabbi.format import format_program
from wabbi.model import Program
from wabbi.parser import Parser
from wabbi.tokenizer import tokenize


def to_ast(program: str) -> Program:
    with open(f"wabbi/tests/{program}") as f:
        source = f.read()
    return Parser(tokenize(source)).parse()


def test_formats_optional_else():
    ast = to_ast("test_else.wb")
    assert format_program(ast) == (
        """func abs(x) {
    if x < 0 {
        return -x;
    }
    return x;
}
print abs(2);
print abs(-2);"""
    )


def test_formats_operators():
    ast = to_ast("test_operators.wb")
    assert format_program(ast) == (
        """var x = 2;
var y = 5;
print x + y;
print x - y;
print x * y;
print x / y;
print y / x;
print -x;
if x < y {
    print 1;
} else {
    print 0;
}
if x <= y {
    print 1;
} else {
    print 0;
}
if y > x {
    print 1;
} else {
    print 0;
}
if y >= x {
    print 1;
} else {
    print 0;
}
if x == y {
    print 0;
} else {
    print 1;
}
if x != y {
    print 1;
} else {
    print 0;
}"""
    )
