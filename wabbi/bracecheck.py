from wabbi.exceptions import WabbitSyntaxError
from wabbi.tokenizer import Token


def validate_braces(tokens: list[Token], source: str, fname: str = "file.wb"):
    curly = []
    paren = []
    errors: list[WabbitSyntaxError] = []

    for token in tokens:
        if token.type_ == "LPAREN":
            paren.append(token)
        elif token.type_ == "RPAREN":
            if len(paren) > 0:
                paren.pop()
            else:
                errors.append(
                    WabbitSyntaxError.from_token(
                        "Found `)` with no opening `(`", fname, source, token
                    )
                )
        elif token.type_ == "LBRACE":
            curly.append(token)
        elif token.type_ == "RBRACE":
            if len(curly):
                curly.pop()
            else:
                errors.append(
                    WabbitSyntaxError.from_token(
                        "Found `}` with no opening `{`", fname, source, token
                    )
                )

    for token in curly:
        errors.append(
            WabbitSyntaxError.from_token(
                "Found `{` with no closing `}", fname, source, token
            )
        )

    for token in paren:
        errors.append(
            WabbitSyntaxError.from_token(
                "Found `(` with no closing `)", fname, source, token
            )
        )
    if errors:
        for err in errors:
            print(err)
        exit()
