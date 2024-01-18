import subprocess
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from typer import Typer

from wabbi.deinit import deinit_variables
from wabbi.fold_constants import fold_constants
from wabbi.format import format_program
from wabbi.llvm import generate_llvm
from wabbi.model import Program
from wabbi.parser import Parser
from wabbi.resolve import resolve_scopes
from wabbi.tokenizer import tokenize as _tokenize
from wabbi.unscript import unscript_toplevel

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
                "wabbi/misc/runtime.c",
                "-o",
                f"wabbi/bin/{output}",
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
    fold: bool = False,
    deinit: bool = False,
    resolve: bool = False,
    unscript: bool = False,
):
    ast = _to_ast(file)
    if fold:
        ast = fold_constants(ast)
    if deinit:
        ast = deinit_variables(ast)
    if resolve:
        ast = resolve_scopes(ast)
    if unscript:
        ast = unscript_toplevel(ast)
    pprint(ast)


@app.command()
def tokenize(file: str) -> None:
    with open(file) as f:
        source = f.read()
    pprint(_tokenize(source))


def _compile_to_llvm(path: str):
    ast = _to_ast(path)
    ast = _simplify_tree(ast)
    return generate_llvm(ast)


def _simplify_tree(ast: Program):
    ast = fold_constants(ast)
    ast = deinit_variables(ast)
    ast = resolve_scopes(ast)
    ast = unscript_toplevel(ast)
    return ast


def _to_ast(file: str) -> Program:
    with open(file) as f:
        source = f.read()
    return Parser(_tokenize(source)).parse()


if __name__ == "__main__":
    app()
