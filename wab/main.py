from wab.deinit import deinit_variables
from wab.fold_constants import fold_constants
from wab.format import format_program
from wab.model import Program
from wab.programs import (
    bad_program_1,
    program_1,
    program_2,
    program_3,
    program_4,
    program_5,
    program_6,
    program_7,
)
from wab.resolve import resolve_scopes
from wab.unscript import unscript_toplevel


def print_source(program: Program):
    print(format_program(program))


def simplify_tree(program: Program):
    program = fold_constants(program)
    program = deinit_variables(program)
    program = resolve_scopes(program)
    program = unscript_toplevel(program)
    return program


print("\n---- PROGRAM 1  ----\n")
print_source(simplify_tree(program_1))
print("\n---- PROGRAM 2  ----\n")
print_source(simplify_tree(program_2))
print("\n---- PROGRAM 3  ----\n")
print_source(simplify_tree(program_3))
print("\n---- PROGRAM 4  ----\n")
print_source(simplify_tree(program_4))
print("\n---- PROGRAM 5  ----\n")
print_source(simplify_tree(program_5))
print("\n---- PROGRAM 6  ----\n")
print_source(simplify_tree(program_6))
print("\n---- PROGRAM 7  ----\n")
print_source(simplify_tree(program_7))
# print("\n---- BAD PROGRAM 1  ----\n")
# print_source(simplify_tree(bad_program_1))
