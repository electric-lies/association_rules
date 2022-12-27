import functools
import itertools
from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class Rule:
    base: set
    head: set
    confidence = float

    def __init__(self, base, head, conf) -> None:
        self.base = base
        self.head = head
        self.confidence = conf

    def __str__(self) -> str:
        return f"Rule from {self.base} to {self.head} with confidence {self.confidence}"


def association_rules(
    big_groups: list[set], baskets: list[set], confidence_thresh: float
):
    res = []
    for group in big_groups:
        for elements in powerset(group):
            confidence = support(group, baskets) / support(
                group.difference(set(elements)), baskets
            )

            if confidence > confidence_thresh:
                res.append(Rule(group.difference(set(elements)), elements, confidence))
    return res


def support(candidate: set, baskets: list[set]) -> float:
    return sum([candidate.issubset(basket) for basket in baskets]) / len(baskets)


def apriori(baskets: list, support_thresh: float):
    i = 0
    # curr_candidates = itertools.accumulate(baskets, lambda acc, x: acc.)
    curr_candidates = [
        set(x) for x in functools.reduce(lambda acc, x: acc.union(x), baskets)
    ]
    # [{"a"}, {"b"}, {"c"}, {"d"}, {"e"}]
    print(curr_candidates)
    frequent_groups = []
    non_frequent_groups = []
    while curr_candidates:
        frequent_candidates, non_frequent_candidates = find_frequent_candidates(
            baskets, support_thresh, curr_candidates
        )

        frequent_groups.extend(frequent_candidates)
        non_frequent_groups.extend(non_frequent_candidates)

        curr_candidates = next_gen_candidates(
            i, non_frequent_candidates, frequent_candidates
        )

        i += 1
        print(f"{len(curr_candidates)=}")
    return frequent_groups


def find_frequent_candidates(baskets, support_thresh, curr_candidates):
    frequent_candidates = []
    non_frequent_candidates = []

    for candidate in curr_candidates:
        if support(candidate, baskets) > support_thresh:
            frequent_candidates.append(candidate)
        else:
            non_frequent_candidates.append(candidate)
    return frequent_candidates, non_frequent_candidates


def next_gen_candidates(i, non_frequent_groups, frequent_candidates):
    curr_candidates = []
    c1: set
    c2: set
    for c1, c2 in itertools.permutations(frequent_candidates, 2):
        if len(c1.intersection(c2)) == i:
            candidate = c1.union(c2)
            if candidate not in curr_candidates and not any(
                [nfg.issubset(candidate) for nfg in non_frequent_groups]
            ):
                curr_candidates.append(candidate)
    return curr_candidates


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

    big_groups = apriori(baskets, support_thresh=0.33)
    rules = association_rules(big_groups, baskets, confidence_thresh=0.50)

    print([str(r) for r in rules])
