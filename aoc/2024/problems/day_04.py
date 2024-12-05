from collections.abc import Iterable
from typing import Self

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 4

    @property
    def test_input_data(self) -> Iterable:
        return [
            "MMMSXXMASM\n",
            "MSAMXMSMSA\n",
            "AMXSXMAAMM\n",
            "MSAMASMSMX\n",
            "XMASAMXAMM\n",
            "XXAMMXXAMA\n",
            "SMSMSASXSS\n",
            "SAXAMASAAA\n",
            "MAMMMXMMMM\n",
            "MXMXAXMASX\n",
        ]

    @property
    def test_solution(self) -> int:
        return 18

    @property
    def test_solution_part_two(self):
        return 9

    @property
    def _solution(self) -> int:
        return 2551

    @property
    def _solution_part_two(self) -> int:
        return 1985

    def _run(self):
        x_letters = []
        a_letters = []
        letters = {}

        for y, row in enumerate(self.input_data_stripped()):
            for x, character in enumerate(row):
                letter = Letter(character, x, y)
                letters[letter.coordinates] = letter
                if "X" == character:
                    x_letters.append(letter)
                if "A" == character:
                    a_letters.append(letter)

        xmas_count = sum(x_letter.xmas_count(letters) for x_letter in x_letters)
        self.verify_solution(xmas_count)

        x_mas_count = sum(a_letter.is_x_mas(letters) for a_letter in a_letters)
        self.verify_solution_part_two(x_mas_count)


def add(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]


class Letter:
    def __init__(self, letter: str, x: int, y: int):
        self.letter = letter
        self.x = x
        self.y = y

    @property
    def next_letter(self) -> str | None:
        match self.letter:
            case "X":
                return "M"
            case "M":
                return "A"
            case "A":
                return "S"
            case "S":
                return None

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def directions(self) -> tuple[tuple[int, int], ...]:
        return (
            (0, 1),  # north
            (1, 1),  # northeast
            (1, 0),  # east
            (1, -1),  # southeast
            (0, -1),  # south
            (-1, -1),  # southwest
            (-1, 0),  # west
            (-1, 1),  # northwest
        )

    def xmas_count(self, letters: dict[tuple[int, int], Self]) -> int:
        return sum(self.is_xmas(letters, direction) for direction in self.directions)

    def is_xmas(self, letters: dict[tuple[int, int], Self], direction: tuple[int, int]) -> bool:
        next_letter = letters.get(add(self.coordinates, direction))
        if not next_letter:
            return False

        if self.next_letter != next_letter.letter:
            return False

        if self.next_letter == "S":
            return True

        return next_letter.is_xmas(letters, direction)

    def is_x_mas(self, letters: dict[tuple[int, int], Self]) -> bool:
        northwest_letter = letters.get((self.x - 1, self.y + 1))
        if not northwest_letter or (northwest_letter.letter != "M" and northwest_letter.letter != "S"):
            return False

        northeast_letter = letters.get((self.x + 1, self.y + 1))
        southwest_letter = letters.get((self.x - 1, self.y - 1))
        southeast_letter = letters.get((self.x + 1, self.y - 1))
        if not northwest_letter or not southwest_letter or not southeast_letter:
            return False

        if (
            northwest_letter.letter == northeast_letter.letter
            and southwest_letter.letter == southeast_letter.letter
            and northwest_letter.letter != southwest_letter.letter
            and "X" != southeast_letter.letter
        ):
            return True

        if (
            northwest_letter.letter == southwest_letter.letter
            and northeast_letter.letter == southeast_letter.letter
            and northwest_letter.letter != northeast_letter.letter
            and "X" != southeast_letter.letter
        ):
            return True

        return False
