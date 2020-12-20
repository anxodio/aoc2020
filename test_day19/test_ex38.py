import regex  # type: ignore
from pathlib import Path
from typing import Dict, List, Tuple

Rules = Dict[int, str]


def build_regex_from_rules(rules: Rules, actual: str = "0") -> str:
    if not actual.isdigit():
        return actual

    rule = rules[int(actual)]
    return (
        f"(?:{''.join([build_regex_from_rules(rules, part) for part in rule.split()])})"
    )


def build_rules_from_lines(lines: List[str]) -> Rules:
    rules: Rules = {}
    for line in lines:
        raw_index, raw_rule = line.split(": ")
        rules[int(raw_index)] = raw_rule.replace('"', "")
    return rules


def parse_input(filename: str) -> Tuple[str, List[str]]:
    with open((Path(__file__).parent / filename)) as f:
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
    # Recursive regex: https://www.regular-expressions.info/recurse.html
    # with help of reddit 😅
    rules[8] = "42 +"
    rules[11] = "(?P<group> 42 (?&group)? 31 )"
    regex = build_regex_from_rules(rules)
    return regex, message_lines


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
        == "(?:(?:a)(?:(?:a)(?:b)|(?:b)(?:a)))"
    )


def test_build_rules_from_lines():
    assert build_rules_from_lines(["0: 1 2", '1: "a"', "2: 1 3 | 3 1", '3: "b"']) == {
        0: "1 2",
        1: "a",
        2: "1 3 | 3 1",
        3: "b",
    }


def test_recursive_rules():
    rules_regex, message_lines = parse_input("input_test.txt")
    assert (
        sum(bool(regex.fullmatch(rules_regex, message)) for message in message_lines)
        == 12
    )


if __name__ == "__main__":
    rules_regex, message_lines = parse_input("input.txt")
    print(sum(bool(regex.fullmatch(rules_regex, message)) for message in message_lines))
