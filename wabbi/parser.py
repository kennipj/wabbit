from functools import partial
from typing import Literal, cast

from wabbi.exceptions import WabbitSyntaxError
from wabbi.model import (
    Assignment,
    BinOp,
    Boolean,
    BooleanExpression,
    Branch,
    Break,
    Call,
    ErrorExpr,
    ExprAsStatement,
    Expression,
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
    Statement,
    UnaryOp,
    Variable,
    VariableDecl,
    While,
)
from wabbi.tokenizer import Token


class Parser:
    def __init__(
        self, tokens: list[Token], source: str, fname: str = "file.wb"
    ) -> None:
        self.tokens = tokens
        self.idx = 0
        self.source = source
        self.fname = fname

    def expect(self, type_: str, fatal: bool = False) -> Token:
        token = self.tokens[self.idx]
        if token.type_ == type_:
            self.idx += 1
            return token
        elif fatal:
            raise ValueError(f"Expected {type_}. Got {token}")
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

    def parse_statement(self, err: WabbitSyntaxError | None = None) -> Statement | None:
        start = self.idx
        to_try = [
            self.parse_assignment,
            self.parse_print,
            self.parse_vardecl,
            self.parse_var,
            self.parse_return,
            self.parse_branch,
            self.parse_func,
            self.parse_while,
            self.parse_break,
            partial(self.parse_expr_as_stmt, err),
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        return None

    def parse_expr_as_stmt(
        self, err: WabbitSyntaxError | None = None
    ) -> ExprAsStatement:
        expr = self.parse_expression()
        self.expect("SEMI")
        return ExprAsStatement(expr=expr)

    def parse_expression(self, err: WabbitSyntaxError | None = None) -> Expression:
        start = self.idx
        to_try = [
            self.parse_add,
            self.parse_mul,
            self.parse_sub,
            self.parse_div,
            self.parse_term,
            partial(self.parse_errorexpr, err),
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_term(self, err: WabbitSyntaxError | None = None) -> Expression:
        start = self.idx
        to_try = [
            self.parse_parenthesis,
            self.parse_unary,
            self.parse_call,
            self.parse_name,
            self.parse_integer,
            partial(self.parse_errorexpr, err),
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_boolexpr(self, err: WabbitSyntaxError | None = None) -> BooleanExpression:
        start = self.idx
        to_try = [
            self.parse_or,
            self.parse_and,
            self.parse_bool_term,
            partial(self.parse_errorexpr, err),
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_bool_term(
        self, err: WabbitSyntaxError | None = None
    ) -> BooleanExpression:
        start = self.idx
        to_try = [
            self.parse_lt,
            self.parse_gt,
            self.parse_lte,
            self.parse_gte,
            self.parse_eq,
            self.parse_neq,
            self.parse_not,
            self.parse_bool,
            partial(self.parse_errorexpr, err),
        ]
        for func in to_try:
            try:
                return func()
            except SyntaxError:
                self.idx = start
        raise SyntaxError(f"Unexpected token: {self.tokens[start]}")

    def parse_or(self) -> LogicalOp:
        lhs = self.parse_bool_term()
        self.expect("OR")
        rhs = self.parse_bool_term()
        return LogicalOp(op="or", lhs=lhs, rhs=rhs)

    def parse_and(self) -> LogicalOp:
        lhs = self.parse_bool_term()
        self.expect("AND")
        rhs = self.parse_bool_term()
        return LogicalOp(op="and", lhs=lhs, rhs=rhs)

    def parse_not(self) -> Negation:
        self.expect("NOT")
        rhs = self.parse_bool_term()
        return Negation(op="not", expr=rhs)

    def parse_bool(self) -> Boolean:
        bool = self.expect("BOOL")
        return Boolean(value=cast(Literal["true", "false"], bool.value))

    def parse_parenthesis(self) -> Parenthesis:
        self.expect("LPAREN")
        expr = self.parse_expression()
        self.expect("RPAREN", fatal=True)
        return Parenthesis(expr)

    def parse_integer(self) -> Integer:
        token = self.expect("INTEGER")
        return Integer(value=int(token.value))

    def parse_unary(self) -> UnaryOp:
        self.expect("MINUS")
        rhs = self.parse_term()
        return UnaryOp(op="-", expr=rhs)

    def parse_lt(self) -> RelationalOp:
        lhs = self.parse_expression()
        self.expect("LT")
        rhs = self.parse_expression()
        return RelationalOp(op="<", lhs=lhs, rhs=rhs)

    def parse_gt(self) -> RelationalOp:
        lhs = self.parse_expression()
        self.expect("GT")
        rhs = self.parse_expression()
        return RelationalOp(op=">", lhs=lhs, rhs=rhs)

    def parse_lte(self) -> RelationalOp:
        lhs = self.parse_expression()
        self.expect("LTE")
        rhs = self.parse_expression()
        return RelationalOp(op="<=", lhs=lhs, rhs=rhs)

    def parse_gte(self) -> RelationalOp:
        lhs = self.parse_expression()
        self.expect("GTE")
        rhs = self.parse_expression()
        return RelationalOp(op=">=", lhs=lhs, rhs=rhs)

    def parse_eq(self) -> Expression:
        lhs = self.parse_expression()
        if tok := self.peek("ASSIGN"):
            self.idx += 1
            self.parse_expression()
            return ErrorExpr(self._make_err(tok, "Unexpected `=`. Did you mean `==`?"))
        self.expect("EQ")
        rhs = self.parse_expression()
        return RelationalOp(op="==", lhs=lhs, rhs=rhs)

    def parse_neq(self) -> RelationalOp:
        lhs = self.parse_expression()
        self.expect("NOTEQ")
        rhs = self.parse_expression()
        return RelationalOp(op="!=", lhs=lhs, rhs=rhs)

    # TODO(kennipj): Maybe refactor these binary operations into 1 func?
    def parse_add(self) -> BinOp:
        lhs = self.parse_term()
        self.expect("PLUS")
        rhs = self.parse_term()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise ValueError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="+", lhs=lhs, rhs=rhs)

    def parse_mul(self) -> BinOp:
        lhs = self.parse_term()
        self.expect("TIMES")
        rhs = self.parse_term()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise ValueError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="*", lhs=lhs, rhs=rhs)

    def parse_sub(self) -> BinOp:
        lhs = self.parse_term()
        self.expect("MINUS")
        rhs = self.parse_term()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise ValueError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="-", lhs=lhs, rhs=rhs)

    def parse_div(self) -> BinOp:
        lhs = self.parse_term()
        self.expect("DIVIDE")
        rhs = self.parse_term()

        if isinstance(lhs, BinOp) or isinstance(rhs, BinOp):
            raise ValueError(f"Unexpected binary operation: {lhs} + {rhs}")
        return BinOp(op="/", lhs=lhs, rhs=rhs)

    def parse_vardecl(self) -> VariableDecl:
        self.expect("VAR")
        name = self.expect("NAME")
        self.expect("SEMI")
        return VariableDecl(name=name.value)

    def parse_var(self) -> Variable:
        self.expect("VAR")
        name = self.expect("NAME")
        self.expect("ASSIGN")
        expr = self.parse_expression()
        self.expect("SEMI", fatal=True)
        return Variable(name=name.value, expr=expr)

    def parse_print(self) -> Print:
        self.expect("PRINT")
        expr = self.parse_expression()
        self.expect("SEMI", fatal=True)
        return Print(expr=expr)

    def parse_return(self) -> Return:
        self.expect("RETURN")
        expr = self.parse_expression()
        self.expect("SEMI", fatal=True)
        return Return(expr=expr)

    def parse_call(self) -> Call:
        func = self.expect("NAME")
        self.expect("LPAREN")
        if not self.peek("RPAREN"):
            args = self.parse_call_args()
        else:
            args = []
        self.expect("RPAREN", fatal=True)
        return Call(name=func.value, args=args)

    def parse_call_args(self) -> list[Expression]:
        args: list[Expression] = []
        while True:
            arg = self.parse_expression()
            if self.peek("RPAREN"):
                args.append(arg)
                break
            self.expect("COMMA", fatal=True)
            args.append(arg)
        return args

    def parse_func(self) -> Function:
        self.expect("FUNC")
        name = self.expect("NAME")
        self.expect("LPAREN")
        args = self.parse_func_args()
        self.expect("RPAREN", fatal=True)
        self.expect("LBRACE")
        statements = self.parse_statements()
        self.expect("RBRACE")
        return Function(name.value, args=args, body=statements)

    def parse_func_args(self) -> list[str]:
        args: list[str] = []
        while True:
            arg = self.peek("NAME")
            if not arg:
                break
            self.expect("NAME", fatal=True)
            if self.peek("RPAREN"):
                args.append(arg.value)
                break
            self.expect("COMMA", fatal=True)
            args.append(arg.value)
        return args

    def parse_while(self) -> While:
        self.expect("WHILE")
        rel = self.parse_boolexpr()
        self.expect("LBRACE", fatal=True)
        statements = self.parse_statements()
        self.expect("RBRACE", fatal=True)
        return While(condition=rel, body=statements)

    def parse_branch(self) -> Branch:
        self.expect("IF")
        rel = self.parse_boolexpr()
        self.expect("LBRACE", fatal=True)
        statements = self.parse_statements()
        self.expect("RBRACE", fatal=True)
        else_ = []
        if self.peek("ELSE"):
            self.expect("ELSE")
            self.expect("LBRACE")
            else_ = self.parse_statements()
            self.expect("RBRACE", fatal=True)
        return Branch(condition=rel, body=statements, else_=else_)

    def parse_assignment(self) -> Assignment:
        name = self.expect("NAME")
        self.expect("ASSIGN")
        expr = self.parse_expression()
        self.expect("SEMI", fatal=True)
        return Assignment(lhs=Name(value=name.value), rhs=expr)

    def parse_break(self) -> Break:
        self.expect("BREAK")
        self.expect("SEMI")
        return Break()

    def parse_name(self) -> Name:
        token = self.expect("NAME", fatal=False)
        return Name(token.value)

    def parse_errorexpr(self, err: WabbitSyntaxError | None) -> ErrorExpr:
        if not err:
            raise SyntaxError("Unhandled exception!")
        return ErrorExpr(err=err)

    def _make_err(self, token: Token, msg: str) -> WabbitSyntaxError:
        return WabbitSyntaxError.from_token(msg, self.fname, self.source, token)
