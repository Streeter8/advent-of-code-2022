from typing import Iterable

from aoc.utilities.aoc import AocBase


class Monkeys:
    def __init__(self, monkeys: dict[str, str], monkey_numbers: dict[str, int]):
        self.monkeys = monkeys
        self.monkey_numbers = monkey_numbers

    @classmethod
    def from_lines(cls, lines: Iterable[str]):
        monkeys = {}
        monkey_numbers = {}

        for line in lines:
            if not line:
                continue

            monkey, number = line.split(": ")
            try:
                number = int(number)
                monkey_numbers[monkey] = number
            except ValueError:
                pass
            finally:
                monkeys[monkey] = number

        return cls(monkeys, monkey_numbers)

    @property
    def root(self) -> int:
        return self.monkey_numbers["root"]

    def evaluate_monkeys(self):
        for monkey in self.monkeys:
            if monkey in self.monkey_numbers:
                continue

            monkey_chain = set()
            self.monkey_numbers[monkey] = self.evaluate_monkey(monkey, monkey_chain)

    def evaluate_monkey(self, monkey: str, monkey_chain: set[str]) -> int:
        if monkey not in monkey_chain:
            monkey_chain = monkey_chain.union({monkey})
        else:
            raise ValueError(f"monkey chain found {monkey}")

        monkey_value = self.monkeys[monkey]
        monkey_one = monkey_value[:4]
        operation = monkey_value[5]
        monkey_two = monkey_value[-4:]

        if not (monkey_one_number := self.monkey_numbers.get(monkey_one)):
            monkey_one_number = self.evaluate_monkey(monkey_one, monkey_chain)
            self.monkey_numbers[monkey_one] = monkey_one_number

        if not (monkey_two_number := self.monkey_numbers.get(monkey_two)):
            monkey_two_number = self.evaluate_monkey(monkey_two, monkey_chain)
            self.monkey_numbers[monkey_two] = monkey_two_number

        match operation:
            case "+":
                return monkey_one_number + monkey_two_number
            case "-":
                return monkey_one_number - monkey_two_number
            case "*":
                return monkey_one_number * monkey_two_number
            case "/":
                return int(monkey_one_number / monkey_two_number)
            case _:
                raise ValueError(f"Unexpected operation received: {operation}")


class MonkeysTwo:
    def __init__(self, monkeys: Monkeys, diff_multiplier: int):
        self.monkeys = monkeys
        self.diff_multiplier = diff_multiplier
        self.humn = None

        root = self.monkeys.monkeys["root"]
        self.val_one = root[:4]
        self.val_two = root[-4:]

        del self.monkeys.monkeys["root"]
        del self.monkeys.monkeys["humn"]

    def find_humn(self):
        humn = 1
        monkeys = Monkeys(dict(self.monkeys.monkeys, humn=f"{humn}"), dict(self.monkeys.monkey_numbers, humn=humn))
        monkeys.evaluate_monkeys()

        while monkeys.monkey_numbers[self.val_one] != monkeys.monkey_numbers[self.val_two]:
            print(f"{humn=}: {monkeys.monkey_numbers[self.val_one]} != {monkeys.monkey_numbers[self.val_two]}")

            if monkeys.monkey_numbers[self.val_one] > monkeys.monkey_numbers[self.val_two]:
                diff = int(
                    (monkeys.monkey_numbers[self.val_one] - monkeys.monkey_numbers[self.val_two]) / self.diff_multiplier
                )
            else:
                diff = int(
                    (monkeys.monkey_numbers[self.val_two] - monkeys.monkey_numbers[self.val_one]) / self.diff_multiplier
                )
            humn += diff or 1

            monkeys = Monkeys(dict(self.monkeys.monkeys, humn=f"{humn}"), dict(self.monkeys.monkey_numbers, humn=humn))
            monkeys.evaluate_monkeys()

        self.humn = humn
        return humn


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 21

    @property
    def test_input_data(self) -> Iterable:
        return [
            "root: pppw + sjmn\n",
            "dbpl: 5\n",
            "cczh: sllz + lgvd\n",
            "zczc: 2\n",
            "ptdq: humn - dvpt\n",
            "dvpt: 3\n",
            "lfqf: 4\n",
            "humn: 5\n",
            "ljgn: 2\n",
            "sjmn: drzm * dbpl\n",
            "sllz: 4\n",
            "pppw: cczh / lfqf\n",
            "lgvd: ljgn * ptdq\n",
            "drzm: hmdt - zczc\n",
            "hmdt: 32\n",
        ]

    @property
    def test_solution(self):
        return 152

    @property
    def test_solution_part_two(self):
        return 301

    @property
    def _solution(self):
        return 194058098264286

    @property
    def _solution_part_two(self):
        return 3592056845086

    def part_one(self):
        monkeys = Monkeys.from_lines(self.input_data_stripped())
        monkeys.evaluate_monkeys()

        self.verify_solution(monkeys.root)

    def part_two(self):
        monkeys = MonkeysTwo(
            Monkeys.from_lines(self.input_data_stripped()),
            diff_multiplier=1 if self.test else 50
        )
        value = monkeys.find_humn()

        self.verify_solution_part_two(value)

    def _run(self):
        self.part_one()
        self.part_two()
