from typing import Iterable

import math

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 8

    @property
    def test_input_data(self) -> Iterable:
        # Part 1 test input data
        # return [
        #     "RL\n",
        #     "\n"
        #     "AAA = (BBB, CCC)\n",
        #     "BBB = (DDD, EEE)\n",
        #     "CCC = (ZZZ, GGG)\n",
        #     "DDD = (DDD, DDD)\n",
        #     "EEE = (EEE, EEE)\n",
        #     "GGG = (GGG, GGG)\n",
        #     "ZZZ = (ZZZ, ZZZ)\n",
        # ]
        return [
            "LR\n",
            "\n",
            "11A = (11B, XXX)\n",
            "11B = (XXX, 11Z)\n",
            "11Z = (11B, XXX)\n",
            "22A = (22B, XXX)\n",
            "22B = (22C, 22C)\n",
            "22C = (22Z, 22Z)\n",
            "22Z = (22B, 22B)\n",
            "XXX = (XXX, XXX)\n",
        ]

    @property
    def test_solution(self):
        return 2

    @property
    def test_solution_part_two(self):
        return 6

    @property
    def _solution(self):
        return 14257

    @property
    def _solution_part_two(self):
        return 16187743689077

    def solve(self):
        input_data = self.input_data_stripped()
        steps = next(input_data)
        step_length = len(steps)

        patches = {}

        for line in input_data:
            if not line:
                continue

            name, left_right = line.split(" = ")
            left_right = left_right.strip("()")
            left, right = left_right.split(", ")
            patches[name.strip()] = {"L": left, "R": right}

        count = 0
        current_patch = "AAA"
        while current_patch != "ZZZ":
            step = steps[count % step_length]
            current_patch = patches[current_patch][step]
            count += 1

        self.verify_solution(count)

    def solve_part_two(self):
        input_data = self.input_data_stripped()
        steps = next(input_data)
        step_length = len(steps)

        patches = {}
        ghost_patches = []
        z_paths = []

        for line in input_data:
            if not line:
                continue

            name, left_right = line.split(" = ")
            name = name.strip()
            left_right = left_right.strip("()")
            left, right = left_right.split(", ")

            patches[name.strip()] = {"L": left, "R": right}
            if name.endswith("A"):
                ghost_patches.append(name)
                z_paths.append(0)

        count = 0
        while not all(z_paths):
            step = steps[count % step_length]
            new_patches = []
            count += 1

            for index, ghost_patch in enumerate(ghost_patches):
                new_patch = patches[ghost_patch][step]
                if new_patch.endswith("Z") and not z_paths[index]:
                    z_paths[index] = count

                new_patches.append(patches[ghost_patch][step])

            ghost_patches = new_patches

        solution = math.lcm(*z_paths)
        self.verify_solution_part_two(solution)

    def _run(self):
        self.solve()
        self.solve_part_two()
