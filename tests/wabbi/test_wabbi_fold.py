from utils import read_source

from wabbi.fold_constants import fold_constants
from wabbi.model import Integer, Print, Program
from wabbi.parser import Parser
from wabbi.tokenizer import tokenize


def test_unary_op_fold():
    source = read_source("test_unary_fold.wb")
    ast = Parser(tokenize(source), source).parse()
    ast = fold_constants(ast)
    assert ast == Program(statements=[Print(Integer(1))])
