from typing import Iterable

from aoc.utilities.aoc import AocBase


class Decoder:
    def __init__(self, input_line: str):
        self.numbers, self.output = input_line.split(" | ")
        self._numbers = self.numbers.split(" ")

        self.solved_numbers = {}

        self.find_uniques()
        self.find_sixes()
        self.find_fives()

        self.code = self.translate()

    def translate(self) -> int:
        code = []
        for number in self.output.split(" "):
            number_set = set(number)
            for _number, encoding in self.solved_numbers.items():
                if number_set == encoding:
                    code.append(str(_number))

        return int("".join(code))

    def _pop_indexes(self, indexes: Iterable[int]) -> None:
        for index in sorted(indexes, reverse=True):
            self._numbers.pop(index)

    def find_uniques(self) -> None:
        indexes = []
        for index, number in enumerate(self._numbers):
            if len(number) == 2:
                indexes.append(index)
                self.solved_numbers[1] = set(number)
            elif len(number) == 3:
                indexes.append(index)
                self.solved_numbers[7] = set(number)
            elif len(number) == 4:
                indexes.append(index)
                self.solved_numbers[4] = set(number)
            elif len(number) == 7:
                indexes.append(index)
                self.solved_numbers[8] = set(number)

        self._pop_indexes(indexes)

    def find_sixes(self) -> None:
        four = self.solved_numbers[4]
        one = self.solved_numbers[1]
        indexes = []

        for index, number in enumerate(self._numbers):
            if len(number) == 6:
                number_set = set(number)
                if number_set.issuperset(four):
                    indexes.append(index)
                    self.solved_numbers[9] = number_set

                elif number_set.issuperset(one):
                    indexes.append(index)
                    self.solved_numbers[0] = number_set

                else:
                    indexes.append(index)
                    self.solved_numbers[6] = number_set

        self._pop_indexes(indexes)

    def find_fives(self) -> None:
        six = self.solved_numbers[6]
        one = self.solved_numbers[1]

        for index, number in enumerate(self._numbers):
            if len(number) == 5:
                number_set = set(number)
                if six.issuperset(number):
                    self.solved_numbers[5] = number_set

                elif number_set.issuperset(one):
                    self.solved_numbers[3] = number_set

                else:
                    self.solved_numbers[2] = number_set

        self._numbers = None


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 8

    @property
    def test_input_data(self) -> Iterable:
        return [
            "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\n",
            "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\n",
            "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\n",
            "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\n",
            "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\n",
            "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\n",
            "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\n",
            "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\n",
            "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\n",
            "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\n",
        ]

    @property
    def test_solution(self) -> int:
        return 26

    @property
    def test_solution_part_two(self) -> int:
        return 61229

    def part_one(self):
        unique_numbers = 0
        unique_lengths = {2, 3, 4, 7}
        for line in self.input_data_stripped():
            output = line.split(" | ")[1]
            for number in output.split(" "):
                if len(number) in unique_lengths:
                    unique_numbers += 1

        self.verify_solution(unique_numbers)

    def part_two(self):
        codes = []
        for line in self.input_data_stripped():
            decoder = Decoder(line)
            codes.append(decoder.code)

        output = sum(codes)
        self.verify_solution_part_two(output)

    def _run(self):
        self.part_one()
        self.part_two()
