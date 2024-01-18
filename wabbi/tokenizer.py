from dataclasses import dataclass

from wabbi.exceptions import WabbitSyntaxError

KEYWORDS = {
    "var": "VAR",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "return": "RETURN",
    "not": "NOT",
    "true": "BOOL",
    "false": "BOOL",
    "or": "OR",
    "and": "AND",
    "break": "BREAK",
}

ONE_CHAR_SYMBOLS = {
    "+": "PLUS",
    "*": "TIMES",
    "-": "MINUS",
    "<": "LT",
    ">": "GT",
    "=": "ASSIGN",
    ";": "SEMI",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    "/": "DIVIDE",
    ",": "COMMA",
}

TWO_CHAR_SYMBOLS = {
    "==": "EQ",
    "<=": "LTE",
    ">=": "GTE",
    "!=": "NOTEQ",
    "//": "COMMENT",
}


@dataclass
class Token:
    type_: str
    value: str
    lineno: int
    column: int

    def __len__(self) -> int:
        return len(self.value)


def tokenize(source: str, fname: str = "file.wb") -> list[Token]:
    tokens = []
    n = 0
    lineno = 1
    last_line_pos = 0
    errors = []
    while n < len(source):
        if source[n] == "\n":
            lineno += 1
            last_line_pos = n
            n += 1

        elif source[n].isspace():
            n += 1

        elif source[n].isalpha():
            token = tokenize_alpha(n, source, lineno, last_line_pos)
            tokens.append(token)
            n += len(token)

        elif source[n].isdigit():
            token = tokenize_digit(n, source, lineno, last_line_pos)
            tokens.append(token)
            n += len(token)

        elif (symbol := peek(n, 1, source)) in TWO_CHAR_SYMBOLS:
            if symbol == "//":
                n = skip_line(n, source)
            else:
                tokens.append(
                    Token(TWO_CHAR_SYMBOLS[symbol], symbol, lineno, n - last_line_pos)
                )
                n += len(symbol)

        elif source[n] in ONE_CHAR_SYMBOLS:
            tokens.append(
                Token(ONE_CHAR_SYMBOLS[source[n]], source[n], lineno, n - last_line_pos)
            )
            n += 1

        else:
            errors.append(
                WabbitSyntaxError(
                    f"Invalid character: `{source[n]}`",
                    fname,
                    source,
                    lineno,
                    n - last_line_pos,
                    1,
                )
            )
            n += 1

    if errors:
        for err in errors:
            print(err)
        exit()
    return tokens


def peek(start: int, num: int, source: str) -> str | None:
    if start + num < len(source) - num:
        return source[start : start + num + 1]
    return None


def tokenize_alpha(start: int, source: str, lineno: int, last_line_pos: int) -> Token:
    n = start
    while n < len(source):
        if not source[n].isdigit() and not source[n].isalpha():
            break
        n += 1
    word = source[start:n]
    if word in KEYWORDS:
        return Token(KEYWORDS[word], word, lineno, start - last_line_pos)
    return Token("NAME", word, lineno, start - last_line_pos)


def tokenize_digit(start: int, source: str, lineno: int, last_line_pos: int) -> Token:
    n = start
    while n < len(source):
        if not source[n].isdigit():
            break
        n += 1
    return Token("INTEGER", source[start:n], lineno, start - last_line_pos)


def skip_line(start: int, source: str) -> int:
    n = start
    while n < len(source):
        if source[n] == "\n":
            break
        n += 1
    return n
