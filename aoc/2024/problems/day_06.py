from collections.abc import Iterable
from enum import Enum
from typing import Self

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 6

    @property
    def test_input_data(self) -> Iterable:
        return [
            "....#.....\n",
            ".........#\n",
            "..........\n",
            "..#.......\n",
            ".......#..\n",
            "..........\n",
            ".#..^.....\n",
            "........#.\n",
            "#.........\n",
            "......#...\n",
        ]

    @property
    def test_solution(self) -> int:
        return 41

    @property
    def test_solution_part_two(self):
        return 6

    @property
    def _solution(self) -> int:
        return 4988

    @property
    def _solution_part_two(self) -> int:
        return 1697

    def part_one(self):
        land_map = Map.from_input(self.input_data_stripped())
        land_map.print_map()
        land_map.walk_guard()
        land_map.print_map()
        self.verify_solution(land_map.land_count())

    def part_two(self):
        land_map = Map.from_input(self.input_data_stripped())

        circles = 0
        for x in range(land_map.column_count):
            for y in range(land_map.row_count):
                new_obstruction = (x, y)
                if new_obstruction in land_map.walls or new_obstruction == land_map.guard_position:
                    continue

                new_land_map = land_map.add_obstruction((x, y))
                circles += new_land_map.walk_guard()

            print(f"Finished with column {x} of {land_map.column_count}")

        self.verify_solution_part_two(circles)

    def _run(self):
        self.part_one()
        self.part_two()


def add(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]


class Direction(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "V"
    WEST = "<"

    def turn_right(self) -> Self:
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH


class Map:
    def __init__(
        self,
        land_map: dict[tuple[int, int], str],
        walls: set[tuple[int, int]],
        guard_position: tuple[int, int],
    ):
        self.land_map = land_map
        self.original_map = dict(self.land_map.items())
        self.walls = walls
        self.guard_position = guard_position
        self.original_guard_position = guard_position
        self.guard_direction = Direction.NORTH

        self.row_count = max(y for _, y in land_map) + 1
        self.column_count = max(x for x, _ in land_map) + 1

        self.used_positions = set()
        self.used_positions.add(self.orientation)

    @classmethod
    def from_input(cls, lines: Iterable[str]) -> Self:
        lines = list(lines)
        lines.reverse()
        land_map = {}
        walls = set()

        for row, line in enumerate(lines):
            for column, character in enumerate(line):
                land_map[(column, row)] = character
                if "#" == character:
                    walls.add((column, row))
                if "^" == character:
                    guard_position = (column, row)

        return cls(land_map, walls, guard_position)

    def add_obstruction(self, wall: tuple[int, int]) -> Self:
        land_map = dict(self.land_map.items())
        walls = set(self.walls)

        land_map[wall] = "#"
        walls.add(wall)

        return Map(land_map, walls, self.original_guard_position)

    @property
    def orientation(self) -> tuple[int, int, Direction]:
        return self.guard_position + (self.guard_direction,)

    @property
    def map(self) -> str:
        land_map = ""
        for row in reversed(range(self.row_count)):
            line = ""
            for column in range(self.column_count):
                position = (column, row)
                if position == self.guard_position:
                    line = f"{line}{self.guard_direction.value}"
                else:
                    line = f"{line}{self.land_map[(column, row)]}"

            land_map = f"{land_map}{line}\n"

        return land_map

    def print_map(self) -> None:
        print(self.map)

    @property
    def step_adjustment(self) -> tuple[int, int]:
        match self.guard_direction:
            case Direction.NORTH:
                return 0, 1
            case Direction.EAST:
                return 1, 0
            case Direction.SOUTH:
                return 0, -1
            case Direction.WEST:
                return -1, 0

    def get_next_step(self) -> tuple[int, int]:
        return add(self.guard_position, self.step_adjustment)

    def walk_guard(self) -> bool:
        while self.walk():
            # self.print_map()
            if self.orientation in self.used_positions:
                return True
            else:
                self.used_positions.add(self.orientation)

        return False

    def walk(self) -> bool:
        next_position = self.get_next_step()
        if not (land := self.land_map.get(next_position)):
            return False

        if "#" == land:
            self.turn()
            return self.walk()

        self.land_map[self.guard_position] = "X"
        self.guard_position = next_position

        return True

    def turn(self) -> None:
        self.guard_direction = self.guard_direction.turn_right()

    def land_count(self) -> int:
        count = sum(1 for land in self.land_map.values() if "X" == land)
        if "X" != self.land_map[self.guard_position]:
            count += 1

        return count
