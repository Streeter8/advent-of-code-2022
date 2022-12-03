from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 3

    @property
    def test_input_data(self) -> Iterable:
        return [
            "vJrwpWtwJgWrhcsFMMfFFhFp\n",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\n",
            "PmmdzqPrVvPwwTWBwg\n",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\n",
            "ttgJtRGJQctTZtZT\n",
            "CrZsJsPPZsGzwwsLwLmpwMDw\n",
        ]

    @property
    def test_solution(self):
        return 157

    @property
    def test_solution_part_two(self):
        return 70

    @property
    def _solution(self):
        return 7821

    @property
    def _solution_part_two(self):
        return 2752

    def part_one(self):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        value = {letter: index for index, letter in enumerate(alphabet, start=1)}

        items = 0
        for rucksack in self.input_data_stripped():
            length = int(len(rucksack) / 2)
            common_item = min(set(rucksack[:length]).intersection(set(rucksack[length:])))
            items += value[common_item]

        self.verify_solution(items)

    def part_two(self):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        value = {letter: index for index, letter in enumerate(alphabet, start=1)}

        rucksacks = list(self.input_data_stripped())
        badges = 0
        for index in range(0, len(rucksacks), 3):
            badges += value[
                min(
                    set(rucksacks[index])
                    .intersection(set(rucksacks[index + 1]))
                    .intersection(set(rucksacks[index + 2]))
                )
            ]

        self.verify_solution_part_two(badges)

    def _run(self):
        self.part_one()
        self.part_two()
