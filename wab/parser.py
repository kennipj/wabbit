from typing import Callable

from wab.model import (
    Assignment,
    BinOp,
    Branch,
    Call,
    Expression,
    Function,
    Integer,
    Name,
    Parenthesis,
    Print,
    Program,
    Return,
    Statement,
    Variable,
    While,
)
from wab.tokenizer import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.idx = 0
        self.excluded_expressions = set()

    def expect(self, type_: str) -> Token:
        token = self.tokens[self.idx]
        if token.type_ == type_:
            self.idx += 1
            return token
        else:
            raise SyntaxError(f"Expected {type_}. Got {token}")

    def peek(self, type_: str, num: int = 0) -> Token | None:
        if not (self.idx + num < len(self.tokens)):
            return None
        token = self.tokens[self.idx + num]
        if token.type_ == type_:
            return token
        return None

    def parse(self) -> Program:
        statements = self.parse_statements()
        return Program(statements=statements)

    def parse_statements(self) -> list[Statement]:
        statements = []
        while stmt := self.parse_statement():
            statements.append(stmt)
            if self.idx >= len(self.tokens):
                break
        return statements

    def parse_statement(self) -> Statement | None:
        start = self.idx
        to_try = [
            self.parse_assignment,
            self.parse_print,
            self.parse_var,
            self.parse_return,
            self.parse_branch,
            self.parse_func,
            self.parse_while,
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        return None

    def parse_expression(self, exclude: list[Callable] | None = None) -> Expression:
        if not exclude:
            exclude = []
        start = self.idx
        to_try = [
            self.parse_add,
            self.parse_mul,
            self.parse_parenthesis,
            self.parse_call,
            self.parse_name,
            self.parse_integer,
        ]
        for func in to_try:
            if func in exclude:
                continue
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_relation(self) -> BinOp:
        start = self.idx
        to_try = [
            self.parse_eq,
            self.parse_lt,
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_parenthesis(self) -> Parenthesis:
        self.expect("LPAREN")
        expr = self.parse_expression()
        self.expect("RPAREN")
        return Parenthesis(expr)

    def parse_integer(self) -> Integer:
        token = self.expect("INTEGER")
        return Integer(value=int(token.value))

    def parse_lt(self) -> BinOp:
        lhs = self.parse_expression()
        self.expect("LT")
        rhs = self.parse_expression()
        return BinOp(op="<", lhs=lhs, rhs=rhs)

    def parse_eq(self) -> BinOp:
        lhs = self.parse_expression()
        self.expect("EQ")
        rhs = self.parse_expression()
        return BinOp(op="==", lhs=lhs, rhs=rhs)

    def parse_add(self) -> BinOp:
        lhs = self.parse_expression(exclude=[self.parse_add, self.parse_mul])
        self.expect("PLUS")
        rhs = self.parse_expression()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise SyntaxError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="+", lhs=lhs, rhs=rhs)

    def parse_mul(self) -> BinOp:
        lhs = self.parse_expression(exclude=[self.parse_add, self.parse_mul])
        self.expect("TIMES")
        rhs = self.parse_expression()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise SyntaxError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="*", lhs=lhs, rhs=rhs)

    def parse_var(self) -> Variable:
        self.expect("VAR")
        name = self.expect("NAME")
        self.expect("ASSIGN")
        expr = self.parse_expression()
        self.expect("SEMI")
        return Variable(name=name.value, expr=expr)

    def parse_print(self) -> Print:
        self.expect("PRINT")
        expr = self.parse_expression()
        self.expect("SEMI")
        return Print(expr=expr)

    def parse_return(self) -> Return:
        self.expect("RETURN")
        expr = self.parse_expression()
        self.expect("SEMI")
        return Return(expr=expr)

    def parse_call(self) -> Call:
        func = self.expect("NAME")
        self.expect("LPAREN")
        arg = self.parse_expression()
        self.expect("RPAREN")
        return Call(name=func.value, args=[arg])

    def parse_func(self) -> Function:
        self.expect("FUNC")
        name = self.expect("NAME")
        self.expect("LPAREN")
        arg = self.expect("NAME")
        self.expect("RPAREN")
        self.expect("LBRACE")
        statements = self.parse_statements()
        self.expect("RBRACE")
        return Function(name.value, args=[arg.value], body=statements)

    def parse_while(self) -> While:
        self.expect("WHILE")
        rel = self.parse_relation()
        self.expect("LBRACE")
        statements = self.parse_statements()
        self.expect("RBRACE")
        return While(condition=rel, body=statements)

    def parse_branch(self) -> Branch:
        self.expect("IF")
        rel = self.parse_relation()
        self.expect("LBRACE")
        statements = self.parse_statements()
        self.expect("RBRACE")
        else_ = []
        if self.peek("ELSE"):
            self.expect("ELSE")
            self.expect("LBRACE")
            else_ = self.parse_statements()
            self.expect("RBRACE")
        return Branch(condition=rel, body=statements, else_=else_)

    def parse_assignment(self) -> Assignment:
        name = self.expect("NAME")
        self.expect("ASSIGN")
        expr = self.parse_expression()
        self.expect("SEMI")
        return Assignment(lhs=Name(value=name.value), rhs=expr)

    def parse_name(self) -> Name:
        token = self.expect("NAME")
        return Name(token.value)