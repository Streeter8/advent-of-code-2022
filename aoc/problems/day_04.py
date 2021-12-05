from typing import Iterable

from aoc.utilities.aoc import AocBase


class BingoCard:
    def __init__(self, bingo_numbers: list[str]):
        columns = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}
        self.bingos = []
        self.numbers = set()

        for line in bingo_numbers:
            row = set()
            for index, number in enumerate(n for n in line.split(" ") if n):
                number = int(number)
                self.numbers.add(number)
                columns[index].add(number)
                row.add(number)
            self.bingos.append(row)

        for column in columns.values():
            self.bingos.append(column)

    def has_bingo(self, marks: set[int]) -> bool:
        if len(self.numbers.intersection(marks)) < 5:
            return False

        for bingo in self.bingos:
            if len(bingo.intersection(marks)) == 5:
                return True

        return False

    def sum_unmarked_numbers(self, marks: set[int]) -> int:
        return sum(self.numbers.difference(marks))


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 4

    def get_bingo_numbers(self) -> list[int]:
        if self.test:
            return [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
        else:
            # Styled for visual brevity
            return (
                [13, 47, 64, 52, 60, 69, 80, 85, 57, 1, 2, 6, 30, 81, 86, 40, 27, 26, 97, 77, 70, 92, 43, 94, 8]
                + [78, 3, 88, 93, 17, 55, 49, 32, 59, 51, 28, 33, 41, 83, 67, 11, 91, 53, 36, 96, 7, 34, 79, 98, 72]
                + [39, 56, 31, 75, 82, 62, 99, 66, 29, 58, 9, 50, 54, 12, 45, 68, 4, 46, 38, 21, 24, 18, 44, 48]
                + [16, 61, 19, 0, 90, 35, 65, 37, 73, 20, 22, 89, 42, 23, 15, 87, 74, 10, 71, 25, 14, 76, 84, 5, 63, 95]
            )

    @property
    def test_input_data(self) -> Iterable:
        return [
            "22 13 17 11  0\n",
            "8  2 23  4 24\n",
            "21  9 14 16  7\n",
            "6 10  3 18  5\n",
            "1 12 20 15 19\n",
            "\n",
            "3 15  0  2 22\n",
            "9 18 13 17  5\n",
            "19  8  7 25 23\n",
            "20 11 10 24  4\n",
            "14 21 16 12  6\n",
            "\n",
            "14 21 17 24  4\n",
            "10 16 15  9 19\n",
            "18  8 23 26 20\n",
            "22 11 13  6  5\n",
            "2  0 12  3  7\n",
        ]

    @property
    def test_solution(self) -> int:
        return 4512

    @property
    def test_solution_part_two(self) -> int:
        return 1924

    def construct_bingo_cards(self) -> list[BingoCard]:
        bingo_cards = []
        numbers = []
        for line in self.input_data_stripped():
            if not line:
                continue

            numbers.append(line)
            if len(numbers) == 5:
                bingo_cards.append(BingoCard(numbers))
                numbers = []

        return bingo_cards

    def part_one(self):
        bingo_cards = self.construct_bingo_cards()
        bingo_numbers = self.get_bingo_numbers()

        for index in range(5, len(bingo_numbers)):
            marks = set(bingo_numbers[:index])
            for bingo_card in bingo_cards:
                if bingo_card.has_bingo(marks):
                    sum_unmarked_numbers = bingo_card.sum_unmarked_numbers(marks)
                    score = sum_unmarked_numbers * bingo_numbers[index - 1]
                    self.verify_solution(score)
                    return

    def part_two(self):
        bingo_cards = self.construct_bingo_cards()
        bingo_numbers = self.get_bingo_numbers()
        last_score = None
        bingos = set()

        for index in range(5, len(bingo_numbers)):
            marks = set(bingo_numbers[:index])
            for bingdex, bingo_card in enumerate(bingo_cards):
                if bingdex in bingos:
                    continue

                if bingo_card.has_bingo(marks):
                    sum_unmarked_numbers = bingo_card.sum_unmarked_numbers(marks)
                    last_score = sum_unmarked_numbers * bingo_numbers[index - 1]
                    bingos.add(bingdex)

        self.verify_solution_part_two(last_score)

    def _run(self):
        self.part_one()
        self.part_two()
