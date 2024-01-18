from utils import read_source

from wabbi.fold_constants import fold_constants
from wabbi.model import Integer, Print, Program, SourceLoc
from wabbi.parser import Parser
from wabbi.tokenizer import tokenize


def test_unary_op_fold():
    source = read_source("test_unary_fold.wb")
    ast = Parser(tokenize(source), source).parse()
    ast = fold_constants(ast)
    assert ast == Program(
        loc=SourceLoc(lineno=0, start=0, end=13),
        statements=[
            Print(
                loc=SourceLoc(lineno=1, start=0, end=12),
                expr=Integer(loc=SourceLoc(lineno=1, start=6, end=12), value=1),
            )
        ],
    )
