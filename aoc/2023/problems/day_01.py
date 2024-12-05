from collections.abc import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input_data(self) -> Iterable:
        # return ["1abc2\n", "pqr3stu8vwx\n", "a1b2c3d4e5f\n", "treb7uchet\n"]
        return [
            "two1nine\n",
            "eightwothree\n",
            "abcone2threexyz\n",
            "xtwone3four\n",
            "4nineeightseven2\n",
            "zoneight234\n",
            "7pqrstsixteen\n",
        ]

    @property
    def test_solution(self):
        return 142

    @property
    def test_solution_part_two(self):
        return 281

    @property
    def _solution(self):
        return 54951

    @property
    def _solution_part_two(self):
        return 55218

    def part_one(self):
        calibration_values = []
        for line in self.input_data_stripped():
            calibration_value = ""
            for character in line:
                if character.isdigit():
                    calibration_value += character
                    break

            for character in reversed(line):
                if character.isdigit():
                    calibration_value += character
                    break

            calibration_values.append(int(calibration_value))

        self.verify_solution(sum(calibration_values))

    def part_two(self):  # noqa: C901
        numbers = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

        calibration_values = []
        for line in self.input_data_stripped():
            calibration_value = ""

            index = len(line) + 1
            _number = None
            for number in numbers:
                _index = line.find(number)
                if -1 < _index < index:
                    index = _index
                    _number = number

            for _index, character in enumerate(line):
                if _index > index:
                    calibration_value += numbers[_number]
                    break

                if character.isdigit():
                    calibration_value += character
                    break

            line = "".join(reversed(line))
            index = len(line) + 1
            _number = None
            for number in numbers:
                number = "".join(reversed(number))
                _index = line.find(number)
                if -1 < _index < index:
                    index = _index
                    _number = "".join(reversed(number))

            for _index, character in enumerate(line):
                if _index > index:
                    calibration_value += numbers[_number]
                    break

                if character.isdigit():
                    calibration_value += character
                    break

            calibration_values.append(int(calibration_value))

        self.verify_solution_part_two(sum(calibration_values))

    def _run(self):
        self.part_one()
        self.part_two()
