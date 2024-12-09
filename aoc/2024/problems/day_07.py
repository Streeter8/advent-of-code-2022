from collections.abc import Iterable
from datetime import datetime
from itertools import product
from zoneinfo import ZoneInfo

from aoc.utilities.aoc import AocBase

CENTRAL = ZoneInfo("US/Central")


def now() -> str:
    return datetime.now(CENTRAL).isoformat()


def add(one: int, two: int) -> int:
    return one + two


def concatenate(one: int, two: int) -> int:
    return int(f"{one}{two}")


def multiply(one: int, two: int) -> int:
    return one * two


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 7

    @property
    def test_input_data(self) -> Iterable:
        return [
            "190: 10 19\n",
            "3267: 81 40 27\n",
            "83: 17 5\n",
            "156: 15 6\n",
            "7290: 6 8 6 15\n",
            "161011: 16 10 13\n",
            "192: 17 8 14\n",
            "21037: 9 7 18 13\n",
            "292: 11 6 16 20\n",
        ]

    @property
    def test_solution(self) -> int:
        return 3749

    @property
    def test_solution_part_two(self):
        return 11387

    @property
    def _solution(self) -> int:
        return 2654749936343

    @property
    def _solution_part_two(self) -> int:
        return 124060392153684

    def part_one(self):
        running_total = 0
        for line in self.input_data_stripped():
            one, two = line.split(": ")
            test_value = int(one)
            data = list(map(int, two.split(" ")))
            total = data[0]
            # print(f"{now()}: Testing {test_value=}")

            for operation_list in product([add, multiply], repeat=len(data) - 1):
                total = data[0]
                for operation, value in zip(operation_list, data[1:]):
                    total = operation(total, value)

                if total == test_value:
                    break

            if total == test_value:
                # print(f"{now()}: Adding {test_value=}")
                running_total += total
            # else:
            #     print(f"{now()}: Passing on {test_value=}")

        self.verify_solution(running_total)

    def part_two(self):
        running_total = 0
        for line in self.input_data_stripped():
            one, two = line.split(": ")
            test_value = int(one)
            data = list(map(int, two.split(" ")))
            total = data[0]
            # print(f"{now()}: Testing {test_value=}")

            for operation_list in product([add, multiply, concatenate], repeat=len(data) - 1):
                total = data[0]
                for operation, value in zip(operation_list, data[1:]):
                    total = operation(total, value)
                    # if test_value < total:
                    #     break

                if total == test_value:
                    break

            if total == test_value:
                # print(f"{now()}: Adding {test_value=}")
                running_total += total
            # else:
            #     print(f"{now()}: Passing on {test_value=}")

        self.verify_solution_part_two(running_total)

    def _run(self):
        self.part_one()
        self.part_two()
