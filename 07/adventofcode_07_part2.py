# %%
import collections
from pprint import pprint

def build_dict_from_lines(line):
    color_dict = collections.defaultdict(list)
    for line in lines:
        # These can be skipped
        if "no other" in line:
            continue

        color_in = " ".join(line.split(" ")[:2])
        for element in line.split("contain")[1].split(","):
            color_num = element.strip().split(" ")[0]
            color_out = " ".join(element.strip().split(" ")[1:-1])
            color_dict[color_out].append((color_num, color_in))
    
    return color_dict

with open("adventofcode_07_input.txt", "r") as f:
    lines = f.readlines()

color_dict = build_dict_from_lines(lines)
# pprint(color_dict)
# print(len(color_dict))

# %%
# How many variants are there to get gold bags?
def gather_bags(color_dict, color_set=set(), outer_color="shiny gold"):
    inner_combinations = color_dict[outer_color]
    inner_set = {col for (_, col) in inner_combinations}
    color_set.update(inner_set)
    for inner_color in inner_set:
        gather_bags(color_dict, color_set, inner_color)
    return color_set

# How many individual bags are required inside your single shiny gold bag?
def gather_bag_count(color_dict, bag_count=1, outer_color="shiny gold"):
    inner_combinations = color_dict[outer_color]
    inner_count = 0
    for num, inner_color in inner_combinations:
        num = int(num)
        for i in range(1, num):
            bag_count += 1
            gather_bag_count(color_dict, bag_count, inner_color)

    return bag_count

print(len(color_dict))
result_count = gather_bag_count(color_dict)
print(result_count)
# %%
