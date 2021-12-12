from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    STEPS = 100

    def __init__(self, test: bool):
        super().__init__(test)
        self.octopuses: dict[tuple, int] = {}

    @property
    def day(self) -> int:
        return 11

    @property
    def test_solution(self):
        return {2: 35, 10: 204, 100: 1656}[self.STEPS]

    @property
    def test_solution_part_two(self) -> int:
        return 195

    def evaluate_octopuses(self):
        for y, line in enumerate(self.input_data):
            for x, octopus in enumerate(line):
                self.octopuses[(x, y)] = int(octopus)

    def get_octopuses_to_flash(self, exclude: set[tuple[int, int]]) -> set[tuple[int, int]]:
        to_flash = set()
        for location, octopus in self.octopuses.items():
            if location not in exclude and octopus > 9:
                to_flash.add(location)

        return to_flash

    def get_adjacent_octopuses(self, octopus: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = octopus
        adjacent_octopuses = []
        if x > 0:
            if y > 0:
                adjacent_octopuses.append((x - 1, y - 1))  # up, left

            adjacent_octopuses.append((x - 1, y))  # left
            if y < 9:
                adjacent_octopuses.append((x - 1, y + 1))  # down, left

        if x < 9:
            if y > 0:
                adjacent_octopuses.append((x + 1, y - 1))  # up, right

            adjacent_octopuses.append((x + 1, y))  # right
            if y < 9:
                adjacent_octopuses.append((x + 1, y + 1))  # down, right

        if y > 0:
            adjacent_octopuses.append((x, y - 1))  # up

        if y < 9:
            adjacent_octopuses.append((x, y + 1))  # down

        return adjacent_octopuses

    def step(self) -> int:
        for location in self.octopuses:
            self.octopuses[location] += 1

        flashes = 0
        octopuses_flashed = set()
        while octopuses_to_flash := self.get_octopuses_to_flash(octopuses_flashed):
            for octopus in octopuses_to_flash:
                flashes += 1
                self.octopuses[octopus] = 0
                octopuses_flashed.add(octopus)

                for adjacent_octopus in self.get_adjacent_octopuses(octopus):
                    if adjacent_octopus not in octopuses_flashed:
                        self.octopuses[adjacent_octopus] += 1

        return flashes

    def octopuses_all_flashed(self) -> bool:
        return all(0 == octopus for octopus in self.octopuses.values())

    def solve(self):
        self.evaluate_octopuses()
        flashes = 0
        step = 0
        while not self.octopuses_all_flashed():
            flashes += self.step()
            if step == self.STEPS:
                self.verify_solution(flashes)
            step += 1

        self.verify_solution_part_two(step)

    def _run(self):
        self.solve()

    @property
    def input_data(self) -> Iterable:
        if self.test:
            return [
                "5483143223",
                "2745854711",
                "5264556173",
                "6141336146",
                "6357385478",
                "4167524645",
                "2176841721",
                "6882881134",
                "4846848554",
                "5283751526",
            ]
        else:
            return [
                "5251578181",
                "6158452313",
                "1818578571",
                "3844615143",
                "6857251244",
                "2375817613",
                "8883514435",
                "2321265735",
                "2857275182",
                "4821156644",
            ]
