from wab.deinit import deinit_variables
from wab.fold_constants import fold_constants
from wab.format import format_program
from wab.model import Program
from wab.programs import program_1, program_2, program_3, program_4, program_5
from wab.resolve import resolve_scopes


def print_source(program: Program):
    print(format_program(program))


def simplify_tree(program: Program):
    program = fold_constants(program)
    program = deinit_variables(program)
    program = resolve_scopes(program)
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
