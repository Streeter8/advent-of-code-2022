from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input_data(self) -> Iterable:
        return [
            "1000\n",
            "2000\n",
            "3000\n",
            "\n",
            "4000\n",
            "\n",
            "5000\n",
            "6000\n",
            "\n",
            "7000\n",
            "8000\n",
            "9000\n",
            "\n",
            "10000\n",
            "\n",
        ]

    @property
    def test_solution(self):
        return 24000

    @property
    def test_solution_part_two(self):
        return 45000

    @property
    def _solution(self):
        return 71780

    @property
    def _solution_part_two(self):
        return 212489

    def solve(self):
        current_value = 0
        elf_magical_energy = []

        for line in self.input_data:
            if value := line.strip():
                current_value += int(value)
            else:
                elf_magical_energy.append(current_value)
                current_value = 0

        top_energy = sorted(elf_magical_energy, reverse=True)

        self.verify_solution(top_energy[0])
        self.verify_solution_part_two(sum(top_energy[:3]))

    def _run(self):
        self.solve()
