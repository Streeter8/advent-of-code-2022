from collections.abc import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 5

    @property
    def test_input_data(self) -> Iterable:
        return [
            "47|53\n",
            "97|13\n",
            "97|61\n",
            "97|47\n",
            "75|29\n",
            "61|13\n",
            "75|53\n",
            "29|13\n",
            "97|29\n",
            "53|29\n",
            "61|53\n",
            "97|53\n",
            "61|29\n",
            "47|13\n",
            "75|47\n",
            "97|75\n",
            "47|61\n",
            "75|61\n",
            "47|29\n",
            "75|13\n",
            "53|13\n",
            "\n",
            "75,47,61,53,29\n",
            "97,61,53,29,13\n",
            "75,29,13\n",
            "75,97,47,61,53\n",
            "61,13,29\n",
            "97,13,75,29,47\n",
        ]

    @property
    def test_solution(self) -> int:
        return 143

    @property
    def test_solution_part_two(self) -> int:
        return 123

    @property
    def _solution(self) -> int:
        return 5374

    @property
    def _solution_part_two(self) -> int:
        return 4260

    @staticmethod
    def new_ordering_rule() -> dict[str, set[int]]:
        return {
            "before": set(),
            "after": set(),
        }

    def _run(self):
        ordering_rules = {}
        updates = []

        for line in self.input_data_stripped():
            if "|" in line:
                before, after = map(int, line.split("|"))
                if before not in ordering_rules:
                    ordering_rules[before] = self.new_ordering_rule()
                if after not in ordering_rules:
                    ordering_rules[after] = self.new_ordering_rule()

                ordering_rules[before]["after"].add(after)
                ordering_rules[after]["before"].add(before)

            if "," in line:
                updates.append(Update(line))

        solution_one = 0
        solution_two = 0

        for update in updates:
            if update.valid_page_ordering(ordering_rules):
                solution_one += update.middle_page
            else:
                solution_two += update.get_sorted_middle_page(ordering_rules)

        self.verify_solution(solution_one)
        self.verify_solution_part_two(solution_two)


class Update:
    def __init__(self, line: str):
        self.pages = list(map(int, line.split(",")))

    @property
    def middle_page(self) -> int:
        return self.pages[(len(self.pages) // 2)]

    def get_sorted_middle_page(self, ordering_rules: dict[int, dict[str, set[int]]]) -> int:
        sorted_pages = []
        for page in self.pages:
            for index, sorted_page in enumerate(list(sorted_pages)):
                if sorted_page in ordering_rules[page]["before"] or page in ordering_rules[sorted_page]["after"]:
                    continue
                else:
                    sorted_pages.insert(index, page)
                    break
            else:
                sorted_pages.append(page)

        return sorted_pages[(len(sorted_pages) // 2)]

    def valid_page_ordering(self, ordering_rules: dict[int, dict[str, set[int]]]) -> bool:
        for next_index, page in enumerate(self.pages[:-1], start=1):
            if self.pages[next_index] not in ordering_rules[page]["after"]:
                return False

        return True
