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

    parser.add_argument(
        "--year",
        type=int,
        help="The problem year",
        default=None,
    )

    args = parser.parse_args()

    day = str(args.day).zfill(2)
    if year := args.year:
        module = f"aoc.{year}.problems.day_{day}"
    else:
        module = f"aoc.problems.day_{day}"

    aoc = importlib.import_module(module)
    _aoc: AocBase = aoc.Aoc(args.test, year)
    _aoc.run()


if __name__ == "__main__":
    main()
