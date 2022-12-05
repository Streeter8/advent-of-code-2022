from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 5

    @property
    def test_input_data(self) -> Iterable:
        return [
            "    [D]    \n",
            "[N] [C]    \n",
            "[Z] [M] [P]\n",
            " 1   2   3 \n",
            "\n",
            "move 1 from 2 to 1\n",
            "move 3 from 1 to 3\n",
            "move 2 from 2 to 1\n",
            "move 1 from 1 to 2\n",
        ]

    @property
    def test_solution(self):
        return "CMZ"

    @property
    def test_solution_part_two(self):
        return "MCD"

    @property
    def _solution(self):
        return "BSDMQFLSP"

    @property
    def _solution_part_two(self):
        return None

    def solve(self):  # noqa: C901 'Aoc.solve' is too complex (11)
        crates = []
        for line in self.input_data_stripped():
            if not line:
                break

            crates.append(line)

        numbers = crates.pop(-1)
        total_creates = int(numbers.strip().rsplit(" ", maxsplit=1)[-1])
        crate_mover_9000 = ["" for _ in range(total_creates)]
        crate_mover_9001 = ["" for _ in range(total_creates)]

        for crate in crates:
            for index in range(total_creates):
                try:
                    letter = crate[index * 4 + 1]
                    if letter != " ":
                        crate_mover_9000[index] = f"{crate_mover_9000[index]}{letter}"
                        crate_mover_9001[index] = f"{crate_mover_9001[index]}{letter}"
                except IndexError:
                    # spaces were cut off
                    break

        for line in self.input_data_stripped():
            try:
                _move, _creates = line.split(" from ")
            except ValueError:
                continue

            move = int(_move.split(" ")[1])
            _start, _end = _creates.split(" to ")
            start = int(_start) - 1
            end = int(_end) - 1

            # Change end first
            # [::-1] effectively reverses string characters
            crate_mover_9000[end] = f"{crate_mover_9000[start][:move][::-1]}{crate_mover_9000[end]}"
            # Remove moved letters
            crate_mover_9000[start] = crate_mover_9000[start][move:]

            crate_mover_9001[end] = f"{crate_mover_9001[start][:move]}{crate_mover_9001[end]}"
            crate_mover_9001[start] = crate_mover_9001[start][move:]

        solution = "".join(word[0] for word in crate_mover_9000 if word)
        self.verify_solution(solution)

        solution_two = "".join(word[0] for word in crate_mover_9001 if word)
        self.verify_solution_part_two(solution_two)

    def _run(self):
        self.solve()
