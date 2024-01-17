import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from typer import Typer

from wab.deinit import deinit_variables
from wab.fold_constants import fold_constants
from wab.format import format_program
from wab.llvm import generate_llvm
from wab.model import Program
from wab.parser import Parser
from wab.resolve import resolve_scopes
from wab.tokenizer import tokenize
from wab.unscript import unscript_toplevel

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
                "wab/misc/runtime.c",
                "-o",
                f"wab/bin/{output}",
            ]
        )


@app.command()
@app.command()
def source(file: str):
    ast = _to_ast(file)
    print(format_program(ast))


def _compile_to_llvm(path: str):
    ast = _to_ast(path)
    ast = _simplify_tree(ast)
    return generate_llvm(ast)


def _simplify_tree(program: Program):
    program = fold_constants(program)
    program = deinit_variables(program)
    program = resolve_scopes(program)
    program = unscript_toplevel(program)
    return program


def _to_ast(file: str) -> Program:
    with open(file) as f:
        source = f.read()
    return Parser(tokenize(source)).parse()


if __name__ == "__main__":
    app()
