from typing import cast

from wab.model import Function, GlobalVar, Integer, Program, Return
from wab.walker import Visitor, Walker


class UnscriptToplevel(Visitor):
    def visit_program(self, node: Program) -> Program:
        new_func = Function(name="main", args=["_"], body=[])
        new_program_stmts = []
        for stmt in node.statements:
            if type(stmt) in {GlobalVar, Function}:
                new_program_stmts.append(stmt)
                continue
            new_func.body.append(stmt)
        new_func.body.append(Return(Integer(0)))
        node.statements = new_program_stmts + [new_func]
        return node


def unscript_toplevel(program: Program) -> Program:
    walker = Walker(UnscriptToplevel([Program]))
    return cast(Program, walker.traverse(program))
