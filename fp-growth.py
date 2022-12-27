import functools
import itertools
from typing import Optional


class Node:
    descedents: Optional[list]
    element: str
    count: int

    def __init__(self, element) -> None:
        self.descedents = None
        self.element = element
        self.count = 0


def dfs(n: Node, f):
    f(n)
    if n.descedents:
        for son in n.descedents:
            dfs(son, f)


if __name__ == "__main__":
    print("hello world")
    baskets = [
        {"a", "b", "c", "d", "e"},
        {"a", "c", "d"},
        {"a", "b", "c", "e"},
        {"a", "c", "d"},
        {"b", "d", "e"},
        {"a", "c", "d", "e"},
    ]

    curr_candidates = list(functools.reduce(lambda acc, x: acc.union(x), baskets))
    support = {
        candidate: sum([candidate in basket for basket in baskets]) / len(baskets)
        for candidate in curr_candidates
    }
    sorted_elements = sorted(curr_candidates, key=lambda x: -support[x])

    print(sorted_elements)

tree = Node("")

curr_node = tree
for basket in baskets:  # type: ignore    pass
    sorted_basket = sorted(basket, key=lambda x: sorted_elements.index(x))
    for element in sorted_basket:
        if curr_node.descedents:
            for son in element:
                if son.element == element:
                    curr_node.count += 1
                    curr_node = son

dfs(tree, lambda n: print(str(n)))
