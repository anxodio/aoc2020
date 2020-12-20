import re
from pathlib import Path
from typing import Dict, List

Rules = Dict[int, str]


def build_regex_from_rules(rules: Rules, index: int = 0) -> str:
    rule = rules[index]
    if rule.isalpha():
        return rule

    subrule = "|".join(
        [
            "".join(
                build_regex_from_rules(rules, int(subindex))
                for subindex in part.split(" ")
            )
            for part in rule.split(" | ")
        ]
    )
    if "|" in rule:
        subrule = f"({subrule})"
    return subrule


def build_rules_from_lines(lines: List[str]) -> Rules:
    rules: Rules = {}
    for line in lines:
        raw_index, raw_rule = line.split(": ")
        if raw_rule[0] == '"':
            raw_rule = raw_rule[1:-1]
        rules[int(raw_index)] = raw_rule
    return rules


def test_build_regex_from_rules():
    assert (
        build_regex_from_rules(
            {
                0: "1 2",
                1: "a",
                2: "1 3 | 3 1",
                3: "b",
            }
        )
        == "a(ab|ba)"
    )


def test_match_with_regex_from_rules():
    regex = build_regex_from_rules(
        {
            0: "4 1 5",
            1: "2 3 | 3 2",
            2: "4 4 | 5 5",
            3: "4 5 | 5 4",
            4: "a",
            5: "b",
        }
    )

    assert bool(re.fullmatch(regex, "ababbb"))
    assert not bool(re.fullmatch(regex, "bababa"))
    assert bool(re.fullmatch(regex, "abbbab"))
    assert not bool(re.fullmatch(regex, "aaabbb"))
    assert not bool(re.fullmatch(regex, "aaaabbb"))


def test_build_rules_from_lines():
    assert build_rules_from_lines(["0: 1 2", '1: "a"', "2: 1 3 | 3 1", '3: "b"']) == {
        0: "1 2",
        1: "a",
        2: "1 3 | 3 1",
        3: "b",
    }


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        rule_lines = []
        message_lines = []
        for line in f:
            clean_line: str = line.rstrip("\n")
            if clean_line == "":
                continue
            elif clean_line[0].isnumeric():
                rule_lines.append(clean_line)
            else:
                message_lines.append(clean_line)
    rules = build_rules_from_lines(rule_lines)
    regex = build_regex_from_rules(rules)
    print(sum(bool(re.fullmatch(regex, message)) for message in message_lines))
