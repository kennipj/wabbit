from dataclasses import dataclass

KEYWORDS = {
    "var": "VAR",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "func": "FUNC",
    "return": "RETURN",
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

    def __len__(self) -> int:
        return len(self.value)


def tokenize(source: str) -> list[Token]:
    tokens = []
    n = 0
    while n < len(source):
        if source[n].isspace():
            n += 1

        elif source[n].isalpha():
            token = tokenize_alpha(n, source)
            tokens.append(token)
            n += len(token)

        elif source[n].isdigit():
            token = tokenize_digit(n, source)
            tokens.append(token)
            n += len(token)

        elif (symbol := peek(n, 1, source)) in TWO_CHAR_SYMBOLS:
            if symbol == "//":
                n = skip_line(n, source)
            else:
                tokens.append(Token(TWO_CHAR_SYMBOLS[symbol], symbol))
                n += len(symbol)

        elif source[n] in ONE_CHAR_SYMBOLS:
            tokens.append(Token(ONE_CHAR_SYMBOLS[source[n]], source[n]))
            n += 1

        else:
            raise SyntaxError(f"Unexpected token: {source[n]}")

    return tokens


def peek(start: int, num: int, source: str) -> str | None:
    if start + num < len(source) - num:
        return source[start : start + num + 1]
    return None


def tokenize_alpha(start: int, source: str) -> Token:
    n = start
    while n < len(source):
        if not source[n].isdigit() and not source[n].isalpha():
            break
        n += 1
    word = source[start:n]
    if word in KEYWORDS:
        return Token(KEYWORDS[word], word)
    return Token("NAME", word)


def tokenize_digit(start: int, source: str) -> Token:
    n = start
    while n < len(source):
        if not source[n].isdigit():
            break
        n += 1
    return Token("INTEGER", source[start:n])


def skip_line(start: int, source: str) -> int:
    n = start
    while n < len(source):
        if source[n] == "\n":
            break
        n += 1
    return n
