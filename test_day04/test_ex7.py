from pathlib import Path
from typing import Dict, List, Iterable, Generator
from itertools import takewhile


Passport = Dict[str, str]


def build_passport_from_lines(lines: Iterable[str]) -> Passport:
    keyvalues = " ".join(lines).split(" ")
    return dict([(keyvalue.split(":")) for keyvalue in keyvalues])  # type: ignore


def separate_passport_lines(raw_lines: List[str]) -> Generator[List[str], None, None]:
    raw_lines_iterator = iter(raw_lines)
    while (lines := list(takewhile(lambda line: line != "", raw_lines_iterator))) :
        yield lines


def count_valid_passports(passports: Iterable[Passport]) -> int:
    return sum(1 for passport in passports if is_valid_passport(passport))


def is_valid_passport(passport: Passport) -> bool:
    # cid is removed from mandatory fields 😈
    MANDATORY_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return MANDATORY_FIELDS.issubset(passport.keys())


def test_is_valid_passport():
    assert (
        is_valid_passport(
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
        is_valid_passport(
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


def test_count_valid_passports():
    assert (
        count_valid_passports(
            [
                {
                    "ecl": "gry",
                    "pid": "860033327",
                    "eyr": "2020",
                    "hcl": "#fffffd",
                    "byr": "1937",
                    "iyr": "2017",
                    "cid": "147",
                    "hgt": "183cm",
                },
                {
                    "iyr": "2013",
                    "ecl": "amb",
                    "cid": "350",
                    "eyr": "2023",
                    "pid": "028048884",
                    "hcl": "#cfa07d",
                    "byr": "1929",
                },
            ]
        )
        == 1
    )


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
