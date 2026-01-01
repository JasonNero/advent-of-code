import math
from dataclasses import dataclass
from pathlib import Path

import pytest

# NOTE: This input needs its dangling whitespace preserved!
test_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


@dataclass
class Problem:
    numbers: list[int]
    operand: str

    def solve(self) -> int:
        match self.operand:
            case "+":
                result = sum(self.numbers)
            case "*":
                result = math.prod(self.numbers)
            case _:
                raise ValueError(f"Unknown operand: {self.operand}")
        return result


def part_one(input_data: str) -> int:
    lines = input_data.strip().splitlines()

    # Get operands and first line, then fill in the rest
    problems: list[Problem] = [
        Problem(
            numbers=[
                num,
            ],
            operand=op,
        )
        for (num, op) in zip(map(int, lines[0].split()), lines[-1].split())
    ]

    for line in lines[1:-1]:
        for i, num in enumerate(map(int, line.split())):
            problems[i].numbers.append(num)

    result = sum([p.solve() for p in problems])
    return result


def part_two(input_data: str) -> int:
    lines = input_data.splitlines()
    problems: list[Problem] = []

    # The operands mark the beginning x-coordinate of a new problem
    operand_indices = [i for i, c in enumerate(lines[-1]) if c in "+*"]

    # Split the input columns by operand indices
    for i in range(len(operand_indices)):
        start_idx = operand_indices[i]
        end_idx = (
            operand_indices[i + 1] - 1
            if i + 1 < len(operand_indices)
            else len(lines[0])
        )

        # Take columns, stack them and strip whitespace before converting to integers
        numbers = []
        for col_idx in range(start_idx, end_idx):
            column = "".join([line[col_idx] for line in lines[:-1]])
            numbers.append(int(column))

        operand = lines[-1][start_idx]
        problems.append(Problem(numbers=numbers, operand=operand))

    result = sum([p.solve() for p in problems])
    return result


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 4_277_556)])
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 3_263_827)])
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../06.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
