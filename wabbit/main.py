import subprocess
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from typer import Typer

from wabbit.add_types import add_types
from wabbit.bracecheck import validate_braces
from wabbit.check_types import check_types
from wabbit.deinit import deinit_variables
from wabbit.fold_constants import fold_constants
from wabbit.format import format_program
from wabbit.llvm import generate_llvm
from wabbit.model import Program
from wabbit.parser import Parser
from wabbit.resolve import resolve_scopes
from wabbit.tokenizer import tokenize as _tokenize
from wabbit.unscript import unscript_toplevel
from wabbit.validator import validate_ast

app = Typer()


@app.command()
def llvm(file: str, output: str | None = None):
    llvm = _compile_to_llvm(file)
    if output:
        with open(output, "w") as f:
            f.write(llvm)
        return
    print(llvm)


@app.command()
def compile(
    in_file: str,
    output: str,
):
    path = Path(output)
    llvm = _compile_to_llvm(in_file)

    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / path.with_suffix(".ll")
        with open(file_path, "w") as f:
            f.write(llvm)
        subprocess.call(
            [
                "clang",
                str(file_path),
                "wabbit/misc/runtime.c",
                "-o",
                f"wabbit/bin/{output}",
            ]
        )


@app.command()
def source(file: str, optimize: bool = False):
    ast = _to_ast(file)
    if optimize:
        ast = _simplify_tree(ast)
    print(format_program(ast))


@app.command()
def ast(
    file: str,
    validate: bool = False,
    precedence: bool = False,
    typed: bool = False,
    fold: bool = False,
    type_check: bool = False,
    deinit: bool = False,
    resolve: bool = False,
    unscript: bool = False,
):
    # TODO(kennipj) Set up automatic dependency-based AST parsing.:
    ast = _to_ast(file)
    if validate:
        ast = validate_ast(ast)
    elif precedence:
        ast = validate_ast(ast)
    elif typed:
        ast = validate_ast(ast)
        ast = add_types(ast)
    elif type_check:
        ast = validate_ast(ast)
        ast = add_types(ast)
        ast = check_types(ast)
    elif fold:
        ast = validate_ast(ast)
        ast = add_types(ast)
        ast = fold_constants(ast)
    elif deinit:
        ast = validate_ast(ast)
        ast = add_types(ast)
        ast = fold_constants(ast)
        ast = deinit_variables(ast)
    elif resolve:
        ast = validate_ast(ast)
        ast = add_types(ast)
        ast = fold_constants(ast)
        ast = deinit_variables(ast)
        ast = resolve_scopes(ast)
    elif unscript:
        ast = validate_ast(ast)
        ast = add_types(ast)
        ast = fold_constants(ast)
        ast = deinit_variables(ast)
        ast = resolve_scopes(ast)
        ast = unscript_toplevel(ast)

    pprint(ast)


@app.command()
def tokenize(file: str) -> None:
    with open(file) as f:
        source = f.read()
    pprint(_tokenize(source, file))


def _compile_to_llvm(path: str):
    ast = _to_ast(path)
    ast = _simplify_tree(ast)
    return generate_llvm(ast)


def _simplify_tree(ast: Program):
    ast = validate_ast(ast)
    # ast = set_precedence(ast)
    ast = add_types(ast)
    ast = check_types(ast)
    ast = fold_constants(ast)
    ast = deinit_variables(ast)
    ast = resolve_scopes(ast)
    ast = unscript_toplevel(ast)
    return ast


def _to_ast(file: str) -> Program:
    with open(file) as f:
        source = f.read()
    tokens = _tokenize(source, file)
    validate_braces(tokens, source, file)
    return Parser(tokens, source, file).parse()


if __name__ == "__main__":
    app()
