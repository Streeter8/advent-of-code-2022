# Advent of Code 2022

This project will house my approaches to the
[2022 Advent of Code Challenges](https://adventofcode.com/2022).

## Managing Python

### Version

I used pyenv to manage my Python version locally.
This code was written and executed in Python 3.11.0,
as this was the Python latest version available on pyenv 2.3.6.

### Install requirements

```shell
# Ensure requirements are up to date
pip install --upgrade pip setuptools wheel
pip install --upgrade -r requirements.txt
```

### Linting and formatting

```shell
# Format Python code
isort . & black .
# Run the Python linter
flake8
```
