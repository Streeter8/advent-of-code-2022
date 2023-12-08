from datetime import datetime
from typing import Iterable

from aoc.utilities.aoc import AocBase


class Rock:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def left(self) -> list[tuple[int, int]]:
        raise NotImplementedError

    @property
    def right(self) -> list[tuple[int, int]]:
        raise NotImplementedError

    @property
    def bottom(self) -> list[tuple[int, int]]:
        raise NotImplementedError

    @property
    def points(self) -> set[tuple[int, int]]:
        raise NotImplementedError

    def blow(self, wind: str, grid: set[tuple[int, int]]) -> None:
        if "<" == wind:
            if self.can_move_left(grid):
                self.move_left()
        else:
            if self.can_move_right(grid):
                self.move_right()

    def move_left(self) -> None:
        self.x -= 1

    def move_right(self) -> None:
        self.x += 1

    def can_move_left(self, grid: set[tuple[int, int]]) -> bool:
        for x, y in self.left:
            if x < 1 or (x - 1, y) in grid:
                return False

        return True

    def can_move_right(self, grid: set[tuple[int, int]]) -> bool:
        for x, y in self.right:
            if x > 5 or (x + 1, y) in grid:
                return False

        return True

    def drop(self, grid: set[tuple[int, int]]) -> bool:
        if self.can_move_down(grid):
            self.y -= 1
            return True

        return False

    def can_move_down(self, grid: set[tuple[int, int]]) -> bool:
        for x, y in self.bottom:
            if (x, y - 1) in grid:
                return False

        return True


class HoriLine(Rock):
    @property
    def points(self) -> set[tuple[int, int]]:
        return {(self.x + _, self.y) for _ in range(4)}

    @property
    def left(self) -> list[tuple[int, int]]:
        return [(self.x, self.y)]

    @property
    def right(self) -> list[tuple[int, int]]:
        return [(self.x + 3, self.y)]

    @property
    def bottom(self) -> list[tuple[int, int]]:
        return [(self.x + _, self.y) for _ in range(4)]


class VertiLine(Rock):
    @property
    def points(self) -> set[tuple[int, int]]:
        return {(self.x, self.y + _) for _ in range(4)}

    @property
    def left(self) -> list[tuple[int, int]]:
        return [(self.x, self.y + _) for _ in range(4)]

    @property
    def right(self) -> list[tuple[int, int]]:
        return self.left

    @property
    def bottom(self) -> list[tuple[int, int]]:
        return [(self.x, self.y)]


class Plus(Rock):
    @property
    def points(self) -> set[tuple[int, int]]:
        return {
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x + 1, self.y + 1),
            (self.x + 2, self.y + 1),
            (self.x + 1, self.y + 2),
        }

    @property
    def left(self) -> list[tuple[int, int]]:
        return [(self.x + 1, self.y + 2), (self.x, self.y + 1), (self.x + 1, self.y)]

    @property
    def right(self) -> list[tuple[int, int]]:
        return [(self.x + 1, self.y + 2), (self.x + 2, self.y + 1), (self.x + 1, self.y)]

    @property
    def bottom(self) -> list[tuple[int, int]]:
        return [(self.x, self.y + 1), (self.x + 1, self.y), (self.x + 2, self.y + 1)]


class BackL(Rock):
    @property
    def points(self) -> set[tuple[int, int]]:
        return {
            (self.x, self.y),
            (self.x + 1, self.y),
            (self.x + 2, self.y),
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y + 2),
        }

    @property
    def left(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x + 2, self.y + 1), (self.x + 2, self.y + 2)]

    @property
    def right(self) -> list[tuple[int, int]]:
        return [(self.x + 2, self.y), (self.x + 2, self.y + 1), (self.x + 2, self.y + 2)]

    @property
    def bottom(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x + 1, self.y), (self.x + 2, self.y)]


class Square(Rock):
    @property
    def points(self) -> set[tuple[int, int]]:
        return {
            (self.x, self.y),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x + 1, self.y + 1),
        }

    @property
    def left(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x, self.y + 1)]

    @property
    def right(self) -> list[tuple[int, int]]:
        return [(self.x + 1, self.y), (self.x + 1, self.y + 1)]

    @property
    def bottom(self) -> list[tuple[int, int]]:
        return [(self.x, self.y), (self.x + 1, self.y)]


