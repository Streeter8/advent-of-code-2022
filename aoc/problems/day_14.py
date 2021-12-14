from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 14

    @property
    def test_input_data(self) -> Iterable:
        return iter([
            "NNCB\n",
            "\n",
            "CH -> B\n",
            "HH -> N\n",
            "CB -> H\n",
            "NH -> C\n",
            "HB -> C\n",
            "HC -> B\n",
            "HN -> C\n",
            "NN -> C\n",
            "BH -> H\n",
            "NC -> B\n",
            "NB -> B\n",
            "BN -> B\n",
            "BB -> N\n",
            "BC -> B\n",
            "CC -> N\n",
            "CN -> C\n",
        ])

    @property
    def test_solution(self) -> int:
        return 1588

    @property
    def test_solution_part_two(self) -> int:
        return 2188189693529

    def step(self, polymer: str, insertion_rules: dict[str, str]) -> str:
        insertions = []
        for index in range(len(polymer) - 1):
            insertions.append(insertion_rules[polymer[index:index + 2]])

        new_polymer = polymer[0]
        for index in range(len(insertions)):
            new_polymer = f"{new_polymer}{insertions[index]}{polymer[index + 1]}"

        return new_polymer

    def analyze_polymer(self, polymer: str) -> dict[str, int]:
        frequencies = {}
        for character in polymer:
            if character in frequencies:
                frequencies[character] += 1
            else:
                frequencies[character] = 1

        return frequencies

    def solve(self):
        input_data = self.input_data_stripped()
        polymer = next(input_data)
        next(input_data)

        insertion_rules = {}
        for line in input_data:
            pair, insert_character = line.split(" -> ")
            insertion_rules[pair] = insert_character

        for _ in range(10):
            print(self.analyze_polymer(polymer))
            polymer = self.step(polymer, insertion_rules)

        results = self.analyze_polymer(polymer)
        result = max(results.values()) - min(results.values())
        self.verify_solution(result)

        # for _ in range(30):
        #     print(self.analyze_polymer(polymer))
        #     polymer = self.step(polymer, insertion_rules)
        #
        # results = self.analyze_polymer(polymer)
        # result = max(results.values()) - min(results.values())
        # self.verify_solution_part_two(result)

    def _run(self):
        self.solve()
