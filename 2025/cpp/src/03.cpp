#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

const std::string TEST_INPUT =
    "987654321111111\n811111111111119\n234234234234278\n818181911112111";

class Bank {
  public:
    Bank(const std::string& blocks) {
        for (char c : blocks) {
            batteries.push_back(c - '0'); // Basically atoi for single digits
        }
        battery_count = batteries.size();
        for (int i = 9; i >= 0; --i) {
            battery_power_indices[i] = std::vector<int>();
        }
        for (size_t i = 0; i < battery_count; ++i) {
            battery_power_indices[batteries[i]].push_back(i);
        }
    }

    auto calculate_joltage(size_t digits = 2) -> long long {
        std::vector<int> selected_powers(digits, -1);
        std::vector<int> selected_indices(digits, -1);

        for (int power = 9; power >= 1; --power) {
            auto& available_indices = battery_power_indices[power];
            for (int current_index : available_indices) {
                for (int current_digit = 0; current_digit < digits;
                     ++current_digit) {
                    if (selected_indices[current_digit] == -1) {
                        bool in_range =
                            current_index <=
                            battery_count - (digits - current_digit);
                        bool not_selected = std::ranges::find(selected_indices,
                                                              current_index) ==
                                            selected_indices.end();
                        int max_previous = -1;
                        if (current_digit > 0) {
                            auto previous = selected_indices |
                                            std::views::take(current_digit);
                            max_previous = *std::ranges::max_element(previous);
                        }
                        bool after_previous = current_index > max_previous;

                        if (in_range && not_selected && after_previous) {
                            selected_powers[current_digit] = power;
                            selected_indices[current_digit] = current_index;
                            break;
                        }
                    }
                }
            }
        }
        long long joltage = 0;
        long long multiplier = 1;
        for (int idx = digits - 1; idx >= 0; --idx) {
            joltage += selected_powers[idx] * multiplier;
            multiplier *= 10;
        }
        return joltage;
    }

  private:
    std::vector<int> batteries;
    std::map<int, std::vector<int>> battery_power_indices;
    size_t battery_count;
};

auto part_one(const std::string& in) -> long long {
    long long total_joltage = 0;
    // For line in string
    for (auto line : in | std::views::split('\n')) {
	if (line.empty()) {
	    continue;
	}
        Bank bank{std::string(line.begin(), line.end())};
        total_joltage += bank.calculate_joltage(2);
    }
    return total_joltage;
}

auto part_two(const std::string& in) -> long long {
    long long total_joltage = 0;
    // For line in string
    for (auto line : in | std::views::split('\n')) {
	if (line.empty()) {
	    continue;
	}
        Bank bank{std::string(line.begin(), line.end())};
        total_joltage += bank.calculate_joltage(12);
    }
    return total_joltage;
}

auto test_part_one() -> void {
    auto result = part_one(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 357" << std::endl;
    assert(result == 357);
}

auto test_part_two() -> void {
    auto result = part_two(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 3121910778619" << std::endl;
    assert(result == 3121910778619);
}

auto main(int argc, char** argv) -> int {
    test_part_one();
    test_part_two();

    std::string filepath = "../03.in";
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filepath);
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string in{buffer.str()};

    long long result_one = part_one(in);
    long long result_two = part_two(in);
    std::cout << "Part one: " << result_one << "\n";
    std::cout << "Part two: " << result_two << "\n";
    return 0;
}
