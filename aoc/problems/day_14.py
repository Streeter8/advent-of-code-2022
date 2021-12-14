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

    def insert(self, polymer: dict[str, int], pair: str, count: int):
        if pair in polymer:
            polymer[pair] += count
        else:
            polymer[pair] = count

    def step(self, polymer: dict[str, int], insertion_rules: dict[str, str]) -> dict[str, int]:
        new_polymer = {}
        for pair, pair_count in polymer.items():
            character = insertion_rules[pair]
            left_pair = f"{pair[0]}{character}"
            right_pair = f"{character}{pair[1]}"

            self.insert(new_polymer, left_pair, pair_count)
            self.insert(new_polymer, right_pair, pair_count)

        return new_polymer

    def analyze_polymer(self, polymer: dict[str, int], start_character: str, end_character: str) -> dict[str, int]:
        frequencies = {}
        for pair, count in polymer.items():
            for character in pair:
                self.insert(frequencies, character, count)

        # All characters are double counted except for the first and last character
        frequencies[start_character] += 1
        frequencies[end_character] += 1

        return {character: int(value / 2) for character, value in frequencies.items()}

    def solve(self):
        input_data = self.input_data_stripped()
        polymer_chain = next(input_data)
        start_character = polymer_chain[0]
        end_character = polymer_chain[-1]
        polymer = {}
        for index in range(len(polymer_chain) - 1):
            pair = polymer_chain[index:index + 2]
            self.insert(polymer, pair, 1)

        # Skip blank line
        next(input_data)

        insertion_rules = {}
        for line in input_data:
            pair, insert_character = line.split(" -> ")
            insertion_rules[pair] = insert_character

        for _ in range(10):
            polymer = self.step(polymer, insertion_rules)

        results = self.analyze_polymer(polymer, start_character, end_character)
        result = max(results.values()) - min(results.values())
        self.verify_solution(result)

        for _ in range(30):
            polymer = self.step(polymer, insertion_rules)

        results = self.analyze_polymer(polymer, start_character, end_character)
        result = max(results.values()) - min(results.values())
        self.verify_solution_part_two(result)

    def _run(self):
        self.solve()
