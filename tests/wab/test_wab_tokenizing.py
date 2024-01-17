from utils import read_source

from wab.tokenizer import Token, tokenize


def test_program_1():
    source = read_source("test_program1.wb")
    assert tokenize(source) == [
        Token(type_="VAR", value="var"),
        Token(type_="NAME", value="x"),
        Token(type_="ASSIGN", value="="),
        Token(type_="INTEGER", value="10"),
        Token(type_="SEMI", value=";"),
        Token(type_="NAME", value="x"),
        Token(type_="ASSIGN", value="="),
        Token(type_="NAME", value="x"),
        Token(type_="PLUS", value="+"),
        Token(type_="INTEGER", value="1"),
        Token(type_="SEMI", value=";"),
        Token(type_="PRINT", value="print"),
        Token(type_="LPAREN", value="("),
        Token(type_="INTEGER", value="23"),
        Token(type_="TIMES", value="*"),
        Token(type_="INTEGER", value="45"),
        Token(type_="RPAREN", value=")"),
        Token(type_="PLUS", value="+"),
        Token(type_="NAME", value="x"),
        Token(type_="SEMI", value=";"),
    ]


def test_program_2():
    source = read_source("test_program2.wb")
    assert tokenize(source) == [
        Token(type_="VAR", value="var"),
        Token(type_="NAME", value="n"),
        Token(type_="ASSIGN", value="="),
        Token(type_="INTEGER", value="0"),
        Token(type_="SEMI", value=";"),
        Token(type_="WHILE", value="while"),
        Token(type_="NAME", value="n"),
        Token(type_="LT", value="<"),
        Token(type_="INTEGER", value="10"),
        Token(type_="LBRACE", value="{"),
        Token(type_="IF", value="if"),
        Token(type_="NAME", value="n"),
        Token(type_="EQ", value="=="),
        Token(type_="INTEGER", value="5"),
        Token(type_="LBRACE", value="{"),
        Token(type_="VAR", value="var"),
        Token(type_="NAME", value="x"),
        Token(type_="ASSIGN", value="="),
        Token(type_="NAME", value="n"),
        Token(type_="TIMES", value="*"),
        Token(type_="INTEGER", value="100"),
        Token(type_="SEMI", value=";"),
        Token(type_="PRINT", value="print"),
        Token(type_="NAME", value="x"),
        Token(type_="SEMI", value=";"),
        Token(type_="RBRACE", value="}"),
        Token(type_="ELSE", value="else"),
        Token(type_="LBRACE", value="{"),
        Token(type_="PRINT", value="print"),
        Token(type_="NAME", value="n"),
        Token(type_="SEMI", value=";"),
        Token(type_="RBRACE", value="}"),
        Token(type_="NAME", value="n"),
        Token(type_="ASSIGN", value="="),
        Token(type_="NAME", value="n"),
        Token(type_="PLUS", value="+"),
        Token(type_="INTEGER", value="1"),
        Token(type_="SEMI", value=";"),
        Token(type_="RBRACE", value="}"),
    ]


def test_program_3():
    source = read_source("test_program3.wb")
    assert tokenize(source) == [
        Token(type_="FUNC", value="func"),
        Token(type_="NAME", value="square"),
        Token(type_="LPAREN", value="("),
        Token(type_="NAME", value="x"),
        Token(type_="RPAREN", value=")"),
        Token(type_="LBRACE", value="{"),
        Token(type_="VAR", value="var"),
        Token(type_="NAME", value="r"),
        Token(type_="ASSIGN", value="="),
        Token(type_="NAME", value="x"),
        Token(type_="TIMES", value="*"),
        Token(type_="NAME", value="x"),
        Token(type_="SEMI", value=";"),
        Token(type_="RETURN", value="return"),
        Token(type_="NAME", value="r"),
        Token(type_="SEMI", value=";"),
        Token(type_="RBRACE", value="}"),
        Token(type_="VAR", value="var"),
        Token(type_="NAME", value="result"),
        Token(type_="ASSIGN", value="="),
        Token(type_="NAME", value="square"),
        Token(type_="LPAREN", value="("),
        Token(type_="INTEGER", value="4"),
        Token(type_="RPAREN", value=")"),
        Token(type_="SEMI", value=";"),
        Token(type_="PRINT", value="print"),
        Token(type_="NAME", value="result"),
        Token(type_="SEMI", value=";"),
    ]
