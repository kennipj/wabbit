import pytest
from utils import read_source

from wab.parser import Parser
from wab.programs import program_1, program_2, program_3
from wab.tokenizer import tokenize


def test_parses_program_1():
    source = read_source("test_program1.wb")
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse()
    assert program == program_1


def test_parses_program_2():
    source = read_source("test_program2.wb")
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse()
    assert program == program_2


def test_parses_program_3():
    source = read_source("test_program3.wb")
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse()
    assert program == program_3


def test_errors_on_chained_additions():
    source = "print 1 + 2 + 3;"
    tokens = tokenize(source)
    parser = Parser(tokens)
    with pytest.raises(ValueError):
        parser.parse()


def test_errors_on_chained_additions_in_if():
    source = "if 1 < 2 {print 1 + 2 + 3;} else {}"
    tokens = tokenize(source)
    parser = Parser(tokens)
    with pytest.raises(ValueError):
        parser.parse()


def test_errors_on_chained_additions_in_else():
    source = "if 1 < 2 {} else {print 1 + 2 + 3}"
    tokens = tokenize(source)
    parser = Parser(tokens)
    with pytest.raises(ValueError):
        parser.parse()
