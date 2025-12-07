from pathlib import Path
import pytest

test_data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"


def part_one(input_data: str) -> int:
    found_ids = []

    for range_string in input_data.strip().split(","):
        lower_str, upper_str = range_string.split("-")

        # print(f"Processing:\t{lower_str}-{upper_str}")
        # Truncate ranges to only include numbers with even length
        lower = int(lower_str)
        if len(lower_str) % 2 == 1:
            # lower end is odd, increase until even
            # e.g. 998-1012 should become 1000-1012
            lower = int("1" + "0" * len(lower_str))

        upper = int(upper_str)
        if len(upper_str) % 2 == 1:
            # upper end is odd, decrease until even
            # e.g. 95-115 should become 95-99
            upper = int("9" * (len(upper_str)-1))

        if lower > upper:
            # Drop invalid ranges
            continue

        # print(f"Truncated to:\t{lower}-{upper}")

        first_half_str = str(lower)[:len(str(lower))//2]
        while True:
            int_to_check = int(first_half_str*2)
            if int_to_check < lower:
                first_half_str = str(int(first_half_str)+1)
            elif int_to_check <= upper:
                found_ids.append(int_to_check)
                first_half_str = str(int(first_half_str)+1)
                # print(f"\t{int_to_check}")
            else:
                break

    return sum(found_ids)

def part_two(input_data: str) -> int:
    pass


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        (test_data, 1227775554),
    ],
)
def test_part_one(input_data, expected_output):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        (test_data, 4174379265),
    ],
)
def test_part_two(input_data, expected_output):
    assert part_two(input_data) == expected_output



if __name__ == "__main__":
    with Path("../02.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    print(f"Part 1a: {result1}")

    # result2 = part_two(input_data)
    # print(f"Part 2: {result2}")
