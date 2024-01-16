import subprocess
from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from typer import Typer

from wab.deinit import deinit_variables
from wab.fold_constants import fold_constants
from wab.format import format_program
from wab.llvm import generate_llvm
from wab.model import Program
from wab.resolve import resolve_scopes
from wab.unscript import unscript_toplevel

app = Typer()


def simplify_tree(program: Program):
    program = fold_constants(program)
    program = deinit_variables(program)
    program = resolve_scopes(program)
    program = unscript_toplevel(program)
    return program


def compile_to_llvm(program: Program, path: Path):
    program = simplify_tree(program)
    source = generate_llvm(program)
    with open(path, "w") as f:
        f.write(source)


@app.command()
def llvm(program: str, output: str | None = None):
    programs = import_module("wab.programs")
    ast = cast(Program, getattr(programs, program))
    if output:
        compile_to_llvm(ast, Path(output))
        return
    ast = simplify_tree(ast)
    print(generate_llvm(ast))


@app.command()
def compile(
    program: str,
    fname: str,
):
    path = Path(fname)

    programs = import_module("wab.programs")
    ast = cast(Program, getattr(programs, program))
    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / path.with_suffix(".ll")
        compile_to_llvm(ast, file_path)
        subprocess.call(
            [
                "clang",
                str(file_path),
                "wab/misc/runtime.c",
                "-o",
                f"wab/bin/{fname}",
            ]
        )


@app.command()
def source(program: str):
    programs = import_module("wab.programs")
    ast = cast(Program, getattr(programs, program))
    print(format_program(ast))


if __name__ == "__main__":
    app()
