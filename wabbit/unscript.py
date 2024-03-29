from typing import cast

from wabbit.model import (
    Function,
    FunctionArg,
    GlobalVar,
    Integer,
    Program,
    Return,
    SourceLoc,
    Type,
)
from wabbit.walker import Visitor, Walker


class UnscriptToplevel(Visitor):
    def visit_program(self, node: Program) -> Program:
        new_func = Function(
            name="main",
            args=[
                FunctionArg(
                    value="_",
                    type_=Type(value="int", loc=SourceLoc(0, 0, 0)),
                    loc=SourceLoc(0, 0, 0),
                )
            ],
            body=[],
            ret_type_=Type(value="int", loc=SourceLoc(0, 0, 0)),
            loc=SourceLoc(lineno=0, start=0, end=0),
        )
        new_program_stmts = []
        for stmt in node.statements:
            if type(stmt) in {GlobalVar, Function}:
                new_program_stmts.append(stmt)
                continue
            new_func.body.append(stmt)
        new_func.body.append(
            Return(
                expr=Integer(value=0, loc=SourceLoc(0, 0, 0)),
                loc=SourceLoc(0, 0, 0),
            )
        )
        node.statements = new_program_stmts + [new_func]
        return node


def unscript_toplevel(program: Program) -> Program:
    walker = Walker(
        UnscriptToplevel(
            to_visit=[Program], pre_visit=[], source=program.source, fname=program.fname
        )
    )
    return cast(Program, walker.traverse(program))
