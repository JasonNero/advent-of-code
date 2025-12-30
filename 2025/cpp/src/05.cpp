#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <ranges>
#include <set>
#include <sstream>
#include <string>
#include <vector>

const std::string TEST_INPUT = "3-5\n"
                               "10-14\n"
                               "16-20\n"
                               "12-18\n"
                               "\n"
                               "1\n"
                               "5\n"
                               "8\n"
                               "11\n"
                               "17\n"
                               "32\n";

struct Range {
    long long start;
    long long end;

    auto contains(long long value) const -> bool {
        return value >= start && value <= end;
    }

    auto length() const -> long long { return end - start + 1; }
};

class RangeSet {
  public:
    RangeSet(std::vector<Range> input_ranges) {
	assert(!input_ranges.empty() && "Input ranges should not be empty");

	// Sort parameters: (range, comparator, projection)
	// - Range to sort: input_ranges
	// - Comparator: default (std::less)
	// - Projection: &Range::start (sort by start member)
	std::ranges::sort(input_ranges, {}, &Range::start);
	auto current_range = input_ranges[0];

	for (const Range& next_range : std::views::drop(input_ranges, 1)) {
	    if (current_range.end + 1 >= next_range.start) {
		current_range.end = std::max(current_range.end, next_range.end);
	    } else {
		ranges.push_back(current_range);
		current_range = next_range;
	    }
	}
	ranges.push_back(current_range);
    }

    auto contains(long long value) const -> bool {
	// Lambda Syntax in C++: `[capture](parameters) -> return_type { body }`
	// Capture 'value' by value to use inside the lambda
	return std::ranges::any_of(ranges, [value](const Range& r) {
	    return r.contains(value);
	});
    }

    auto length() const -> long long {
	long long total_length = 0;
	for (const Range& r : ranges) {
	    total_length += r.length();
	}
	return total_length;
    }

  private:
    std::vector<Range> ranges;
};

auto parse_input(const std::string& input_data)
    -> std::pair<std::vector<Range>, std::set<long long>> {
    
    std::vector<Range> ranges;
    std::set<long long> ids;
    std::istringstream stream {input_data};
    std::string line;
    bool parsing_ranges = true;

    while (std::getline(stream, line)) {
	if (line.empty()) {
	    parsing_ranges = false;
	    continue;
	}
	if (parsing_ranges) {
	    size_t dash_pos = line.find('-');
	    long long start = std::stoll(line.substr(0, dash_pos));
	    long long end = std::stoll(line.substr(dash_pos + 1));
	    ranges.push_back(Range{start, end});
	} else {
	    ids.insert(std::stoll(line));
	}
    }
    return {ranges, ids};
}

auto part_one(const std::string& input_data) -> long long {
    auto [ranges, ids] = parse_input(input_data);
    RangeSet range_set(ranges);
    long long fresh_count = 0;
    for (long long id : ids) {
	if (range_set.contains(id)) {
	    fresh_count++;
	}
    }
    return fresh_count;
}

auto part_two(const std::string& input_data) -> long long {
    auto [ranges, ids] = parse_input(input_data);
    RangeSet range_set(ranges);
    long long total_length = range_set.length();
    return total_length;
}

auto test_part_one() -> void {
    auto result = part_one(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 3" << std::endl;
    assert(result == 3);
}

auto test_part_two() -> void {
    auto result = part_two(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 14" << std::endl;
    assert(result == 14);
}

auto main() -> int {
    test_part_one();
    test_part_two();

    std::string filepath = "../05.in";
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
