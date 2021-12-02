import argparse
import importlib

from aoc.utilities.aoc import AocBase


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--day",
        type=int,
        help="The problem day must be specified",
        required=True,
    )

    parser.add_argument(
        "--test",
        type=bool,
        help="Is this a test run",
        default=False,
    )

    args = parser.parse_args()

    day = str(args.day).zfill(2)

    aoc = importlib.import_module(f"aoc.problems.day_{day}")
    _aoc: AocBase = aoc.Aoc(args.test)
    _aoc.run()


if __name__ == "__main__":
    main()
