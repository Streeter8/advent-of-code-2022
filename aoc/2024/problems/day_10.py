from collections.abc import Iterable
from typing import Self

from aoc.utilities.aoc import AocBase


def add(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]


TURNS = (
    (0, 1),  # North
    (1, 0),  # East
    (0, -1),  # South
    (-1, 0),  # West
)


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 10

    @property
    def test_input_data(self) -> Iterable:
        return [
            "89010123\n",
            "78121874\n",
            "87430965\n",
            "96549874\n",
            "45678903\n",
            "32019012\n",
            "01329801\n",
            "10456732\n",
        ]

    @property
    def test_solution(self) -> int:
        return 36

    @property
    def test_solution_part_two(self) -> int:
        return 81

    @property
    def _solution(self) -> int:
        return 760

    @property
    def _solution_part_two(self) -> int:
        return 1764

    def _run(self):
        land_map = Map.from_input(self.input_data_stripped())
        self.verify_solution(land_map.analyze_trailheads())
        self.verify_solution_part_two(land_map.analyze_trailheads_all_paths())


class Map:
    def __init__(
        self,
        land_map: dict[tuple[int, int], int],
        trailheads: set[tuple[int, int]],
    ):
        self.land_map = land_map
        self.trailheads = trailheads

    @classmethod
    def from_input(cls, lines: Iterable[str]) -> Self:
        lines = list(lines)
        lines.reverse()
        land_map = {}
        trailheads = set()

        for row, line in enumerate(lines):
            for column, character in enumerate(line):
                height = int(character)
                land_map[(column, row)] = height

                if 0 == height:
                    trailheads.add((column, row))

        return cls(land_map, trailheads)

    def analyze_trailheads(self) -> int:
        peak_count = 0
        for trailhead in self.trailheads:
            peaks = self.peak_count([trailhead], 0)
            peak_count += len(peaks)

        return peak_count

    def peak_count(self, positions: Iterable[tuple[int, int]], height: int) -> set[tuple[int, int]]:
        new_positions = set()
        new_height = height + 1

        for position in positions:
            for turn in TURNS:
                new_position = add(position, turn)
                new_position_height = self.land_map.get(new_position)
                if new_position_height and new_position_height == new_height:
                    new_positions.add(new_position)

        if 9 == new_height:
            return new_positions

        return self.peak_count(new_positions, new_height)

    def analyze_trailheads_all_paths(self) -> int:
        peaks = self.peak_count_all_paths(self.trailheads, 0)
        return len(peaks)

    def peak_count_all_paths(self, positions: Iterable[tuple[int, int]], height: int) -> list[tuple[int, int]]:
        new_positions = []
        new_height = height + 1

        for position in positions:
            for turn in TURNS:
                new_position = add(position, turn)
                new_position_height = self.land_map.get(new_position)
                if new_position_height and new_position_height == new_height:
                    new_positions.append(new_position)

        if 9 == new_height:
            return new_positions

        return self.peak_count_all_paths(new_positions, new_height)
