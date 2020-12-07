import re
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class Rule:
    bag: str
    contents: Dict[str, int]


def line_to_rule(line: str) -> Rule:
    # It can be done with only 1 regular expression? 🤔
    bag, raw_contents = line.split(" bags contain ")
    contents: Dict[str, int] = {
        match_object[2]: int(match_object[1])
        for match_object in re.findall(r"((\d) (\w+ \w+) bags?[,\.])", raw_contents)
    }
    return Rule(bag=bag, contents=contents)


def rules_to_graph(rules: List[Rule]) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(rule.bag for rule in rules)
    for rule in rules:
        graph.add_edges_from(
            (rule.bag, content_bag) for content_bag, quantity in rule.contents.items()
        )
    return graph


def count_bags_containing_bag(graph: nx.DiGraph, bag_name: str) -> int:
    return len(nx.algorithms.dag.ancestors(graph, bag_name))


def test_line_to_rule_with_no_bags():
    assert line_to_rule("faded blue bags contain no other bags.") == Rule(
        bag="faded blue", contents={}
    )


def test_line_to_rule_with_one_bag():
    assert line_to_rule("bright white bags contain 1 shiny gold bag.") == Rule(
        bag="bright white", contents={"shiny gold": 1}
    )


def test_line_to_rule_with_various_bags():
    assert line_to_rule(
        "shiny gold bags contain 2 dark olive bag, 2 vibrant plum bags, 3 bright white bags."
    ) == Rule(
        bag="shiny gold",
        contents={"dark olive": 2, "vibrant plum": 2, "bright white": 3},
    )


def test_rules_to_graph():
    graph = rules_to_graph(
        [
            Rule(bag="a", contents={}),
            Rule(bag="b", contents={}),
            Rule(
                bag="c",
                contents={"a": 5, "b": 6},
            ),
        ]
    )
    assert list(graph.nodes) == ["a", "b", "c"]
    assert list(graph.edges) == [("c", "a"), ("c", "b")]


def test_count_bags_containing_bag():
    graph = rules_to_graph(
        [
            Rule(bag="a", contents={}),
            Rule(bag="b", contents={}),
            Rule(
                bag="c",
                contents={"a": 5, "b": 6},
            ),
            Rule(
                bag="d",
                contents={"a": 3, "b": 4},
            ),
            Rule(
                bag="e",
                contents={"c": 1, "d": 2},
            ),
        ]
    )
    assert count_bags_containing_bag(graph, "a") == 3
    assert count_bags_containing_bag(graph, "c") == 1


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rules = [line_to_rule(line.rstrip("\n")) for line in f]

    print(count_bags_containing_bag(rules_to_graph(rules), "shiny gold"))
