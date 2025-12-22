from pathlib import Path
import pytest
import itertools

test_input = """
987654321111111
811111111111119
234234234234278
818181911112111"""


class Bank:
    def __init__(self, blocks: str):
        self.batteries = [int(b) for b in blocks]
        self.battery_power_indices = {int(i): [] for i in range(10, 0, -1)}
        for idx, power in enumerate(self.batteries):
            self.battery_power_indices[power].append(idx)

    def calculate_joltage(self) -> int:
        first_power = -1
        first_index = -1
        second_power = -1
        second_index = -1
        for power in range(10, 0, -1):
            indices = self.battery_power_indices[power]
            for i in indices:
                if first_index == -1 and i != len(self.batteries) - 1:
                    first_power = power
                    first_index = i
                    continue
                
                if second_index == -1 and i > first_index:
                    second_power = power
                    second_index = i
                    break

        # print(f"First power: {first_power} at index {first_index}, Second power: {second_power} at index {second_index}")
        return first_power * 10 + second_power

def part_one(input_data: str) -> int:
    total_joltage = 0
    for bank in input_data.strip().splitlines():
        b = Bank(bank)
        joltage = b.calculate_joltage()
        # print(f"Bank: {bank} => Joltage: {joltage}")
        total_joltage += joltage
    return total_joltage

def part_two(input_data: str) -> int:
    return 0 


@pytest.mark.parametrize(
    "input_data, expected_output", 
    [(test_input, 357)]
)
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize(
    "input_data, expected_output", 
    [(test_input, 0)]
)
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../03.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
