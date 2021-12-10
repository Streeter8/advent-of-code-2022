from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    PARENS = {"(": ")", "[": "]", "{": "}", "<": ">"}
    CORRUPTION_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
    COMPLETION_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}

    @property
    def day(self) -> int:
        return 10

    @property
    def test_input_data(self) -> Iterable:
        return [
            "[({(<(())[]>[[{[]{<()<>>\n",
            "[(()[<>])]({[<{<<[]>>(\n",
            "{([(<{}[<>[]}>{[]{[(<()>\n",
            "(((({<>}<{<{<>}{[]{[]{}\n",
            "[[<[([]))<([[{}[[()]]]\n",
            "[{[{({}]{}}([{[{{{}}([]\n",
            "{<[[]]>}<{[{[{[]{()[[[]\n",
            "[<(<(<(<{}))><([]([]()\n",
            "<{([([[(<>()){}]>(<<{{\n",
            "<{([{{}}[<[[[<>{}]]]>[]]\n",
        ]

    @property
    def test_solution(self) -> int:
        return 26397

    @property
    def test_solution_part_two(self):
        return 288957

    def solve(self):
        corruption_count = {")": 0, "]": 0, "}": 0, ">": 0}
        completion_scores = []

        for line in self.input_data_stripped():
            stack = []
            for character in line:
                if character in self.PARENS:
                    stack.append(character)
                elif character == self.PARENS[stack[-1]]:
                    stack.pop()
                else:
                    corruption_count[character] += 1
                    stack = None
                    break

            if stack:
                completion_score = 0
                for character in reversed(stack):
                    completion_score *= 5
                    completion_score += self.COMPLETION_SCORES[character]
                completion_scores.append(completion_score)

        corruption_score = sum(
            self.CORRUPTION_SCORES[character] * count for character, count in corruption_count.items()
        )
        self.verify_solution(corruption_score)

        completion_score = sorted(completion_scores)[int(len(completion_scores) / 2)]
        self.verify_solution_part_two(completion_score)

    def _run(self):
        self.solve()
