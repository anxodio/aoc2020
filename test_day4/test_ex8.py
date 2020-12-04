from pathlib import Path
from typing import Dict, List, Iterable
import re


Passport = Dict[str, str]


def build_passport_from_lines(lines: Iterable[str]) -> Passport:
    keyvalues = " ".join(lines).split(" ")
    return dict(((keyvalue.split(":")) for keyvalue in keyvalues))  # type: ignore


def separate_passport_lines(raw_lines: List[str]) -> Iterable[List[str]]:
    lines: List[str] = []
    for raw_line in raw_lines:
        if raw_line == "":
            yield lines
            lines = []
        else:
            lines.append(raw_line)
    yield lines


def count_valid_passports(passports: Iterable[Passport]) -> int:
    return sum(1 for passport in passports if is_valid_passport(passport))


def is_valid_passport(passport: Passport) -> bool:
    return (
        _has_all_mandatory_fields(passport)
        and _birth_year_is_valid(int(passport["byr"]))
        and _issue_year_is_valid(int(passport["iyr"]))
        and _expiration_year_is_valid(int(passport["eyr"]))
        and _height_is_valid(passport["hgt"])
        and _hair_color_is_valid(passport["hcl"])
        and _eye_color_is_valid(passport["ecl"])
        and _pid_is_valid(passport["pid"])
    )


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


def _height_is_valid(height: str) -> bool:
    try:
        number, metric = int(height[0:-2]), height[-2:]
    except Exception:
        return False

    if metric == "cm":
        return 150 <= number <= 193
    elif metric == "in":
        return 59 <= number <= 76
    else:
        return False


def _hair_color_is_valid(hair_color: str) -> bool:
    return bool(re.match(r"#[a-fA-F0-9]{6}$", hair_color))


def _eye_color_is_valid(eye_color: str) -> bool:
    VALID_EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    return eye_color in VALID_EYE_COLORS


def _pid_is_valid(pid: str) -> bool:
    return bool(re.match(r"[0-9]{9}$", pid))


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


def test_height_is_valid():
    assert _height_is_valid("60in") is True
    assert _height_is_valid("190cm") is True
    assert _height_is_valid("190in") is False
    assert _height_is_valid("190") is False
    assert _height_is_valid("1") is False


def test_hair_color_is_valid():
    assert _hair_color_is_valid("#123abc") is True
    assert _hair_color_is_valid("#123abz") is False
    assert _hair_color_is_valid("123abc") is False


def test_eye_color_is_valid():
    assert _eye_color_is_valid("brn") is True
    assert _eye_color_is_valid("wat") is False


def test_pid_is_valid():
    assert _pid_is_valid("000000001") is True
    assert _pid_is_valid("0123456789") is False


def test_count_valid_passports():
    assert (
        count_valid_passports(
            [
                {
                    "iyr": "2019",
                    "hcl": "#602927",
                    "eyr": "1967",
                    "hgt": "170cm",
                    "ecl": "grn",
                    "pid": "012533040",
                    "byr": "1946",
                },
                {
                    "eyr": "2029",
                    "ecl": "blu",
                    "cid": "129",
                    "byr": "1989",
                    "iyr": "2014",
                    "pid": "896056539",
                    "hcl": "#a97842",
                    "hgt": "165cm",
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
