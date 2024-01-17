from copy import deepcopy
from dataclasses import fields
from typing import Callable, Literal, Sequence, cast

from wabbi.model import Expression, Node

DIRECTION = Literal["backwards", "forwards", "both"]


class Visitor:
    def __init__(self, to_visit: list[type[Node]]) -> None:
        self.to_visit = to_visit


class Walker:
    def __init__(self, visitor: Visitor) -> None:
        self._to_call: dict[type[Node], Callable[[Node], Node | list[Node]]] = {
            node_type: getattr(visitor, f"visit_{node_type.__name__.lower()}")
            for node_type in visitor.to_visit
        }

    def traverse(
        self, node: Node | Sequence[Node], direction: DIRECTION = "backwards"
    ) -> Node | Sequence[Node]:
        match node:
            case list():
                return self._traverse_nodes(node, direction)
            case Node():
                return self._traverse_node(node, direction)
            case _:
                return node

    def _traverse_node(self, node: Node, direction: DIRECTION):
        match_res = None
        new_node = deepcopy(node)
        if not isinstance(node, Node):
            return node

        if direction == "forwards" or direction == "both":
            if func := self._to_call.get(type(node)):
                match_res = cast(Expression, func(new_node))

        for field in fields(node):
            val = getattr(node, field.name)
            res = self.traverse(val, direction)
            setattr(new_node, field.name, res)

        if direction == "backwards" or direction == "both":
            if func := self._to_call.get(type(node)):
                match_res = cast(Expression, func(new_node))

        return match_res or new_node

    def _traverse_nodes(
        self, nodes: Sequence[Node], direction: DIRECTION
    ) -> Sequence[Node]:
        new_nodes = []
        for node in nodes:
            res = self.traverse(node, direction)
            if isinstance(res, list):
                new_nodes.extend(res)
            else:
                new_nodes.append(res)
        return new_nodes
