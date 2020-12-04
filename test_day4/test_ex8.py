from pathlib import Path
from typing import Dict, List, Iterable
from dataclasses import dataclass


Passport = Dict[str, str]


def build_passport_from_lines(lines: List[str]) -> Passport:
    keyvalues = " ".join(lines).split(" ")
    return dict(((keyvalue.split(":")) for keyvalue in keyvalues))


def separate_passport_lines(raw_lines: List[str]) -> Iterable[List[str]]:
    lines = []
    for raw_line in raw_lines:
        if raw_line == "":
            yield lines
            lines = []
        else:
            lines.append(raw_line)
    yield lines


def count_valid_passports(passports: List[Passport]) -> int:
    return sum(1 for passport in passports if is_valid_passport(passport))


def is_valid_passport(passport: Passport) -> bool:
    return _has_all_mandatory_fields(passport)


def _has_all_mandatory_fields(passport: Passport) -> bool:
    # cid is removed from mandatory fields 😈
    MANDATORY_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return MANDATORY_FIELDS.issubset(passport.keys())


def _birth_year_is_valid(year: int) -> bool:
    return 1920 <= year <= 2002


def _issue_year_is_valid(year: int) -> bool:
    return 2010 <= year <= 2020


def _expiration_year_is_valid(year: int) -> bool:
    return 2020 <= year <= 2030


def test_has_all_mandatory_fields():
    assert (
        _has_all_mandatory_fields(
            {
                "ecl": "gry",
                "pid": "860033327",
                "eyr": "2020",
                "hcl": "#fffffd",
                "byr": "1937",
                "iyr": "2017",
                "cid": "147",
                "hgt": "183cm",
            }
        )
        is True
    )
    assert (
        _has_all_mandatory_fields(
            {
                "iyr": "2013",
                "ecl": "amb",
                "cid": "350",
                "eyr": "2023",
                "pid": "028048884",
                "hcl": "#cfa07d",
                "byr": "1929",
            }
        )
        is False
    )


def test_birth_year_is_valid():
    assert _birth_year_is_valid(2002) is True
    assert _birth_year_is_valid(2003) is False


def test_issue_year_is_valid():
    assert _issue_year_is_valid(2010) is True
    assert _issue_year_is_valid(2009) is False


def test_expiration_year_is_valid():
    assert _expiration_year_is_valid(2022) is True
    assert _expiration_year_is_valid(3000) is False


# def test_count_valid_passports():
#     assert (
#         count_valid_passports(
#             [
#                 {
#                     "ecl": "gry",
#                     "pid": "860033327",
#                     "eyr": "2020",
#                     "hcl": "#fffffd",
#                     "byr": "1937",
#                     "iyr": "2017",
#                     "cid": "147",
#                     "hgt": "183cm",
#                 },
#                 {
#                     "iyr": "2013",
#                     "ecl": "amb",
#                     "cid": "350",
#                     "eyr": "2023",
#                     "pid": "028048884",
#                     "hcl": "#cfa07d",
#                     "byr": "1929",
#                 },
#             ]
#         )
#         == 1
#     )


def test_build_passport_from_lines():
    assert build_passport_from_lines(
        [
            "hcl:#ae17e1 iyr:2013",
            "eyr:2024",
            "ecl:brn pid:760753108 byr:1931",
            "hgt:179cm",
        ]
    ) == {
        "hcl": "#ae17e1",
        "iyr": "2013",
        "eyr": "2024",
        "ecl": "brn",
        "pid": "760753108",
        "byr": "1931",
        "hgt": "179cm",
    }


def test_separate_passport_lines():
    assert list(
        separate_passport_lines(
            [
                "hcl:#ae17e1 iyr:2013",
                "eyr:2024",
                "",
                "ecl:brn pid:760753108 byr:1931",
                "hgt:179cm",
            ]
        )
    ) == [
        [
            "hcl:#ae17e1 iyr:2013",
            "eyr:2024",
        ],
        [
            "ecl:brn pid:760753108 byr:1931",
            "hgt:179cm",
        ],
    ]


if __name__ == "__main__":
    with open((Path(__file__).parent / "input.txt")) as f:
        raw_passports = [line.rstrip("\n") for line in f]

    passports = (
        build_passport_from_lines(raw_passport)
        for raw_passport in separate_passport_lines(raw_passports)
    )

    print(count_valid_passports(passports))
