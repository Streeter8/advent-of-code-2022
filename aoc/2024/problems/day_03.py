import re
from collections.abc import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 3

    @property
    def test_input_data(self) -> Iterable:
        return (
            "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
        )

    @property
    def test_solution(self) -> int:
        return 161

    @property
    def test_solution_part_two(self):
        return 48

    @property
    def _solution(self) -> int:
        return 189600467

    @property
    def _solution_part_two(self):
        return 107069718

    def part_one(self):
        count = 0
        data = "\n".join(self.input_data)
        results = re.findall(r"mul\(\d{1,3}\,\d{1,3}\)", data)
        for result in results:
            result = result.strip("mul()")
            x, y = map(int, result.split(","))
            count += x * y

        self.verify_solution(count)

    def part_two(self):
        do = True
        count = 0
        if self.test:
            data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        else:
            data = "\n".join(self.input_data)

        results = re.findall(r"mul\(\d{1,3}\,\d{1,3}\)|do\(\)|don\'t\(\)", data)
        for result in results:
            if result == "do()":
                do = True
                continue

            if result == "don't()":
                do = False
                continue

            if do:
                result = result.strip("mul()")
                x, y = map(int, result.split(","))
                count += x * y

        self.verify_solution_part_two(count)

    def _run(self):
        self.part_one()
        self.part_two()
