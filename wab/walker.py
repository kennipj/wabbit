from copy import deepcopy
from dataclasses import fields
from typing import Callable, cast

from wab.model import Expression, Node


class Visitor:
    def __init__(self, to_visit: list[type[Node]]) -> None:
        self.to_visit = to_visit


class Walker:
    def __init__(self, visitor: Visitor) -> None:
        self._to_call: dict[type[Node], Callable[[Node], Node | list[Node]]] = {
            node_type: getattr(visitor, f"visit_{node_type.__name__.lower()}")
            for node_type in visitor.to_visit
        }

    def traverse(self, node: Node | list[Node]) -> Node | list[Node]:
        match node:
            case list():
                return self.traverse_nodes(node)
            case Node():
                return self.traverse_node(node)
            case _:
                return node

    def traverse_node(self, node: Node):
        match_res = None
        new_node = deepcopy(node)
        if not isinstance(node, Node):
            return node
        for field in fields(node):
            val = getattr(node, field.name)
            res = self.traverse(val)
            setattr(new_node, field.name, res)

        if func := self._to_call.get(type(node)):
            match_res = cast(Expression, func(new_node))
        return match_res or new_node

    def traverse_nodes(self, nodes: list[Node]) -> list[Node]:
        new_nodes = []
        for node in nodes:
            res = self.traverse(node)
            if isinstance(res, list):
                new_nodes.extend(res)
            else:
                new_nodes.append(res)
        return new_nodes
