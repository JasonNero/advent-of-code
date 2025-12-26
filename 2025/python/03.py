from pathlib import Path

import pytest

test_input = """
987654321111111
811111111111119
234234234234278
818181911112111"""


class Bank:
    def __init__(self, blocks: str):
        self.batteries = [int(b) for b in blocks]
        self.battery_count = len(self.batteries)
        self.battery_power_indices = {int(i): [] for i in range(9, 0, -1)}
        for idx, power in enumerate(self.batteries):
            self.battery_power_indices[power].append(idx)

    def calculate_joltage(self, digits=2) -> int:
        selected_powers = [-1] * digits
        selected_indices = [-1] * digits
        for power in range(9, 0, -1):
            available_indices = self.battery_power_indices[power]
            for current_index in available_indices:
                for current_digit in range(digits):
                    if selected_indices[current_digit] == -1:
                        # Only up to length-(digits - current_digit) can be taken
                        # and index cannot be already taken
                        # and index must be greater than previous indices
                        in_range = current_index <= self.battery_count - (
                            digits - current_digit
                        )
                        not_selected = current_index not in selected_indices
                        after_previous = current_index > max(
                            selected_indices[:current_digit], default=-1
                        )
                        if in_range and not_selected and after_previous:
                            selected_powers[current_digit] = power
                            selected_indices[current_digit] = current_index
                            break
        joltage = sum(
            power * (10 ** (digits - idx - 1))
            for idx, power in enumerate(selected_powers)
        )
        return joltage


def part_one(input_data: str) -> int:
    total_joltage = 0
    for bank in input_data.strip().splitlines():
        b = Bank(bank)
        joltage = b.calculate_joltage()
        total_joltage += joltage
    return total_joltage


def part_two(input_data: str) -> int:
    total_joltage = 0
    for bank in input_data.strip().splitlines():
        b = Bank(bank)
        joltage = b.calculate_joltage(digits=12)
        total_joltage += joltage
    return total_joltage


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 357)])
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 3121910778619)])
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../03.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