class RockTower:
    def __init__(self, winds: str, rocks: int):
        self.winds = winds
        self.wind_count = len(self.winds)

        self.rocks = rocks

        self.grid = set((_, 0) for _ in range(7))
        self.rock = None
        self.falling_rocks = [HoriLine, Plus, BackL, VertiLine, Square]
        self.falling_rocks_count = len(self.falling_rocks)

    @property
    def tower(self) -> str:
        tower = ""
        for y in reversed(range(self.height + 1)):
            if 0 == y:
                break

            tower += f"{y}".zfill(4)
            tower += ": |"
            for x in range(7):
                if (x, y) in self.grid:
                    tower += "#"
                else:
                    tower += "."
            tower += "|\n"

        tower += "+-------+"
        return tower

    @property
    def height(self) -> int:
        return max(y for _, y in self.grid) if self.grid else 0

    def add_rock(self, rock: int) -> None:
        self.rock = self.falling_rocks[rock % self.falling_rocks_count](2, self.height + 4)

    # def drop_rocks(self):
    #     height = self.height
    #
    #     points_to_drop = set()
    #     for x, y in self.grid:
    #         if y < height - 1000:
    #             points_to_drop.add((x, y))
    #
    #     self.grid = self.grid - points_to_drop

    def harden_rock(self) -> None:
        self.grid = self.grid.union(self.rock.points)
        self.rock = None

    @property
    def top_points(self) -> tuple[tuple[int, int]]:
        height = self.height

        return (
            (0, height - max(y for x, y in self.grid if x == 0)),
            (1, height - max(y for x, y in self.grid if x == 1)),
            (2, height - max(y for x, y in self.grid if x == 2)),
            (3, height - max(y for x, y in self.grid if x == 3)),
            (4, height - max(y for x, y in self.grid if x == 4)),
            (5, height - max(y for x, y in self.grid if x == 5)),
            (6, height - max(y for x, y in self.grid if x == 6)),
        )

    def simulate(self) -> int:
        now = datetime.now()
        wind_count = 0

        rock_patterns = set()
        pattern_rocks = set()
        first_rock = None
        repeating_rocks = None
        offset = None
        repeating_height = None

        for rock in range(self.rocks):
            wind_start = wind_count % self.wind_count

            self.add_rock(rock)
            self.rock.blow(self.winds[wind_count % self.wind_count], self.grid)
            wind_count += 1

            while self.rock.drop(self.grid):
                self.rock.blow(self.winds[wind_count % self.wind_count], self.grid)
                wind_count += 1

            rock_pattern = rock % self.falling_rocks_count, wind_start, wind_count % self.wind_count
            if rock_pattern not in rock_patterns:
                rock_patterns.add(rock_pattern)
                # first_rock = None
            else:
                if first_rock and rock_pattern == first_rock[2]:
                    print((rock, self.height, (rock_pattern, self.top_points)))

                if (rock_pattern, self.top_points) not in pattern_rocks:
                    pattern_rocks.add((rock_pattern, self.top_points))
                    if not first_rock:
                        print((rock, self.height, (rock_pattern, self.top_points)))
                        first_rock = rock, self.height, rock_pattern
                    # elif first_rock[2] == rock_pattern:
                else:
                    # print(first_rock)
                    # print(rock, self.height, (rock_pattern, self.top_points))
                    repeating_rocks = rock - first_rock[0]
                    offset = first_rock[0]
                    repeating_height = self.height - first_rock[1]
                    if first_rock and rock_pattern == first_rock[2]:
                        print((repeating_rocks, offset, repeating_height))

            self.harden_rock()
            if repeating_rocks and offset and repeating_height:
                break

        if not repeating_rocks or not offset or not repeating_height:
            return self.height

        remaining_steps = (self.rocks - offset) % repeating_rocks
        print(remaining_steps)
        for step in range(remaining_steps):
            self.add_rock(rock)
            self.rock.blow(self.winds[wind_count % self.wind_count], self.grid)
            wind_count += 1

            while self.rock.drop(self.grid):
                self.rock.blow(self.winds[wind_count % self.wind_count], self.grid)
                wind_count += 1

        computed_height = (
            self.height - (repeating_height * 2) - 1 + int(self.rocks / repeating_rocks) * repeating_height
        )
        return computed_height


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 17

    @property
    def test_input_data(self) -> Iterable:
        return [">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

    @property
    def steps(self) -> int:
        return 2022

    @property
    def test_solution(self):
        return 3068

    @property
    def test_solution_part_two(self):
        return 1514285714288

    @property
    def _solution(self):
        return 3157

    @property
    def _solution_part_two(self):
        return None

    def part_one(self):
        winds = list(self.input_data_stripped())[0]
        tower = RockTower(winds, self.steps)
        tower.simulate()

        # print(tower.tower)

        self.verify_solution(tower.height)

    def part_two(self):
        winds = list(self.input_data_stripped())[0]
        tower = RockTower(winds, 1000000000000)
        computed_height = tower.simulate()

        if not self.test:
            assert 1581449272867 < computed_height
            assert 1581449274346 < computed_height

        self.verify_solution_part_two(computed_height)

    def _run(self):
        self.part_one()
        self.part_two()
